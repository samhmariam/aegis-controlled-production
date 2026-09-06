from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from aegis.domain.base import content_hash
from aegis.tools.models import ActionProposal

PROPOSED_AT = datetime(2026, 9, 6, 12, 0, tzinfo=UTC)

VALID_ARGUMENTS: dict[str, object] = {
    "claim_id": "claim-example-001",
    "reason_codes": ["missing_vehicle_reference"],
}


def valid_proposal_payload() -> dict[str, object]:
    return {
        "run_id": "run-example-001",
        "action_id": "action-example-001",
        "tool_name": "request_information",
        "arguments": VALID_ARGUMENTS,
        "arguments_hash": content_hash(VALID_ARGUMENTS),
        "rationale": "Vehicle reference is required to assess a motor claim.",
        "cited_clause_ids": ("clause-collision-001",),
        "confidence": 0.87,
        "consequential": False,
        "proposed_by": "principal-example-001",
        "model_id": "gpt-5",
        "model_version": "2026-09-01",
        "prompt_version": "v1",
        "proposed_at": PROPOSED_AT,
    }


def test_valid_proposal_parses() -> None:
    proposal = ActionProposal.model_validate(valid_proposal_payload())

    assert proposal.action_id == "action-example-001"
    assert proposal.tool_name == "request_information"
    assert dict(proposal.arguments) == VALID_ARGUMENTS
    assert proposal.confidence == pytest.approx(0.87)
    assert proposal.consequential is False


def test_arguments_as_raw_string_is_rejected() -> None:
    payload = valid_proposal_payload()
    payload["arguments"] = '{"claim_id": "claim-example-001"}'

    with pytest.raises(ValidationError, match="arguments"):
        ActionProposal.model_validate(payload)


def test_mismatched_arguments_hash_is_rejected() -> None:
    payload = valid_proposal_payload()
    payload["arguments_hash"] = content_hash({"claim_id": "claim-other-001"})

    with pytest.raises(ValidationError, match="arguments_hash does not match arguments"):
        ActionProposal.model_validate(payload)


@pytest.mark.parametrize("confidence", [-0.01, 1.01])
def test_confidence_outside_zero_one_is_rejected(confidence: float) -> None:
    payload = valid_proposal_payload()
    payload["confidence"] = confidence

    with pytest.raises(ValidationError, match="confidence"):
        ActionProposal.model_validate(payload)


def test_extra_field_is_rejected() -> None:
    payload = valid_proposal_payload()
    payload["debug_notes"] = "model also considered escalation"

    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        ActionProposal.model_validate(payload)
