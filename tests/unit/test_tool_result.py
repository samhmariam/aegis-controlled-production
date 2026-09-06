from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from aegis.tools.models import ToolResult

STARTED_AT = datetime(2026, 9, 6, 12, 0, tzinfo=UTC)
COMPLETED_AT = datetime(2026, 9, 6, 12, 1, tzinfo=UTC)


def valid_tool_result_payload() -> dict[str, object]:
    return {
        "tool_name": "request_information",
        "invocation_id": "invocation-example-001",
        "idempotency_key": "idemkey-001",
        "status": "succeeded",
        "effect_id": "effect-example-001",
        "retryable": False,
        "error_code": None,
        "error_message": None,
        "started_at": STARTED_AT,
        "completed_at": COMPLETED_AT,
    }


def test_succeeded_result_constructs() -> None:
    result = ToolResult.model_validate(valid_tool_result_payload())

    assert result.status.value == "succeeded"
    assert result.effect_id == "effect-example-001"


def test_denied_result_constructs() -> None:
    payload = valid_tool_result_payload()
    payload.update(
        status="denied",
        effect_id=None,
        error_code="authorization_denied",
        error_message="The action was denied by policy.",
    )

    result = ToolResult.model_validate(payload)

    assert result.status.value == "denied"
    assert result.error_code == "authorization_denied"


def test_failed_result_constructs() -> None:
    payload = valid_tool_result_payload()
    payload.update(
        status="failed",
        effect_id=None,
        error_code="tool_unavailable",
        error_message="The downstream tool was unavailable.",
    )

    result = ToolResult.model_validate(payload)

    assert result.status.value == "failed"
    assert result.error_code == "tool_unavailable"


def test_uncertain_result_constructs_with_idempotency_key() -> None:
    payload = valid_tool_result_payload()
    payload.update(
        idempotency_key="idemkey-001",
        status="uncertain",
        effect_id=None,
        retryable=True,
        error_code="timeout",
        error_message="The tool call timed out before a result was received.",
    )

    result = ToolResult.model_validate(payload)

    assert result.status.value == "uncertain"
    assert result.retryable is True
    assert result.idempotency_key == "idemkey-001"


def test_duplicate_result_constructs() -> None:
    payload = valid_tool_result_payload()
    payload.update(
        idempotency_key="idemkey-001",
        status="duplicate",
    )

    result = ToolResult.model_validate(payload)

    assert result.status.value == "duplicate"
    assert result.effect_id == "effect-example-001"


def test_succeeded_without_effect_id_is_rejected() -> None:
    payload = valid_tool_result_payload()
    payload["effect_id"] = None

    with pytest.raises(ValidationError, match="succeeded must carry the effect_id"):
        ToolResult.model_validate(payload)


def test_succeeded_without_idempotency_key_is_rejected() -> None:
    payload = valid_tool_result_payload()
    payload["idempotency_key"] = None

    with pytest.raises(ValidationError, match="succeeded must carry an idempotency_key"):
        ToolResult.model_validate(payload)


def test_failed_with_blank_error_code_is_rejected() -> None:
    payload = valid_tool_result_payload()
    payload.update(
        status="failed",
        effect_id=None,
        error_code="   ",
    )

    with pytest.raises(ValidationError, match="error_code"):
        ToolResult.model_validate(payload)


def test_completed_before_started_is_rejected() -> None:
    payload = valid_tool_result_payload()
    payload["completed_at"] = STARTED_AT.replace(hour=11, minute=59)

    with pytest.raises(ValidationError, match="completed_at cannot precede started_at"):
        ToolResult.model_validate(payload)
