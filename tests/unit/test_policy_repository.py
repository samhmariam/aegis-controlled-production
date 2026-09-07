from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta

import pytest

from aegis.context.service import ContextService, RetrievalStatus
from aegis.errors import (
    ClaimNotAccessibleError,
    IdentityInvalidError,
    PolicyVersionUnavailableError,
)
from aegis.identity.principal import AuthenticationMethod, Principal, PrincipalType
from aegis.persistence.connection import connect
from aegis.persistence.policy_repository import PolicyRepository
from aegis.persistence.ranking import query_tokens, rank_by_token_overlap
from aegis.persistence.seed import run_seed
from tests.conftest import FIXTURES_DIR, PRINCIPALS_FILE, seed_into
from tests.unit.test_seed import table_digest

pytestmark = pytest.mark.unit

HANDLER_A = "principal-handler-a"
HANDLER_B = "principal-handler-b"
AUDITOR_A = "principal-auditor-a"


def principal_from_db(conn, principal_id: str, *, lifetime: int = 900) -> Principal:
    """Build a Principal from a seeded row without needing the raw demo token."""
    row = conn.execute(
        "SELECT * FROM principals WHERE principal_id = ?", (principal_id,)
    ).fetchone()
    now = datetime.now(UTC)
    return Principal(
        principal_id=str(row["principal_id"]),
        principal_type=PrincipalType(str(row["principal_type"])),
        tenant_id=str(row["tenant_id"]),
        scopes=frozenset(json.loads(str(row["scopes"]))),
        roles=frozenset(json.loads(str(row["roles"]))),
        authenticated_at=now,
        expires_at=now + timedelta(seconds=lifetime),
        authentication_method=AuthenticationMethod.DEMO_TOKEN,
    )


@pytest.fixture
def service_and_conn(seeded_db):
    conn = connect(seeded_db)
    yield ContextService(PolicyRepository(conn), max_clauses=4, excerpt_chars=400), conn
    conn.close()


# --- correct retrieval -------------------------------------------------------

def test_motor_claim_retrieves_its_policy_v2_clauses(service_and_conn):
    service, conn = service_and_conn
    result = service.retrieve(
        principal=principal_from_db(conn, HANDLER_A), claim_id="claim-cm-0001", query="excess"
    )

    assert result.status is RetrievalStatus.RETRIEVED
    assert result.bundle.policy_version == "v2"
    assert result.bundle.clause_ids == ("clause-cm-motor-0001-excess",)


def test_property_claim_retrieves_its_own_tenant_clauses(service_and_conn):
    service, conn = service_and_conn
    result = service.retrieve(
        principal=principal_from_db(conn, HANDLER_B), claim_id="claim-cd-0006", query="excess"
    )

    assert result.bundle.tenant_id == "tenant-cotswold-demo-b"
    assert all(cid.startswith("clause-cd-") for cid in result.bundle.clause_ids)


def test_retrieved_clauses_belong_to_the_authorised_policy_and_version(service_and_conn):
    service, conn = service_and_conn
    result = service.retrieve(
        principal=principal_from_db(conn, HANDLER_A),
        claim_id="claim-cm-0001",
        query="excess settlement authority",
    )

    for clause_id in result.bundle.clause_ids:
        row = conn.execute(
            "SELECT policy_id, policy_version, tenant_id FROM policy_clauses WHERE clause_id = ?",
            (clause_id,),
        ).fetchone()
        assert row["policy_id"] == result.bundle.policy_id
        assert row["policy_version"] == result.bundle.policy_version
        assert row["tenant_id"] == result.bundle.tenant_id


# --- denial ------------------------------------------------------------------

def test_cross_tenant_claim_is_not_accessible(service_and_conn):
    service, conn = service_and_conn
    with pytest.raises(ClaimNotAccessibleError):
        service.retrieve(
            principal=principal_from_db(conn, HANDLER_A),
            claim_id="claim-cd-0006",
            query="excess",
        )


def test_same_tenant_unentitled_claim_is_not_accessible(service_and_conn):
    """Tenant membership alone does not grant the claim."""
    service, conn = service_and_conn
    with pytest.raises(ClaimNotAccessibleError):
        service.retrieve(
            principal=principal_from_db(conn, HANDLER_A),
            claim_id="claim-cm-0002",
            query="excess",
        )


def test_entitled_claim_without_claims_read_scope_is_not_accessible(service_and_conn):
    service, conn = service_and_conn
    with pytest.raises(ClaimNotAccessibleError):
        service.retrieve(
            principal=principal_from_db(conn, AUDITOR_A),
            claim_id="claim-cm-0001",
            query="excess",
        )


def test_expired_principal_is_rejected_before_any_query(service_and_conn):
    service, conn = service_and_conn
    expired = principal_from_db(conn, HANDLER_A, lifetime=1)
    expired = expired.model_copy(
        update={
            "authenticated_at": datetime.now(UTC) - timedelta(hours=2),
            "expires_at": datetime.now(UTC) - timedelta(hours=1),
        }
    )
    with pytest.raises(IdentityInvalidError):
        service.retrieve(principal=expired, claim_id="claim-cm-0001", query="excess")


def test_inaccessible_and_nonexistent_claims_return_identical_denials(service_and_conn):
    """Proves the response content carries no existence signal. Not a timing claim."""
    service, conn = service_and_conn
    principal = principal_from_db(conn, HANDLER_A)

    with pytest.raises(ClaimNotAccessibleError) as inaccessible:
        service.retrieve(principal=principal, claim_id="claim-cd-0006", query="excess")
    with pytest.raises(ClaimNotAccessibleError) as absent:
        service.retrieve(principal=principal, claim_id="claim-zz-9999", query="excess")

    assert type(inaccessible.value) is type(absent.value)
    assert str(inaccessible.value) == str(absent.value)
    assert inaccessible.value.error_code == absent.value.error_code


# --- version freshness -------------------------------------------------------

def test_stale_policy_version_fails_without_substituting_v2(service_and_conn):
    service, conn = service_and_conn
    with pytest.raises(PolicyVersionUnavailableError) as exc:
        service.retrieve(
            principal=principal_from_db(conn, HANDLER_A),
            claim_id="claim-cm-0011-stale-policy",
            query="excess",
        )

    assert exc.value.error_code == "policy_version_stale"


def test_missing_policy_version_fails_explicitly(service_and_conn):
    service, conn = service_and_conn
    conn.execute(
        "UPDATE claims SET loss_at = '2024-01-01T00:00:00Z' WHERE claim_id = 'claim-cm-0001'"
    )

    with pytest.raises(PolicyVersionUnavailableError) as exc:
        service.retrieve(
            principal=principal_from_db(conn, HANDLER_A), claim_id="claim-cm-0001", query="excess"
        )

    assert exc.value.error_code == "policy_version_missing"


# --- no evidence -------------------------------------------------------------

def test_no_matching_clause_returns_empty_bundle_with_limitation(service_and_conn):
    service, conn = service_and_conn
    result = service.retrieve(
        principal=principal_from_db(conn, HANDLER_A),
        claim_id="claim-cm-0001",
        query="flood earthquake subsidence",
    )

    assert result.status is RetrievalStatus.NO_EVIDENCE
    assert result.bundle.clause_ids == ()
    assert any("no clause" in limitation for limitation in result.bundle.limitations)


# --- injection ---------------------------------------------------------------

def test_injection_in_claim_text_cannot_change_retrieval_scope(service_and_conn):
    service, conn = service_and_conn
    result = service.retrieve(
        principal=principal_from_db(conn, HANDLER_A),
        claim_id="claim-cm-0012-injection",
        query="excess settlement authority",
    )

    assert result.bundle.tenant_id == "tenant-cotswold-demo-a"
    assert result.bundle.policy_id == "policy-cm-motor-0001"
    assert all(cid.startswith("clause-cm-") for cid in result.bundle.clause_ids)
    assert "claimant-ref-b-0004" not in json.dumps(result.bundle.model_dump(mode="json"))


def test_injection_text_used_as_the_query_cannot_change_scope(service_and_conn):
    service, conn = service_and_conn
    description = conn.execute(
        "SELECT description FROM claims WHERE claim_id = 'claim-cm-0012-injection'"
    ).fetchone()["description"]

    result = service.retrieve(
        principal=principal_from_db(conn, HANDLER_A),
        claim_id="claim-cm-0012-injection",
        query=description,
    )

    assert result.bundle.tenant_id == "tenant-cotswold-demo-a"
    assert all(cid.startswith("clause-cm-") for cid in result.bundle.clause_ids)


def test_user_query_cannot_inject_fts_operators(service_and_conn):
    service, conn = service_and_conn
    result = service.retrieve(
        principal=principal_from_db(conn, HANDLER_A),
        claim_id="claim-cm-0001",
        query='excess" OR policy_clauses_fts MATCH "settlement',
    )

    assert all(cid.startswith("clause-cm-motor-0001") for cid in result.bundle.clause_ids)


# --- fallback ranker ---------------------------------------------------------

def test_deterministic_fallback_ranking_is_stable_and_order_independent():
    tokens = query_tokens("excess settlement")
    forward = [("clause-a", "the excess is 250"), ("clause-b", "excess and settlement apply")]
    assert rank_by_token_overlap(tokens, forward) == ("clause-b", "clause-a")
    assert rank_by_token_overlap(tokens, list(reversed(forward))) == ("clause-b", "clause-a")


def test_fallback_repository_returns_the_same_clauses_as_fts(seeded_db):
    conn = connect(seeded_db)
    principal = principal_from_db(conn, HANDLER_A)
    fts = ContextService(PolicyRepository(conn, use_fts=True), max_clauses=4, excerpt_chars=400)
    plain = ContextService(PolicyRepository(conn, use_fts=False), max_clauses=4, excerpt_chars=400)

    a = fts.retrieve(principal=principal, claim_id="claim-cm-0001", query="excess")
    b = plain.retrieve(principal=principal, claim_id="claim-cm-0001", query="excess")

    assert set(a.bundle.clause_ids) == set(b.bundle.clause_ids)
    conn.close()


# --- seed idempotency (required category, asserted in the gate file) ----------

def test_seed_rerun_leaves_row_counts_and_contents_unchanged(tmp_path):
    db_path, first = seed_into(tmp_path)
    before = table_digest(db_path)

    second = run_seed(
        database_path=db_path,
        demo_root=db_path.parent,
        fixtures_dir=FIXTURES_DIR,
        principals_file=PRINCIPALS_FILE,
    )

    assert second.inserted == {}
    assert second.unchanged["claims"] == first.inserted["claims"]
    assert table_digest(db_path) == before
