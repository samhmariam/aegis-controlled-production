"""Permission-aware retrieval. Authorization predicates run inside the query, before ranking."""

from __future__ import annotations

import sqlite3
from collections.abc import Sequence
from dataclasses import dataclass

from aegis.errors import ClaimNotAccessibleError, PolicyVersionUnavailableError
from aegis.identity.principal import Principal
from aegis.persistence.connection import fts5_available
from aegis.persistence.ranking import fts_match_expression, rank_by_token_overlap

REQUIRED_SCOPE = "claims:read"
SUPERVISOR_ROLE = "claims_supervisor"


@dataclass(frozen=True)
class ClaimRecord:
    claim_id: str
    tenant_id: str
    policy_id: str
    claim_type: str
    loss_at: str
    description: str


@dataclass(frozen=True)
class VersionRecord:
    policy_id: str
    policy_version: str
    effective_from: str
    effective_to: str | None


@dataclass(frozen=True)
class ClauseRecord:
    clause_id: str
    policy_id: str
    policy_version: str
    tenant_id: str
    text: str
    content_hash: str


class PolicyRepository:
    def __init__(self, conn: sqlite3.Connection, *, use_fts: bool | None = None) -> None:
        self._conn = conn
        self.uses_fts = fts5_available(conn) if use_fts is None else use_fts

    # ---- authorization boundary -------------------------------------------------

    def entitled_claim(self, *, principal: Principal, claim_id: str) -> ClaimRecord:
        """Resolve a claim through the entitlement boundary, or refuse.

        Zero rows is the single denial path. The query cannot distinguish 'not yours' from
        'not there', so neither can the caller — and neither does this process.
        """
        if REQUIRED_SCOPE not in principal.scopes:
            raise ClaimNotAccessibleError
        row = self._conn.execute(
            "SELECT claim_id, tenant_id, policy_id, claim_type, loss_at, description"
            " FROM claims c"
            " WHERE c.claim_id = :claim_id"
            "   AND c.tenant_id = :tenant_id"
            "   AND (:is_supervisor = 1"
            "        OR EXISTS (SELECT 1 FROM principal_claim_entitlements e"
            "                   WHERE e.principal_id = :principal_id"
            "                     AND e.claim_id = c.claim_id))",
            {
                "claim_id": claim_id,
                "tenant_id": principal.tenant_id,
                "principal_id": principal.principal_id,
                "is_supervisor": 1 if SUPERVISOR_ROLE in principal.roles else 0,
            },
        ).fetchone()
        if row is None:
            raise ClaimNotAccessibleError
        return ClaimRecord(
            claim_id=str(row["claim_id"]),
            tenant_id=str(row["tenant_id"]),
            policy_id=str(row["policy_id"]),
            claim_type=str(row["claim_type"]),
            loss_at=str(row["loss_at"]),
            description=str(row["description"]),
        )

    # ---- version selection (D1) -------------------------------------------------

    def applicable_version(self, *, claim: ClaimRecord, now: str) -> VersionRecord:
        """The version whose effective window contains the loss date. Never substituted.

        Note a real edge in the fixtures: v1 ends 2025-12-31T23:59:59Z and v2 begins
        2026-01-01T00:00:00Z, so a loss inside that one-second gap resolves to no version and
        is reported missing rather than guessed. That is the intended behaviour.
        """
        row = self._conn.execute(
            "SELECT policy_id, policy_version, effective_from, effective_to"
            " FROM policy_versions"
            " WHERE policy_id = :policy_id"
            "   AND tenant_id = :tenant_id"
            "   AND effective_from <= :loss_at"
            "   AND (effective_to IS NULL OR :loss_at < effective_to)",
            {
                "policy_id": claim.policy_id,
                "tenant_id": claim.tenant_id,
                "loss_at": claim.loss_at,
            },
        ).fetchone()
        if row is None:
            raise PolicyVersionUnavailableError("policy_version_missing", claim.policy_id)

        version = VersionRecord(
            policy_id=str(row["policy_id"]),
            policy_version=str(row["policy_version"]),
            effective_from=str(row["effective_from"]),
            effective_to=None if row["effective_to"] is None else str(row["effective_to"]),
        )
        if version.effective_to is not None and version.effective_to < now:
            raise PolicyVersionUnavailableError("policy_version_stale", claim.policy_id)
        return version

    # ---- retrieval --------------------------------------------------------------

    def search_clauses(
        self,
        *,
        tenant_id: str,
        version: VersionRecord,
        tokens: Sequence[str],
        limit: int,
    ) -> tuple[ClauseRecord, ...]:
        """Rank only within the authorised (tenant, policy, version) triple."""
        if not tokens:
            return ()
        scope = {
            "tenant_id": tenant_id,
            "policy_id": version.policy_id,
            "policy_version": version.policy_version,
        }
        if self.uses_fts:
            rows = self._conn.execute(
                "WITH authorised AS ("
                "  SELECT rowid FROM policy_clauses"
                "  WHERE tenant_id = :tenant_id"
                "    AND policy_id = :policy_id"
                "    AND policy_version = :policy_version)"
                " SELECT c.clause_id, c.policy_id, c.policy_version, c.tenant_id,"
                "        c.text, c.content_hash"
                " FROM policy_clauses_fts f"
                " JOIN policy_clauses c ON c.rowid = f.rowid"
                " WHERE f.rowid IN (SELECT rowid FROM authorised)"
                "   AND policy_clauses_fts MATCH :match"
                " ORDER BY bm25(policy_clauses_fts), c.clause_id"
                " LIMIT :limit",
                {**scope, "match": fts_match_expression(tokens), "limit": limit},
            ).fetchall()
            return tuple(self._to_clause(row) for row in rows)

        rows = self._conn.execute(
            "SELECT clause_id, policy_id, policy_version, tenant_id, text, content_hash"
            " FROM policy_clauses"
            " WHERE tenant_id = :tenant_id"
            "   AND policy_id = :policy_id"
            "   AND policy_version = :policy_version",
            scope,
        ).fetchall()
        candidates = {str(row["clause_id"]): self._to_clause(row) for row in rows}
        ordered = rank_by_token_overlap(
            tokens, [(cid, rec.text) for cid, rec in candidates.items()]
        )
        return tuple(candidates[cid] for cid in ordered[:limit])

    def clause_for_citation(
        self, *, tenant_id: str, clause_id: str, policy_id: str, policy_version: str
    ) -> ClauseRecord | None:
        """Tenant-scoped like every other read: a citation helper must not cross tenants."""
        row = self._conn.execute(
            "SELECT clause_id, policy_id, policy_version, tenant_id, text, content_hash"
            " FROM policy_clauses"
            " WHERE clause_id = :clause_id AND tenant_id = :tenant_id"
            "   AND policy_id = :policy_id AND policy_version = :policy_version",
            {
                "clause_id": clause_id,
                "tenant_id": tenant_id,
                "policy_id": policy_id,
                "policy_version": policy_version,
            },
        ).fetchone()
        return None if row is None else self._to_clause(row)

    def clause_any_version(self, *, tenant_id: str, clause_id: str) -> ClauseRecord | None:
        """Find a clause within a tenant without constraining its policy version."""
        row = self._conn.execute(
            "SELECT clause_id, policy_id, policy_version, tenant_id, text, content_hash"
            " FROM policy_clauses"
            " WHERE clause_id = :clause_id AND tenant_id = :tenant_id",
            {"clause_id": clause_id, "tenant_id": tenant_id},
        ).fetchone()
        return None if row is None else self._to_clause(row)

    @staticmethod
    def _to_clause(row: sqlite3.Row) -> ClauseRecord:
        return ClauseRecord(
            clause_id=str(row["clause_id"]),
            policy_id=str(row["policy_id"]),
            policy_version=str(row["policy_version"]),
            tenant_id=str(row["tenant_id"]),
            text=str(row["text"]),
            content_hash=str(row["content_hash"]),
        )
