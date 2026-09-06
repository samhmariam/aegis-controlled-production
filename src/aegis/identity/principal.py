from datetime import datetime
from enum import StrEnum
from typing import Self

from pydantic import Field, model_validator

from aegis.domain.base import PrincipalId, StrictModel, TenantId, UtcDatetime


class PrincipalType(StrEnum):
    USER = "user"
    WORKLOAD = "workload"
    OPERATOR = "operator"


class AuthenticationMethod(StrEnum):
    # Enum identifiers for auth methods, not credential values.
    DEMO_TOKEN = "demo_token"  # noqa: S105 - Sprint 1 only, explicitly non-production
    WORKLOAD_SECRET = "workload_secret"  # noqa: S105


class Principal(StrictModel):
    principal_id: PrincipalId
    principal_type: PrincipalType
    tenant_id: TenantId
    scopes: frozenset[str] = Field(min_length=1)
    roles: frozenset[str] = Field(default_factory=frozenset)
    authenticated_at: UtcDatetime
    expires_at: UtcDatetime
    authentication_method: AuthenticationMethod

    @model_validator(mode="after")
    def _check_window(self) -> Self:
        if self.authenticated_at >= self.expires_at:
            raise ValueError("expires_at must be after authenticated_at")
        return self

    def is_expired(self, now: datetime) -> bool:
        return now >= self.expires_at
