from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from aegis.domain.models import WorkflowResult, WorkflowStatus
from aegis.tools.models import ToolStatus

STARTED_AT = datetime(2026, 9, 6, 12, 0, tzinfo=UTC)
COMPLETED_AT = STARTED_AT + timedelta(minutes=1)


def valid_workflow_result_payload() -> dict[str, object]:
    return {
        "run_id": "run-example-001",
        "claim_id": "claim-example-001",
        "tenant_id": "tenant-example-001",
        "status": "completed",
        "action_id": "action-example-001",
        "decision_id": "decision-example-001",
        "result_invocation_id": "invocation-example-001",
        "result_status": "succeeded",
        "explanation": "The synthetic workflow completed successfully.",
        "started_at": STARTED_AT,
        "completed_at": COMPLETED_AT,
    }


def test_completed_workflow_result_has_action_and_result_references() -> None:
    result = WorkflowResult.model_validate(valid_workflow_result_payload())

    assert result.status is WorkflowStatus.COMPLETED
    assert result.result_invocation_id == "invocation-example-001"
    assert result.result_status is ToolStatus.SUCCEEDED


def test_result_status_without_result_reference_is_rejected() -> None:
    payload = valid_workflow_result_payload()
    payload["result_invocation_id"] = None

    with pytest.raises(
        ValidationError,
        match="result_invocation_id and result_status must be provided together",
    ):
        WorkflowResult.model_validate(payload)


def test_result_reference_without_result_status_is_rejected() -> None:
    payload = valid_workflow_result_payload()
    payload["result_status"] = None

    with pytest.raises(
        ValidationError,
        match="result_invocation_id and result_status must be provided together",
    ):
        WorkflowResult.model_validate(payload)


def test_stopped_workflow_requires_completed_at() -> None:
    payload = valid_workflow_result_payload()
    payload.update(
        status="stopped",
        result_invocation_id=None,
        result_status=None,
        completed_at=None,
    )

    with pytest.raises(ValidationError, match="stopped is terminal and requires completed_at"):
        WorkflowResult.model_validate(payload)


def test_completed_at_before_started_at_is_rejected() -> None:
    payload = valid_workflow_result_payload()
    payload["completed_at"] = STARTED_AT - timedelta(seconds=1)

    with pytest.raises(ValidationError, match="completed_at cannot precede started_at"):
        WorkflowResult.model_validate(payload)


def test_extra_field_is_rejected() -> None:
    payload = valid_workflow_result_payload()
    payload["raw_result"] = {"claim": "sensitive"}

    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        WorkflowResult.model_validate(payload)
