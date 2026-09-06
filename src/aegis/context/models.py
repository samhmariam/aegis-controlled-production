"""Retrieval-plane contracts: what evidence was retrieved, from where, when, and how it is proved.

Data contracts only. Permission-aware retrieval arrives on Day 2 in policy_repository.py;
nothing in this module proves that a principal was entitled to see a clause.
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Self

from pydantic import Field, StringConstraints, model_validator

from aegis.domain.base import (
    ClaimId,
    ClauseId,
    PolicyId,
    PolicyVersion,
    Sha256Hash,
    StrictModel,
    TenantId,
    UtcDatetime,
)
from aegis.domain.base import content_hash as compute_content_hash
from aegis.domain.models import ClaimType

Limitation = Annotated[str, StringConstraints(min_length=1, max_length=500)]


class PolicyClause(StrictModel):
    """One versioned, authoritative clause. Its hash is recomputed, never trusted from input."""

    clause_id: ClauseId
    policy_id: PolicyId
    tenant_id: TenantId
    policy_version: PolicyVersion
    line_of_business: ClaimType
    effective_from: UtcDatetime
    effective_to: UtcDatetime | None = None
    text: str = Field(min_length=1, max_length=8000)
    content_hash: Sha256Hash

    @staticmethod
    def hash_payload(
        *,
        clause_id: ClauseId,
        policy_id: PolicyId,
        policy_version: PolicyVersion,
        text: str,
    ) -> dict[str, str]:
        """The single definition of what a clause hash covers.

        Identity plus version plus text: changing any one of them must produce a different hash.
        Effective dates are deliberately excluded — a corrected date is a metadata fix, not new
        authoritative content.
        """
        return {
            "clause_id": clause_id,
            "policy_id": policy_id,
            "policy_version": policy_version,
            "text": text,
        }

    @classmethod
    def sealed(  # noqa: PLR0913 - keyword-only factory mirrors the model fields
        cls,
        *,
        clause_id: ClauseId,
        policy_id: PolicyId,
        tenant_id: TenantId,
        policy_version: PolicyVersion,
        line_of_business: ClaimType,
        effective_from: datetime,
        text: str,
        effective_to: datetime | None = None,
    ) -> Self:
        """Construct a clause with its hash computed, so no caller hand-writes one."""
        digest = compute_content_hash(
            cls.hash_payload(
                clause_id=clause_id,
                policy_id=policy_id,
                policy_version=policy_version,
                text=text,
            )
        )
        return cls(
            clause_id=clause_id,
            policy_id=policy_id,
            tenant_id=tenant_id,
            policy_version=policy_version,
            line_of_business=line_of_business,
            effective_from=effective_from,
            effective_to=effective_to,
            text=text,
            content_hash=digest,
        )

    @model_validator(mode="after")
    def _check_invariants(self) -> Self:
        if self.effective_to is not None and self.effective_from >= self.effective_to:
            raise ValueError("effective_to must be after effective_from")
        expected = compute_content_hash(
            self.hash_payload(
                clause_id=self.clause_id,
                policy_id=self.policy_id,
                policy_version=self.policy_version,
                text=self.text,
            )
        )
        if self.content_hash != expected:
            raise ValueError("content_hash does not match clause content")
        return self

    def is_effective_at(self, moment: datetime) -> bool:
        """Half-open window: effective_from is inclusive, effective_to is exclusive."""
        if moment < self.effective_from:
            return False
        return self.effective_to is None or moment < self.effective_to


class ClauseExcerpt(StrictModel):
    """A quoted fragment, carrying the hash of the clause it came from.

    source_content_hash is the hash of the whole source clause, not of the excerpt text. That is
    what lets a reviewer confirm the excerpt was taken from a clause version that has not changed.
    """

    clause_id: ClauseId
    excerpt: str = Field(min_length=1, max_length=2000)
    source_content_hash: Sha256Hash


class ContextBundle(StrictModel):
    """Everything the model was shown for one claim, with provenance.

    Tenant and ownership coherence cannot be checked here — there is no repository on Day 1.
    Day 2's policy_repository is responsible for never assembling a bundle across a tenant boundary.
    """

    claim_id: ClaimId
    tenant_id: TenantId
    policy_id: PolicyId
    policy_version: PolicyVersion
    clause_ids: tuple[ClauseId, ...]
    excerpts: tuple[ClauseExcerpt, ...]
    retrieval_query: str = Field(min_length=1, max_length=1000)
    retrieved_at: UtcDatetime
    limitations: tuple[Limitation, ...]

    @model_validator(mode="after")
    def _check_invariants(self) -> Self:
        declared = list(self.clause_ids)
        if len(set(declared)) != len(declared):
            raise ValueError("clause_ids contains duplicates")

        excerpted = [excerpt.clause_id for excerpt in self.excerpts]
        if len(set(excerpted)) != len(excerpted):
            raise ValueError("excerpts contain duplicate clause_id values")

        if set(declared) != set(excerpted):
            raise ValueError("each declared clause_id needs exactly one excerpt, and vice versa")

        if not declared and not self.limitations:
            raise ValueError("an empty bundle must record why no clause was retrieved")

        return self

    def excerpt_for(self, clause_id: str) -> ClauseExcerpt | None:
        return next((e for e in self.excerpts if e.clause_id == clause_id), None)
