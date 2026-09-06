from datetime import UTC, datetime
from decimal import Decimal

import pytest
from pydantic import TypeAdapter, ValidationError

from aegis.domain.base import UtcDatetime, canonical_json, content_hash


def test_canonical_json_is_key_order_independent() -> None:
    first = canonical_json({"alpha": 1, "beta": 2})
    second = canonical_json({"beta": 2, "alpha": 1})

    assert first == second


def test_absent_and_null_fields_hash_identically() -> None:
    with_null = content_hash({"claim": "approved", "reason": None})
    without_null = content_hash({"claim": "approved"})

    assert with_null == without_null


def test_content_hash_changes_when_any_value_changes() -> None:
    original = content_hash({"claim": "approved"})
    changed = content_hash({"claim": "rejected"})

    assert original != changed


def test_decimal_is_hashed_as_string_not_float() -> None:
    payload = {"amount": Decimal("10.50")}

    assert canonical_json(payload) == '{"amount":"10.50"}'
    assert content_hash(payload) != content_hash({"amount": 10.5})


def test_naive_datetime_is_rejected() -> None:
    adapter = TypeAdapter(UtcDatetime)

    with pytest.raises(ValidationError):
        adapter.validate_python(datetime(2026, 9, 5, 12, 0, 0))


def test_offset_datetime_normalises_to_utc() -> None:
    adapter = TypeAdapter(UtcDatetime)

    result = adapter.validate_python("2026-09-05T14:00:00+02:00")

    assert result == datetime(2026, 9, 5, 12, 0, 0, tzinfo=UTC)
    assert result.tzinfo is UTC
