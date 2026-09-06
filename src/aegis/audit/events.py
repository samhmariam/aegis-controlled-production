"""Canonical audit events. The hash-chained ledger and its verifier arrive on Day 6."""

from __future__ import annotations

from enum import StrEnum
from typing import Any, Self

from pydantic import Field, model_validator

from aegis.domain.base import (
    ActionId,
    ApprovalId,
    CorrelationId,
    DecisionId,
    EventId,
    PolicyVersion,
    PrincipalId,
    RunId,
    Sha256Hash,
    StrictModel,
    UtcDatetime,
)
from aegis.domain.base import content_hash as compute_content_hash
from aegis.tools.models import ToolStatus


class EventType(StrEnum):
    RUN_STARTED = "run_started"
    CONTEXT_RETRIEVED = "context_retrieved"
    ACTION_PROPOSED = "action_proposed"
    AUTHORIZATION_DECIDED = "authorization_decided"
    APPROVAL_REQUESTED = "approval_requested"
    APPROVAL_RECORDED = "approval_recorded"
    TOOL_INVOKED = "tool_invoked"
    TOOL_RESULT_RECORDED = "tool_result_recorded"
    RUN_COMPLETED = "run_completed"
    KILL_SWITCH_ENGAGED = "kill_switch_engaged"


class EventCore(StrictModel):
    """Every field of an event except its hash. Callers build one of these; the ledger seals it."""

    sequence: int = Field(ge=0)
    event_id: EventId
    correlation_id: CorrelationId
    run_id: RunId
    action_id: ActionId | None = None
    event_type: EventType
    actor_principal_id: PrincipalId
    workload_identity: str = Field(min_length=1, max_length=120)
    model_version: str = Field(min_length=1, max_length=60)
    prompt_version: str = Field(min_length=1, max_length=60)
    policy_version: PolicyVersion
    tool_version: str = Field(min_length=1, max_length=60)
    decision_id: DecisionId | None = None
    approval_id: ApprovalId | None = None
    arguments_hash: Sha256Hash | None = None
    result_status: ToolStatus | None = None
    occurred_at: UtcDatetime
    previous_event_hash: Sha256Hash | None = None

    @model_validator(mode="after")
    def _check_chain_position(self) -> Self:
        if self.sequence == 0 and self.previous_event_hash is not None:
            raise ValueError("the first event in a chain has no previous hash")
        if self.sequence > 0 and self.previous_event_hash is None:
            raise ValueError("every event after the first must link to its predecessor")
        return self

    def hash_payload(self) -> dict[str, Any]:
        """JSON-mode dump: datetimes and enums become their serialised form on both sides."""
        return self.model_dump(mode="json")


class CanonicalEvent(EventCore):
    """A sealed event. The hash covers every field of the core, and nothing else."""

    event_hash: Sha256Hash

    @classmethod
    def seal(cls, core: EventCore) -> Self:
        return cls(**core.model_dump(), event_hash=compute_content_hash(core.hash_payload()))

    @model_validator(mode="after")
    def _verify_hash(self) -> Self:
        core = EventCore.model_validate(self.model_dump(exclude={"event_hash"}))
        if self.event_hash != compute_content_hash(core.hash_payload()):
            raise ValueError("event_hash does not match event content")
        return self
