from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from aegis.approvals.models import ApprovalRecord

ISSUED_AT = datetime(2026, 9, 6, 12, 0, tzinfo=UTC)
EXPIRES_AT = datetime(2026, 9, 6, 13, 0, tzinfo=UTC)


def valid_approval_payload() -> dict[str, object]:
    return {
        "approval_id": "approval-example-001",
        "run_id": "run-example-001",
        "action_id": "action-example-001",
        "tool_name": "request_information",
        "arguments_hash": "sha256:" + "a" * 64,
        "decision_id": "decision-example-001",
        "approver_principal_id": "principal-example-001",
        "decision": "approve",
        "issued_at": ISSUED_AT,
        "expires_at": EXPIRES_AT,
        "nonce": "a" * 32,
    }


def test_valid_approval_record_parses() -> None:
    approval = ApprovalRecord.model_validate(valid_approval_payload())

    assert approval.approval_id == "approval-example-001"
    assert approval.decision.value == "approve"
    assert approval.is_consumed is False


def test_expiry_before_issue_is_rejected() -> None:
    payload = valid_approval_payload()
    payload["expires_at"] = ISSUED_AT

    with pytest.raises(ValidationError, match="expires_at must be after issued_at"):
        ApprovalRecord.model_validate(payload)


def test_consumed_at_before_issue_is_rejected() -> None:
    payload = valid_approval_payload()
    payload["consumed_at"] = datetime(2026, 9, 6, 11, 59, tzinfo=UTC)

    with pytest.raises(ValidationError, match="consumed_at cannot precede issued_at"):
        ApprovalRecord.model_validate(payload)


def test_consumed_at_after_expiry_is_rejected() -> None:
    payload = valid_approval_payload()
    payload["consumed_at"] = datetime(2026, 9, 6, 13, 1, tzinfo=UTC)

    with pytest.raises(ValidationError, match="consumed_at cannot follow expires_at"):
        ApprovalRecord.model_validate(payload)


def test_malformed_nonce_is_rejected() -> None:
    payload = valid_approval_payload()
    payload["nonce"] = "not-a-valid-nonce"

    with pytest.raises(ValidationError, match="nonce"):
        ApprovalRecord.model_validate(payload)


def test_unknown_field_is_rejected() -> None:
    payload = valid_approval_payload()
    payload["debug_notes"] = "unexpected field"

    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        ApprovalRecord.model_validate(payload)
