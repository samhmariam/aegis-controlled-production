"""HTTP-boundary contracts. Domain validation lives in the contracts, never in a handler."""

from __future__ import annotations

from typing import Literal

from aegis.context.citations import CitationOutcome
from aegis.context.models import ContextBundle
from aegis.context.service import RetrievalResult, RetrievalStatus
from aegis.domain.base import (
    ClaimId,
    ClauseId,
    PolicyId,
    PolicyVersion,
    Sha256Hash,
    StrictModel,
    TenantId,
    UtcDatetime,
)
from aegis.domain.models import ClaimType


class HealthResponse(StrictModel):
    status: Literal["ok"]
    service: Literal["aegis"]
    checked_at: UtcDatetime


class VersionResponse(StrictModel):
    service: Literal["aegis"]
    app_version: str
    schema_version: str
    environment: Literal["local", "demo"]


class ClaimValidationResponse(StrictModel):
    valid: Literal[True]
    claim_id: ClaimId
    tenant_id: TenantId
    claim_type: ClaimType
    completeness_issues: tuple[str, ...]
    validated_at: UtcDatetime


class ErrorDetail(StrictModel):
    field: str
    code: str


class ErrorEnvelope(StrictModel):
    error_code: str
    details: tuple[ErrorDetail, ...]


class ContextResponse(StrictModel):
    status: RetrievalStatus
    bundle: ContextBundle

    @classmethod
    def from_result(cls, result: RetrievalResult) -> ContextResponse:
        return cls(status=result.status, bundle=result.bundle)


class CitationVerificationResponse(StrictModel):
    clause_id: ClauseId
    policy_id: PolicyId
    policy_version: PolicyVersion
    claimed_hash: Sha256Hash
    recomputed_hash: Sha256Hash | None
    outcome: CitationOutcome
    verified_at: UtcDatetime
