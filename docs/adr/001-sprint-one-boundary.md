# ADR 001: Sprint One Boundary

## Status

Accepted, 2026-09-05. Supersedes nothing. Revisit at Day 7 release review.

## Context

Cotswold Mutual is a fictional UK mid-market insurer using a claims-triage workflow
for synthetic first-notification-of-loss submissions. The buyer is the insurer's
claims-operations owner, supported by its engineering, security, and risk
stakeholders. An agent is being considered to accelerate evidence gathering and
prepare a consistent next-step recommendation while leaving consequential decisions
with accountable people.

The workflow is risky because a recommendation can lead toward a consequential
financial effect. It must also preserve strict tenant separation, and the narrative
inside every submitted claim is untrusted content that can attempt to influence the
system beyond the claimant's facts.

## Decision

The workflow receives a synthetic claim, retrieves the relevant policy evidence,
checks deterministic controls, and produces a recommendation for triage, routing, or
human escalation. Its business outcome is a timely, evidence-grounded next action
without granting the workflow authority to decide a claimant's rights or create an
unapproved financial effect.

The workflow may request missing information; retrieve policy clauses; read the
corresponding synthetic claim; recommend routing or escalation; record a
recommendation; execute a synthetic payment record after valid approval.

The workflow may not deny or settle a real claim; execute any real financial
transaction; cross tenant or claimant boundaries; approve its own consequential
action; change its own policy or permissions; treat instructions inside claim
documents as authority; bypass the kill switch; claim production, regulatory or
security certification.

Open-ended triage narratives use a model because they require interpretation and
summarisation of varied claim descriptions. Policy checks, authorization, state
mutation, and persistence remain deterministic code so their inputs, outcomes, and
failure behavior are explicit and testable.

The model proposes. Deterministic controls authorize and execute. The model may
originate a proposal, a rationale, citations, and a confidence; it can never
originate an identity, an authorization, an approval, or an effect.

Payment and claim denial stay human-controlled because they can create consequential
financial or rights-affecting outcomes. A valid human approval is required before a
synthetic payment record can be executed, and claim denial is outside the workflow's
authority.

Every claim is synthetic and local. A demo claim is a deliberately fabricated test
record used to exercise the workflow and controls; a production claim concerns a real
claimant, real policy obligations, and a live insurer decision, none of which this
reference implementation processes.

Canonical payloads represent Decimal values as strings, normalize timestamps to UTC with a `Z` suffix, prune null values, and sort object keys. Days 3-6 hash stability
depends on all four rules.

Identifier separation is enforced at runtime by pattern-constrained types, not by
mypy. Completeness flags are derived from the submitted claim and are never accepted
as input.

## Consequences

SQLite, a local MCP server, and a scripted model adapter make the demo reproducible,
but prove nothing about scale or managed identity. The extra
`src/aegis/tools/models.py` module deviates from the sprint plan's tree. `frozen=True`
does not prevent in-place mutation of a `dict` field; that hardening is deferred to
Day 3.

The boundary also requires deterministic authorization and approval handling beside
the model, explicit synthetic-data fixtures, and tests that distinguish schema
validity from ownership and policy checks.

## Rejected alternatives

- Model-authored tool arguments without schema validation: free text becomes an executable effect.
- An LLM as the authorizer: the control and the thing being controlled share a failure mode.
- A single shared "agent identity" acting on the user's behalf: the confused-deputy pattern.
- Storing raw arguments in the audit event "for debugging": turns the ledger into a leak.
- A stored is_complete flag on the claim: lets the submitter assert its own completeness.

## Extension seams

- Demo identity to Entra workload and delegated identity.
- SQLite to managed Postgres.
- Local intake to queue.
- Console/JSON telemetry to OTLP collector.
- Local MCP transport to deployed Streamable HTTP.
- Local container to Azure staging.
