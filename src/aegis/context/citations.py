"""Provenance verification: does this citation resolve to unchanged stored content?"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from aegis.context.models import ContextBundle, PolicyClause
from aegis.domain.base import (
    ClauseId,
    PolicyId,
    PolicyVersion,
    Sha256Hash,
    StrictModel,
    UtcDatetime,
)
from aegis.domain.base import content_hash as compute_content_hash
from aegis.persistence.policy_repository import PolicyRepository


class CitationOutcome(StrEnum):
    VERIFIED = "verified"
    CLAUSE_NOT_FOUND = "clause_not_found"
    VERSION_MISMATCH = "version_mismatch"
    HASH_MISMATCH = "hash_mismatch"
    EXCERPT_NOT_IN_SOURCE = "excerpt_not_in_source"


class Citation(StrictModel):
    clause_id: ClauseId
    policy_id: PolicyId
    policy_version: PolicyVersion
    excerpt: str
    claimed_hash: Sha256Hash


class CitationVerification(StrictModel):
    clause_id: ClauseId
    policy_id: PolicyId
    policy_version: PolicyVersion
    claimed_hash: Sha256Hash
    recomputed_hash: Sha256Hash | None
    outcome: CitationOutcome
    verified_at: UtcDatetime

    @property
    def verified(self) -> bool:
        return self.outcome is CitationOutcome.VERIFIED


def citations_from_bundle(bundle: ContextBundle) -> tuple[Citation, ...]:
    return tuple(
        Citation(
            clause_id=excerpt.clause_id,
            policy_id=bundle.policy_id,
            policy_version=bundle.policy_version,
            excerpt=excerpt.excerpt,
            claimed_hash=excerpt.source_content_hash,
        )
        for excerpt in bundle.excerpts
    )


def verify_citation(
    repository: PolicyRepository, *, tenant_id: str, citation: Citation
) -> CitationVerification:
    """Recompute from stored text. Echoing the response's own hash verifies nothing."""
    moment = datetime.now(UTC)

    def result(outcome: CitationOutcome, recomputed: str | None) -> CitationVerification:
        return CitationVerification(
            clause_id=citation.clause_id,
            policy_id=citation.policy_id,
            policy_version=citation.policy_version,
            claimed_hash=citation.claimed_hash,
            recomputed_hash=recomputed,
            outcome=outcome,
            verified_at=moment,
        )

    stored = repository.clause_for_citation(
        tenant_id=tenant_id,
        clause_id=citation.clause_id,
        policy_id=citation.policy_id,
        policy_version=citation.policy_version,
    )
    if stored is None:
        # Distinguishes 'no such clause' from 'that clause is not at that version'.
        anywhere = repository.clause_any_version(
            tenant_id=tenant_id, clause_id=citation.clause_id
        )
        return result(
            CitationOutcome.CLAUSE_NOT_FOUND if anywhere is None
            else CitationOutcome.VERSION_MISMATCH,
            None,
        )

    recomputed = compute_content_hash(
        PolicyClause.hash_payload(
            clause_id=stored.clause_id,
            policy_id=stored.policy_id,
            policy_version=stored.policy_version,
            text=stored.text,
        )
    )
    if recomputed != stored.content_hash:
        return result(CitationOutcome.HASH_MISMATCH, recomputed)   # the stored row was tampered
    if recomputed != citation.claimed_hash:
        return result(CitationOutcome.HASH_MISMATCH, recomputed)   # the response was tampered
    if citation.excerpt not in stored.text:
        return result(CitationOutcome.EXCERPT_NOT_IN_SOURCE, recomputed)
    return result(CitationOutcome.VERIFIED, recomputed)
