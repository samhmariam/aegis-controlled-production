# AEGIS Threat Model

## Assets

The protected assets are synthetic claims and policy clauses, tenant boundaries,
principal and approval bindings, tool-effect records, audit evidence, configuration,
and the kill-switch state. The intended business outcome is a policy-grounded triage
recommendation; no model output is itself an authority to create a consequential
effect.

## Actors

Actors include a claimant submitting untrusted narrative content, an authenticated
operator or approver, the constrained workflow and its model, MCP tool services, and
an attacker able to influence claim, retrieved-policy, or tool-output content. The
demo also uses a local identity provider and local persistence components whose
limitations are recorded below rather than represented as production controls.

## Trust Boundaries

Claim descriptions, retrieved clause text, and tool output are **untrusted content**.
They may be supplied to the model as data, but they cannot set identity, authorize an
action, mutate workflow state, or alter policy. The **trusted control plane** contains
authorization, approvals, the audit ledger, and settings. It validates structured
inputs and applies deterministic checks independently of model recommendations.

## Threats

| # | Threat | Prevention (design) | Detection | Response | Residual risk | Executable proof |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Indirect prompt injection | Retrieved and claimant text enter the prompt as data; only a validated `ActionProposal` can reach the gate. | Proposal cites clauses that do not support it; denial reason codes. | Deny, log, mark the run for review. | A persuasive injection can still produce a *proposal*; only the gate stops the effect. | Adversarial scenario, Day 10. |
| 2 | Confused deputy | `Principal` is supplied below the model; no model output can set the acting identity. | Decisions record principal and scopes. | Deny, alert on identity mismatch. | Demo identity provider is not a real IdP. | Unauthorized-call denial, Day 3. |
| 3 | Cross-tenant leakage | `tenant_id` on every contract; distinct ID patterns; tenant-bound repositories. | Referential-integrity and ownership tests. | Deny with `tenant_mismatch`. | No row-level enforcement until Day 2 persistence. | Cross-tenant negative test, Day 2. |
| 4 | Excessive tool scope | Capability manifest; narrow tools; `tool_name` pattern. | Tool not in manifest produces `tool_not_in_manifest`. | Deny. | Manifest does not exist yet. | Manifest/authorization test, Day 3. |
| 5 | Approval substitution or replay | Approval binds run, action, tool, exact arguments hash, approver, TTL, and single-use nonce. | Hash mismatch, expiry, `consumed_at` already set. | Reject and require fresh approval. | Nonce store is Day 5. | Mutation/reuse/expiry tests, Day 5. |
| 6 | Duplicate effect after retry | Stable idempotency key; `duplicate` status returning the original effect ID. | Duplicate status in the ledger. | Return the original effect, never a second one. | Effect ledger is Day 3. | Timeout/duplicate test, Day 3. |
| 7 | Stale context | Policy version, clause version, content hash, and retrieval timestamp on every bundle. | Version mismatch against the current policy. | Refuse to act on stale context. | Retrieval is Day 2. | Version/freshness assertion, Day 2. |
| 8 | Audit manipulation | Canonical hash-linked events; sequence and previous-hash validation. | Chain verification fails. | Halt and preserve the run for inspection. | Ledger is in-memory contracts only today. | Ledger verification test, Day 6. |
| 9 | Kill-switch race | Check immediately before every new effect, not at run start. | `kill_switch_active` reason code. | Deny the pending effect; the run stays inspectable and resumable. | No switch implemented today. | Kill-switch test, Day 5. |
| 10 | Secrets in telemetry | Events carry `arguments_hash`, never raw arguments; safe error messages only. | Model-field test; redaction tests. | Rotate and redact. | Span attributes are not yet emitted. | Redaction tests, Day 7. |

## Evidence Discipline

For every Day 1 row, the proof column names a *later* day. No row represents an
implemented control today; treating planned controls as current capability would
inflate claims before the release gates can verify them.
