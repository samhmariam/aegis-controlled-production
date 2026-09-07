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

## Day 2 — 2026-09-06

**Decisions**
- Apply D1: select the policy version whose effective window contains `loss_at`; report explicit missing or stale failures and never substitute a newer version.
- Apply D2: enforce credential validity, expiry, scope, tenant ownership, and claim entitlement before retrieval; make cross-tenant and nonexistent-claim denials identical.
- Apply D5: use bounded lexical retrieval with SQLite FTS5 BM25 when available and a deterministic token-overlap fallback otherwise.
- Preserve canonical clause hashes and verify citations against stored text rather than trusting response-provided hashes.

**Commands run**
- `uv run pytest tests/unit/test_policy_repository.py tests/integration/test_context_api.py -q` — 27 passed.
- `uv run pytest -q` — 139 passed, 1 deprecation warning.
- `uv run ruff check .` — passed.
- `uv run mypy src` — passed; 34 source files checked.
- Authorized API smoke for `/claims/claim-cm-0001/context?query=excess` — HTTP 200.
- Denied API smoke for `claim-cd-0006` and `claim-zz-9999` — identical HTTP 404 envelopes.

**Evidence produced**
- Authorized bundle: `docs/evidence/day-02-context-bundle.md`, synthetic ID `evidence-day02-context-0001`; `claim-cm-0001` resolved to `policy-cm-motor-0001` version `v2` and `clause-cm-motor-0001-excess`.
- Citation outcomes: `docs/evidence/day-02-citation-verification.md`, synthetic ID `evidence-day02-citation-0001`; verified source and tampered-source `hash_mismatch`.
- Denied retrieval: `docs/evidence/day-02-denied-retrieval.md`, synthetic ID `evidence-day02-denied-0001`; cross-tenant and nonexistent claims both returned `{"error_code":"claim_not_accessible","details":[]}`.
- ADR: `docs/adr/007-permission-aware-retrieval.md` covering D1, D2, and D5.
- Current commit recorded in each evidence artifact: `f07c357222f0f3593201e118679249590eaf340e`.

**Honest limitation**

> The evidence uses synthetic local data and a demo credential provider. It proves response
> equivalence and content authorization, not timing-side-channel resistance, production
> identity lifecycle controls, distributed database concurrency, or semantic retrieval quality.

**Focused effort:** permission-aware retrieval, safe fixture seeding, provenance verification, API error envelopes, and reproducible evidence capture.

**Next risk**

> Day 3 must pin and verify the MCP protocol revision and Python SDK version from the
> current specification and changelog before implementing a transport boundary.
