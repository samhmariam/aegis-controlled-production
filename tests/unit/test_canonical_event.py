from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from aegis.audit.events import CanonicalEvent, EventCore, EventType

OCCURRED_AT = datetime(2026, 9, 6, 12, 0, tzinfo=UTC)
PREVIOUS_EVENT_HASH = "sha256:" + "b" * 64


def valid_core_payload() -> dict[str, object]:
    return {
        "sequence": 0,
        "event_id": "event-example-001",
        "correlation_id": "corr-example-001",
        "run_id": "run-example-001",
        "action_id": "action-example-001",
        "event_type": "tool_invoked",
        "actor_principal_id": "principal-example-001",
        "workload_identity": "aegis-agent",
        "model_version": "gpt-5-2026-09-01",
        "prompt_version": "v1",
        "policy_version": "v1",
        "tool_version": "request-information-v1",
        "decision_id": "decision-example-001",
        "approval_id": "approval-example-001",
        "arguments_hash": "sha256:" + "a" * 64,
        "result_status": "succeeded",
        "occurred_at": OCCURRED_AT,
        "previous_event_hash": None,
    }


def valid_core() -> EventCore:
    return EventCore.model_validate(valid_core_payload())


def test_sealed_event_verifies() -> None:
    core = valid_core()
    event = CanonicalEvent.seal(core)

    verified = CanonicalEvent.model_validate(event.model_dump())

    assert verified == event


def test_event_reloaded_from_json_still_verifies() -> None:
    event = CanonicalEvent.seal(valid_core())

    reloaded = CanonicalEvent.model_validate_json(event.model_dump_json())

    assert reloaded == event


def test_sequence_zero_rejects_previous_hash() -> None:
    payload = valid_core_payload()
    payload["previous_event_hash"] = PREVIOUS_EVENT_HASH

    with pytest.raises(ValidationError, match="first event in a chain has no previous hash"):
        EventCore.model_validate(payload)


def test_sequence_above_zero_requires_previous_hash() -> None:
    payload = valid_core_payload()
    payload["sequence"] = 1

    with pytest.raises(
        ValidationError,
        match="every event after the first must link to its predecessor",
    ):
        EventCore.model_validate(payload)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("event_id", "event-mutated-001"),
        ("correlation_id", "corr-mutated-001"),
        ("event_type", EventType.RUN_COMPLETED),
        ("workload_identity", "different-agent"),
        ("model_version", "different-model"),
        ("occurred_at", datetime(2026, 9, 6, 12, 1, tzinfo=UTC)),
    ],
)
def test_mutating_any_field_breaks_the_hash(field: str, value: object) -> None:
    event = CanonicalEvent.seal(valid_core())
    payload = event.model_dump()
    payload[field] = value

    with pytest.raises(ValidationError, match="event_hash does not match event content"):
        CanonicalEvent.model_validate(payload)


def test_event_model_has_no_raw_arguments_field() -> None:
    assert "arguments" not in CanonicalEvent.model_fields
