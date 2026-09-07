"""Assemble a permission-aware ContextBundle with provenance and explicit outcomes."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from aegis.context.models import ClauseExcerpt, ContextBundle
from aegis.domain.base import StrictModel, to_canonical_timestamp
from aegis.errors import IdentityInvalidError
from aegis.identity.principal import Principal
from aegis.persistence.policy_repository import PolicyRepository
from aegis.persistence.ranking import build_excerpt, query_tokens


class RetrievalStatus(StrEnum):
    RETRIEVED = "retrieved"
    NO_EVIDENCE = "no_evidence"


class RetrievalResult(StrictModel):
    """Explicit outcome plus the bundle.

    Stale and missing versions are not members of this type: they raise
    PolicyVersionUnavailableError, so no caller can mistake them for an empty result. Denial
    raises before retrieval begins.
    """

    status: RetrievalStatus
    bundle: ContextBundle


class ContextService:
    def __init__(
        self, repository: PolicyRepository, *, max_clauses: int, excerpt_chars: int
    ) -> None:
        self._repo = repository
        self._max_clauses = max_clauses
        self._excerpt_chars = excerpt_chars

    def retrieve(self, *, principal: Principal, claim_id: str, query: str) -> RetrievalResult:
        now = datetime.now(UTC)
        if principal.is_expired(now):
            raise IdentityInvalidError("principal has expired")

        claim = self._repo.entitled_claim(principal=principal, claim_id=claim_id)
        version = self._repo.applicable_version(
            claim=claim, now=to_canonical_timestamp(now)
        )

        tokens = query_tokens(query)
        clauses = self._repo.search_clauses(
            tenant_id=claim.tenant_id,
            version=version,
            tokens=tokens,
            limit=self._max_clauses,
        )

        limitations = [
            "retrieval method: "
            f"{'sqlite fts5 bm25' if self._repo.uses_fts else 'deterministic token overlap'};"
            " lexical only, no semantic matching",
            "the query was reduced to alphanumeric tokens before search, so operators and"
            " punctuation in the query text are not honoured",
            "policy version was selected by claim loss date; a superseded version is refused,"
            " never substituted",
        ]
        if not clauses:
            limitations.append(
                f"no clause in {version.policy_id} {version.policy_version} matched the query"
            )

        bundle = ContextBundle(
            claim_id=claim.claim_id,
            tenant_id=claim.tenant_id,
            policy_id=version.policy_id,
            policy_version=version.policy_version,
            clause_ids=tuple(clause.clause_id for clause in clauses),
            excerpts=tuple(
                ClauseExcerpt(
                    clause_id=clause.clause_id,
                    excerpt=build_excerpt(clause.text, tokens, width=self._excerpt_chars),
                    source_content_hash=clause.content_hash,
                )
                for clause in clauses
            ),
            retrieval_query=query,
            retrieved_at=now,
            limitations=tuple(limitations),
        )
        return RetrievalResult(
            status=RetrievalStatus.RETRIEVED if clauses else RetrievalStatus.NO_EVIDENCE,
            bundle=bundle,
        )
