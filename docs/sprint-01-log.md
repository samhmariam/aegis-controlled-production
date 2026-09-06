# Sprint 1 log

## Day 1 — 2026-09-05

**Decisions**
- Define a constrained synthetic claims-triage boundary with deterministic controls outside the model — model output cannot become authority or an effect — open-ended model-only triage was rejected because it couples recommendation and authorization.
- Use strict Pydantic contracts and canonical payload hashing at trust boundaries — inputs and integrity checks remain testable and reproducible — permissive or unvalidated payloads were rejected because they allow ambiguous state and executable free text.
- Keep all fixture data synthetic and free of real identifiers — the reference implementation can demonstrate controls without personal data — using representative personal or contact data was rejected because it creates unnecessary privacy risk.

**Commands run**
- `uv run ruff check .`
- `uv run mypy src`
- `uv run pytest`

**Evidence produced**
- contracts: `src/aegis/domain/base.py`, `src/aegis/domain/models.py`, `src/aegis/context/models.py`, `src/aegis/identity/principal.py`, `src/aegis/approvals/models.py`, `src/aegis/authorization/decision.py`, `src/aegis/tools/models.py`, `src/aegis/audit/events.py`, `src/aegis/config.py`, `src/aegis/api/`, 107 unit tests
- fixtures: 2 tenants, 6 policies, 12 claims, 6 negative cases, 1 injection case
- ADR: `docs/adr/001-sprint-one-boundary.md`
- threat model: `docs/threat-model.md`, 10 threats with residual risk
- API: `/health`, `/version`, `/claims/validate` — automated checks pass; a manual `/version` request returned successfully

**Honest limitation**

> Day 1 proves the contracts and the executable boundary. It does not prove governed tools,
> permission-aware retrieval, durable execution, approval enforcement or audit verification —
> those are designed, not implemented.

**Focused effort:** not recorded

**Next risk**

> Day 2 must pin the MCP protocol revision and SDK version from the current specification and
> changelog, including the authorization and schema-boundary contract, before Day 3 implements
> a potentially incompatible or unsafe transport boundary.
