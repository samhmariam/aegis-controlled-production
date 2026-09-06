"""Thin routes. Every rule they appear to enforce is enforced by a contract."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends

from aegis.api.schemas import ClaimValidationResponse, HealthResponse, VersionResponse
from aegis.config import Settings, get_settings
from aegis.domain.models import ClaimSubmission

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Liveness of this process only. It asserts nothing about downstream services."""
    return HealthResponse(status="ok", service="aegis", checked_at=datetime.now(UTC))


@router.get("/version", response_model=VersionResponse)
def version(settings: Annotated[Settings, Depends(get_settings)]) -> VersionResponse:
    return VersionResponse(
        service="aegis",
        app_version=settings.app_version,
        schema_version=settings.schema_version,
        environment=settings.environment,
    )


@router.post("/claims/validate", response_model=ClaimValidationResponse)
def validate_claim(claim: ClaimSubmission) -> ClaimValidationResponse:
    """Schema-only validation. No persistence, no retrieval, no tool call."""
    return ClaimValidationResponse(
        valid=True,
        claim_id=claim.claim_id,
        tenant_id=claim.tenant_id,
        claim_type=claim.claim_type,
        completeness_issues=claim.completeness_issues(),
        validated_at=datetime.now(UTC),
    )
