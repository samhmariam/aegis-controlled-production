import json
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from aegis.api.app import app
from aegis.config import get_settings

CLAIMS_PATH = Path("data/synthetic/claims.json")


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="module")
def synthetic_claims() -> list[dict[str, Any]]:
    return json.loads(CLAIMS_PATH.read_text(encoding="utf-8"))


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_does_not_claim_downstream_health(client: TestClient) -> None:
    response = client.get("/health")

    assert set(response.json()) == {"status", "service", "checked_at"}


def test_version_reports_app_and_schema_version(client: TestClient) -> None:
    response = client.get("/version")
    settings = get_settings()

    assert response.status_code == 200
    assert response.json()["app_version"] == settings.app_version
    assert response.json()["schema_version"] == settings.schema_version


def test_validate_accepts_a_synthetic_claim(
    client: TestClient, synthetic_claims: list[dict[str, Any]]
) -> None:
    claim = synthetic_claims[0]
    response = client.post("/claims/validate", json=claim)

    assert response.status_code == 200
    assert response.json()["valid"] is True
    assert response.json()["claim_id"] == claim["claim_id"]


def test_validate_reports_completeness_issues(
    client: TestClient, synthetic_claims: list[dict[str, Any]]
) -> None:
    response = client.post("/claims/validate", json=synthetic_claims[8])

    assert response.status_code == 200
    assert response.json()["completeness_issues"] == ["missing_vehicle_reference"]


def test_validate_rejects_unknown_field(
    client: TestClient, synthetic_claims: list[dict[str, Any]]
) -> None:
    claim = {**synthetic_claims[0], "unexpected": "value"}
    response = client.post("/claims/validate", json=claim)

    assert response.status_code == 422
    assert response.json()["error_code"] == "claim_schema_invalid"
    assert any(detail["code"] == "extra_forbidden" for detail in response.json()["details"])


def test_validate_rejects_substituted_identifier(
    client: TestClient, synthetic_claims: list[dict[str, Any]]
) -> None:
    claim = {**synthetic_claims[0], "tenant_id": synthetic_claims[0]["claim_id"]}
    response = client.post("/claims/validate", json=claim)

    assert response.status_code == 422
    assert any(
        detail["field"] == "tenant_id" and detail["code"] == "string_pattern_mismatch"
        for detail in response.json()["details"]
    )


def test_validate_does_not_echo_claim_description(
    client: TestClient, synthetic_claims: list[dict[str, Any]]
) -> None:
    injection_claim = synthetic_claims[11]
    hostile_text = injection_claim["description"]
    response = client.post("/claims/validate", json=injection_claim)

    assert response.status_code == 200
    assert hostile_text not in response.text
