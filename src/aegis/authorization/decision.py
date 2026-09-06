"""The deterministic gate's output contract. The gate itself arrives on Day 5."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Self

from pydantic import Field, model_validator

from aegis.domain.base import (
    ActionId,
    DecisionId,
    PolicyVersion,
    PrincipalId,
    RunId,
    Sha256Hash,
    StrictModel,
    TenantId,
    ToolName,
    UtcDatetime,
)


class DecisionOutcome(StrEnum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_APPROVAL = "require_approval"


class ReasonCode(StrEnum):
    WITHIN_POLICY = "within_policy"
    TENANT_MISMATCH = "tenant_mismatch"
    SCOPE_MISSING = "scope_missing"
    AMOUNT_ABOVE_AUTONOMOUS_LIMIT = "amount_above_autonomous_limit"
    CONSEQUENTIAL_ACTION_REQUIRES_HUMAN = "consequential_action_requires_human"
    TOOL_NOT_IN_MANIFEST = "tool_not_in_manifest"
    KILL_SWITCH_ACTIVE = "kill_switch_active"
    PRINCIPAL_EXPIRED = "principal_expired"


class AuthorizationDecision(StrictModel):
    """One decision about one proposed action, bound to the exact arguments that were judged."""

    decision_id: DecisionId
    policy_version: PolicyVersion
    principal_id: PrincipalId
    tenant_id: TenantId
    run_id: RunId
    action_id: ActionId
    tool_name: ToolName
    arguments_hash: Sha256Hash
    outcome: DecisionOutcome
    reason_code: ReasonCode
    explanation: str = Field(min_length=1, max_length=1000)
    required_approver_role: str | None = Field(default=None, min_length=1, max_length=60)
    decided_at: UtcDatetime
    expires_at: UtcDatetime

    @model_validator(mode="after")
    def _check_invariants(self) -> Self:
        if self.decided_at >= self.expires_at:
            raise ValueError("expires_at must be after decided_at")

        needs_role = self.outcome is DecisionOutcome.REQUIRE_APPROVAL
        if needs_role and self.required_approver_role is None:
            raise ValueError("require_approval must name the approver role")
        if not needs_role and self.required_approver_role is not None:
            raise ValueError("required_approver_role is only valid for require_approval")

        if (
            self.outcome is DecisionOutcome.ALLOW
            and self.reason_code is not ReasonCode.WITHIN_POLICY
        ):
            raise ValueError("an allow decision must carry reason_code within_policy")
        if (
            self.outcome is not DecisionOutcome.ALLOW
            and self.reason_code is ReasonCode.WITHIN_POLICY
        ):
            raise ValueError("within_policy is only valid for an allow decision")

        return self

    def is_expired(self, now: datetime) -> bool:
        return now >= self.expires_at
