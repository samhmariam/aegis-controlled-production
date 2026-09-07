"""Fixture loading and validation. The seed and the fixture tests share these definitions."""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from aegis.domain.base import (
    Money,
    PolicyId,
    PolicyVersion,
    StrictModel,
    TenantId,
    UtcDatetime,
    content_hash,
)
from aegis.domain.models import ClaimType, Currency


class PolicyFixture(StrictModel):
    policy_id: PolicyId
    tenant_id: TenantId
    policy_version: PolicyVersion
    line_of_business: ClaimType
    effective_from: UtcDatetime
    effective_to: UtcDatetime | None = None
    autonomous_settlement_limit: Money
    currency: Currency


def load_json_array(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError(f"{path} must contain a JSON array")
    return payload


def record_hash(payload: Mapping[str, Any]) -> str:
    """Idempotency identity for a seeded row.

    Hashes the fixture object exactly as authored. canonical_json prunes None values, so an
    absent key and an explicit null hash identically — which is what makes 'unchanged' stable
    across reruns.
    """
    return content_hash(payload)
