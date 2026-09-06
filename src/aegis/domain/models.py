from enum import StrEnum
from typing import Self

from pydantic import Field, model_validator

from aegis.domain.base import (
    ActionId,
    ClaimantReference,
    ClaimId,
    DecisionId,
    InvocationId,
    Money,
    PolicyId,
    RunId,
    StrictModel,
    TenantId,
    UtcDatetime,
)
from aegis.tools.models import ToolStatus


class ClaimType(StrEnum):
    MOTOR = "motor"
    PROPERTY = "property"


class Currency(StrEnum):
    GBP = "GBP"


class IncidentDetails(StrictModel):
    location_reference: str | None = Field(default=None, max_length=120)
    vehicle_reference: str | None = Field(default=None, min_length=1, max_length=60)
    property_reference: str | None = Field(default=None, min_length=1, max_length=60)
    third_party_involved: bool | None = None
    police_reference: str | None = Field(default=None, max_length=60)


class ClaimSubmission(StrictModel):
    claim_id: ClaimId
    tenant_id: TenantId
    policy_id: PolicyId
    claim_type: ClaimType
    claimant_reference: ClaimantReference
    loss_at: UtcDatetime
    submitted_at: UtcDatetime
    description: str = Field(min_length=1, max_length=4000)
    incident: IncidentDetails
    amount: Money | None = None
    currency: Currency | None = None

    @model_validator(mode="after")
    def _check_consistency(self) -> Self:
        if self.loss_at > self.submitted_at:
            raise ValueError("loss_at must not be after submitted_at")
        if self.amount is not None and self.currency is None:
            raise ValueError("currency is required when amount is present")
        if self.currency is not None and self.amount is None:
            raise ValueError("amount is required when currency is present")
        return self

    def completeness_issues(self) -> tuple[str, ...]:
        """Derived business-completeness reason codes; never accepted as input."""
        issues: list[str] = []
        if self.claim_type is ClaimType.MOTOR and self.incident.vehicle_reference is None:
            issues.append("missing_vehicle_reference")
        if self.claim_type is ClaimType.PROPERTY and self.incident.property_reference is None:
            issues.append("missing_property_reference")
        if self.amount is None:
            issues.append("missing_claimed_amount")
        return tuple(issues)


class WorkflowStatus(StrEnum):
    COMPLETED = "completed"
    AWAITING_APPROVAL = "awaiting_approval"
    DENIED = "denied"
    FAILED = "failed"
    STOPPED = "stopped"


class WorkflowResult(StrictModel):
    run_id: RunId
    claim_id: ClaimId
    tenant_id: TenantId
    status: WorkflowStatus
    action_id: ActionId | None = None
    decision_id: DecisionId | None = None
    result_invocation_id: InvocationId | None = None
    result_status: ToolStatus | None = None
    explanation: str = Field(min_length=1, max_length=2000)  # safe text; no raw claim content
    started_at: UtcDatetime
    completed_at: UtcDatetime | None = None

    @model_validator(mode="after")
    def _check_invariants(self) -> Self:
        terminal = self.status in (
            WorkflowStatus.COMPLETED,
            WorkflowStatus.DENIED,
            WorkflowStatus.FAILED,
            WorkflowStatus.STOPPED,
        )
        if terminal and self.completed_at is None:
            raise ValueError(f"{self.status} is terminal and requires completed_at")
        if self.status is WorkflowStatus.AWAITING_APPROVAL and self.completed_at is not None:
            raise ValueError("a run awaiting approval has not completed")
        has_result_reference = self.result_invocation_id is not None
        has_result_status = self.result_status is not None
        if has_result_reference != has_result_status:
            raise ValueError("result_invocation_id and result_status must be provided together")
        if self.completed_at is not None and self.completed_at < self.started_at:
            raise ValueError("completed_at cannot precede started_at")
        return self
