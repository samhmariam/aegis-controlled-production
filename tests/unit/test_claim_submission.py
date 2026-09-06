from datetime import UTC, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from aegis.domain.models import ClaimSubmission, ClaimType


@pytest.fixture
def valid_synthetic_claim() -> dict[str, object]:
    return {
        "claim_id": "claim-abc-123",
        "tenant_id": "tenant-xyz-789",
        "policy_id": "policy-abc-123",
        "claim_type": ClaimType.MOTOR,
        "claimant_reference": "claimant-ref-customer-123",
        "loss_at": datetime(2026, 9, 1, 10, 0, tzinfo=UTC),
        "submitted_at": datetime(2026, 9, 2, 10, 0, tzinfo=UTC),
        "description": "Collision while reversing into a parked vehicle.",
        "incident": {"vehicle_reference": "vehicle-123"},
        "amount": Decimal("1250.00"),
        "currency": "GBP",
    }


def test_valid_synthetic_claim_parses(valid_synthetic_claim: dict[str, object]) -> None:
    claim = ClaimSubmission.model_validate(valid_synthetic_claim)

    assert claim.claim_id == "claim-abc-123"
    assert claim.claim_type is ClaimType.MOTOR


def test_unknown_field_is_rejected(valid_synthetic_claim: dict[str, object]) -> None:
    valid_synthetic_claim["unexpected"] = "value"

    with pytest.raises(ValidationError) as exc_info:
        ClaimSubmission.model_validate(valid_synthetic_claim)

    assert exc_info.value.errors()[0]["type"] == "extra_forbidden"


def test_claim_id_in_tenant_field_is_rejected(valid_synthetic_claim: dict[str, object]) -> None:
    valid_synthetic_claim["tenant_id"] = "claim-abc-123"

    with pytest.raises(ValidationError) as exc_info:
        ClaimSubmission.model_validate(valid_synthetic_claim)

    error = exc_info.value.errors()[0]
    assert error["type"] == "string_pattern_mismatch"
    assert error["loc"] == ("tenant_id",)


def test_tenant_id_in_claim_field_is_rejected(valid_synthetic_claim: dict[str, object]) -> None:
    valid_synthetic_claim["claim_id"] = "tenant-xyz-789"

    with pytest.raises(ValidationError) as exc_info:
        ClaimSubmission.model_validate(valid_synthetic_claim)

    error = exc_info.value.errors()[0]
    assert error["type"] == "string_pattern_mismatch"
    assert error["loc"] == ("claim_id",)


def test_negative_amount_is_rejected(valid_synthetic_claim: dict[str, object]) -> None:
    valid_synthetic_claim["amount"] = Decimal("-0.01")

    with pytest.raises(ValidationError) as exc_info:
        ClaimSubmission.model_validate(valid_synthetic_claim)

    assert exc_info.value.errors()[0]["type"] == "greater_than_equal"


def test_amount_without_currency_is_rejected(valid_synthetic_claim: dict[str, object]) -> None:
    valid_synthetic_claim["currency"] = None

    with pytest.raises(ValidationError, match="currency is required when amount is present"):
        ClaimSubmission.model_validate(valid_synthetic_claim)


def test_currency_without_amount_is_rejected(valid_synthetic_claim: dict[str, object]) -> None:
    valid_synthetic_claim["amount"] = None

    with pytest.raises(ValidationError, match="amount is required when currency is present"):
        ClaimSubmission.model_validate(valid_synthetic_claim)


def test_loss_after_submission_is_rejected(valid_synthetic_claim: dict[str, object]) -> None:
    valid_synthetic_claim["loss_at"] = datetime(2026, 9, 3, 10, 0, tzinfo=UTC)

    with pytest.raises(ValidationError, match="loss_at must not be after submitted_at"):
        ClaimSubmission.model_validate(valid_synthetic_claim)


def test_naive_timestamps_are_rejected(valid_synthetic_claim: dict[str, object]) -> None:
    valid_synthetic_claim["loss_at"] = datetime(2026, 9, 1, 10, 0)
    valid_synthetic_claim["submitted_at"] = datetime(2026, 9, 2, 10, 0)

    with pytest.raises(ValidationError) as exc_info:
        ClaimSubmission.model_validate(valid_synthetic_claim)

    assert {error["type"] for error in exc_info.value.errors()} == {"timezone_aware"}


def test_completeness_issues_reports_missing_vehicle_reference(
    valid_synthetic_claim: dict[str, object],
) -> None:
    valid_synthetic_claim["incident"] = {}

    claim = ClaimSubmission.model_validate(valid_synthetic_claim)

    assert claim.completeness_issues() == ("missing_vehicle_reference",)


@pytest.mark.parametrize(
    ("claim_type", "incident"),
    [
        (ClaimType.MOTOR, {"vehicle_reference": "   "}),
        (ClaimType.PROPERTY, {"property_reference": "   "}),
    ],
)
def test_blank_incident_reference_is_rejected(
    valid_synthetic_claim: dict[str, object],
    claim_type: ClaimType,
    incident: dict[str, str],
) -> None:
    valid_synthetic_claim["claim_type"] = claim_type
    valid_synthetic_claim["incident"] = incident

    with pytest.raises(ValidationError, match="reference"):
        ClaimSubmission.model_validate(valid_synthetic_claim)
