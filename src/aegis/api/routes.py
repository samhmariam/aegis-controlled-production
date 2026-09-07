"""Thin routes. Every rule they appear to enforce is enforced by a contract."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from aegis.api.dependencies import current_principal, get_context_service
from aegis.api.schemas import (
    ClaimValidationResponse,
    ContextResponse,
    HealthResponse,
    VersionResponse,
)
from aegis.config import Settings, get_settings
from aegis.context.service import ContextService
from aegis.domain.base import ClaimId
from aegis.domain.models import ClaimSubmission
from aegis.identity.principal import Principal

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


@router.get("/claims/{claim_id}/context", response_model=ContextResponse)
def claim_context(
    claim_id: ClaimId,
    query: Annotated[str, Query(min_length=1, max_length=1000)],
    principal: Annotated[Principal, Depends(current_principal)],
    service: Annotated[ContextService, Depends(get_context_service)],
) -> ContextResponse:
    """Permission-aware policy context. Tenant scope comes from the principal, never the URL."""
    return ContextResponse.from_result(
        service.retrieve(principal=principal, claim_id=claim_id, query=query)
    )
