# ADR 007: Permission-Aware Retrieval

## Status

Accepted

## Context

Day 2 retrieval must select authoritative policy evidence without allowing a caller to
cross tenant boundaries, retrieve an unentitled claim, or substitute a newer policy
version for the version applicable to the claim's loss date. Retrieval also needs a
bounded, deterministic search contract so evidence remains reviewable and reproducible.

The repository is local SQLite with synthetic fixtures. FTS5 is available in the
observed environment, but a deterministic fallback is required for environments where
that extension is unavailable.

## Decision

1. **D1 — applicable policy version and freshness.** Select the policy version whose
   half-open effective window `[effective_from, effective_to)` contains the claim's
   `loss_at`, scoped by both tenant and policy. If no window applies, return the explicit
   `policy_version_missing` failure. If the selected version has ended before the current
   time, return `policy_version_stale`. Never substitute the newest or currently active
   version.
2. **D2 — entitlement before retrieval.** Resolve a principal from the credential and
   require that it is unexpired, has `claims:read`, belongs to the claim tenant, and is
   either a `claims_supervisor` or explicitly entitled to the claim. Apply tenant and
   entitlement predicates in the repository query before ranking. Wrong-tenant,
   unentitled, and nonexistent claims return the same `404` error envelope:
   `{"error_code":"claim_not_accessible","details":[]}`. Invalid identity may return
   the distinct `401` identity error.
3. **D5 — bounded deterministic search.** Use SQLite FTS5 BM25 when available and a
   deterministic token-overlap ranker otherwise, behind the same repository method.
   Lowercase and extract alphanumeric tokens, discard tokens shorter than two
   characters, cap the query at twelve tokens, bind the FTS expression as a parameter,
   return at most `k` clauses, and produce a bounded excerpt around the first match.
   Fallback ties are ordered by ascending clause ID. Raw query text is never concatenated
   into SQL or an FTS expression.

## Consequences

- A claim evaluated against a stale or missing policy window fails explicitly instead of
  receiving silently substituted evidence.
- Repository reads cannot expose another tenant's claim or clauses through URL or query
  parameters, and denial responses do not disclose whether a claim exists.
- Retrieval behavior is reproducible across FTS5 and non-FTS5 environments, with a
  documented lexical-only limitation and bounded context output.
- The system does not provide timing-side-channel resistance; tests establish response
  equivalence, not timing equivalence.
- Evidence remains synthetic and local; this decision does not establish production
  identity issuance, revocation, or distributed database concurrency guarantees.

## Verification

- `tests/unit/test_policy_repository.py` verifies correct tenant/policy/version retrieval,
  entitlement denial, stale and missing versions, no-evidence behavior, injection
  resistance, and FTS5/fallback result equivalence.
- `tests/integration/test_context_api.py` verifies authorized `claim-cm-0001` retrieval,
  identical cross-tenant/nonexistent `404` responses, stale-version `409` handling, and
  API-level provenance and tamper detection.
- The focused command
  `uv run pytest tests/unit/test_policy_repository.py tests/integration/test_context_api.py -q`
  passed with 27 tests.
- The full quality checks passed at commit
  `f07c357222f0f3593201e118679249590eaf340e`: `uv run ruff check .`, `uv run mypy src`,
  and `uv run pytest -q` (139 tests passed).
