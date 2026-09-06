# ADR 005: Context Retrieval Contracts

## Status

Accepted

## Context

The retrieval plane supplies policy evidence to claim evaluation. Its contracts must
preserve authoritative-content integrity and make an incomplete retrieval outcome
auditable without encouraging fabricated citations.

## Decision

1. `PolicyClause.hash_payload` is the single definition of the fields covered by a
   clause content hash. Both fixture construction and validation use this method, so
   their hash inputs cannot drift apart.
2. Clause hashes cover clause identity, policy identity, policy version, and text.
   Effective dates are deliberately excluded. We treat a corrected effective date as
   a metadata correction, not as changed authoritative content. The alternative of
   hashing effective dates was considered and rejected because it would make a
   metadata correction appear to create new clause content.
3. An empty `ContextBundle` is valid only when `limitations` explains why retrieval
   produced no clauses. "No relevant clause found" is a legitimate outcome; forcing
   a clause would encourage an unsupported citation.
4. `ClauseExcerpt.source_content_hash` identifies the hash of the complete source
   clause. It is not a hash of the excerpt text. The explicit name fixes the
   provenance contract for retrieval fixtures and later repository integration.
5. A future bundle-level hash must sort `clause_ids` before hashing. Current bundle
   input is not required to be sorted, so retrieval or file ordering must not affect
   a future deterministic bundle hash.

## Consequences

- Changes to a clause's identity, policy version, or text require a new content hash.
- Effective-date corrections retain the same clause content hash when all hashed
  fields are unchanged.
- Consumers can represent no-result retrievals honestly and must retain their stated
  limitation.
- Provenance checks compare each excerpt's `source_content_hash` with its complete
  source clause, rather than calculating a digest for the quoted fragment.
- Any bundle-level integrity feature must define canonical clause-ID ordering before
  it is introduced.

## Verification

The implementation is in `src/aegis/context/models.py`. Unit tests should verify the
shared hash payload contract, date exclusion from clause hashes, empty-bundle
limitations, and excerpt-to-source hash provenance.