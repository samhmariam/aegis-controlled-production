"""Tool-plane contracts: what the model proposed, and what came back from executing it."""

from __future__ import annotations

from collections.abc import Mapping
from enum import StrEnum
from typing import Self

from pydantic import Field, JsonValue, model_validator

from aegis.domain.base import (
    ActionId,
    ClauseId,
    IdempotencyKey,
    InvocationId,
    PrincipalId,
    RunId,
    Sha256Hash,
    StrictModel,
    ToolName,
    UtcDatetime,
)
from aegis.domain.base import content_hash as compute_content_hash


class ActionProposal(StrictModel):
    run_id: RunId
    action_id: ActionId
    tool_name: ToolName
    arguments: Mapping[str, JsonValue]
    arguments_hash: Sha256Hash
    rationale: str = Field(min_length=1, max_length=2000)
    cited_clause_ids: tuple[ClauseId, ...]
    confidence: float = Field(ge=0.0, le=1.0)
    consequential: bool
    proposed_by: PrincipalId
    model_id: str = Field(min_length=1, max_length=120)
    model_version: str = Field(min_length=1, max_length=60)
    prompt_version: str = Field(min_length=1, max_length=60)
    proposed_at: UtcDatetime

    @model_validator(mode="after")
    def _verify_arguments_hash(self) -> Self:
        if self.arguments_hash != compute_content_hash(dict(self.arguments)):
            raise ValueError("arguments_hash does not match arguments")
        return self


class ToolStatus(StrEnum):
    SUCCEEDED = "succeeded"
    DENIED = "denied"
    FAILED = "failed"
    UNCERTAIN = "uncertain"
    DUPLICATE = "duplicate"


class ToolResult(StrictModel):
    """The outcome of one tool invocation, including the outcomes that are not knowable."""

    tool_name: ToolName
    invocation_id: InvocationId
    idempotency_key: IdempotencyKey | None
    status: ToolStatus
    effect_id: str | None = Field(default=None, max_length=120)
    retryable: bool
    error_code: str | None = Field(
        default=None,
        min_length=1,
        max_length=60,
        pattern=r"^[a-z][a-z0-9_]*$",
    )
    error_message: str | None = Field(default=None, max_length=500)
    started_at: UtcDatetime
    completed_at: UtcDatetime

    @model_validator(mode="after")
    def _check_invariants(self) -> Self:
        if self.completed_at < self.started_at:
            raise ValueError("completed_at cannot precede started_at")

        produced_effect = self.status in (ToolStatus.SUCCEEDED, ToolStatus.DUPLICATE)

        if produced_effect:
            if self.effect_id is None:
                raise ValueError(f"{self.status} must carry the effect_id it created or matched")
            if self.idempotency_key is None:
                raise ValueError(f"{self.status} must carry an idempotency_key")
            if self.error_code is not None or self.error_message is not None:
                raise ValueError(f"{self.status} must not carry error fields")
            if self.retryable:
                raise ValueError(f"{self.status} must not be retryable")
        else:
            if self.effect_id is not None:
                raise ValueError(f"{self.status} must not claim an effect_id")
            if self.error_code is None:
                raise ValueError(f"{self.status} requires a machine-readable error_code")

        if self.status is ToolStatus.DENIED and self.retryable:
            raise ValueError("a denied call must not be retryable; the decision will not change")

        if self.status is ToolStatus.UNCERTAIN and self.retryable and self.idempotency_key is None:
            raise ValueError("an uncertain call is only retryable under an idempotency key")

        return self

    @property
    def duration_ms(self) -> int:
        return int((self.completed_at - self.started_at).total_seconds() * 1000)
