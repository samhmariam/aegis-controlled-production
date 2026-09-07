"""Shared contract primitives: strict base model, identifier types, canonical hashing."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from datetime import UTC, datetime
from decimal import Decimal
from typing import Annotated, Any

from pydantic import AfterValidator, AwareDatetime, BaseModel, ConfigDict, Field, StringConstraints

SCHEMA_VERSION = "2026-09-05.1"


class StrictModel(BaseModel):
    """Base for every external contract: unknown fields error, instances are immutable."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
    )


def _to_utc(value: datetime) -> datetime:
    return value.astimezone(UTC)


def to_canonical_timestamp(value: datetime) -> str:
    """The single textual form for a timestamp: UTC, ISO-8601, 'Z' suffix, sortable as text."""
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")



UtcDatetime = Annotated[AwareDatetime, AfterValidator(_to_utc)]

TenantId = Annotated[str, StringConstraints(pattern=r"^tenant-[a-z0-9][a-z0-9-]{2,47}$")]
ClaimId = Annotated[str, StringConstraints(pattern=r"^claim-[a-z0-9][a-z0-9-]{2,47}$")]
PolicyId = Annotated[str, StringConstraints(pattern=r"^policy-[a-z0-9][a-z0-9-]{2,47}$")]
ClauseId = Annotated[str, StringConstraints(pattern=r"^clause-[a-z0-9][a-z0-9-]{2,47}$")]
PrincipalId = Annotated[str, StringConstraints(pattern=r"^principal-[a-z0-9][a-z0-9-]{2,47}$")]
RunId = Annotated[str, StringConstraints(pattern=r"^run-[a-z0-9][a-z0-9-]{2,47}$")]
ActionId = Annotated[str, StringConstraints(pattern=r"^action-[a-z0-9][a-z0-9-]{2,47}$")]
DecisionId = Annotated[str, StringConstraints(pattern=r"^decision-[a-z0-9][a-z0-9-]{2,47}$")]
ApprovalId = Annotated[str, StringConstraints(pattern=r"^approval-[a-z0-9][a-z0-9-]{2,47}$")]
ToolName = Annotated[str, StringConstraints(pattern=r"^[a-z][a-z0-9_]{2,48}$")]
InvocationId = Annotated[str, StringConstraints(pattern=r"^invocation-[a-z0-9][a-z0-9-]{2,47}$")]
IdempotencyKey = Annotated[str, StringConstraints(pattern=r"^[a-z0-9][a-z0-9-]{7,63}$")]
EventId = Annotated[str, StringConstraints(pattern=r"^event-[a-z0-9][a-z0-9-]{2,47}$")]
CorrelationId = Annotated[str, StringConstraints(pattern=r"^corr-[a-z0-9][a-z0-9-]{2,47}$")]
ClaimantReference = Annotated[str, StringConstraints(pattern=r"^claimant-ref-[a-z0-9-]{3,40}$")]
Sha256Hash = Annotated[str, StringConstraints(pattern=r"^sha256:[0-9a-f]{64}$")]
PolicyVersion = Annotated[str, StringConstraints(pattern=r"^v[0-9]{1,4}$")]
Money = Annotated[Decimal, Field(ge=0, max_digits=12, decimal_places=2)]


def _canonical_default(value: Any) -> str:
    """Serialise the only non-JSON types allowed inside a canonical payload."""
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, datetime):
        return to_canonical_timestamp(value)
    raise TypeError(f"non-canonical type in payload: {type(value).__name__}")


def _prune(value: Any) -> Any:
    """Drop None-valued keys so an absent field and an explicit null hash identically."""
    if isinstance(value, Mapping):
        return {k: _prune(v) for k, v in value.items() if v is not None}
    if isinstance(value, (list, tuple)):
        return [_prune(item) for item in value]
    return value


def canonical_json(payload: Mapping[str, Any]) -> str:
    return json.dumps(
        _prune(payload),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=_canonical_default,
    )


def content_hash(payload: Mapping[str, Any]) -> str:
    digest = hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"
