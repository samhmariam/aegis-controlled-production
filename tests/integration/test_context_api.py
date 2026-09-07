from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient

from aegis.api.app import create_app
from aegis.api.dependencies import get_connection
from aegis.context.citations import Citation, CitationOutcome, verify_citation
from aegis.persistence.connection import connect
from aegis.persistence.policy_repository import PolicyRepository

pytestmark = pytest.mark.integration

TOKENS = {  # synthetic demo credentials; environment values support local overrides
    "handler_a": os.getenv(
        "AEGIS_DEMO_TOKEN_HANDLER_A", "1dJHYvMah8OKx0pzOF7wrfMNRw3817vo"
    ),
    "handler_b": os.getenv(
        "AEGIS_DEMO_TOKEN_HANDLER_B", "Ixgb6QVA_3N0nEG4OJ-UMxhYinqEtEhz"
    ),
}


@pytest.fixture
def client(seeded_db):
    app = create_app()
    conn = connect(seeded_db)
    app.dependency_overrides[get_connection] = lambda: conn
    yield TestClient(app, raise_server_exceptions=False)
    conn.close()
    app.dependency_overrides.clear()


def auth(name: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {TOKENS[name]}"}


def test_authorized_context_request_returns_bundle_with_provenance(client):
    response = client.get("/claims/claim-cm-0001/context", params={"query": "excess"},
                          headers=auth("handler_a"))

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "retrieved"
    assert body["bundle"]["policy_version"] == "v2"
    assert body["bundle"]["excerpts"][0]["source_content_hash"].startswith("sha256:")
    assert body["bundle"]["limitations"]


def test_response_tenant_is_the_principal_tenant_not_the_query_string(client):
    response = client.get(
        "/claims/claim-cm-0001/context",
        params={"query": "excess", "tenant_id": "tenant-cotswold-demo-b"},
        headers=auth("handler_a"),
    )

    assert response.json()["bundle"]["tenant_id"] == "tenant-cotswold-demo-a"


def test_cross_tenant_request_returns_404_claim_not_accessible(client):
    response = client.get("/claims/claim-cd-0006/context", params={"query": "excess"},
                          headers=auth("handler_a"))

    assert response.status_code == 404
    assert response.json() == {"error_code": "claim_not_accessible", "details": []}


def test_nonexistent_claim_response_is_identical_to_inaccessible(client):
    inaccessible = client.get("/claims/claim-cd-0006/context", params={"query": "excess"},
                              headers=auth("handler_a"))
    absent = client.get("/claims/claim-zz-9999/context", params={"query": "excess"},
                        headers=auth("handler_a"))

    assert inaccessible.status_code == absent.status_code
    assert inaccessible.json() == absent.json()


def test_missing_credential_returns_401(client):
    response = client.get("/claims/claim-cm-0001/context", params={"query": "excess"})

    assert response.status_code == 401
    assert response.json()["error_code"] == "identity_invalid"


def test_stale_policy_version_returns_409(client):
    response = client.get("/claims/claim-cm-0011-stale-policy/context",
                          params={"query": "excess"}, headers=auth("handler_a"))

    assert response.status_code == 409
    assert response.json()["error_code"] == "policy_version_stale"


def test_no_evidence_returns_200_with_empty_bundle(client):
    response = client.get("/claims/claim-cm-0001/context",
                          params={"query": "flood earthquake subsidence"},
                          headers=auth("handler_a"))

    assert response.status_code == 200
    assert response.json()["status"] == "no_evidence"
    assert response.json()["bundle"]["clause_ids"] == []
    assert response.json()["bundle"]["limitations"]


def test_citation_from_api_response_verifies_against_stored_source(client, seeded_db):
    body = client.get("/claims/claim-cm-0001/context", params={"query": "excess"},
                      headers=auth("handler_a")).json()
    excerpt = body["bundle"]["excerpts"][0]
    conn = connect(seeded_db, read_only=True)

    verification = verify_citation(
        PolicyRepository(conn),
        tenant_id=body["bundle"]["tenant_id"],
        citation=Citation(
            clause_id=excerpt["clause_id"],
            policy_id=body["bundle"]["policy_id"],
            policy_version=body["bundle"]["policy_version"],
            excerpt=excerpt["excerpt"],
            claimed_hash=excerpt["source_content_hash"],
        ),
    )

    assert verification.outcome is CitationOutcome.VERIFIED
    conn.close()


def test_tampered_stored_clause_fails_verification(client, seeded_db):
    """The test that proves verification recomputes rather than echoes."""
    body = client.get("/claims/claim-cm-0001/context", params={"query": "excess"},
                      headers=auth("handler_a")).json()
    excerpt = body["bundle"]["excerpts"][0]

    conn = connect(seeded_db)
    conn.execute("UPDATE policy_clauses SET text = text || ' and anything goes'"
                 " WHERE clause_id = ?", (excerpt["clause_id"],))

    verification = verify_citation(
        PolicyRepository(conn),
        tenant_id=body["bundle"]["tenant_id"],
        citation=Citation(
            clause_id=excerpt["clause_id"],
            policy_id=body["bundle"]["policy_id"],
            policy_version=body["bundle"]["policy_version"],
            excerpt=excerpt["excerpt"],
            claimed_hash=excerpt["source_content_hash"],
        ),
    )

    assert verification.outcome is CitationOutcome.HASH_MISMATCH
    conn.close()


def test_error_bodies_do_not_leak_database_details(client):
    response = client.get("/claims/claim-cd-0006/context", params={"query": "excess"},
                          headers=auth("handler_a"))

    text = response.text.lower()
    assert "sqlite" not in text
    assert "data/local" not in text
    assert "traceback" not in text
