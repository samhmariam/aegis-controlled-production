"""Human approval as data bound to one proposed effect. The service arrives on Day 5."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Annotated, Self

from pydantic import StringConstraints, model_validator

from aegis.domain.base import (
    ActionId,
    ApprovalId,
    DecisionId,
    PrincipalId,
    RunId,
    Sha256Hash,
    StrictModel,
    ToolName,
    UtcDatetime,
)


class ApprovalDecision(StrEnum):
    APPROVE = "approve"
    REJECT = "reject"


class ApprovalRecord(StrictModel):
    """An approval is data bound to one proposed effect.

    Any mutation of amount, payee, claim, action or policy decision invalidates this approval:
    the arguments hash and decision id are part of the binding, so a changed proposal no longer
    matches a previously issued record.
    """

    approval_id: ApprovalId
    run_id: RunId
    action_id: ActionId
    tool_name: ToolName
    arguments_hash: Sha256Hash
    decision_id: DecisionId
    approver_principal_id: PrincipalId
    decision: ApprovalDecision
    issued_at: UtcDatetime
    expires_at: UtcDatetime
    nonce: Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{32}$")]
    consumed_at: UtcDatetime | None = None

    @model_validator(mode="after")
    def _check_invariants(self) -> Self:
        if self.issued_at >= self.expires_at:
            raise ValueError("expires_at must be after issued_at")
        if self.consumed_at is not None:
            if self.consumed_at < self.issued_at:
                raise ValueError("consumed_at cannot precede issued_at")
            if self.consumed_at > self.expires_at:
                raise ValueError("consumed_at cannot follow expires_at")
        return self

    @property
    def is_consumed(self) -> bool:
        return self.consumed_at is not None

    def is_usable_at(self, moment: datetime) -> bool:
        """Single-use: an approval is spendable once, before expiry, and only if it approves."""
        return (
            self.decision is ApprovalDecision.APPROVE
            and not self.is_consumed
            and self.issued_at <= moment < self.expires_at
        )

    def binds(self, *, run_id: str, action_id: str, tool_name: str, arguments_hash: str) -> bool:
        """Every element of the binding must match; any mutation invalidates the approval."""
        return (
            self.run_id == run_id
            and self.action_id == action_id
            and self.tool_name == tool_name
            and self.arguments_hash == arguments_hash
        )
