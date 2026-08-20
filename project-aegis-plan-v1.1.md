# Project AEGIS — 38 Build Milestones to Evidence of Controlled Agent Production and Enterprise Integration

> **Service positioning (client delivery only):** I help regulated and data-intensive organizations move AI agents from pilot to controlled production by testing their behavior, securing MCP and tool access, implementing measurable release, operating and cost controls, and integrating agents with the identity, data and legacy systems the enterprise already runs.
>
> **Demonstrated claim (repository):** AEGIS demonstrates controlled-production engineering and six enterprise integration patterns against a real identity provider, managed cloud services and an independent third-party API, using synthetic data.
>
> **Technical shorthand:** I secure, evaluate, cost-control and enterprise-integrate production-oriented agent systems.

The two registers above are deliberately separate. The service positioning describes what the practice does inside a real client estate and may appear only in outreach and proposal material, clearly framed as the service. The demonstrated claim is the only integration claim the repository, README and articles may make, because the reference estate is provisioned by the project itself: the "legacy system" is a synthetic batch producer and the system of record is a newly created managed database. They prove integration engineering patterns, not integration into a pre-existing estate.

> **Revision record (2026-08-20, revision 4):** Added **Day 0**, an environment and access preflight gate covering runtime, both model providers, Azure subscription and offer type, Entra administration rights, GitHub OIDC capability and repository visibility, and expected cloud cost. It is a gate rather than a milestone — the count remains 38 — but an open preflight item now blocks Day 22 entry, because those failures carry procurement lead time and the elapsed-time guidance assumes the access already exists. Companion change in `aegis-resource-guide.md`: a minimum-viable reference path with a four-to-six-hour preflight, per-milestone consultation table and research rule; MCP `2026-07-28` named as the default target with the official conformance suite added under a pinned version and expected-failure baseline; FOCUS deferred out of base v1.0 to a narrow Day 22 bridge; ATLAS mapping made selective; the weekly watchlist replaced by three review cadences; and the PyRIT repository corrected to `microsoft/PyRIT` after the `Azure/PyRIT` archive.
>
> **Revision record (2026-08-20, revision 3):** Pre-implementation corrections from external review. The asynchronous consumer is rebuilt on the correct primitive: an inbox/idempotency record, workflow state and audit event commit in one Postgres transaction under PeekLock, the message is settled only after commit, and the transactional outbox is scoped to its actual job of emitting downstream messages; the claim becomes an effectively-once business effect under tested at-least-once redelivery, with both crash windows tested separately. A Day 2 MCP protocol-contract ADR now pins the protocol revision and SDK version with a compatibility window, header and stateless-handling rules, issuer/audience/resource/scope validation, a no-token-passthrough prohibition and schema-depth bounds, each becoming a Day 3 contract test; the revision identifier must be read from the current specification rather than assumed, and the enterprise-integration ADR renumbers to 003. The delivery forecast is rebased to 38 ordered milestones and a 220-hour target within a 205–250 hour range (v1.0 130h, v1.1 50h, v1.2 40h), with v1.0 triggers moving to 100/130 hours, elapsed-time guidance by weekly capacity, and ten overloaded milestones split into separately exitable lettered halves recorded in a new split register. Postgres row-level security gains a role-topology contract — non-owner runtime role, `NOBYPASSRLS`, four-command cross-claim denial, `FORCE ROW LEVEL SECURITY`, tested privileged-role exclusion — and an identity-derived scoping predicate that the model cannot influence. A new Day 28a independently challenges the fifth chain and the assessment instrument before commercial activation, with the labelled self-review fallback required beside every integration claim if no reviewer is available. Smaller corrections: thirty manual labels are described as a calibration floor, telemetry redaction and a pinned OpenTelemetry semantic-convention version become tested requirements, build provenance names a predicate and verification rule, and the threat model crosswalks a dated agentic threat taxonomy.
>
> **Revision record (2026-08-20, revision 2):** Release-contract corrections from external review. Day 26 now promotes the signed `v1.1-integration-controls` artifact after inherited v1.0 gates *and* applicable v1.1 integration gates, not any v1.0-passing build. The gate-to-release mapping is rewritten: the pre-staging portion of the spend gate becomes mandatory for v1.1 (paid resources exist from Day 23), and v1.2 adds a staging contract/smoke rerun of gates 1–4 with escalation to full suites on variance, priced in the Day 22 re-estimate. Active-token containment now applies to every authenticated MCP request including protected reads, with any cache TTL declared and tested, and the Day 27 drill verifies that a revoked identity's reads stop. Both integration offer rows activate together only after `v1.2-cloud-operation`; until then the third role and fifth chain appear marked in-progress. Azure and Entra become the mandatory reference implementation with AWS/GCP as documented future ports. Resource-group "quota ceilings" are replaced with an accurate capacity-restriction package (subscription/provider/region quotas, resource-group-scoped Azure Policy deny rules, IaC capacity limits, oversized-deployment rejection test). Stale cardinalities corrected: six propositions, two current consulting offers plus a third at v1.2, four evidence bundles rising to five, and a base-v1.0 time-budget label.
>
> **Revision record (2026-08-20, revision 1):** The enterprise-integration extension is incorporated as Days 22–28, shipped as two releases — `v1.1-integration-controls` (Days 22–25) and `v1.2-cloud-operation` (Days 26–28) — with separate 30/25-hour budgets and 22/30 and 18/25-hour triggers. The former extension Day 27 is split into a `[B]` drill/re-verification milestone (Day 27) and an `[A]` commercial-conversion milestone (Day 28). A sixth proposition joins the canonical table, blocked until both integration releases ship, with a six-row CI validation against the competence ledger. New machinery: a two-class control-preservation variance taxonomy, an implementable cloud-spend control package, split Entra revocation semantics (issuance revocation and active-token containment), integration acceptance gates, two integration offer rows and a defined assessment instrument. The market position is split into service-positioning and demonstrated-claim registers. The original v1.0 plan and the standalone integration extension are retired; both remain recoverable in Git history, and this document governs.
>
> **Revision record (2026-08-13):** The schedule is expressed as 21 ordered build milestones over approximately 5–6 calendar weeks, with explicit day-exit and v1.0-release conditions plus 75/100-hour effort controls. Each milestone is labelled for the shared, delivery, advisory or bridge track; the README and two evidence guides provide distinct contracting and consulting buyer journeys over one evidence source. Cost control remains in the headline position, but its attribution component is extraction-ready rather than a second distributed product. Audit evidence separates Day 7 local-anchor verification from the externally anchored release checkpoint required through Day 13/20. Evaluation gates use uncertainty, holdout-custody rules and a precomputed integer pass count. External practitioner review and adversarial self-review are labelled separately. The security audit remains a Day 14 draft and Day 19 final issuance so it can incorporate the Day 18 incident exercise. A build-first development register now limits books, courses and credentials to named, timeboxed weaknesses with validation and stop rules; the Day 19 pack includes an explicit AI Act classification determination.

Project AEGIS is the worked proof behind both statements. It is not another agent demo. It starts with a deliberately limited pilot, exposes why that pilot is unsafe to release, and produces an evidence-backed path to a controlled production candidate.

The reference use case is an insurance claims-triage agent for a fictional UK mid-market insurer, **Cotswold Mutual**. The agent ingests synthetic first-notification-of-loss documents, retrieves policy terms, checks deterministic fraud indicators, and recommends the next action. It may request missing information or route work, but it never settles a claim or makes a rights-affecting decision without an authenticated human approval.

**Base v1.0 time budget:** 25 ordered build milestones across Days 1–21, targeted at **130 focused hours** within a 125–145 hour forecast range. This is a planning trigger, not a promise that the evidence fits the estimate. Routine milestones target 4–6 hours; the lettered halves of Days 7, 8, 13 and 19 exist because each of those milestones carries two to four distinct engineering outcomes. “Day” below means an ordered milestone, not a promise that every outcome fits one fixed session; a lettered half is a separately exitable milestone. “Week” labels are build phases, not calendar weeks. Actual duration is governed by mandatory evidence gates: at 100 logged hours the remaining effort is reforecast, and at 130 logged hours with any mandatory gate blocked, work pauses for a dated re-plan. Evidence depth wins over tool count, and a launched release with accurate claims beats an unlaunched or under-evidenced v1.0. Days 22–28 form the enterprise-integration extension with separate budgets and triggers defined in the effort-control section; Day 22 may not start until `v1.0-aegis` is tagged.

**Whole-programme envelope:** 38 ordered milestones and a **220-hour target** across all three releases, within a 205–250 hour forecast range. Elapsed time depends on sustainable weekly capacity rather than the hour count alone: roughly 7–8 weeks at 35 focused hours per week, 9–12 weeks at 25, and 15–18 weeks at 15. These ranges assume Azure tenant and subscription access already exist; procurement, administrator approval and reviewer availability add elapsed time without adding engineering hours. Outreach timing is planned against the elapsed figure, not the hour count. The forecast is deliberately set where it can be met: a published effort log that lands near its estimate is itself evidence of the estimating judgment the Production-Readiness Assessment sells, and a baseline known to be low would convert the variance triggers below into a formality.

**Repository rule:** every claim in the README must link to a test, generated result, trace, report, or runbook. If the repository cannot reproduce it, the project does not claim it.

**Development rule:** build by default. Learn just in time only when a named weakness blocks the quality of a decision, artifact or commercial interaction, and stop when that weakness is resolved well enough to continue building. `docs/development-register.md` governs books, courses and credentials through a specific-gap, near-term-conversion, timebox and validation decision; it is not a reading list and creates no prerequisite to begin Day 1.

---

## What AEGIS must prove

AEGIS must let a technical buyer verify six propositions without relying on certificates or self-description. The first five are established by `v1.0-aegis`; the sixth is blocked until `v1.2-cloud-operation` ships and may not be asserted before then.

| Proposition | Reproducible proof | Buyer-facing artifact |
|---|---|---|
| The pilot can become a controlled production candidate | Baseline gap assessment, release policy, signed build evidence, rollback exercise and production-readiness score | Production-Readiness Assessment and 90-day remediation plan |
| Agent behavior is tested rather than “vibe checked” | Versioned holdout set, calibrated scoring, repeated runs, slice results, adversarial cases and model-migration diff | EvalOps scorecard and migration regression report |
| MCP and tool access is constrained outside the model | Per-tool authorization, short-lived identities, capability manifests, egress limits, approval enforcement and negative security tests | MCP Security / NHI Audit report |
| Release and operating controls are measurable | Quality, security, cost and reliability gates; SLOs; alerts; change record; incident and recovery evidence | Release evidence pack and AgentOps runbook |
| Cost is attributable and controlled without hiding quality loss | Per-claim attribution, quality-adjusted unit economics, forecast variance, caps, anomaly tests and safe degradation | Power BI executive dashboard and FinOps-for-Agents report |
| The agent integrates with a real identity provider, managed cloud services and an independent third-party API without weakening any v1.0 control — **blocked until `v1.2-cloud-operation`** | Real-IdP issuance-revocation and active-token-containment tests, batch reconciliation with drift detection, third-party outage drill, IaC-provisioned staging deployment, cloud rollback exercise, unchanged sealed-suite pass in the integrated environment | Enterprise Integration Readiness Assessment and integration runbook |

**Six-row validation:** CI checks that the README propositions table contains exactly six rows and that every row's proof column resolves to at least one competence-ledger chain with a runnable test command; a propositions row without a ledger chain fails the build. While the sixth row is blocked, its status is shown in the table and the claims register prohibits asserting it publicly.

### Contracting-to-consulting continuum

AEGIS has one implementation and one evidence source, exposed through two buyer journeys. Track labels on each milestone indicate its **primary** function; they do not create separate implementations or duplicate artifacts. The labels extend to the integration milestones: Day 22 `[S]`, Days 23–26 `[D]`, Days 27a–27b and 28a `[B]`, Day 28b `[A]`.

| Label | Track | Primary question answered | Typical output |
|---|---|---|---|
| `[S]` | Shared control spine | What requirements, risks, boundaries and evidence govern both routes? | Engagement brief, threat model, policies, claims and competence ledgers |
| `[D]` | Delivery evidence | Can this engineer implement, test and operate the control? | Code, tests, CI gates, traces, packages and runbooks |
| `[A]` | Advisory conversion | Can this consultant diagnose the gap, support a decision and prioritize remediation? | Assessments, executive evidence, recommendations and roadmap |
| `[B]` | Bridge | Can the same technical evidence support both an engineering and an executive decision? | Audit, migration decision, incident evidence, economics and launch proof |

```text
                    [S] Shared control spine
                              |
             +----------------+----------------+
             |                                 |
             v                                 v
     [D] Delivery evidence             [A] Advisory conversion
     implement + verify                assess + recommend
             |                                 |
             +---------------+-----------------+
                             v
                       [B] Bridge evidence
               technical fact -> buyer decision
                             |
                             v
                   scoped remediation follow-on
```

The delivery guide and advisory guide are navigation layers over this evidence. Engineering produces facts once; advisory artifacts interpret, prioritize and price the response to those facts.

### The competence ledger

Maintain `docs/evidence/competence-ledger.md` from Day 1. Each row uses this chain:

```text
Buyer requirement
      |
      v
Risk / failure mode -> control -> automated test -> generated evidence
                                              |
                                              v
                              operating metric + named owner
```

The ledger prevents polished reports from drifting away from implemented controls. It is also the index a reviewer uses to navigate the repository.

---

## Definition of “controlled production” for this project

AEGIS is a public reference implementation using synthetic data. It cannot prove that a real insurer is compliant or that the system has operated at commercial scale. In this project, **controlled production candidate** means all of the following are evidenced:

1. The mission, prohibited actions, human decision rights and risk boundaries are explicit.
2. The model cannot grant itself permissions; deterministic code authorizes every consequential tool call.
3. Quality, safety, security, cost and reliability thresholds gate a release.
4. Every decision and tool action is attributable to a model, prompt, policy, identity, data and code version.
5. A tested stop, rollback and recovery path exists.
6. SLOs, alerts, runbooks, ownership and incident procedures exist for operation after release.
7. Residual risks and unsupported claims are disclosed.

The README must say **“production-oriented reference implementation”** or **“controlled production candidate,”** not “production-proven system.” Regulatory mappings are technical evidence crosswalks, not legal opinions or certifications.

---

## Scope guardrails

### Mandatory core

- Two synthetic claim types: motor and property.
- One LangGraph workflow and three MCP tool domains: policy retrieval, claims records and mock payments.
- Claude as the baseline model and one alternate model for migration testing.
- Deterministic policy enforcement outside the LLM.
- Functional, adversarial, security, cost and reliability tests.
- One local/staging deployment path with a reproducible container build.
- Four integrated evidence bundles: readiness, security, EvalOps and AgentOps/cost.

**Integration extension — `v1.1-integration-controls` (Days 22–25):**

- Real IdP integration for all three MCP domain identities, with issuance-revocation and active-token-containment tests executed against the real IdP.
- One legacy-style batch interface with reconciliation and drift detection.
- One genuinely external third-party API on a non-consequential (advisory/enrichment) path.
- One asynchronous queue-based intake path with idempotency and dead-letter evidence.
- Sealed behavioral, adversarial and audit-verification suites re-run against the locally integrated environment, with every difference classified under the variance taxonomy.
- README, competence-ledger and six-row propositions validation wiring.

**Integration extension — `v1.2-cloud-operation` (Days 26–28):**

- One IaC-provisioned cloud staging environment with CI promotion and an exercised cloud rollback.
- The combined integration incident drill and full staging re-verification of the sealed suites.
- The Enterprise Integration Readiness Assessment, integration runbook, both commercial offer rows, the updated guides and README entry-point text, and the edited, published, link-checked article 4.

### Stretch only after all release gates pass

- Garak in addition to PyRIT.
- promptfoo in addition to the primary Python/DeepEval harness.
- A public container image or hosted demo.
- More claim types, multi-agent coordination or real-time streaming.
- A second dashboard beyond the Power BI executive view.
- Standalone packaging, versioning or distribution of the cost-attribution component outside the AEGIS release.
- A second cloud region or environment tier (dev → staging promotion chain).
- An API-gateway or iPaaS front (e.g. APIM) in front of the MCP services.
- SharePoint/Graph API as a document store for policy PDFs.
- Contract-testing tooling (e.g. Pact) beyond the hand-rolled contract tests.

### NOT in scope

- Real customer, claimant or insurer data: synthetic data only avoids privacy and contractual risk.
- Autonomous settlement, claim denial or payment: those actions remain human-authorized because this is a high-impact workflow.
- A legal conclusion of UK GDPR, FCA, Consumer Duty, ISO/IEC 42001 or EU AI Act compliance: AEGIS supplies technical evidence only.
- Production load or availability claims: local/staging tests can demonstrate engineering controls, not commercial-scale operation.
- A custom identity provider, policy engine, vector database or observability platform: use established components and focus effort on integration and evidence. Integrating the real managed identity provider on Days 23 and 26 is in scope and is the point; building one is not.
- Multi-agent or A2A architecture: it adds surface area without strengthening the three core service offers.
- General reading programmes or new certifications on the v1.0 critical path: targeted learning is admitted only through the development register after the work exposes a named weakness.
- A self-managed Kafka cluster or streaming platform; a managed queue exercises the async pattern at appropriate scale.
- Building an ESB, iPaaS or custom gateway.
- Real customer, claimant or insurer data through any integration seam: batch files, database rows and queue messages carry only generated synthetic content, and the third-party API receives only synthetic, non-personal lookup values (fictional postcodes drawn from published test ranges, or public company numbers).
- Autonomous consequential actions through any integration seam: the third-party API and batch feed inform recommendations only; payment, denial and settlement remain authenticated human actions.
- Any public claim of integration into a pre-existing enterprise estate (see the integration claims discipline).

### Predeclared descope ladder (overrun-prone days)

Descope decisions are written now, before schedule pressure exists, so a slip triggers a predefined cut rather than an improvised one. Any cut taken is disclosed in the claims register with a dated decision record.

| Milestone | Minimum condition to exit the day | Deferred work and release effect |
|---|---|---|
| Day 7 — traceability and release contract | Sequence-numbered hash chain, separate signer identity, verifier, signed heads checked through the local anchor adapter and frozen release policy | External CI/transparency-log anchor wiring moves to Day 13, or Day 20 with deferred provenance work. Article 1 may remain an edited draft. Audit and reproducibility gates remain blocked until the externally stored release checkpoint verifies. |
| Day 8 — evaluation protocol | Normal target: at least 100 sealed holdout cases. Descope floor: 60 cases, 30 blind human-labelled calibration cases, five core rubrics and minimum primary-slice sizes declared. At `n=60`, the Wilson condition dominates: `54/60` fails and at least `55/60` (91.67%) is required. | Secondary slice expansion may remain diagnostic. The behavioral release gate stays blocked if the 60-case floor, holdout custody, primary-slice coverage, judge calibration or precomputed integer pass count is incomplete. |
| Day 13 — release gate | PR lanes for deterministic/security tests and behavioral canary; seeded authorization-bypass and behavioral-regression failures | Day 17 receives the reconciled cost lane. Day 20 receives container/SBOM/provenance and vulnerable-dependency regression. Until recovered, cost, supply-chain and reproducibility gates remain blocked and those public claims must be withheld. |
| Day 15 — cost attribution | Happy-path and retry attribution reconciled for both claim types; unattributed events surfaced rather than discarded | Day 17 receives failed-call, cache-hit and telemetry-loss treatment. Until recovered, the 100% captured-event attribution gate and cost-control claim remain blocked. |
| Day 18 — SLOs and incident exercise | One scripted injection incident with measured detect/contain/recover times; alerts for unauthorized action, audit failure and mandatory-escalation failure | Broader alert coverage may remain a disclosed roadmap item. Stop, recovery and the three critical alerts are mandatory for v1.0. |
| Day 19 — governance pack | Pilot/final readiness assessments, final security audit, 90-day roadmap and dated AI Act classification determination; crosswalk covers implemented controls | Additional framework crosswalk rows may remain open actions, but every public regulatory mapping must link to implemented evidence and retain its caveat. The classification determination, independent Article 50 analysis and reclassification triggers are mandatory. |
| Day 23 — identity plane | All three MCP identities and the audit signer resolved through Entra; issuance revocation proven; active-token containment proven within the declared maximum window | CI OIDC federation may defer to Day 26. Until recovered, the "no stored cloud secrets" claim is withheld. |
| Day 24 — legacy and third party | Batch ingestion with reconciliation totals and at least one detected seeded drift; third-party client with timeout, retry-with-jitter and fail-degraded behavior under a forced outage | Duplicate-file and late-file handling may defer to Day 25 close or Day 27, with the reconciliation gate blocked until recovered. |
| Day 25 — async intake and v1.1 tag | Queue consumer proves idempotency under redelivery and routes a poison message to the DLQ with an alert | Post-commit settlement ordering and the crash-window tests may defer to Day 27; the effectively-once claim and the `v1.1-integration-controls` tag are withheld until recovered. |
| Day 26 — cloud staging | `terraform/bicep apply` from a clean state produces a working environment; one CI-promoted deploy; one exercised rollback to the previous release | Environment-teardown/rebuild timing evidence may defer to Day 27. The reproducible-environment claim requires at least one clean rebuild before v1.2. |
| Day 27 — drill and staging re-verification | Combined incident drill executed with measured times; staging re-verification classified under the variance taxonomy | Additional drill scenarios may remain disclosed roadmap items. Open control regressions block `v1.2-cloud-operation`. |
| Day 28a — independent integration challenge | One external practitioner review across the declared scope, or the documented self-review fallback with its label applied everywhere an integration claim appears | Reviewer unavailability triggers the labelled fallback, never silent omission. The challenge itself may not defer past Day 28a. |
| Day 28b — commercial conversion | Assessment, offer rows, README entry-point text and published article 4 complete | No conversion artifact may defer past Day 28b; if any is incomplete, v1.2 does not tag and the sixth proposition stays blocked. |

Slip order when any milestone overruns: stretch tooling first (Garak, promptfoo, hosted demo), additional scenarios second and non-evidentiary polish third. Deferred work is entered in `docs/evidence/deferred-work-register.md` with an owner, receiving milestone, blocked release gate and prohibited public claim. A milestone may close with deferred work; `v1.0-aegis` may not ship while any mandatory gate remains blocked. The executive conversion layer never slips (next section).

### Effort-control triggers

Log actual focused time by milestone in `docs/evidence/effort-log.csv` using `date,milestone,hours,cumulative_hours,outcome,deferred_work`. Time spent on implementation, evaluation, evidence production, review, remediation and activated just-in-time development counts; passive CI/runtime wait does not. The development register permits at most three active resources and four focused learning hours per build week.

- **At 100 cumulative hours:** forecast the effort remaining for every blocked mandatory gate and record likely calendar variance, cuts available through the ladder and reviewer/launch impacts. No new learning resource is activated unless its time and blocked decision are included in that forecast.
- **At 130 cumulative hours:** if any mandatory gate is blocked, stop discretionary work, stretch work and development activity and issue a dated re-plan before continuing. Development may resume only when the re-plan identifies a timeboxed resource as the shortest safe path to clearing a named mandatory gate. The re-plan must choose one or more of: cut non-gate scope through the ladder; extend the calendar while retaining the full release contract; or reduce the target deliverable and withdraw the associated public claims.
- **Release-label invariant:** removing, weakening or knowingly leaving a mandatory gate blocked changes the release target. The result may be labelled a preview, partial-evidence release or `v0.x` candidate, but it may not be tagged `v1.0-aegis` or described as the complete controlled-production evidence pack.

The trigger exists to expose variance early, not to make 130 hours a deadline that overrides evidence.

**Integration budgets (Days 22–28):** the integration releases carry their own budgets and triggers, separate from and additional to the v1.0 controls above. `v1.1-integration-controls` (7 milestones across Days 22–25) is targeted at 50 focused hours within a 45–55 hour range, with a forecast trigger at 38 and a re-plan trigger at 50; `v1.2-cloud-operation` (6 milestones across Days 26–28) at 40 focused hours within a 35–50 hour range, with triggers at 30 and 40. The combined ~90-hour forecast is a planning trigger, re-confirmed in the Day 22 ADR once the concrete Azure services are fixed. All extension time logs into the same `docs/evidence/effort-log.csv` with labels `day-22` through `day-28` so total project effort remains one auditable series. Release-label invariants: `v1.1-integration-controls` may not ship while any Day 22–25 mandatory gate is blocked; `v1.2-cloud-operation` may not ship while any integration gate — including article 4 publication and the commercial artifacts — is blocked; the sixth proposition stays blocked until both releases ship; a partial result is labelled `-rc` with its blocked gates disclosed. Day 22 may not start until `v1.0-aegis` is tagged.

### Milestone split register

Ten milestones each carry two or more distinct engineering outcomes and are therefore split into lettered halves. The split changes sequencing honesty, not scope: no work is added or removed, and every existing cross-reference to "Day 7", "Day 13" and so on continues to address the whole milestone. Each half is separately exitable, separately tagged (`day-07a`, `day-07b`) and separately logged in `docs/evidence/effort-log.csv`. Where the descope ladder names a milestone, the ladder condition applies at the **b-half** exit unless stated otherwise.

| Milestone | First half (a) | Second half (b) |
|---|---|---|
| Day 7 `[B]` | OTel/Langfuse trace pipeline, semantic-convention pinning and telemetry redaction tests | Hash-chain audit, signer identity, local anchor, verifier tests, frozen release policy, reviewer confirmation, video 1 |
| Day 8 `[D]` | Dataset design, dev/calibration/holdout split, custody rules, manifest hashing, five rubrics | Thirty blind manual labels, judge calibration, statistical fixtures, pre-result gate manifest |
| Day 13 `[D]` | Four CI lanes (deterministic/security, behavioral canary, supply chain, provisional cost) and seeded blocking records | Container build, SBOM, provenance predicate and verification rule, external audit-anchor wiring, release-evidence generator |
| Day 19 `[A]` | Control-evidence matrix, AI Act classification determination, model/system cards, data sheet | Pilot and final readiness assessments, 90-day roadmap, final security audit issuance |
| Day 23 `[D]` | Entra app registrations per MCP domain, Key Vault signer custody, GitHub OIDC federation | Issuance revocation, active-token containment with declared window, re-run negative identity suite, NHI register variance column |
| Day 24 `[D]` | Batch file contract, ingestion, reconciliation, quarantine, five seeded failures | Managed Postgres migration, runtime/owner role topology, RLS bypass tests, third-party client and forced-outage drill |
| Day 25 `[D]` | Webhook, queue, inbox/idempotency consumer, DLQ, replay, kill-switch extension | Locally integrated re-verification of sealed suites, variance classification, `v1.1-integration-controls` tag |
| Day 26 `[D]` | IaC authoring, clean-state provision, CI promotion with digest-provenance check | Cloud rollback, teardown/rebuild, egress-restriction proof, spend reconciliation |
| Day 27 `[B]` | Combined integration incident drill with measured detection, containment and read-containment evidence | Staging re-verification: sealed suites plus the contract/smoke rerun of integration gates 1–4 |
| Day 28 `[A]` | Independent integration challenge of the fifth chain and assessment instrument, or labelled self-review fallback | Assessment issuance, offer rows, guide and README updates, article 4 publication, sixth-proposition unblock, `v1.2-cloud-operation` tag, outreach |

### Non-slippable executive conversion layer

The buyer of the wedge assessment is an executive who will never run the reviewer commands. For that audience the entire project reduces to four artifacts, which therefore carry the same release-blocker status as silent critical-path failures:

1. Executive-facing video 3 (no code walkthrough).
2. The service one-pager mapping offers to evidence.
3. The static Power BI dashboard export.
4. The Production-Readiness Assessment of the pilot and the final candidate.

If engineering scope and these four artifacts ever compete for time, engineering scope takes the descope ladder; these four do not. “Non-slippable” means they must exist before public launch, not that they can substitute for a blocked technical release gate. If the underlying evidence is incomplete, the artifact states the gap and `v1.0-aegis` waits.

After the integration milestones begin, the **Enterprise Integration Readiness Assessment** and the **published article 4** join this layer for `v1.2-cloud-operation`: they may not be traded away for engineering scope, and if the underlying evidence is incomplete the artifact states the gap and v1.2 waits.

### Preparation schedule for overloaded milestones

Large reports and launch assets are assembled continuously rather than started on their named milestone.

| Preparation starts | Incremental work | Final assembly milestone |
|---|---|---|
| Day 1 | Create the two-entry-point README, delivery/advisory guides, service-to-artifact matrix, reviewer-guide, service-one-pager, readiness-assessment skeletons and just-in-time development register; begin practitioner outreach. Draft the commercial artifacts before activating consulting-craft material. | Days 19–21 |
| Day 2 | Create the control-evidence matrix, AI Act classification-determination, system-card and data-sheet skeletons from the threat model | Day 19 |
| Days 4–7 | Capture reusable traces, diagrams and demo clips; outline article 1 as boundary decisions are made | Day 7 |
| Days 8–13 | Populate the security-audit draft from baseline attacks, remediation, kill tests and release evidence; outline article 2 and capture video clips | Day 14 |
| Days 15–17 | Export dashboard views as each metric lands; populate the service one-pager and outline article 3 | Days 17 and 20 |
| Day 18 | Storyboard the executive video from the measured incident, release and economics evidence | Day 20 |
| Day 22 | Readiness-assessment skeleton from the integration instrument; offer-row skeletons; article 4 outline | Day 28 |
| Days 23–25 | Capture variance records, seeded-failure traces and containment-window evidence as each seam lands | Days 25 and 28 |
| Day 26 | Capture provision/deploy/rollback timestamps and spend-reconciliation extracts | Day 27 |
| Day 27 | Fold drill timeline and staging variance record into the assessment draft | Day 28 |

The named milestone is the review and issuance point, not the first time the artifact is opened.

### Buyer-navigation artifacts

The repository has two maintained entry guides, both generated from or linked to the same competence ledger and release evidence.

#### `docs/delivery-evidence-guide.md` — “Hiring an engineer?”

This guide is for engineering managers, AI/ML platform leads and security architects assessing contracting fit. It must contain:

1. The concrete delivery roles supported: Agent EvalOps/LLMOps Engineer, Agentic AI/MCP Security Engineer and — marked in-progress until `v1.2-cloud-operation` ships — Agent Integration Engineer, with AgentOps cost implementation as adjacent evidence.
2. A system architecture and trust-boundary summary.
3. Five traceable delivery chains: EvalOps/model migration, MCP/NHI security, release/operations, cost attribution and enterprise integration (problem → integration ADR → code location → contract/reconciliation tests → seeded failure → generated result → limitation → client-team ownership).
4. For each chain: problem, code location, test command, seeded failure, generated result, limitation and what the engineer would own inside a client team.
5. A clean-checkout quick start and one-command evidence-generation path.
6. Direct links to the test/evidence artifacts in the service-to-artifact matrix; no copied score or claim that can drift from the source result.

#### `docs/advisory-evidence-guide.md` — “Assessing a consulting engagement?”

This guide is for CTO, CISO, Head of AI, risk, operations and finance buyers. It must contain:

1. The pilot-to-controlled-production problem and evidence-based assessment method.
2. The six assessment dimensions: boundaries, data/integration, evaluation, security/identity, release/operations and cost.
3. The pilot-versus-candidate findings, release blockers, residual risks and ship/hold logic.
4. Two current consulting offers: Production-Readiness Technical Assessment and Agent Cost and Unit-Economics Diagnostic, joined by a third — the Enterprise Integration Readiness Assessment (assessment-type, like the readiness assessment; not assurance) — once `v1.2-cloud-operation` ships. EvalOps/Model-Migration Assurance and MCP/Agent-Control Review appear as evidence-backed future expansions after real client delivery, not implied current assurance authority.
5. For each offer: buyer, triggering problem, scope, inputs, outputs, exclusions, underlying tests/evidence and likely remediation path.
6. Direct links to the executive summary, final assessment, audit, dashboard and 90-day roadmap; no compliance certification or production-scale claim.

#### README navigation contract

The README places these two entry points immediately after the opening positioning and four proof points:

```markdown
## Hiring an engineer?

Start with the [Delivery Evidence Guide](docs/delivery-evidence-guide.md) to inspect the implementation, test commands, seeded failures and generated evidence for EvalOps, model migration, MCP security, release controls and cost attribution.

## Assessing a consulting engagement?

Start with the [Advisory Evidence Guide](docs/advisory-evidence-guide.md) to review the readiness method, executive findings, release blockers, service scopes and 90-day remediation path.
```

CI checks that both guide links and every guide-to-evidence link resolve. These are navigation layers, not new evidence stores.

The block above is the Day 20 (v1.0 launch) wording. On Day 28 both entry-point blocks are replaced with the following exact text, and CI re-checks the links and the six-row propositions table:

```markdown
## Hiring an engineer?

Start with the [Delivery Evidence Guide](docs/delivery-evidence-guide.md) to inspect the implementation, test commands, seeded failures and generated evidence for EvalOps, model migration, MCP security, release controls, cost attribution and enterprise integration.

## Assessing a consulting engagement?

Start with the [Advisory Evidence Guide](docs/advisory-evidence-guide.md) to review the readiness method, executive findings, release blockers, service scopes, the enterprise integration readiness method and the 90-day remediation path.
```

#### Integration offers (assembled Day 28)

Both offers consume the same six-seam evidence produced on Days 22–28; neither creates a second implementation or evidence store.

**Contracting offer — Enterprise Agent Integration Engineering** (added to `docs/delivery-evidence-guide.md`):

| Field | Content |
|---|---|
| Buyer | Engineering managers, AI/ML platform leads, integration architects assessing contracting fit |
| Triggering problem | An agent pilot works in a sandbox but is blocked on identity, data, legacy, third-party, async or deployment integration into the estate |
| Scope | Hands-on implementation of the six-seam patterns inside the client's stack: workload identity, batch/file contracts with reconciliation, system-of-record access, resilient third-party clients, queue-based intake, IaC-promoted deployment |
| Inputs | Estate inventory, identity tenant access, target-system contracts, existing pipeline definitions |
| Outputs | Working integrations with contract/reconciliation tests, seeded-failure evidence, runbooks and variance records |
| Exclusions | Building ESB/iPaaS/IdP platforms; production operation ownership; real-data migration design authority |
| Underlying tests/evidence | The fifth delivery chain: Days 23–26 code, test commands, seeded failures and generated results |
| Likely remediation path | Seam-by-seam implementation ordered by consequential-action exposure, then detection gaps, then recovery gaps |

**Consulting offer — Enterprise Integration Readiness Assessment** (added to `docs/advisory-evidence-guide.md` as the third current offer):

| Field | Content |
|---|---|
| Buyer | CTO, CISO, Head of AI, platform and integration leadership |
| Triggering problem | Leadership cannot tell whether the agent pilot's integration approach will survive contact with the estate, or what integration work stands between pilot and controlled production |
| Scope | Assessment of the six seams against the instrument below; findings, blockers, residual risks and a prioritized remediation plan |
| Inputs | Architecture documentation, identity model, interface contracts, deployment pipeline definitions, interviews |
| Outputs | Scored per-seam findings, release-blocker list, residual-risk register, prioritized remediation roadmap, executive decision recommendation |
| Exclusions | Compliance certification, production-scale attestation, vendor selection authority, legal opinions |
| Underlying tests/evidence | The worked assessment in `assessment/integration-readiness.md`, applied to AEGIS's own pilot-vs-integrated states, plus the six-seam evidence it cites |
| Likely remediation path | 90-day phased plan ordered by the prioritization rule in the instrument |

#### The integration assessment instrument

`assessment/integration-readiness.md` applies this instrument; the same instrument is the method sold in the consulting offer.

**Evidence required per seam:**

| Seam | Minimum evidence to score above Absent |
|---|---|
| Identity | Per-workload identity inventory; issuance-revocation and active-token-containment tests with a declared window; secret-storage audit |
| Legacy/batch | Written file contracts; reconciliation with control totals; drift/late/duplicate/truncation detection tests; quarantine behavior |
| System of record | Scoped access model with negative tests on the real engine; versioned migrations; parameterized access audit |
| Third party | Timeout/retry/circuit-breaker configuration; forced-outage degradation evidence; dependency terms and version record |
| Async | Idempotency evidence under redelivery; DLQ and replay procedure; audit coupling across the boundary; stop behavior |
| Deployment | IaC reproducibility (clean provision and rebuild); promotion with provenance verification; exercised rollback |

**Finding scale (per seam):** `Implemented` (evidence-linked, objective met), `Partial` (objective partly met; named owner and action), `Absent` (no credible evidence), `Not applicable` (justified in writing). Individual findings within a seam carry a severity: `Critical` (a consequential action can occur without its control), `High` (prevention or containment objective unmet), `Medium` (detection or recovery objective unmet), `Low` (hygiene or documentation).

**Release blockers:** any Critical finding; any High finding on a consequential-action path; any control regression under the variance taxonomy. A blocked seam blocks the ship recommendation regardless of aggregate posture — no averaging.

**Residual-risk treatment:** every non-blocking open finding enters an accepted-residual-risk register with owner, rationale, compensating control (if any) and review date. Unowned risks may not be accepted.

**Remediation prioritization:** order by (1) consequential-action exposure, (2) detection gaps, (3) recovery gaps, (4) hygiene; phased into a 90-day plan with a named first sprint.

**Executive decision:** the assessment ends in exactly one of `Ship`, `Hold` (with the blocking findings listed), or `Conditional ship` (with named conditions, owners and dates). The AEGIS worked example records the decision for the pilot state and the integrated state.

---

## Reference architecture

```text
 Synthetic claim                 Control plane
 document + form          +---------------------------+
        |                 | versioned agent-policy    |
        v                 | identity + capability reg |
  [Data classification]   | release thresholds        |
        |                 | kill switch + budgets     |
        v                 +-------------+-------------+
  [Untrusted-content                    |
   boundary]                            v
        |                    [Policy decision point]
        v                               |
  [LangGraph workflow] <----------------+
        |
        +---------- propose tool action ----------+
        |                                         |
        v                                         v
 [Policy retrieval MCP]  [Claims-record MCP]  [Mock-payment MCP]
 read-only identity       scoped read/write     human approval +
 egress allowlist         row/action checks     hard value limits
        |                     |                     |
        +---------------------+---------------------+
                              |
                    [Tamper-evident audit + OTel]
                              |
             +----------------+----------------+
             |                |                |
             v                v                v
   [Signed checkpoint] [Eval/release evidence] [Cost attribution]
             |                |                |
             v                +--------+-------+
    [External audit anchor]            |
                                       v
                              [Power BI evidence]
                                       |
             +-------------------------+
                              v
                  [Release / operate / rollback]
```

**Security invariant:** prompts may recommend an action but never authorize it. The policy decision point and each MCP server independently enforce identity, scope, claim-value limits and approval state.

**Audit invariant:** the ledger is described as **tamper-evident**, not immutable. Each event has a monotonic sequence number and includes a correlation ID, timestamp, actor/NHI, model and prompt version, policy version, tool-arguments hash, authorization result, human-approval reference, cost and outcome. Event hashes form a chain. Periodic chain heads are signed by an audit-signer identity whose private key is unavailable to the agent and ordinary ledger writer. Day 7 verifies the signing and tamper-detection algorithms through a testable local anchor adapter. For v1.0, a signed release head must be stored outside the ledger through CI build attestation or a transparency-log-backed mechanism wired on Day 13 or recovered on Day 20; a real WORM/retention-locked store remains a production deployment option. Verification must detect mutation, reordering, middle deletion, tail truncation and full-chain replacement. The claims register states the trust assumption: compromise of both ledger storage and external signing/anchor control is outside the reference implementation’s protection.

Days 22–28 replace the mocked seams of this diagram with the real estate defined in the next section: Entra ID workload identities and Key Vault signer custody, a managed Postgres system of record, a batch file contract, a genuinely external enrichment API, queue-based intake and an IaC-provisioned cloud staging environment.

---

## Enterprise integration (Days 22–28): landscape, releases and controls

AEGIS v1.0 is deliberately self-contained: the MCP domains are mocks the project builds, identity integration is a paper mapping to Entra, and deployment stops at local/staging. The project's own market research identifies "insufficient tool/data access" and legacy-integration "innovation theatre" as leading pilot-to-production killers, so Days 22–28 convert the integration story from designed-for to demonstrated by making the **systems** real — never the claims, claimants or policies, which remain synthetic throughout.

### Target enterprise landscape

```text
                         Microsoft Entra ID tenant
                (app registrations, workload identity federation,
                     Key Vault for the audit-signer key)
                                   |
            +----------------------+----------------------+
            |                      |                      |
            v                      v                      v
   [Policy admin system]   [Claims core DB]      [GitHub Actions CI]
   "legacy": nightly CSV    managed Postgres      OIDC federation ->
   batch drop to storage    row-level access      short-lived cloud
   (no API; file contract)  via MCP identity      credentials, no
            |                      |              stored secrets
            v                      v                      |
      [Ingestion +          [Claims-record MCP]           v
       reconciliation]             |               [IaC pipeline]
            |                      |               Bicep/Terraform ->
            v                      |               cloud staging env
   [Policy-retrieval MCP]          |               (containerized
            |                      |                AEGIS + MCPs)
            +----------+-----------+
                       |
                       v
              [LangGraph workflow]
                       |
         +-------------+--------------+
         |                            |
         v                            v
  [Async intake queue]      [Third-party enrichment API]
  FNOL webhook -> queue      real external service
  idempotent consumer,       (e.g. postcode/address or
  DLQ, inbox transaction     company lookup): rate limits,
                             outages and versioning are
                             genuinely outside our control
```

| Seam | Real component | Enterprise pattern exercised |
|---|---|---|
| Identity | Entra ID app registrations, workload identity federation, Key Vault | Per-workload identity in a real IdP; secretless CI; managed key custody |
| Legacy data | Nightly CSV/flat-file batch drop to object storage | File-contract integration, reconciliation, schema drift, late/partial/duplicate files |
| System of record | Managed Postgres | Parameterized access, migrations, row-level scoping under a real DB engine |
| Third party | One genuinely external API (e.g. postcodes.io address validation or Companies House lookup for fraud enrichment) | Rate limits, timeouts, outages, versioning and terms the project cannot change |
| Async | Managed queue (e.g. Azure Service Bus / Storage Queue) for FNOL intake | Webhook → queue → idempotent consumer, dead-letter handling, replay, poison messages |
| Deployment | Cloud staging via IaC, promoted from CI | Reproducible environments, managed identity at runtime, cloud rollback |

**Azure and Entra are the mandatory reference implementation**, not one option among several. Every downstream milestone, gate, claim and closure row names Entra ID, Key Vault and the Azure managed services above, and the skill-to-proof and gap-closure sections treat Azure/Entra depth as the specific competence being evidenced; a substitution would silently invalidate all of them. AWS and GCP equivalents (identity federation with RDS and SQS) are pattern-equivalent **future ports**, documented as such and out of scope for v1.1 and v1.2. The Day 22 ADR confirms the concrete Azure services, region, subscription-offer eligibility and the re-estimated effort budget; it does not reopen the platform choice.

### Release structure

| Release | Milestones | Scope | Initial budget | Forecast trigger | Re-plan trigger |
|---|---|---|---|---|---|
| `v1.1-integration-controls` | Days 22, 23a–b, 24a–b, 25a–b (7 milestones) | Identity plane, legacy batch, system of record, third-party API, async intake — integrated and verified locally against real services | 50 focused hours (45–55) | 38 hours | 50 hours |
| `v1.2-cloud-operation` | Days 26a–b, 27a–b, 28a–b (6 milestones) | IaC cloud staging, CI promotion, cloud rollback, integration incident drill, staging re-verification (sealed suites plus the contract/smoke rerun of gates 1–4), independent integration challenge, commercial assembly and article publication | 40 focused hours (35–50) | 30 hours | 40 hours |

The two halves are separate releases because they carry different risk profiles: Days 22–25 are runnable locally against real managed services, while Days 26–28 depend on cloud provisioning friction, billing latency and vendor behavior outside the project's control.

The v1.2 budget carries the staging contract/smoke rerun of gates 1–4 in addition to the sealed-suite re-verification. The Day 22 re-estimate must price that rerun explicitly rather than discovering it at the 18-hour forecast trigger; if it cannot fit, the descope ladder cuts drill breadth and non-evidentiary polish before it cuts rerun coverage.

### Control-preservation rule: variance taxonomy

Every control proven in v1.0 must continue to meet or exceed its control objective in the integrated environment. Differences are classified into exactly two classes; there is no third category and no silent absorption.

| Class | Definition | Treatment |
|---|---|---|
| **Implementation variance** | A different lifetime, mechanism or provider behavior that still **meets or exceeds** the v1.0 control objective (e.g., an Entra-imposed minimum token lifetime, a managed queue's redelivery semantics) | Recorded in the claims register with a dated disposition: objective, v1.0 mechanism, integrated mechanism, evidence that the objective still holds. Does not block release. |
| **Control regression** | Weaker prevention, detection or recovery than v1.0 evidenced (e.g., a longer window in which a revoked identity can act, a batch path that can partially load, an audit event that can be lost across the async boundary) | **Blocks the affected release tag and the sixth proposition** until remediated or the objective is restored by a compensating control whose test passes. A regression may not be dispositioned as a variance. |

The sealed behavioral suite, the adversarial suite and full audit-chain verification are re-run against the locally integrated environment before `v1.1-integration-controls` is tagged, and against the staging environment before `v1.2-cloud-operation` is tagged. Every result difference is classified under this taxonomy with a dated record.

### Cloud spend controls

Azure budgets trigger notifications but do not stop consumption; hard spending limits exist only on certain subscription offers; and cost data arrives with latency. An absolute "spend stays under cap" release gate is therefore not implementable and is **not** claimed. The implementable control package, configured before any Day 23 resource is created and versioned in `controls/cloud-budget.yaml`, is:

1. **Eligibility record:** whether the subscription offer supports a hard spending limit, recorded in the Day 22 ADR; if supported, the limit is enabled.
2. **Tiered alerts:** budget alerts at 50%, 75% and 90% of the recorded monthly cap, delivered to a monitored channel.
3. **Automated teardown:** a scripted, tested teardown of all nonessential extension resources, runnable in one command and triggered manually on a 90% alert.
4. **Capacity restrictions:** record the existing subscription, provider and region service quotas (Azure quotas are subscription-scoped and often further divided by provider and region; a resource group is not a quota boundary); apply resource-group-scoped Azure Policy deny rules for allowed resource types, regions and SKUs; set explicit maximum replicas, throughput and capacity in IaC; and test that an oversized deployment is rejected.
5. **Daily reconciliation:** observed spend reconciled daily against forecast in the effort/cost log; unexplained variance is investigated the same day.
6. **Latency disclosure:** the runbook and readiness assessment state explicitly that billing latency prevents a universal absolute cap and that the controls above bound, detect and respond to spend rather than guarantee a ceiling.

Cloud cost appears in the existing attribution model as a visible **infrastructure** cost class, never mixed into measured per-claim model/tool cost. This package is itself FinOps-for-Agents evidence.

### Integration claims discipline

Permitted after `v1.1-integration-controls`:

- "Integrates with a real enterprise identity provider using per-workload identities, with issuance revocation and a declared active-token containment window — covering protected reads as well as consequential calls — proven by fail-closed tests."
- "Demonstrates legacy batch, managed-database, third-party API and asynchronous integration patterns with reconciliation, drift detection and safe degradation, on synthetic data."

Permitted only after **both** releases (`v1.2-cloud-operation`):

- "Demonstrates six enterprise integration patterns against a real identity provider, managed cloud services and an independent third-party API, using synthetic data."
- "Deploys to a cloud staging environment from infrastructure-as-code with provenance-verified promotion and an exercised rollback."
- The sixth proposition, asserted through the canonical table.

Prohibited (entered in the claims register as prohibited language):

- Any claim of production operation, commercial scale, real-data processing or availability guarantees.
- "Enterprise-proven" or any phrase implying operation inside a real client estate.
- "Integrates with the identity, data and legacy systems the enterprise already runs" as a repository or article claim. That sentence is service positioning for client delivery and may appear only in outreach/proposal material clearly framed as the service offered, never as a description of what AEGIS demonstrates.
- Any absolute cloud-spend guarantee; spend controls bound, detect and respond, they do not cap.
- Describing the third-party or batch integrations as consequential-action paths; they are advisory inputs under the unchanged human-decision boundary.
- Asserting the sixth proposition, in any channel, before both integration releases have shipped.
- Presenting integration evidence that received only the Day 28a self-review fallback without that label attached; where no independent review was completed, the limitation is disclosed beside the integration claim in every location it appears.

---

## Technology choices

| Concern | Core choice | Reason |
|---|---|---|
| Agent workflow | Python, typed LangGraph state | Familiar to buyers and inspectable in tests |
| Tool protocol | Official MCP Python SDK, pinned to the protocol revision and SDK version fixed in `docs/adr/002-mcp-protocol-contract.md` | Makes protocol security and capability boundaries visible, and prevents the project demonstrating a superseded MCP deployment model |
| Models | Claude plus one alternate | Supports a concrete migration regression exercise |
| Deterministic tests | pytest | Control enforcement must not depend on probabilistic judges |
| Behavioral evaluation | DeepEval plus versioned Python fixtures | Supports repeatable scoring while keeping raw cases inspectable |
| System red team | PyRIT plus custom indirect-injection corpus | Exercises end-to-end attacks and tool misuse |
| Observability | OpenTelemetry plus self-hosted Langfuse | Links traces, evaluation, latency and cost |
| Analytics | DuckDB, dbt and Power BI | Demonstrates data engineering, SQL and executive reporting |
| Packaging | Locked dependencies, Docker Compose, OCI image CI, SBOM and provenance | Establishes a reproducible release artifact rather than a laptop-only demo |
| Identity (Days 22–28) | Entra ID workload identities plus Key Vault | Real-IdP integration with secretless CI and managed signer custody |
| Legacy interface (Days 22–28) | Object-storage CSV drop under a written file contract | Exercises reconciliation, drift detection and quarantine against a file-based system |
| System of record (Days 22–28) | Managed Postgres | Row-level scoping and versioned migrations on a real engine |
| Async intake (Days 22–28) | Managed queue (Service Bus or Storage Queue) | Idempotency, dead-letter and replay patterns without operating a broker |
| Third party (Days 22–28) | One genuinely external enrichment API | Rate limits, outages and versioning outside the project's control |
| Infrastructure (Days 22–28) | Bicep or Terraform with CI promotion | Reproducible cloud staging, provenance-verified deploys and exercised rollback |

Tool breadth is not a success metric. Garak and promptfoo remain stretch integrations unless they find distinct failures the core harness misses.

---

## Quantitative acceptance gates

Thresholds are versioned in `controls/release-policy.yaml`. Day 4 establishes the pilot baseline; Day 7 freezes the candidate thresholds before remediation results are known.

| Gate | Minimum release condition |
|---|---|
| Boundary enforcement | 0 unauthorized consequential tool executions; 0 human-approval bypasses across the full deterministic and adversarial suite |
| High-risk escalation | 100% recall on holdout cases marked mandatory-escalation; denominator and confidence interval reported; deterministic boundary tests remain zero-tolerance |
| Behavioral quality | Normal holdout target ≥100; permitted floor 60. Require both ≥90% observed task success and a lower 95% Wilson bound ≥80%. The harness precomputes and publishes the minimum integer successes before results are revealed: at `n=60`, `55/60` passes while `54/60` fails; at `n=100`, `90/100` passes. Each primary claim-type and value-band slice has at least 20 cases and at least 80% observed success with its interval reported; all secondary slice results and denominators are diagnostic. |
| Grounding | At least 95% policy citations resolve to the retrieved source passage; no fabricated policy identifier in the holdout set |
| Security | 0 open critical/high findings in the release threat model; attack success rate reported before and after control changes |
| Kill and recovery | Global stop prevents the next tool execution; credentials revoke successfully; last known good release can be restored using the runbook |
| Audit | 100% of consequential decisions have complete correlation fields; the signed external head verifies; mutation, reordering, middle deletion, tail deletion and full-chain replacement tests fail verification |
| Cost | 100% of captured variable model/tool cost events map to a claim and stage; missing telemetry remains visible as unattributed and blocks sign-off; release stays within the approved quality-adjusted cost envelope |
| Reliability | No silent failure paths in critical flows; defined timeout/retry/human-handoff behavior passes integration tests |
| Reproducibility | Clean checkout can run tests, build the container and generate the evidence index from documented commands |

The exact quality and cost envelope may change after baseline measurement, but changes require a dated decision record. A team may not lower a safety threshold solely to make the demo pass.

### Integration acceptance gates (Days 22–28)

Thresholds are versioned in `controls/release-policy.yaml` under an `integration:` section, frozen at Day 22 exit. A gate may not be weakened to make a release ship.

**Gate-to-release mapping:**

- **`v1.1-integration-controls`:** gates 1–4; gate 6 in the locally integrated environment; and the pre-staging portion of gate 8 — eligibility record, tiered alerts, tested teardown, capacity restrictions and daily reconciliation for the paid managed resources created on Days 23–25 (Key Vault, Postgres, storage, queue). Paid resources exist from Day 23, so spend control is not deferrable to v1.2.
- **`v1.2-cloud-operation`:** gate 5; gate 6 in staging; gates 7 and 8 in full; **plus a staging contract/smoke rerun of gates 1–4**. The Day 27 drill exercises three seams and does not substitute for this rerun.

**Staging rerun scope and escalation:** the rerun is contract- and smoke-level — one representative case per gate condition (an identity negative case, a reconciliation control-total check, a third-party degradation path, a queue redelivery and DLQ route) — confirming the controls hold under staging's managed identity bindings, networking and service configuration. Any environment-specific variance triggers the corresponding full failure suite for that gate before v1.2 may tag.

| # | Gate | Minimum release condition |
|---|---|---|
| 1 | Identity | 0 long-lived stored secrets in code, CI or IaC; issuance revocation proven; active-token containment within the declared published window on **every authenticated request, protected reads included** (declared cache TTL tested at its expiry boundary); expired/wrong-audience/wrong-scope fail closed against the real IdP; signer-key custody exclusion proven |
| 2 | Reconciliation | 100% of ingested batch rows reconcile to control totals; all five seeded batch failures detected and quarantined; 0 partial loads |
| 3 | Third party | Forced outage produces degraded-but-safe triage; 0 consequential actions depend on the third-party response; 0 fabricated enrichment values |
| 4 | Async | Effectively-once business effect under tested at-least-once redelivery (duplicate delivery → exactly one workflow effect); poison message → DLQ + alert; crash before commit → no workflow state and no audit event; crash after commit but before settlement → redelivery deduplicates, no second start; no message settled before its transaction commits; stop → 0 consequential calls with messages preserved |
| 5 | Deployment | Clean-state IaC provision, CI-promoted deploy with digest-provenance match, exercised rollback and one teardown/rebuild all evidenced |
| 6 | Control preservation | Sealed behavioral, adversarial and audit-verification suites pass in the integrated environment (locally for v1.1, staging for v1.2); every difference classified under the variance taxonomy; **0 open control regressions**; implementation variances dispositioned with dated records |
| 7 | Conversion | Both offer rows complete in the required format; assessment issued using the defined instrument; README entry-point text in place; article 4 published and link-checked; six-row propositions validation passes; the Day 28a integration challenge is complete with accurate provenance, or the self-review fallback label appears everywhere an integration claim does |
| 8 | Spend | Spend-control package fully configured and evidenced (eligibility record, tiered alerts, tested teardown, capacity restrictions, daily reconciliation); no unexplained daily variance open at tag time; latency limitation disclosed in runbook and assessment. The pre-staging portion applies from Day 23, when the first paid resources are created |

---

## Daily delivery standard

Every milestone ends with:

1. A small, tagged commit (`day-01` through `day-28`; split milestones tag each half separately as `day-07a`, `day-07b` and so on, giving 38 tags).
2. Tests for the new happy path, boundary and failure path.
3. An update to the competence ledger and threat/control traceability.
4. A reproducible command and captured result under `artifacts/day-XX/`.
5. A short engineering log: decision, evidence, limitation and next risk.
6. An update to `docs/evidence/effort-log.csv`; at 75/100-hour crossings, the required forecast or re-plan record.
7. When a buyer-relevant result changes, update the relevant delivery/advisory guide link and `docs/service-to-artifact-matrix.md`; do not copy the result into a second evidence source.
8. If a named weakness activates or completes development work, update `docs/development-register.md`, log the time and record whether the validation and stop rule passed. No update is required when no resource is active.

No secrets, even fake reusable secrets, are committed to Git history. An insecure “as-found” pilot is represented by a clearly isolated test fixture and assessment snapshot, not by deliberately leaking credentials.

---

## Week 1 — Turn an unsafe pilot into a governed candidate

### Day 0 `[S]` — Environment and access preflight

A gate, not a milestone: it produces no evidence and carries no track deliverable, but Days 22–28 cannot start without it and its failures have **procurement lead time measured in weeks, not hours**. The whole-programme elapsed-time guidance assumes tenant and subscription access already exist; this is where that assumption is tested, while there is still time to resolve it in parallel with Days 1–21.

Confirm and record, in `docs/evidence/preflight.md`: Python runtime compatibility for the pinned toolchain; working API access and billing for the baseline model **and** the alternate migration model; an Azure subscription with a usable region, its offer type and whether it supports a hard spending limit; **Entra administration rights sufficient to create app registrations and configure workload identity federation**; GitHub OIDC capability for the target repository and its visibility setting (which determines the transparency-log trust model on Day 7b); and an expected cloud-cost estimate for the integration releases.

**Done when:** every item is confirmed with the date checked and the account or tenant it was confirmed against; any item that is blocked has a named owner, a request raised, and an expected resolution date recorded. A blocked Entra or subscription item does not stop Day 1, but it becomes a tracked dependency on Day 22 entry, and Day 22 may not begin while it is open.

### Day 1 `[S]` — Define the buyer problem and pilot baseline

Create a one-page engagement brief: business objective, intended users, affected parties, prohibited outcomes, decision rights and measurable success. Build a deliberately limited pilot assessment showing the normal gaps: no formal release gate, broad tool identity, incomplete audit, no cost attribution and ad hoc evaluation. Create the competence ledger and an assumptions/claims register. Create empty, linked skeletons for the README, `docs/delivery-evidence-guide.md`, `docs/advisory-evidence-guide.md`, reviewer guide, `docs/service-to-artifact-matrix.md`, service one-pager and readiness assessment, and begin outreach to two prospective practitioner reviewers. Adopt `docs/development-register.md` with no active resource: attempt the engagement and advisory artifacts first. Only if that attempt exposes a material discovery, scope or executive-framing weakness may the timeboxed consulting-craft candidate be activated and the artifacts revised.

**Deliverables:** `docs/engagement-brief.md`, `assessment/pilot-baseline.md`, `docs/evidence/competence-ledger.md`, `docs/evidence/effort-log.csv`, `docs/claims-register.md`, `docs/development-register.md`, README with both entry-point headings, `docs/delivery-evidence-guide.md`, `docs/advisory-evidence-guide.md`, `docs/service-to-artifact-matrix.md` skeleton, remaining launch-artifact skeletons and reviewer outreach log.

**Done when:** every positioning phrase maps to at least one planned control and proof artifact; unsupported production or compliance claims are listed as prohibited language; both README entry points resolve to their guide skeletons and the guides declare their distinct audience and evidence contract; the development register starts with no active resource or contains a dated four-gate activation decision with a timebox, validation and stop rule.

### Day 2 `[S]` — Threat model, data model and architecture decision record

Create the synthetic data generator for 50 base claims and parameterized scenario variants. Classify fields, define retention/redaction rules and mark all uploaded documents as untrusted. Write a STRIDE-style threat model covering indirect prompt injection, confused-deputy behavior, excessive agency, data exfiltration, over-privileged NHI, MCP supply chain, audit tampering and denial of wallet. Cross-walk the threat rows against a current published agentic threat taxonomy — the OWASP agentic-applications list is the intended reference — covering at minimum goal hijacking, unexpected code execution and memory/context poisoning; cite the taxonomy's exact title, version and date, and record any of its categories judged out of scope with a reason. Record why consequential decisions remain human-owned.

**MCP protocol contract.** Selecting the official SDK is not a protocol decision. Before Day 3, record `docs/adr/002-mcp-protocol-contract.md` fixing: the supported MCP protocol revision and the exact Python SDK version; whether the implementation targets that revision exclusively or also supports a stated earlier one; stateless request handling and horizontal-routing assumptions; required protocol and routing header validation for the chosen transport; issuer, audience/resource and scope validation; a prohibition on passing an upstream token through to another MCP server or third party; bounded JSON Schema depth and safe handling of external `$ref` values; expected behavior for missing, unknown and deprecated protocol versions; and which MCP authorization requirements apply to the Entra workload-to-workload design versus which are user-delegation requirements that do not. **Read the current specification and SDK changelog and write the ADR from what is actually there** — the repository rule forbids recording a revision identifier or breaking-change list the project has not verified. The revision recorded here becomes part of the release evidence and the tampered-config CI check.

**Deliverables:** `data/generator/`, `docs/adr/001-controlled-agent-boundary.md`, `docs/adr/002-mcp-protocol-contract.md`, `docs/threat-model.md` with the agentic-taxonomy crosswalk, `docs/data-governance.md`.

**Done when:** each high-risk threat has a planned prevention/detection/recovery control and named future test; every crosswalk row cites a dated taxonomy version and either a planned test or a scoped-out reason; the MCP ADR names a verified protocol revision and SDK version with its compatibility window; generated data contains no real person or policy content.

### Day 3 `[D]` — Build capability-scoped MCP services

Build three MCP domains: read-only policy retrieval, scoped claims-record access and a mock-payment service. Publish a machine-readable capability manifest for each server, including owner, allowed operations, data class, required identity, approval requirement, timeout, egress and decommission method. Parameterize all database access and validate inputs at the tool boundary.

Implement the protocol contract fixed in `docs/adr/002-mcp-protocol-contract.md` and turn each of its clauses into a test: protocol and routing header validation, stateless request handling, issuer/audience/resource/scope validation, refusal to pass an upstream token through to another server or third party, JSON Schema depth bounds and external `$ref` rejection, and the declared behavior for missing, unknown and deprecated protocol versions.

**Deliverables:** `mcp/`, `controls/capabilities/`, `docs/mcp-trust-boundaries.md`, `tests/protocol/` contract suite.

**Done when:** negative tests prove that unknown tools, invalid arguments, cross-claim access and direct payment attempts are rejected without calling the model; every clause of the MCP protocol ADR has a passing contract test; a request carrying a missing, unknown or deprecated protocol version is handled exactly as the ADR declares.

### Day 4 `[D]` — Build and measure the pilot workflow

Implement the LangGraph workflow: intake, validation, policy retrieval, coverage analysis, deterministic fraud indicators, recommendation and human queue. Run it on a development set and capture quality, latency, cost, escalation and failure data. This becomes the honest “before” state.

**Deliverables:** `src/aegis/`, `tests/integration/`, `artifacts/baseline/scorecard.json`, pilot trace bundle.

**Done when:** the end-to-end happy path and at least five failure paths run reproducibly; limitations are visible rather than silently patched.

### Day 5 `[D]` — Enforce objectives and boundaries as code

Create `controls/agent-policy.yaml` for allowed actions, prohibited actions, confidence thresholds, value bands, approval rules and per-run cost limits. Implement a deterministic policy decision point plus enforcement at every MCP server. The agent may autonomously request missing information and route a claim; payment, denial and settlement remain authenticated human actions.

**Deliverables:** versioned policy, enforcement service/module, `docs/boundary-design.md`, policy test matrix.

**Done when:** prompt text cannot change authorization; all allow, deny and escalation branches have deterministic tests; policy decisions appear in the audit event.

### Day 6 `[D]` — Implement NHI and MCP security controls

Use separate workload identities per MCP domain with minimum scopes, short lifetimes and explicit owners. Implement token expiry/revocation tests, secret scanning, egress allowlists and an NHI lifecycle register. Pin dependencies and generate an MCP/server software bill of materials. Document a realistic production mapping to Entra workload identity or the client’s identity provider without building a custom IdP.

**Deliverables:** `security/nhi-register.yaml`, `security/access-matrix.md`, SBOM, before/after privilege diff.

**Done when:** expired, wrong-audience, wrong-scope and revoked credentials all fail closed; the identity register covers provision, rotate, monitor and decommission.

### Days 7a–7b `[B]` — Add traceability and freeze the release contract

Instrument model, retrieval, authorization and tool calls with OTel/Langfuse. Pin the OpenTelemetry GenAI semantic-convention schema version behind a thin adapter rather than emitting against whatever version the SDK happens to default to — those conventions are still evolving — and record the pinned version in the release evidence so a convention change surfaces as a dated decision rather than silent trace drift. Test that traces and telemetry redact secrets, credentials and raw tool arguments: the audit ledger stores an arguments hash, and no span attribute, log line or Langfuse payload may carry the underlying values. Add sequence-numbered hash-chain events, a separate audit-signer identity, signed checkpoints, a local anchor adapter and verification tests. The agent and ordinary ledger writer must not have the signing key. Freeze `controls/release-policy.yaml`, including quality, security, cost and reliability gates, before Week 2 remediation begins. Confirm the two practitioners approached on Day 1 and assign different evidence chains. They may review the evaluation protocol, rubric and sampling code on Day 8, but they may not see sealed cases or results before the model, prompt and policy versions are frozen. Document an adversarial self-review fallback, explicitly labelled non-independent. Record engineer-facing video 1; article 1 may exit as an edited draft if the audit core overruns.

**Day-exit deliverables:** trace pipeline, `audit/`, signer and local-anchor adapters, verifier tests, frozen release policy, `docs/evidence/audit-field-map.md`, reviewer scopes/commitments or documented non-independent fallback, video 1 and article 1 draft, `v0.1-controlled-boundaries`.

**Day-exit minimum:** a claim is traceable from input to decision, identity, tool, cost and human approval; the semantic-convention version is pinned and recorded, and redaction tests prove no secret or raw tool argument reaches a trace; mutation, reordering, middle deletion, tail deletion and full-chain replacement all fail against a signed head verified through the local anchor adapter; the release policy is frozen.

**v1.0 done when:** the signed release checkpoint is persisted and verified through an external CI-attestation or transparency-log-backed anchor stored separately from the audit ledger.

---

## Week 2 — Test behavior, attack the system and gate releases

### Days 8a–8b `[D]` — Design a defensible evaluation protocol

Create versioned development, calibration and sealed holdout sets. Target at least 100 sealed holdout cases; 60 is the disclosed descope floor. Define human-written rubrics for task success, grounding, escalation, claimant communication and policy compliance. Label at least 30 representative cases manually, blind to model output, and use them to calibrate any LLM judge. Thirty is a **calibration floor** — enough to detect gross judge miscalibration on the primary rubrics, not enough to establish judge reliability broadly — and every published agreement figure carries that limitation beside its denominator. Predeclare claim type and value band as primary release slices, with at least 20 holdout cases in each reported primary slice; ambiguity and document quality remain secondary diagnostic slices unless adequately powered. Hash the sealed holdout manifest and restrict access so reviewers can inspect the protocol, rubric and sampling code but not exact cases or results before the model, prompt and policy versions are frozen. Before revealing results, compute and persist the minimum integer successes satisfying both the point estimate and Wilson lower-bound requirements for the actual holdout size. Draft the method rationale and hand-check the threshold before consulting additional learning material. If a method choice, calculation or reviewer challenge cannot be defended, activate only the timeboxed statistics candidate in `docs/development-register.md`, revise the protocol and stop as soon as the fixture and explanation validate. Record limitations; do not claim demographic fairness from synthetic operational data.

**Deliverables:** `evals/datasets/`, `evals/rubrics/`, `docs/evaluation-protocol.md`, hand-checked statistical fixtures, judge-calibration report and a pre-result gate manifest containing the holdout size, point threshold, Wilson threshold and minimum passing success count; development-register decision/outcome only if the statistics candidate activated.

**Done when:** development cases cannot leak into the holdout; holdout custody and manifest verification are documented; judge agreement and disagreement examples are published; primary-slice denominators meet the predeclared minimum; the gate manifest shows `55/60` as the minimum at the descope floor or the correctly computed count for a larger set; deterministic controls are never scored only by an LLM judge.

### Day 9 `[D]` — Build the behavioral EvalOps harness

Implement deterministic assertions plus DeepEval behavioral metrics. Run repeated trials for non-deterministic cases and report denominators, Wilson confidence intervals, model/prompt/policy version and slice results. The release result must evaluate both the 90% point threshold and the 80% lower-bound threshold using the pre-result gate manifest; primary slices have predeclared floors and secondary slices are visibly diagnostic. The machine-readable scorecard includes `holdout_size`, `observed_successes`, `minimum_successes_required`, `point_threshold` and `wilson_lower_threshold`. Add empty, malformed, contradictory, large and timeout cases.

**Deliverables:** `evals/`, baseline evaluation result, machine-readable scorecard and human-readable summary.

**Done when:** one command recreates the scorecard; failures link back to trace IDs; no aggregate score can conceal a failed mandatory-escalation slice.

### Day 10 `[D]` — Establish the adversarial baseline

Use PyRIT and a custom corpus of at least 20 indirect injections embedded in claim documents and tool results. Cover exfiltration, approval bypass, cross-claim access, policy override, fabricated evidence, tool enumeration and denial of wallet. Measure attempted compromise, blocked compromise and actual unauthorized action separately. Preserve raw evidence and do not remediate until the baseline is captured.

**Deliverables:** `redteam/`, threat-to-test map, raw findings, baseline attack report.

**Done when:** each attack has a success definition and trace; the report distinguishes model misbehavior from an authorization failure.

### Day 11 `[D]` — Contain, remediate and re-test

Apply layered controls: untrusted-content separation, minimal context, schema validation, output encoding, least privilege, egress restriction, policy enforcement and human approval. Prompt hardening is defense in depth, not the authorization boundary. Re-run the unchanged attack suite and publish before/after results plus residual risk.

**Deliverables:** remediation changes, `redteam/before-after-results.md`, residual-risk register.

**Done when:** consequential unauthorized tool execution is zero; any remaining prompt manipulation is visibly contained and cannot become authority.

### Day 12 `[D]` — Add kill, circuit-breaker and safe-degradation controls

Implement global pause, per-agent credential revocation, tool-level circuit breakers, request admission control and budget alerts. A budget breach must stop new low-priority work and hand active claims to a human queue; it must not silently abandon an in-flight high-impact workflow. Test halt, drain, resume and stale-worker behavior.

**Deliverables:** runtime controls, `docs/runbooks/kill-and-recovery.md`, scripted rogue-agent scenario and video evidence.

**Done when:** the next consequential tool call is blocked after a stop; revoked workers cannot resume with cached credentials; operators receive a clear state and recovery action.

### Days 13a–13b `[D]` — Build the release-gate core

GitHub Actions runs four lanes: deterministic/security tests on every PR, a fast behavioral canary, container/SBOM/vulnerability checks, and a request-level token/cost budget derived from Day 4 telemetry. Nightly runs execute the full behavioral and adversarial suites. Generate a single release evidence bundle with code, model, prompt, policy, dataset and dependency versions. Wire the signed audit release head into build provenance so the ledger checkpoint and release versions form one externally persisted, independently verifiable release record. Build the OCI image and attach provenance against a **named predicate and target level**, with a declared trusted-builder and signer policy and an explicit verification rule stating what a verifier checks and what causes rejection; record the predicate version in the release evidence. Confirm the current provenance specification version before pinning it rather than assuming one. Publishing to a registry is stretch. Days 15–17 replace the provisional request budget with reconciled, quality-adjusted workflow cost gates.

**Day-exit deliverables:** PR workflows for deterministic/security tests and the behavioral canary, release-evidence generator, and sample failed/passed authorization and behavioral change records.

**v1.0 recovery deliverables:** external audit-anchor wiring, container build, SBOM, provenance, vulnerable-dependency regression, reconciled cost lane and seeded cost-regression record. Items completed on Day 13 need no recovery; deferred items retain the receiving milestones declared in the descope ladder.

**Day-exit minimum:** authorization-bypass and behavioral-regression changes are independently blocked on pull requests. Any deferred lane is recorded with its receiving milestone and corresponding blocked v1.0 claim.

**v1.0 done when:** the externally stored signed audit head verifies; seeded bad changes separately demonstrate blocking for authorization bypass, behavioral regression, vulnerable dependency and cost regression; container, SBOM and provenance evidence is generated; no gate is merely documented.

### Day 14 `[B]` — Prove model-migration control and issue the draft security audit

Swap to the alternate model without retuning thresholds. Run the sealed evaluation and compare quality, security, latency, cost and slice behavior with uncertainty shown. Make a ship/hold recommendation. Then issue the Agent Security, MCP Access, Kill-Switch and NHI Audit as a dated draft: scope, method, as-found state, evidence, remediation, residual risk and exclusions, with the Day 18 incident exercise referenced as scheduled validation of the containment and recovery findings. Final issuance happens on Day 19, after the exercise supplies the strongest detection, containment and recovery evidence — the audit should cite a measured drill, not a documented intention. Record engineer-facing video 2 and draft article 2 on adversarial evaluation and safe model migration.

**Deliverables:** `docs/reports/model-migration-regression.md`, `docs/reports/agent-security-audit-draft.md`, video 2, `v0.2-security-eval-candidate`.

**Done when:** the migration decision follows predeclared thresholds; the audit’s every finding links to evidence and does not imply certification or legal sign-off.

---

## Week 3 — Control cost and demonstrate operation after release

### Day 15 `[D]` — Build end-to-end cost attribution

Extract token, model, tool and latency telemetry into DuckDB. Build dbt models that reconcile captured provider/model usage events to claim, workflow stage, retry, model and MCP tool. Organize the attribution logic as `packages/agent_cost_attribution/`: a clearly named, independently testable, extraction-ready internal package with a narrow input/output contract, its own README and a synthetic worked example, while retaining the AEGIS dependency lock, version and release pipeline. Standalone installation, semantic versioning and distribution are post-v1.0 work triggered by demonstrated demand. Track unattributed events as errors rather than dropping them. Version the price table and separate measured usage from assumed currency conversion, infrastructure or human-cost inputs. The FinOps credential candidate remains post-v1.0 and does not block Days 15–17; use the pinned FOCUS and FinOps references needed for the artifact, then return to building.

**Deliverables:** `packages/agent_cost_attribution/`, internal-package contract tests and README, `finops/`, dbt tests, reconciliation report and attribution schema.

**Day-exit minimum:** captured happy-path and retry cost events for both claim types reconcile within a declared tolerance; any missing failure, cache or telemetry-loss treatment is visible in the deferred-work register and keeps cost sign-off blocked.

**v1.0 done when:** 100% of captured variable model/tool cost events map to a claim and stage; fan-out, retries, failed calls and cache hits receive explicit treatment; telemetry loss creates an unattributed bucket and blocks sign-off rather than disappearing.

### Day 16 `[B]` — Measure quality-adjusted unit economics

Calculate cost per attempted claim, successfully triaged claim and correctly triaged claim. Show latency, escalation and quality beside price so a cheap but unsafe model cannot appear optimal. Create a transparent human-handler comparator with editable assumptions and sensitivity ranges, not a fabricated ROI claim.

**Deliverables:** semantic metrics layer, unit-economics notebook/report, Power BI model and static export.

**Done when:** every dashboard number traces to a dbt model; changing the human-cost or model-price assumption updates the result; limitations are displayed on the dashboard.

### Day 17 `[D]` — Close the cost-control loop safely

Implement per-run and daily budgets, anomaly detection, model/tool fan-out limits and admission throttling. Couple every cost policy to a minimum quality and safety floor. Test spikes, price-table changes, retry storms and telemetry loss. Complete any Day 15 deferred treatment for failed calls and cache hits. Replace Day 13’s provisional cost gate with the reconciled workflow metrics and seeded cost-regression failure. Write the FinOps-for-Agents operating runbook and complete article 3 from its running outline.

**Deliverables:** cost policies and tests, `docs/runbooks/agent-cost-operations.md`, cost-control before/after report.

**Done when:** cost controls contain a simulated denial-of-wallet attack without bypassing approval, losing audit data or silently reducing the mandatory escalation rate.

### Day 18 `[B]` — Establish SLOs and run an incident exercise

Define SLIs/SLOs for task success, mandatory escalation, unauthorized action, p95 latency, audit completeness, cost attribution and recovery. Create alerts and an owner/RACI table. Run a scripted incident: indirect injection causes suspicious behavior, monitoring detects it, the operator stops and revokes the agent, evidence is preserved, the last known good release is restored, and the sealed suite verifies recovery. Record timestamps and gaps in a blameless post-incident report.

**Deliverables:** `operations/slos.yaml`, alerts, RACI, incident timeline, post-incident report and recovery evidence.

**Done when:** mean time to detect, contain and recover are measured; no step relies on undocumented operator memory; the incident creates follow-up actions.

### Days 19a–19b `[A]` — Produce the governance and production-readiness packs

Create one evidence-led control matrix rather than five repetitive documents. Cross-reference NIST AI RMF, ISO/IEC 42001-style controls and applicable EU/UK technical obligations with scope and date caveats. Draft the mapping first. If it cannot explain the system boundary, control objective, owner, evidence, residual gap and review cadence—or an advisor finds checklist-style reasoning—activate only the timeboxed governance-primer candidate in `docs/development-register.md`, revise the mapping and stop when the review passes. Add model/system cards, change-management record, data sheet and incident process. Include the dated, counsel-reviewable AI Act classification determination defined by `aegis-resource-guide.md`: system boundary and intended purpose; provider/deployer role; Article 6(1), Annex III and any Article 6(3) reasoning; an independent Article 50 assessment; other applicable regimes; legal-review status; and reclassification triggers. Apply the Production-Readiness Assessment to the original pilot and the final candidate, then produce a prioritized 90-day client roadmap. Issue the final security audit: incorporate the Day 18 incident-exercise evidence (measured detection, containment and recovery times) into the containment and recovery findings the Day 14 draft flagged as scheduled validation, and record any variance between drafted expectation and exercised result.

**Deliverables:** `governance/control-evidence-matrix.md`, `governance/ai-act-classification-determination.md`, system card, data sheet, `assessment/final-readiness.md`, `assessment/90-day-roadmap.md`, `docs/reports/agent-security-audit.md` (final issuance); development-register decision/outcome only if the governance candidate activated.

**Done when:** every “implemented” control links to executable evidence, every partial control has an owner and action, no regulatory status is asserted without qualification, the AI Act determination separates Annex III and Article 50 reasoning and records change triggers, and any activated learning has passed its validation and stopped.

### Day 20 `[A]` — Package the repository as buyer-verifiable evidence

Recover any Day 13 deferred external audit-anchor wiring, container, SBOM, provenance and vulnerable-dependency regression work first; if the externally anchored release head or any other mandatory provenance evidence remains incomplete, v1.0 does not ship. Finalize the README around the buyer journey: pilot gap, architecture, attacks found, controls, release decision, operation and economics. Put four proof points above the fold, followed immediately by the exact “Hiring an engineer?” and “Assessing a consulting engagement?” entry points. Finalize `docs/delivery-evidence-guide.md` and `docs/advisory-evidence-guide.md` from the same competence ledger and release manifest. Complete the one-command reviewer path and `docs/service-to-artifact-matrix.md`, use the static dashboard views exported since Day 16, and record executive-facing video 3 from the Day 18 storyboard.

**Deliverables:** polished two-entry-point README, `docs/delivery-evidence-guide.md`, `docs/advisory-evidence-guide.md`, completed `docs/service-to-artifact-matrix.md`, `docs/reviewer-guide.md`, static dashboard exports, executive video and service one-pager.

**Done when:** a clean engineering reviewer can navigate from the delivery guide to code, commands, seeded failures and generated results; an executive buyer can navigate from the advisory guide to findings, service scope and roadmap without reading code; CI confirms that all README, guide, matrix and evidence links resolve; links contain no private tokens, local-only paths or unsupported claims.

### Day 21 `[B]` — External challenge if available, launch and conversion

Collect the reviews from the two practitioners recruited on Day 7, each covering a different evidence chain. Record each reviewer’s role, scope, date, consent to attribution and conflicts of interest. If either reviewer dropped out, run the documented adversarial self-review fallback for that evidence chain, but label the result “adversarial self-review — no independent review completed” everywhere it appears. Resolve or disclose findings. Edit and publish the three articles developed across Days 7, 14 and 17: boundary-first security, behavioral/model-migration evaluation and quality-adjusted AgentOps cost. Tag `v1.0-aegis` only if every mandatory release gate is clear, publish the repository and videos, and contact ten relevant UK insurance/financial-services prospects with the readiness assessment as the entry offer. Do not start a value-pricing course or FinOps credential to prepare for generic outreach. After v1.0, activate consulting-pricing or credential development only when a qualified proposal, repeated role requirement, recruiter screen or prospect objection supplies the market evidence required by `docs/development-register.md`.

**Deliverables:** review findings, provenance and dispositions; accurate external-review or self-review label; three articles; conditional `v1.0-aegis`; outreach tracker; post-v1.0 development candidates remain inactive unless the tracker records their activation evidence.

**Done when:** critical findings are fixed; accepted residual risks are explicit; every mandatory release gate is clear; review provenance is accurate; the public materials use the aligned positioning consistently.

---

## Week 4 — Integrate with the enterprise estate (Days 22–25)

Week 4 begins only after `v1.0-aegis` is tagged. "Week" remains a build phase, not a calendar week. These milestones ship as `v1.1-integration-controls`.

### Day 22 `[S]` — Integration landscape, ADR, canonical wiring and threat-model delta

Confirm the concrete Azure services, region, subscription spending-limit eligibility, capacity restrictions and the re-estimated effort budget in `docs/adr/003-enterprise-integration-architecture.md`; the ADR records the AWS/GCP equivalents as future ports rather than reopening the platform choice. Re-confirm that the MCP protocol revision pinned on Day 2 is still current, and record any revision change as a dated decision with its compatibility impact. Extend the threat model with the new trust boundaries: compromised batch file, poisoned third-party response, queue replay, cloud-credential theft, IaC-state tampering and staging-environment drift. Each new threat gets a planned prevention/detection/recovery control and a named future test. Extend the capability manifests: the third-party API and batch feed are registered as tool domains with owner, data class, egress destination and decommission method, even though they are advisory-only. Configure the cloud-spend control package (tiered alerts, recorded quotas and Azure Policy deny rules, teardown script skeleton, reconciliation log) before any Day 23 resource is created. Add the blocked sixth proposition row to the repository README, add the corresponding competence-ledger chains, and wire the six-row CI validation. Add the Agent Integration Engineer role and fifth-chain skeleton to the delivery guide and service-to-artifact matrix, both marked in-progress until `v1.2-cloud-operation` ships.

**Deliverables:** `docs/adr/003-enterprise-integration-architecture.md`, threat-model delta, extended capability manifests, `controls/cloud-budget.yaml`, README propositions row (blocked), competence-ledger chains, six-row CI check, updated guide/matrix skeletons.

**Entry condition:** every Day 0 preflight item is closed. An open Entra-administration, subscription, or model-access item blocks Day 22 entry regardless of `v1.0-aegis` status, because the remaining integration milestones all depend on it.

**Done when:** every new trust boundary has a threat row with a planned test; the spend-control package is active and evidenced; the six-row validation passes with the sixth row shown as blocked; no landscape component requires real personal data to function.

### Days 23a–23b `[D]` — Real identity plane

Replace locally issued MCP workload tokens with Entra ID app registrations: one per MCP domain, minimum scopes, documented owner and lifecycle. Move the audit-signer key into Key Vault with access policies that exclude the agent and ordinary ledger writer, preserving the signer-separation invariant under a real custodian. Configure workload identity federation so GitHub Actions obtains short-lived cloud credentials via OIDC with no stored secrets.

Revocation is tested as **two distinct properties**, because continuous access evaluation does not cover a custom API that validates issued JWTs locally, and workload identity federation by itself gives no revocation awareness to the MCP servers:

1. **Issuance revocation:** disabling the service principal prevents acquisition of any new token, proven against the real IdP.
2. **Active-token containment:** an already-issued token is rejected on **every authenticated MCP request** — protected reads included, not only consequential calls — within a **declared maximum containment window**, achieved by a named mechanism: short token lifetime, a resource-side denylist consulted by the MCP servers on each authenticated request, or another mechanism recorded in the ADR. A revoked identity must not continue reading policy terms or claims records until token expiry. If identity state is cached for performance, the cache TTL is declared as part of the containment window and tested at its expiry boundary. The window is published in the NHI register and the readiness assessment. If the achievable window is longer than the v1.0 local implementation's, that difference is classified under the variance taxonomy: a documented implementation variance if the containment objective still holds, a control regression (release blocker) if it does not.

Re-run the remaining Day 6 negative identity suite (expired, wrong-audience, wrong-scope) against the real IdP. Update the NHI register: each identity's provision/rotate/monitor/decommission entry names the real tenant object, and the register gains a variance column recording every difference the managed service imposes, with its taxonomy class.

**Deliverables:** Entra configuration as code (or scripted, exported and versioned), Key Vault signer integration, federated CI credential flow, issuance-revocation and active-token-containment test evidence with the declared window, re-executed negative identity tests, updated `security/nhi-register.yaml` with classified variance column.

**Done when:** no MCP identity or CI job uses a long-lived stored secret; issuance revocation and active-token containment both pass with captured evidence and a published window; expired, wrong-audience and wrong-scope tokens fail closed against the real IdP; signer-key custody exclusion is proven by a denied-access test; every variance is classified and no control regression is open.

### Days 24a–24b `[D]` — Legacy batch integration and real third-party API

**Legacy seam:** stand up the "policy admin system" as a nightly synthetic CSV drop to object storage under a written file contract (`docs/contracts/policy-admin-batch.md`: schema, encoding, delivery window, sequence numbering, control totals). Build the ingestion pipeline into the policy-retrieval backing store with reconciliation: row counts and control totals must match, and mismatches quarantine the file rather than partially load it. Seed and prove detection of: schema drift (renamed and retyped column), late file, duplicate file, truncated file and a control-total mismatch. Migrate the claims-record MCP backing store to managed Postgres with versioned migrations and row-level scoping tests re-run against the real engine. Row-level security is proven through the **role topology**, not only through policy behavior, because a suite that connects as a well-behaved test role will pass while an over-powered runtime role silently bypasses RLS in the deployed system. Prove all of the following against the credentials the runtime actually uses: the runtime role is distinct from the migration/table-owner role and owns no table; the runtime role holds `NOBYPASSRLS`; the runtime cannot disable row security or alter policies; `FORCE ROW LEVEL SECURITY` (or the documented engine-equivalent) is set where the owner would otherwise bypass; and cross-claim attempts fail for `SELECT`, `INSERT`, `UPDATE` and `DELETE` alike. Table-owner and privileged-role bypass behavior is tested explicitly and those roles are excluded from every runtime credential.

**The scoping predicate is identity-derived.** The claim and tenant context used by RLS is derived server-side from the validated workload identity and the authorized claim binding — never from a client-supplied parameter, a request field or anything the model can influence. This is the Day 5 invariant applied at the database boundary: a model-supplied tenant predicate would let the agent widen its own data access through the ORM without ever touching the policy decision point.

**Third-party seam:** integrate one genuinely external API on the fraud-enrichment path (address validation or company lookup) as advisory input only. The client implements timeout, bounded retry with jitter, response schema validation, and a circuit breaker that degrades to "enrichment unavailable — flagged for human note" rather than blocking triage or fabricating a value. Force a real failure (block egress to the API) and capture the degradation trace. Record the API's terms, rate limits and version in the capability manifest; only synthetic, non-personal lookup values are ever sent.

**Deliverables:** batch contract, ingestion and reconciliation code with quarantine path, seeded-drift evidence set, Postgres migration and re-run scoping tests, third-party client with outage drill trace, updated threat-to-test map.

**Done when:** all five seeded batch failures are detected and quarantined with alerts, none partially loads; the outage drill shows degraded-but-safe triage with the gap visible to the human reviewer; no consequential action depends on the third-party response; row-level scoping holds on the real engine under the runtime role's own credentials, with role separation, `NOBYPASSRLS`, four-command cross-claim denial and identity-derived predicates all evidenced, and privileged-role bypass tested and excluded.

### Days 25a–25b `[D]` — Asynchronous intake and v1.1 verification

Replace the synchronous FNOL intake with an enterprise-shaped path: an inbound webhook validates and enqueues; an idempotent consumer starts the workflow.

**Consumer transaction model.** The broker dequeue and the database write cannot be one transaction, so the consumer uses an inbox/idempotency design with settlement ordered after commit:

1. Receive under PeekLock with manual settlement — never auto-complete.
2. In a **single Postgres transaction**, insert a persistent inbox record keyed by message or business ID under a unique constraint, create the workflow state, and write the corresponding audit event.
3. Commit that transaction.
4. Complete the Service Bus message only after the commit succeeds.
5. On transaction failure, abandon the message or let the lock expire; redelivery is then deduplicated by the inbox record's unique constraint.
6. Use a transactional **outbox** only where processing must emit a downstream message — that is the problem an outbox solves, and it is not the coupling required here.

Because PeekLock delivery is at-least-once and redelivery remains possible by design, the claim is an **effectively-once business effect under tested at-least-once redelivery**, never unqualified exactly-once delivery.

Prove: duplicate delivery produces exactly one workflow effect; a poison message routes to the dead-letter queue with an alert and a runbook entry rather than a retry storm; replay from the DLQ after a fix is possible and audited; ordering assumptions are either not required or explicitly enforced. Test both crash windows separately — a crash before commit must leave no workflow state and no audit event, and a crash after commit but before settlement must produce redelivery that deduplicates rather than a second workflow start. Verify the kill switch stops queue consumption: after a global stop, messages accumulate safely and no consequential tool call occurs — extending the Day 12 race test to the async path.

Close the release: re-run the sealed behavioral suite, the adversarial suite and full audit-chain verification against the locally integrated environment (real identity, real backing stores, real third party, async intake). Classify every difference from the v1.0 results under the variance taxonomy. Tag `v1.1-integration-controls` only if all Day 22–25 gates are clear and no control regression is open.

**Deliverables:** webhook + queue + consumer implementation, inbox/idempotency schema with its unique constraint, DLQ and replay test evidence, crash-before-commit and crash-before-settlement tests, extended kill-switch test, `docs/runbooks/async-intake-operations.md`, locally-integrated re-verification results with classified variance record, conditional `v1.1-integration-controls`.

**Done when:** redelivery, poison-message, replay, crash-before-commit and crash-before-settlement scenarios each have a passing test with captured traces; no message is settled before its transaction commits; the stop test shows zero consequential calls after halt with messages preserved; audit completeness (100% correlation fields) holds across the async boundary; the sealed suites pass in the locally integrated environment with every variance classified and zero open control regressions.

---

## Week 5 — Operate in the cloud and convert (Days 26–28)

These milestones ship as `v1.2-cloud-operation`.

### Days 26a–26b `[D]` — Cloud staging from infrastructure-as-code

Author IaC (Bicep or Terraform) for the full staging environment: container runtime for the agent and MCP services, managed identity bindings, Postgres, queue, storage, Key Vault references, egress restrictions and the capacity restrictions from the spend-control package. Provision from a clean state. Wire CI promotion: CI promotes the signed `v1.1-integration-controls` artifact to staging only after all inherited v1.0 gates and all applicable v1.1 integration gates pass, deploying with the Day 23 federated credentials; the deployed image digest must match that release's signed provenance (provenance check at deploy time). A build that clears only the v1.0 gates may not be promoted. Exercise a cloud rollback: deploy a release, deploy its successor, roll back using the runbook, and verify with the smoke suite. Tear down and rebuild once to prove reproducibility, exercising the automated-teardown control in the process. Runtime egress in staging is restricted to the declared allowlist (model API, third-party API, telemetry), re-proving the Day 6 egress control in a real network.

**Deliverables:** `infra/` IaC, CI deploy workflow with provenance check, deploy/rollback/rebuild evidence with timestamps, staging smoke suite, egress-restriction proof, exercised teardown evidence.

**Done when:** clean-state provision succeeds from documented commands; the deployed digest is verified against release provenance; rollback restores the prior release with smoke evidence; one full teardown/rebuild is captured; no credential is stored in CI or IaC state in plaintext; daily spend reconciliation shows no unexplained variance.

### Days 27a–27b `[B]` — Integration incident drill and staging re-verification

Day 27a is the drill; Day 27b is the staging re-verification.

Run a scripted integration incident on staging combining three real seams: the third-party API becomes unavailable mid-run, a drifted batch file arrives, and one MCP credential is revoked live. Measure detection, containment and continued-safe-operation behavior. The revocation step must verify that the revoked identity's **protected reads stop within the declared containment window**, not only its consequential calls — the drill exercises the Day 23 containment mechanism end to end, including any declared cache TTL. Write the blameless report with follow-ups.

Then re-verify in staging: re-run the complete sealed behavioral suite, the adversarial suite and full audit-chain verification, plus the contract/smoke rerun of integration gates 1–4 defined in the gate mapping. Classify every difference from the v1.1 results under the variance taxonomy, and escalate any environment-specific variance to that gate's full failure suite.

**Deliverables:** integration incident report with measured times and read-containment evidence, staging re-verification results (sealed suites plus gates 1–4 rerun) with classified variance record, follow-up action list.

**Done when:** the drill shows safe degradation with zero unauthorized consequential actions and zero reads by the revoked identity after the containment window; mean time to detect and contain are measured; the staging sealed-suite and gates 1–4 rerun results carry zero open control regressions; any escalated full suite has run and passed; no step relies on undocumented operator memory.

### Day 28a `[B]` — Independent challenge of the integration chain

The base release is externally challenged on Day 21; the fifth delivery chain and the six-seam assessment instrument would otherwise travel from internal staging verification straight to commercial activation without the same scrutiny. That asymmetry is not defensible when the instrument itself is the thing being sold, so the integration evidence receives its own challenge before any of it is marketed.

Recruit one external practitioner — ideally an integration or platform engineer rather than one of the Day 21 reviewers, so the perspective is genuinely new — and scope the review to: the fifth traceable delivery chain end to end; the six-seam assessment instrument, its finding scale and its scoring guidance; at least one identity revocation and containment trace; the async redelivery and crash-window evidence; the IaC promotion, rollback and rebuild evidence; and whether the demonstrated claim in the repository is still narrower than the service-positioning claim. Record the reviewer's role, scope, date, consent to attribution and conflicts of interest exactly as Day 21 does. Resolve or disclose every finding.

If no reviewer is available, run the documented adversarial self-review fallback across the same scope and label the result "adversarial self-review — no independent review completed" **everywhere the integration claim appears**, including beside the sixth proposition, in the readiness assessment and in both offer rows. The fallback is permitted; concealing it is not.

**Deliverables:** integration review findings, provenance and dispositions; accurate external-review or self-review label applied to every location carrying an integration claim.

**Done when:** critical findings are fixed; accepted residual risks are explicit; review provenance is accurate; the demonstrated-versus-service claim boundary has been independently checked or the self-review label is applied everywhere it belongs.

### Day 28b `[A]` — Commercial conversion and integration launch

Assemble the commercial conversion package: the Enterprise Integration Readiness Assessment applied via the instrument to AEGIS's own pilot and integrated states, the integration runbook, both offer rows in `docs/service-to-artifact-matrix.md`, the finalized fifth chain in `docs/delivery-evidence-guide.md`, the updated `docs/advisory-evidence-guide.md`, the Day 28 README entry-point text, and the service one-pager update. **Edit and publish article 4** — "Enterprise integration is the missing half of agent production-readiness" — and link it from the README and advisory guide; CI verifies the links resolve. Unblock the sixth proposition row in the README propositions table. Tag `v1.2-cloud-operation` only if every integration gate is clear. Run a second outreach wave adding the integration assessment to the follow-on offer set for the prospects contacted on Day 21.

**Deliverables:** `assessment/integration-readiness.md`, `docs/runbooks/integration-operations.md`, both offer rows, updated guides, README entry-point text, service one-pager, published and link-checked article 4, unblocked sixth proposition, conditional `v1.2-cloud-operation`, updated outreach tracker.

**Done when:** article 4 is publicly published with resolving links, not a draft; both offer rows and the assessment instrument are complete; the six-row CI validation passes with the sixth row unblocked; the assessment claims only what the evidence shows; the outreach tracker records the second wave.

---

## Test and evidence strategy

```text
Code / prompt / model / policy / dependency change
                        |
                        v
        +---------------+----------------+
        |               |                |
 deterministic      behavioral       supply-chain
 + security tests   canary eval       build checks
        |               |                |
        +---------------+----------------+
                        |
                 cost regression
                        |
             all mandatory gates pass?
                  /             \
                no               yes
                |                 |
          blocked change     signed candidate
                                  |
                           staged operation test
                                  |
                       release or rollback record
```

### Test layers

- **Unit:** policy parsing, authorization decisions, budget math, audit hashing, field-level redaction and cost attribution.
- **Telemetry:** no secret, credential or raw tool argument appears in any span attribute, log line or Langfuse payload; the pinned semantic-convention version is asserted in release evidence.
- **Contract:** MCP schemas, identity audience/scope, timeout behavior, error normalization, batch file contracts and third-party response schemas.
- **Integration:** agent-to-MCP-to-audit flow, human approval, kill switch, trace correlation and cost capture.
- **Behavioral:** development, calibration and sealed holdout cases with repeat runs and slice reporting.
- **Adversarial:** indirect injection, exfiltration, privilege escalation, denial of wallet and compromised tool output.
- **Release:** seeded-regression tests prove that each CI gate can fail for the intended reason.
- **Operations:** stop, revoke, drain, rollback, recover and post-recovery evaluation; cloud rollback, environment teardown/rebuild and daily spend reconciliation (Days 26–28).
- **Integration (Days 22–25):** batch reconciliation and quarantine, seeded drift/late/duplicate/truncation failures, third-party outage degradation, queue idempotency/DLQ/replay, and inbox-transaction settlement ordering across both crash windows.

### Critical production failure modes

| Failure | Required handling | Required proof |
|---|---|---|
| Model proposes an unauthorized payment | Independent policy and MCP denial; alert and audit | Deterministic negative test and attack trace |
| Human approval token is replayed or belongs to another claim | Bind approval to claim, action, amount, actor and expiry | Replay/cross-claim tests |
| MCP server times out after a write | Idempotency key, status reconciliation and human-visible uncertain state | Timeout-after-write integration test |
| Kill switch races with a queued tool call | Server-side enforcement at execution time | Concurrent stop/tool test |
| Audit event is dropped, reordered or rewritten | Fail or quarantine consequential flow; verify the signed externally anchored head | Mutation, reordering, middle/tail deletion, full-chain replacement and anchor-unavailable tests |
| Cost telemetry is missing | Mark spend unattributed and block cost sign-off | Reconciliation failure test |
| Budget trips during an active claim | Stop admissions, preserve active state, hand off visibly | Budget-spike and recovery test |
| Model migration improves aggregate score but harms a critical slice | Per-slice release threshold blocks migration | Seeded slice-regression test |
| Evaluation judge is biased or unstable | Calibrate against human labels and publish disagreement | Judge calibration artifact |
| Dependency or MCP configuration changes silently | Lock, inventory, scan and version in release evidence | Tampered lock/config CI test |
| Batch file partially loads after a mismatch | Quarantine the whole file; zero partial loads | Seeded truncation and control-total-mismatch tests |
| Revoked identity's already-issued token is still accepted | Containment within the declared maximum window via a named mechanism | Issuance-revocation and active-token-containment tests |
| Consumer crashes between queue consume and audit record | Inbox record, workflow state and audit event commit in one transaction; the message is settled only after commit, so redelivery deduplicates | Crash-before-commit and crash-before-settlement integration tests |
| Deployed image differs from the signed release | Deploy-time digest-provenance check blocks the deploy | Seeded provenance-mismatch test |
| Cloud spend variance is unexplained | Daily reconciliation blocks the release tag until dispositioned | Reconciliation-variance test |

Any silent critical-path failure is a release blocker.

---

## Gap-closure matrix

| Previously identified gap | How AEGIS addresses it | Evidence of closure |
|---|---|---|
| GitHub projects may show building, not breaking and evaluating | The same system is baselined, attacked, remediated and regression-tested | Raw attack corpus, before/after report and permanent security regression suite |
| Weak statistical evaluation evidence | Separate development/calibration/holdout sets, repeated runs, confidence intervals, slices and human judge calibration | Evaluation protocol, calibration report and sealed migration report |
| Limited production monitoring and incident feedback evidence | SLOs, alerts, RACI, live stop/revoke/rollback exercise and post-incident actions | Incident timeline, recovery evidence and post-incident report |
| IAM/NHI depth not visible | Workload identity separation, short-lived scopes, lifecycle register, replay/revocation tests and production IdP mapping | Access matrix, NHI register and negative identity tests |
| AppSec and MCP supply-chain practice not visible | Threat model, input/schema controls, egress constraints, SBOM, dependency/config checks and adversarial tool-output tests | Threat-to-test matrix, SBOM and release evidence |
| Kill-switch claims may be documentary only | Server-side stop, credential revocation, concurrency test and recovery runbook | Recorded exercise and automated halt tests |
| Consulting ability and executive translation not visible | Engagement brief, client-style assessments, audit, 90-day roadmap and executive dashboard | Four buyer-facing evidence bundles at v1.0, five after `v1.2-cloud-operation`, plus the reviewer guide |
| Product/operating boundary design not demonstrated | Explicit decision rights, policy as code, human ownership, value limits and residual-risk register | Boundary design, policy tests and competence ledger |
| FinOps knowledge not demonstrated | Reconciled attribution, quality-adjusted unit economics, safe cost policies and forecast/variance reporting | dbt tests, Power BI model and AgentOps cost report |
| Regulated-sector expertise could be overclaimed | Insurance-specific controls with dated, scoped evidence mappings and legal caveats | Claims register and qualified control-evidence crosswalk |
| “Production” credibility exceeds a local demo | Reproducible artifact, complete release gate, staged operations exercise, rollback and explicit limitations | Release bundle, build provenance, SLOs and readiness assessment |
| Enterprise Azure/Entra depth remains limited | Days 23 and 26 perform real tenant work: app registrations, workload identity federation, Key Vault custody and managed-identity bindings in staging | Issuance-revocation and containment tests against the real IdP, NHI register with tenant objects, staging deployment evidence |
| All MCP backends are self-built mocks | Managed Postgres system of record, legacy batch feed and a genuinely external API (Days 24–25) | Migration tests, reconciliation report, outage drill trace |
| No deployment beyond local/staging on one machine | IaC-provisioned cloud staging, CI promotion with provenance check, cloud rollback (Day 26) | Provision/deploy/rollback/rebuild evidence with timestamps |
| No heterogeneous-failure evidence | Combined third-party outage + batch drift + live credential rotation drill (Day 27) | Integration incident report with measured detect/contain times |
| Delivery guide names two roles; no integration offer exists on either buyer journey | Third role, fifth delivery chain, one contracting and one consulting offer row over the same six-seam evidence, and a defined assessment instrument (Day 28) | Updated delivery and advisory guides, service-to-artifact matrix rows, issued readiness assessment, published article 4 |

The Entra row is closed to staging scope by the integration milestones; operation inside a real client tenant at commercial scale remains outside what a synthetic reference project can claim, and the claims register keeps that limit explicit.

---

## Skill-to-proof coverage

| Existing capability | Evidence AEGIS must expose |
|---|---|
| CAISP | Threat model, adversarial baseline, layered containment, residual-risk register, incident exercise and security audit |
| CMCPSE | MCP trust boundaries, machine-readable capability manifests, workload identities, tool authorization, supply-chain inventory and negative protocol tests |
| Microsoft analytics engineering and Power BI | Tested semantic metrics, traceable executive dashboard, quality/cost/latency views and editable unit-economic assumptions |
| AWS data engineering and machine learning | Versioned data pipelines, reproducible model comparison, deployment artifact, telemetry flow and operational measurement |
| DeepLearning.AI data/ML/deep learning/MLOps | Dataset discipline, behavioral evaluation, drift/regression gates, model lineage and release automation |
| LangChain/LangGraph and Claude engineering | Typed agent workflow, tool-use controls, model migration and trace-driven debugging |
| Software architecture | ADRs, explicit trust/component boundaries, failure handling, dependency control and reversible release design |
| Responsible AI | Human decision rights, prohibited actions, transparent limitations, slice analysis, contestable handoff and qualified governance mapping |
| Python and advanced SQL | Inspectable control implementation, tests, evaluation harness, DuckDB/dbt attribution and evidence generation |
| Enterprise integration engineering | Real-IdP identity tests, batch reconciliation and drift detection, third-party degradation evidence, async intake proofs, IaC deployment and rollback evidence (the fifth delivery chain) |

The point is not to mention the certifications in every report. It is to make the corresponding engineering judgment inspectable. The README can then link from each capability to the strongest artifact rather than presenting a catalogue of course badges.

---

## Service-to-artifact matrix

Maintain the following as `docs/service-to-artifact-matrix.md`. Paths in the implemented repository must be clickable links to the named test, generated result or decision artifact. The matrix is generated or checked against the competence ledger so a service claim cannot outlive its evidence.

| Commercial route | Mode and buyer | Triggering problem | Underlying executable tests | Generated technical evidence | Buyer decision/output | Likely follow-on |
|---|---|---|---|---|---|---|
| Adversarial EvalOps and Model-Migration Engineering | Contracting; AI/ML platform or engineering lead | Agent behavior is evaluated informally, model changes are risky, or releases lack regression gates | Holdout integrity and judge-calibration tests; deterministic boundary tests; adversarial suite; seeded aggregate and critical-slice regressions; cross-model CI run | `docs/evaluation-protocol.md`; machine-readable scorecard; adversarial before/after results; CI failed/passed records; `docs/reports/model-migration-regression.md` | Engineer can implement a defensible eval harness, identify regressions and automate ship/hold thresholds | Eval harness build, migration implementation, observability and recurring regression maintenance |
| Agentic Security and Technical Governance Engineering | Contracting; security architect, CISO engineering lead or agent-platform lead | MCP/tool access is over-privileged, identities are shared, prompt injection can reach authority, or stop/recovery is untested | Wrong-scope/audience/expiry/replay tests; cross-claim and approval-bypass tests; indirect-injection suite; audit tamper tests; concurrent kill/revoke/recovery tests; dependency/config regression | Threat model; capability manifests; access matrix and NHI register; attack traces; signed audit verification; SBOM/provenance; kill/recovery evidence; final security audit | Engineer can implement and prove least privilege, deterministic authorization, containment, traceability and recovery | MCP/NHI remediation, security regression engineering, incident-readiness implementation and later control review |
| Agent Production-Readiness Technical Assessment | Consulting; CTO, Head of AI, CISO or programme sponsor | Pilot works but the organization cannot justify release or identify the minimum remediation path | Evidence completeness checks across all mandatory gates; end-to-end reviewer command; release/rollback exercise; link and claims validation | Pilot baseline; competence ledger; release policy and manifest; final readiness assessment; residual-risk register; control-evidence matrix; 90-day roadmap | Release, hold or reduce autonomy; prioritized blockers, accountable owners and 30/60/90-day remediation plan | Fixed-scope EvalOps, security, operating-control or cost remediation engagement |
| Agent Cost and Unit-Economics Diagnostic | Consulting; CTO, platform lead, FinOps lead or CFO delegate | Spend cannot be attributed to workflows/outcomes, forecasts drift, or cheaper configurations may conceal quality loss | dbt attribution/reconciliation tests; retry/fan-out/cache/failure cases; telemetry-loss test; seeded cost regression; budget-spike and denial-of-wallet tests | Attribution schema and reconciliation report; quality-adjusted unit-economics report; Power BI export; cost-control before/after report; AgentOps cost runbook | Establish cost per attempted/successful/correct outcome, locate unattributed spend and approve safe control/optimization priorities | Attribution implementation, budget controls, model/tool optimization and recurring cost-quality monitoring |
| Enterprise Agent Integration Engineering (after `v1.2-cloud-operation`) | Contracting; engineering manager, AI/ML platform lead or integration architect | Agent pilot works in a sandbox but is blocked on identity, data, legacy, third-party, async or deployment integration into the estate | Issuance-revocation and containment tests; batch reconciliation and seeded-drift tests; third-party outage drill; queue idempotency/DLQ/inbox-transaction tests; IaC provision/rollback/rebuild checks | Entra configuration and NHI register with tenant objects; batch contract and reconciliation report; degradation traces; async runbook; `infra/` with deploy/rollback evidence; classified variance records | Engineer can implement the six-seam patterns with contract tests, seeded failures and safe degradation inside a client stack | Seam-by-seam integration implementation ordered by consequential-action exposure, then detection gaps, then recovery gaps |
| Enterprise Integration Readiness Assessment (after `v1.2-cloud-operation`) | Consulting; CTO, CISO, Head of AI, platform or integration leadership | Leadership cannot tell whether the pilot's integration approach will survive contact with the estate, or what integration work stands between pilot and controlled production | The six-seam evidence checks defined by the assessment instrument; staging re-verification; incident drill | `assessment/integration-readiness.md` (worked pilot-vs-integrated example); per-seam findings and severities; release-blocker list; residual-risk register; 90-day remediation roadmap | Ship, hold or conditional-ship decision with named conditions, owners and dates | Fixed-scope integration engineering engagement on the prioritized seams |

The first two rows are the immediate contracting propositions and the Production-Readiness and Cost rows are the initial consulting offers. Both integration rows activate together, only after `v1.2-cloud-operation` ships, because each cites six-seam evidence that includes the IaC provision, rollback and rebuild artifacts produced on Days 26–27; both are assembled on Day 28. Until then the Agent Integration Engineer role and the fifth delivery chain appear in the guides marked in-progress, in the same way the sixth proposition appears blocked — visible as work underway, never as an available offer. Security reviews and model-migration assurance may later become consulting offers when real client delivery supplies independent production evidence and references.

---

## Post-launch evidence bundles and commercial use

| Evidence bundle | Core artifacts | Consulting opportunity | Contract roles supported |
|---|---|---|---|
| Production Readiness | Pilot/final assessments, release contract, 90-day roadmap, reviewer guide | Agent Production-Readiness Assessment | Agentic AI Solutions Architect, AI Production Engineer, Responsible AI Technical Lead |
| MCP and Agent Security | Threat model, access matrix, NHI register, attack results, kill/recovery proof, audit report | Agent Security and Kill-Switch/NHI Audit | Agentic AI Security Engineer, MCP Security Engineer, AI Application Security Engineer |
| EvalOps and Migration | Protocol, calibrated harness, holdout results, CI gates and model diff | Adversarial EvalOps harness and model-migration assurance | Agent EvalOps Engineer, LLMOps/MLOps Engineer, AI Quality Engineer |
| AgentOps and Cost | Extraction-ready `packages/agent_cost_attribution/`, quality-adjusted economics, budget controls, SLOs and Power BI | FinOps-for-Agents diagnostic and remediation | AgentOps Engineer, AI FinOps Engineer, LLM Observability Engineer |
| Enterprise Integration (after `v1.2-cloud-operation`) | Readiness assessment, integration runbook, classified variance records, six-seam evidence (identity, batch, system of record, third party, async, deployment) | Enterprise Integration Readiness Assessment | Agent Integration Engineer, AI Platform/Integration Engineer |

The primary wedge remains the **Production-Readiness Assessment**; the Integration Readiness Assessment is the second assessment-type offer once both integration releases ship. Security, EvalOps, cost and integration remediation are the evidence-backed follow-on engagements.

---

## Final public narrative

The repository should tell one story:

> Cotswold Mutual had a functioning claims-agent pilot, but it lacked evidence that its behavior, permissions, economics and operation were controlled. AEGIS defined the decision boundary, moved authorization outside the model, secured MCP identities and capabilities, built calibrated behavioral and adversarial evaluation, made quality/security/cost/reliability tests release gates, and proved stop, rollback and recovery through an incident exercise. It then integrated the agent with a real identity provider, a managed system of record, a legacy batch feed, an independent third-party API, asynchronous intake and an IaC-provisioned cloud staging environment — and re-proved every control in that integrated estate. The result is not a compliance certificate or a claim of real production scale; it is a reproducible controlled-production evidence pack and a worked example of how I help clients cross that gap.

That narrative aligns the technical shorthand with the buyer outcome:

- **“I secure”** becomes constrained identities, deterministic authorization, tested containment and recovery.
- **“I evaluate”** becomes calibrated holdout evidence, adversarial regression and model-migration decisions.
- **“I cost-control”** becomes reconciled, quality-adjusted unit economics and safe operating limits.
- **“I enterprise-integrate”** becomes real workload identity, reconciled batch interfaces, resilient third-party clients, audited async intake and provenance-verified cloud deployment — claimable only after both integration releases ship.
- **“Production agent systems”** becomes measurable release, SLO, incident, rollback and ownership controls, with honest limits on what a synthetic reference implementation proves.

Project AEGIS then functions as the bulwark of competence: one coherent system in which the code, tests, traces, dashboards and consulting artifacts all support the same market promise.
