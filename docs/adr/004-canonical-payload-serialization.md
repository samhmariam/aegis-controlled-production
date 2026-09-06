# ADR 004: Canonical Payload Serialization

## Status

Accepted

## Context

Canonical payloads are hashed for audit and integrity purposes. Equivalent business
payloads must serialize to the same bytes regardless of mapping insertion order or
whether optional fields are omitted or explicitly null.

## Decision

Canonical payload serialization follows these rules:

1. Monetary values use `Decimal` and are serialized as plain decimal strings. Floats
   are never used.
2. Datetimes are normalized to UTC and serialized as ISO-8601 strings ending in `Z`.
3. Keys whose values are `None` are omitted recursively, so an absent key and an
   explicitly null key have the same canonical representation and content hash.
4. Object keys are sorted, JSON separators are tight (`,` and `:`), and non-ASCII
   characters are preserved rather than ASCII-escaped.

Content hashes are SHA-256 digests of the resulting UTF-8 canonical JSON.

## Consequences

- Payload producers must provide monetary values as `Decimal` rather than float.
- Timestamp inputs must be timezone-aware so they can be normalized to UTC.
- `null` cannot carry a semantic distinction from an omitted optional field in a
  canonical payload.
- Hashes are stable across key ordering and Unicode content, provided the payload
  follows these serialization rules.

## Verification

The implementation is in `src/aegis/domain/base.py`. Unit tests verify deterministic
key ordering, null-key pruning, decimal representation, and UTC timestamp formatting.