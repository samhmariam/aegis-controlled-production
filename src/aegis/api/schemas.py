"""HTTP-boundary contracts. Domain validation lives in the contracts, never in a handler."""

from __future__ import annotations

from typing import Literal

from aegis.domain.base import ClaimId, StrictModel, TenantId, UtcDatetime
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
