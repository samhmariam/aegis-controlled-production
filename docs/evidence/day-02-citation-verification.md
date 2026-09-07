# Day 2 Citation Verification Evidence

- **Evidence ID:** `evidence-day02-citation-0001`
- **Current commit:** `f07c357222f0f3593201e118679249590eaf340e`
- **Producing tests:**
  - `uv run pytest tests/integration/test_context_api.py::test_citation_from_api_response_verifies_against_stored_source -q`
  - `uv run pytest tests/integration/test_context_api.py::test_tampered_stored_clause_fails_verification -q`

## Verified result

- **Synthetic claim:** `claim-cm-0001`
- **Clause:** `clause-cm-motor-0001-excess`
- **Inspected policy:** `policy-cm-motor-0001`, version `v2`
- **Outcome:** `verified`
- **Assertion:** `test_citation_from_api_response_verifies_against_stored_source` asserts `CitationOutcome.VERIFIED` after recomputing the hash from the stored clause text and checking the excerpt.

## Hash mismatch result

- **Synthetic claim:** `claim-cm-0001`
- **Clause:** `clause-cm-motor-0001-excess`
- **Inspected policy:** `policy-cm-motor-0001`, version `v2`
- **Mutation:** the test appends `and anything goes` to the stored clause text.
- **Outcome:** `hash_mismatch`
- **Assertion:** `test_tampered_stored_clause_fails_verification` asserts `CitationOutcome.HASH_MISMATCH`.

Both outcomes are produced by recomputing the canonical clause hash; the response-supplied hash is never trusted as proof.
