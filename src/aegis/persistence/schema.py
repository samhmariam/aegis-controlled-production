"""The one place tables are defined. Versioned; applied by aegis-seed, never by a service."""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime

from aegis.domain.base import SCHEMA_VERSION, to_canonical_timestamp

PERSISTENCE_SCHEMA_VERSION = "2026-09-06.1"
DEMO_DATABASE_PURPOSE = "demo"

#: Every table the canonical plan names. Used by the idempotency digest; never interpolated
#: from user input, which is what keeps ruff S608 satisfied.
CANONICAL_TABLES: tuple[str, ...] = (
    "tenants",
    "policies",
    "policy_versions",
    "policy_clauses",
    "claims",
    "principals",
    "principal_claim_entitlements",
    "recommendations",
    "approvals",
    "payments",
    "idempotency_records",
    "audit_events",
    "system_controls",
)

SCHEMA_SQL = """
CREATE TABLE schema_meta (
    id               INTEGER PRIMARY KEY CHECK (id = 1),
    schema_version   TEXT NOT NULL,
    contract_version TEXT NOT NULL,
    database_purpose TEXT NOT NULL CHECK (database_purpose = 'demo'),
    created_at       TEXT NOT NULL
);

CREATE TABLE tenants (
    tenant_id    TEXT PRIMARY KEY,
    display_name TEXT NOT NULL
);

CREATE TABLE policies (
    policy_id        TEXT PRIMARY KEY,
    tenant_id        TEXT NOT NULL REFERENCES tenants(tenant_id),
    line_of_business TEXT NOT NULL CHECK (line_of_business IN ('motor','property'))
);

CREATE TABLE policy_versions (
    policy_id                   TEXT NOT NULL REFERENCES policies(policy_id),
    policy_version              TEXT NOT NULL,
    tenant_id                   TEXT NOT NULL REFERENCES tenants(tenant_id),
    effective_from              TEXT NOT NULL,
    effective_to                TEXT,
    autonomous_settlement_limit TEXT NOT NULL,
    currency                    TEXT NOT NULL,
    record_hash                 TEXT NOT NULL,
    PRIMARY KEY (policy_id, policy_version),
    CHECK (effective_to IS NULL OR effective_to > effective_from)
);

CREATE TABLE policy_clauses (
    clause_id        TEXT PRIMARY KEY,
    policy_id        TEXT NOT NULL,
    policy_version   TEXT NOT NULL,
    tenant_id        TEXT NOT NULL REFERENCES tenants(tenant_id),
    line_of_business TEXT NOT NULL,
    effective_from   TEXT NOT NULL,
    effective_to     TEXT,
    text             TEXT NOT NULL,
    content_hash     TEXT NOT NULL,
    FOREIGN KEY (policy_id, policy_version)
        REFERENCES policy_versions(policy_id, policy_version)
);
CREATE INDEX idx_clauses_scope ON policy_clauses(tenant_id, policy_id, policy_version);

CREATE TABLE claims (
    claim_id           TEXT PRIMARY KEY,
    tenant_id          TEXT NOT NULL REFERENCES tenants(tenant_id),
    policy_id          TEXT NOT NULL REFERENCES policies(policy_id),
    claim_type         TEXT NOT NULL CHECK (claim_type IN ('motor','property')),
    claimant_reference TEXT NOT NULL,
    loss_at            TEXT NOT NULL,
    submitted_at       TEXT NOT NULL,
    description        TEXT NOT NULL,
    amount             TEXT,
    currency           TEXT,
    record_hash        TEXT NOT NULL
);
CREATE INDEX idx_claims_tenant ON claims(tenant_id, claim_id);

CREATE TABLE principals (
    principal_id      TEXT PRIMARY KEY,
    tenant_id         TEXT NOT NULL REFERENCES tenants(tenant_id),
    principal_type    TEXT NOT NULL,
    scopes            TEXT NOT NULL,
    roles             TEXT NOT NULL,
    credential_sha256 TEXT NOT NULL UNIQUE,
    lifetime_seconds  INTEGER NOT NULL CHECK (lifetime_seconds > 0)
);

CREATE TABLE principal_claim_entitlements (
    principal_id TEXT NOT NULL REFERENCES principals(principal_id),
    claim_id     TEXT NOT NULL REFERENCES claims(claim_id),
    PRIMARY KEY (principal_id, claim_id)
);

-- Tables below mirror Day 1 contracts. No service reads or writes them today.

CREATE TABLE recommendations (            -- mirrors tools.models.ActionProposal
    action_id       TEXT PRIMARY KEY,
    run_id          TEXT NOT NULL,
    claim_id        TEXT NOT NULL REFERENCES claims(claim_id),
    tool_name       TEXT NOT NULL,
    arguments_json  TEXT NOT NULL,
    arguments_hash  TEXT NOT NULL,
    rationale       TEXT NOT NULL,
    cited_clause_ids TEXT NOT NULL,
    confidence      REAL NOT NULL CHECK (confidence BETWEEN 0.0 AND 1.0),
    consequential   INTEGER NOT NULL CHECK (consequential IN (0,1)),
    proposed_by     TEXT NOT NULL,
    model_id        TEXT NOT NULL,
    model_version   TEXT NOT NULL,
    prompt_version  TEXT NOT NULL,
    proposed_at     TEXT NOT NULL
);

CREATE TABLE approvals (                  -- mirrors approvals.models.ApprovalRecord
    approval_id           TEXT PRIMARY KEY,
    run_id                TEXT NOT NULL,
    action_id             TEXT NOT NULL REFERENCES recommendations(action_id),
    tool_name             TEXT NOT NULL,
    arguments_hash        TEXT NOT NULL,
    decision_id           TEXT NOT NULL,
    approver_principal_id TEXT NOT NULL REFERENCES principals(principal_id),
    decision              TEXT NOT NULL CHECK (decision IN ('approve','reject')),
    issued_at             TEXT NOT NULL,
    expires_at            TEXT NOT NULL,
    nonce                 TEXT NOT NULL UNIQUE,
    consumed_at           TEXT,
    CHECK (expires_at > issued_at)
);

CREATE TABLE payments (                   -- synthetic effects only; mirrors tools.models.ToolResult
    effect_id       TEXT PRIMARY KEY,
    invocation_id   TEXT NOT NULL UNIQUE,
    tool_name       TEXT NOT NULL,
    claim_id        TEXT NOT NULL REFERENCES claims(claim_id),
    idempotency_key TEXT,
    status          TEXT NOT NULL
        CHECK (status IN ('succeeded','denied','failed','uncertain','duplicate')),
    amount          TEXT NOT NULL,
    currency        TEXT NOT NULL,
    started_at      TEXT NOT NULL,
    completed_at    TEXT NOT NULL
);

CREATE TABLE idempotency_records (
    idempotency_key TEXT PRIMARY KEY,
    tool_name       TEXT NOT NULL,
    arguments_hash  TEXT NOT NULL,
    effect_id       TEXT,
    status          TEXT NOT NULL,
    created_at      TEXT NOT NULL
);

CREATE TABLE audit_events (               -- mirrors audit.events.CanonicalEvent
    sequence            INTEGER PRIMARY KEY,
    event_id            TEXT NOT NULL UNIQUE,
    correlation_id      TEXT NOT NULL,
    run_id              TEXT NOT NULL,
    action_id           TEXT,
    event_type          TEXT NOT NULL,
    actor_principal_id  TEXT NOT NULL,
    workload_identity   TEXT NOT NULL,
    model_version       TEXT NOT NULL,
    prompt_version      TEXT NOT NULL,
    policy_version      TEXT NOT NULL,
    tool_version        TEXT NOT NULL,
    decision_id         TEXT,
    approval_id         TEXT,
    arguments_hash      TEXT,
    result_status       TEXT,
    occurred_at         TEXT NOT NULL,
    previous_event_hash TEXT,
    event_hash          TEXT NOT NULL UNIQUE
);

CREATE TABLE system_controls (
    control_name TEXT PRIMARY KEY,
    enabled      INTEGER NOT NULL CHECK (enabled IN (0,1)),
    updated_at   TEXT NOT NULL
);

CREATE VIRTUAL TABLE policy_clauses_fts USING fts5(
    text,
    content='policy_clauses',
    content_rowid='rowid',
    tokenize='unicode61'
);
"""


def apply_schema(conn: sqlite3.Connection) -> None:
    """Create every table and stamp the demo marker. Called once, by the seed command."""
    statement = ""
    for line in SCHEMA_SQL.splitlines(keepends=True):
        statement += line
        if sqlite3.complete_statement(statement):
            conn.execute(statement)
            statement = ""
    if statement.strip():
        raise sqlite3.OperationalError("incomplete schema statement")
    conn.execute(
        "INSERT INTO schema_meta"
        " (id, schema_version, contract_version, database_purpose, created_at)"
        " VALUES (1, ?, ?, ?, ?)",
        (
            PERSISTENCE_SCHEMA_VERSION,
            SCHEMA_VERSION,
            DEMO_DATABASE_PURPOSE,
            to_canonical_timestamp(datetime.now(UTC)),
        ),
    )
    conn.execute("INSERT INTO system_controls VALUES ('kill_switch', 0, ?)",
                 (to_canonical_timestamp(datetime.now(UTC)),))


def rebuild_search_index(conn: sqlite3.Connection) -> None:
    """Repopulate the external-content FTS index after bulk loading."""
    conn.execute("INSERT INTO policy_clauses_fts(policy_clauses_fts) VALUES('rebuild')")
