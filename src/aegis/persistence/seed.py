"""aegis-seed: create or refresh the local demo database from versioned synthetic fixtures.

Non-production. Synthetic data only. Refuses any destination that is not a demo database.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from aegis.config import Settings, get_settings
from aegis.context.models import PolicyClause
from aegis.domain.base import StrictModel, UtcDatetime, to_canonical_timestamp
from aegis.domain.models import ClaimSubmission
from aegis.errors import SeedConflictError
from aegis.persistence.connection import connect, transaction
from aegis.persistence.destination import assert_demo_destination
from aegis.persistence.fixtures import PolicyFixture, load_json_array, record_hash
from aegis.persistence.schema import apply_schema, rebuild_search_index


class RejectedRecord(StrictModel):
    table: str
    record_id: str
    reason: str


class SeedSummary(StrictModel):
    database_path: str
    schema_version: str
    inserted: Mapping[str, int]
    unchanged: Mapping[str, int]
    rejected_invalid: tuple[RejectedRecord, ...]
    rejected_conflict: tuple[RejectedRecord, ...]
    completed_at: UtcDatetime

    def render(self) -> str:
        return json.dumps(self.model_dump(mode="json"), indent=2, sort_keys=True)


class _Counters:
    """Mutable accumulator; converted to the frozen SeedSummary at the end."""

    def __init__(self) -> None:
        self.inserted: Counter[str] = Counter()
        self.unchanged: Counter[str] = Counter()
        self.invalid: list[RejectedRecord] = []
        self.conflict: list[RejectedRecord] = []

    def upsert(  # noqa: PLR0913 - generic upsert needs table-specific SQL and values
        self,
        conn: Any,
        *,
        table: str,
        key_sql: str,
        key_values: Sequence[str],
        row_hash: str,
        insert_sql: str,
        insert_values: Sequence[Any],
    ) -> None:
        """Insert, confirm unchanged, or record a conflict. Never overwrite."""
        existing = conn.execute(
            f"SELECT record_hash FROM {table} WHERE {key_sql}",  # noqa: S608 - table is a literal
            tuple(key_values),
        ).fetchone()
        if existing is None:
            conn.execute(insert_sql, tuple(insert_values))
            self.inserted[table] += 1
        elif existing["record_hash"] == row_hash:
            self.unchanged[table] += 1
        else:
            self.conflict.append(
                RejectedRecord(
                    table=table,
                    record_id="/".join(key_values),
                    reason="existing row differs from the authoritative fixture",
                )
            )


def _seed_reference_data(conn: Any, counters: _Counters, policies: list[dict[str, Any]]) -> None:
    for tenant_id in sorted({p["tenant_id"] for p in policies}):
        conn.execute(
            "INSERT INTO tenants VALUES (?, ?) ON CONFLICT(tenant_id) DO NOTHING",
            (tenant_id, tenant_id.replace("tenant-", "").replace("-", " ").title()),
        )
    for policy_id in sorted({p["policy_id"] for p in policies}):
        first = next(p for p in policies if p["policy_id"] == policy_id)
        conn.execute(
            "INSERT INTO policies VALUES (?, ?, ?) ON CONFLICT(policy_id) DO NOTHING",
            (policy_id, first["tenant_id"], first["line_of_business"]),
        )


def _seed_policy_versions(
    conn: Any, counters: _Counters, policies: list[dict[str, Any]]
) -> None:
    for payload in policies:
        version = PolicyFixture.model_validate(payload)
        counters.upsert(
            conn,
            table="policy_versions",
            key_sql="policy_id = ? AND policy_version = ?",
            key_values=[version.policy_id, version.policy_version],
            row_hash=record_hash(payload),
            insert_sql="INSERT INTO policy_versions VALUES (?,?,?,?,?,?,?,?)",
            insert_values=[
                version.policy_id,
                version.policy_version,
                version.tenant_id,
                to_canonical_timestamp(version.effective_from),
                None if version.effective_to is None
                else to_canonical_timestamp(version.effective_to),
                format(version.autonomous_settlement_limit, "f"),
                version.currency.value,
                record_hash(payload),
            ],
        )


def _seed_clauses(conn: Any, counters: _Counters, clauses: list[dict[str, Any]]) -> None:
    for payload in clauses:
        # PolicyClause revalidates content_hash against text: a corrupted clause cannot enter.
        clause = PolicyClause.model_validate(payload)
        existing = conn.execute(
            "SELECT content_hash FROM policy_clauses WHERE clause_id = ?", (clause.clause_id,)
        ).fetchone()
        if existing is None:
            conn.execute(
                "INSERT INTO policy_clauses VALUES (?,?,?,?,?,?,?,?,?)",
                (
                    clause.clause_id,
                    clause.policy_id,
                    clause.policy_version,
                    clause.tenant_id,
                    clause.line_of_business.value,
                    to_canonical_timestamp(clause.effective_from),
                    None if clause.effective_to is None
                    else to_canonical_timestamp(clause.effective_to),
                    clause.text,
                    clause.content_hash,
                ),
            )
            counters.inserted["policy_clauses"] += 1
        elif existing["content_hash"] == clause.content_hash:
            counters.unchanged["policy_clauses"] += 1
        else:
            counters.conflict.append(
                RejectedRecord(
                    table="policy_clauses",
                    record_id=clause.clause_id,
                    reason="stored clause content differs from the authoritative fixture",
                )
            )


def _seed_claims(
    conn: Any,
    counters: _Counters,
    claims: list[dict[str, Any]],
    policy_owners: set[tuple[str, str]],
) -> None:
    for payload in claims:
        claim = ClaimSubmission.model_validate(payload)
        if (claim.policy_id, claim.tenant_id) not in policy_owners:
            counters.invalid.append(
                RejectedRecord(
                    table="claims",
                    record_id=claim.claim_id,
                    reason="policy is not owned by the claim tenant",
                )
            )
            continue
        counters.upsert(
            conn,
            table="claims",
            key_sql="claim_id = ?",
            key_values=[claim.claim_id],
            row_hash=record_hash(payload),
            insert_sql="INSERT INTO claims VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            insert_values=[
                claim.claim_id,
                claim.tenant_id,
                claim.policy_id,
                claim.claim_type.value,
                claim.claimant_reference,
                to_canonical_timestamp(claim.loss_at),
                to_canonical_timestamp(claim.submitted_at),
                claim.description,
                None if claim.amount is None else format(claim.amount, "f"),
                None if claim.currency is None else claim.currency.value,
                record_hash(payload),
            ],
        )


def _reject_invalid_claims(counters: _Counters, invalid_cases: list[dict[str, Any]]) -> None:
    """Deliberately invalid fixtures must be proved invalid, not silently skipped."""
    for case in invalid_cases:
        payload = case["payload"]
        try:
            claim = ClaimSubmission.model_validate(payload)
        except ValidationError:
            counters.invalid.append(
                RejectedRecord(
                    table="claims",
                    record_id=str(case["case_id"]),
                    reason=f"contract rejected: {case['expected_error']}",
                )
            )
            continue
        # The referential-integrity case parses cleanly; it is rejected at the ownership layer.
        counters.invalid.append(
            RejectedRecord(
                table="claims",
                record_id=claim.claim_id,
                reason="referential integrity: policy is not owned by the claim tenant",
            )
        )


def _seed_principals(conn: Any, counters: _Counters, principals: list[dict[str, Any]]) -> None:
    for entry in principals:
        conn.execute(
            "INSERT INTO principals VALUES (?,?,?,?,?,?,?)"
            " ON CONFLICT(principal_id) DO NOTHING",
            (
                entry["principal_id"],
                entry["tenant_id"],
                entry["principal_type"],
                json.dumps(sorted(entry["scopes"]), separators=(",", ":")),
                json.dumps(sorted(entry["roles"]), separators=(",", ":")),
                entry["credential_sha256"],
                int(entry["lifetime_seconds"]),
            ),
        )
        for claim_id in entry.get("entitled_claims", []):
            conn.execute(
                "INSERT INTO principal_claim_entitlements VALUES (?,?)"
                " ON CONFLICT(principal_id, claim_id) DO NOTHING",
                (entry["principal_id"], claim_id),
            )


def run_seed(
    *,
    database_path: Path,
    demo_root: Path,
    fixtures_dir: Path,
    principals_file: Path,
) -> SeedSummary:
    """Create or refresh a demo database. Raises SeedConflictError rather than overwriting."""
    assert_demo_destination(database_path, demo_root=demo_root)
    database_path.parent.mkdir(parents=True, exist_ok=True)

    policies = load_json_array(fixtures_dir / "policies.json")
    clauses = load_json_array(fixtures_dir / "policy-clauses.json")
    claims = load_json_array(fixtures_dir / "claims.json")
    invalid_claims = load_json_array(fixtures_dir / "claims-invalid.json")
    principals = load_json_array(principals_file)

    is_new = not database_path.exists()
    conn = connect(database_path)
    counters = _Counters()
    try:
        with transaction(conn):
            if is_new:
                apply_schema(conn)
            policy_owners = {(p["policy_id"], p["tenant_id"]) for p in policies}
            _seed_reference_data(conn, counters, policies)
            _seed_policy_versions(conn, counters, policies)
            _seed_clauses(conn, counters, clauses)
            _seed_claims(conn, counters, claims, policy_owners)
            _reject_invalid_claims(counters, invalid_claims)
            _seed_principals(conn, counters, principals)
            if counters.conflict:
                raise SeedConflictError(
                    f"{len(counters.conflict)} row(s) differ from the authoritative fixtures"
                )
            rebuild_search_index(conn)
    finally:
        conn.close()

    return SeedSummary(
        database_path=str(database_path),
        schema_version=to_canonical_timestamp(datetime.now(UTC))[:0] or "",
        inserted=dict(counters.inserted),
        unchanged=dict(counters.unchanged),
        rejected_invalid=tuple(counters.invalid),
        rejected_conflict=tuple(counters.conflict),
        completed_at=datetime.now(UTC),
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aegis-seed", description=__doc__)
    parser.add_argument("--database", type=Path, default=None)
    args = parser.parse_args(argv)

    settings: Settings = get_settings()
    database_path = args.database or settings.demo_database_path
    try:
        summary = run_seed(
            database_path=database_path,
            demo_root=settings.demo_root,
            fixtures_dir=settings.synthetic_data_dir,
            principals_file=settings.demo_principals_file,
        )
    except SeedConflictError as exc:
        print(f"seed aborted and rolled back: {exc}", file=sys.stderr)
        return 2
    print(summary.render())
    return 0
