from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from aegis.authorization.decision import AuthorizationDecision

DECIDED_AT = datetime(2026, 9, 6, 12, 0, tzinfo=UTC)
EXPIRES_AT = datetime(2026, 9, 6, 13, 0, tzinfo=UTC)


def valid_decision_payload() -> dict[str, object]:
    return {
        "decision_id": "decision-example-001",
        "policy_version": "v1",
        "principal_id": "principal-example-001",
        "tenant_id": "tenant-example-001",
        "run_id": "run-example-001",
        "action_id": "action-example-001",
        "tool_name": "request_information",
        "arguments_hash": "sha256:" + "a" * 64,
        "outcome": "allow",
        "reason_code": "within_policy",
        "explanation": "The requested action is within policy.",
        "decided_at": DECIDED_AT,
        "expires_at": EXPIRES_AT,
    }


@pytest.mark.parametrize(
    ("outcome", "reason_code", "required_approver_role"),
    [
        ("allow", "within_policy", None),
        ("deny", "scope_missing", None),
        ("require_approval", "consequential_action_requires_human", "claims-manager"),
    ],
)
def test_each_decision_outcome_constructs(
    outcome: str,
    reason_code: str,
    required_approver_role: str | None,
) -> None:
    payload = valid_decision_payload()
    payload["outcome"] = outcome
    payload["reason_code"] = reason_code
    payload["required_approver_role"] = required_approver_role

    decision = AuthorizationDecision.model_validate(payload)

    assert decision.outcome.value == outcome
    assert decision.reason_code.value == reason_code
    assert decision.required_approver_role == required_approver_role


def test_unknown_outcome_is_rejected() -> None:
    payload = valid_decision_payload()
    payload["outcome"] = "escalate"

    with pytest.raises(ValidationError, match="outcome"):
        AuthorizationDecision.model_validate(payload)


def test_require_approval_without_approver_role_is_rejected() -> None:
    payload = valid_decision_payload()
    payload["outcome"] = "require_approval"
    payload["reason_code"] = "consequential_action_requires_human"

    with pytest.raises(ValidationError, match="require_approval must name the approver role"):
        AuthorizationDecision.model_validate(payload)


def test_require_approval_with_blank_approver_role_is_rejected() -> None:
    payload = valid_decision_payload()
    payload["outcome"] = "require_approval"
    payload["reason_code"] = "consequential_action_requires_human"
    payload["required_approver_role"] = "   "

    with pytest.raises(ValidationError, match="required_approver_role"):
        AuthorizationDecision.model_validate(payload)


def test_allow_with_approver_role_is_rejected() -> None:
    payload = valid_decision_payload()
    payload["required_approver_role"] = "claims-manager"

    with pytest.raises(
        ValidationError,
        match="required_approver_role is only valid for require_approval",
    ):
        AuthorizationDecision.model_validate(payload)


def test_expiry_before_decision_is_rejected() -> None:
    payload = valid_decision_payload()
    payload["expires_at"] = DECIDED_AT

    with pytest.raises(ValidationError, match="expires_at must be after decided_at"):
        AuthorizationDecision.model_validate(payload)
