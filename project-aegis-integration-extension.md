# Project AEGIS — Integration Extension: 6 Build Milestones to Evidence of Enterprise Agent Integration

> **Superseded (2026-08-20):** This extension has been incorporated into the governing plan, `project-aegis-plan-v1.1.md`, as Days 22–28 (the former Day 27 was split into a `[B]` drill/re-verification milestone and an `[A]` commercial-conversion milestone). This file is retained for provenance only and receives no further updates. On any conflict, the governing plan controls.

> **Service positioning (client delivery only):** I help regulated and data-intensive organizations move AI agents from pilot to controlled production by testing their behavior, securing MCP and tool access, implementing measurable release, operating and cost controls, and integrating agents with the identity, data and legacy systems the enterprise already runs.
>
> **Demonstrated claim (repository):** AEGIS demonstrates six enterprise integration patterns against a real identity provider, managed cloud services and an independent third-party API, using synthetic data.
>
> **Technical shorthand:** I secure, evaluate, cost-control and enterprise-integrate production-oriented agent systems.

The two registers above are deliberately separate. The service positioning describes what the practice does inside a real client estate and may appear only in outreach and proposal material, clearly framed as the service. The demonstrated claim is the only integration claim the repository, README and articles may make, because the reference estate is provisioned by the project itself: the "legacy system" is a synthetic batch producer and the system of record is a newly created managed database. They prove integration engineering patterns, not integration into a pre-existing estate.

> **Revision record (2026-08-20, revision 2):** Applied external review findings. The single release is split into `v1.1-integration-controls` (Days 22–25) and `v1.2-cloud-operation` (Days 26–27), each with its own effort budget, triggers and descope ladder; the sixth proposition remains blocked until both ship. The sixth proposition now literally joins the canonical "What AEGIS must prove" table in the base plan and README, with a six-row CI validation against the competence ledger. A commercial conversion section adds one contracting offer row and one consulting offer row over the same six-seam evidence, the exact README entry-point text, and a defined assessment instrument. Control preservation now uses a two-class variance taxonomy: implementation variances are dispositioned, control regressions block release. The market-position overclaim is split into service positioning versus demonstrated claim. The absolute cloud-spend gate is replaced with an implementable control package acknowledging Azure billing latency. The Entra revocation test is split into issuance revocation and active-token containment with a declared maximum window. Article 4 must be edited and published, link-checked, before `v1.2-cloud-operation` may be tagged.
>
> **Revision record (2026-08-20, revision 1):** Initial draft adding the third delivery role — Agent Integration Engineer — after `v1.0-aegis`, without modifying the v1.0 release contract, its mandatory gates or the base plan's 75/100-hour effort controls.

## Why this extension exists

The base plan's own market research identifies "insufficient tool/data access" (33% of negative-ROI cases, Forrester) and legacy-integration "innovation theatre" — demos that work in sandboxes but lack standardised integration to live stacks — as leading pilot-to-production killers. Yet AEGIS v1.0 is deliberately self-contained: all three MCP domains are mocks the project builds, identity integration is a paper mapping to Entra, and deployment stops at local/staging. A buyer inspecting v1.0 can verify evaluation, security and cost competence, but can only *infer* integration competence.

This extension converts the integration story from **designed-for** to **demonstrated** by replacing three self-contained seams with real ones:

1. **A real identity plane** — Microsoft Entra ID workload identities and federation, not locally issued tokens.
2. **Real managed services and a real third-party API** — a genuine database, a legacy-style batch interface, and an external service the project does not control.
3. **A real deployed environment** — cloud staging provisioned from infrastructure-as-code, promoted from CI, with rollback exercised in the cloud rather than on a laptop.

The data remains synthetic throughout. The extension makes the **systems** real, never the claims, claimants or policies.

**Consistency note on scope guardrails:** the base plan excludes *building* a custom identity provider, policy engine or observability platform. This extension complies: it *integrates* established managed services (Entra ID, a managed queue, a managed database) and spends effort on integration and evidence, exactly as the guardrail directs.

---

## The sixth proposition joins the canonical table

The base plan's "What AEGIS must prove" table and the repository README propositions section are the **canonical** statements of what AEGIS proves. This extension does not maintain a parallel table. On Day 22, the following row is appended to both canonical locations, marked **blocked** until both extension releases ship:

| Proposition | Reproducible proof | Buyer-facing artifact |
|---|---|---|
| The agent integrates with a real identity provider, managed cloud services and an independent third-party API without weakening any v1.0 control | Real-IdP issuance-revocation and active-token-containment tests, batch reconciliation with drift detection, third-party outage drill, IaC-provisioned staging deployment, cloud rollback exercise, unchanged sealed-suite pass in the integrated environment | Enterprise Integration Readiness Assessment and integration runbook |

**Update targets (Day 22):** `project-aegis-plan-v1.1.md` § "What AEGIS must prove"; the repository README propositions section; `docs/evidence/competence-ledger.md` (new chain rows); `docs/service-to-artifact-matrix.md`.

**Validation:** CI checks that the README propositions table contains exactly six rows and that every row's proof column resolves to at least one competence-ledger chain with a runnable test command. A propositions row without a ledger chain fails the build. While the sixth row is blocked, its status is shown in the table and the claims register prohibits asserting it publicly.

### Delivery role added

`docs/delivery-evidence-guide.md` gains a third supported role and a fifth traceable delivery chain:

| Role | Delivery chain | Chain contents |
|---|---|---|
| Agent Integration Engineer | Enterprise integration | Problem → integration ADR → code location → contract/reconciliation tests → seeded failure (drift, outage, rotation) → generated result → limitation → what the engineer would own inside a client team |

---

## Release structure, time budget and effort controls

The extension ships as **two releases**, because its two halves carry different risk profiles: Days 22–25 are runnable locally against real managed services, while Days 26–27 depend on cloud provisioning friction, billing latency and vendor behavior outside the project's control.

| Release | Milestones | Scope | Initial budget | Forecast trigger | Re-plan trigger |
|---|---|---|---|---|---|
| `v1.1-integration-controls` | Days 22–25 | Identity plane, legacy batch, system of record, third-party API, async intake — integrated and verified locally against real services | 30 focused hours | 22 hours | 30 hours |
| `v1.2-cloud-operation` | Days 26–27 | IaC cloud staging, CI promotion, cloud rollback, integration incident drill, staging re-verification, commercial assembly and article publication | 25 focused hours | 18 hours | 25 hours |

The combined ~55-hour forecast is a planning trigger, not a promise; it is explicitly subject to the Day 22 vendor decisions and is re-estimated in the Day 22 ADR once concrete services are chosen. At each forecast trigger, forecast the effort remaining for every blocked gate in that release and record likely variance and available cuts. At each re-plan trigger with any mandatory gate blocked, stop discretionary work and issue a dated re-plan that cuts through the descope ladder, extends the calendar, or reduces the target and withdraws the associated claims.

**Release-label invariants:**

- `v1.1-integration-controls` may not ship while any Day 22–25 mandatory gate is blocked.
- `v1.2-cloud-operation` may not ship while any extension gate is blocked, including article 4 publication and the commercial conversion artifacts.
- The **sixth proposition remains blocked** — in the canonical table, the README and all public claims — until **both** releases have shipped.
- A partial result is labelled `-rc` with its blocked gates disclosed.

Log extension time in the existing `docs/evidence/effort-log.csv` with milestone labels `day-22` … `day-27` so total project effort remains one auditable series.

### Control-preservation rule: variance taxonomy

Every control proven in v1.0 must continue to meet or exceed its control objective in the integrated environment. Differences are classified into exactly two classes; there is no third category and no silent absorption.

| Class | Definition | Treatment |
|---|---|---|
| **Implementation variance** | A different lifetime, mechanism or provider behavior that still **meets or exceeds** the v1.0 control objective (e.g., Entra-imposed minimum token lifetime, a managed queue's redelivery semantics) | Recorded in the claims register with a dated disposition: objective, v1.0 mechanism, integrated mechanism, evidence that the objective still holds. Does not block release. |
| **Control regression** | Weaker prevention, detection or recovery than v1.0 evidenced (e.g., a longer window in which a revoked identity can act, a batch path that can partially load, an audit event that can be lost across the async boundary) | **Blocks the affected release tag and the sixth proposition** until remediated or the objective is restored by a compensating control whose test passes. A regression may not be dispositioned as a variance. |

The sealed behavioral suite, the adversarial suite and full audit-chain verification are re-run against the locally integrated environment before `v1.1-integration-controls` is tagged, and against the staging environment before `v1.2-cloud-operation` is tagged. Every result difference is classified under this taxonomy with a dated record.

### Cloud spend controls

Azure budgets trigger notifications but do not stop consumption; hard spending limits exist only on certain subscription offers; and cost data arrives with latency. An absolute "spend stays under cap" release gate is therefore not implementable and is **not** claimed. The implementable control package, configured before any Day 23 resource is created and versioned in `controls/cloud-budget.yaml`, is:

1. **Eligibility record:** whether the subscription offer supports a hard spending limit, recorded in the Day 22 ADR; if supported, the limit is enabled.
2. **Tiered alerts:** budget alerts at 50%, 75% and 90% of the recorded monthly cap, delivered to a monitored channel.
3. **Automated teardown:** a scripted, tested teardown of all nonessential extension resources, runnable in one command and triggered manually on a 90% alert.
4. **Quota ceilings:** maximum SKU and instance-count quotas set at the resource-group level so a misconfiguration cannot scale expensively.
5. **Daily reconciliation:** observed spend reconciled daily against forecast in the effort/cost log; unexplained variance is investigated the same day.
6. **Latency disclosure:** the runbook and readiness assessment state explicitly that billing latency prevents a universal absolute cap and that the controls above bound, detect and respond to spend rather than guarantee a ceiling.

Cloud cost appears in the existing attribution model as a visible **infrastructure** cost class, never mixed into measured per-claim model/tool cost. This package is itself FinOps-for-Agents evidence.

---

## Target enterprise landscape

Cotswold Mutual's fictional estate is defined so each integration seam exercises a distinct, realistic enterprise pattern. All services are free-tier or low-cost managed offerings; nothing is built where an established component exists.

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
  DLQ, outbox pattern        company lookup): rate limits,
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

**Not required:** the exact vendors above are defaults, not commitments. Any equivalent managed substitution (AWS/GCP identity federation, RDS, SQS) is acceptable if it exercises the same pattern; the choice is recorded in the Day 22 ADR together with the re-estimated effort budget.

---

## Scope guardrails

### Mandatory core

**`v1.1-integration-controls` (Days 22–25):**

- Real IdP integration for all three MCP domain identities, with issuance-revocation and active-token-containment tests executed against the real IdP.
- One legacy-style batch interface with reconciliation and drift detection.
- One genuinely external third-party API on a non-consequential (advisory/enrichment) path.
- One asynchronous queue-based intake path with idempotency and dead-letter evidence.
- Sealed behavioral, adversarial and audit-verification suites re-run against the locally integrated environment, with every difference classified under the variance taxonomy.
- Canonical propositions-table update with six-row CI validation.

**`v1.2-cloud-operation` (Days 26–27):**

- One IaC-provisioned cloud staging environment with CI promotion and an exercised cloud rollback.
- The combined integration incident drill.
- Full re-verification of the sealed suites in staging.
- The Enterprise Integration Readiness Assessment, integration runbook, both commercial offer rows, the updated guides and README entry-point text, and the edited, **published**, link-checked article 4.

### Stretch only after all extension gates pass

- A second cloud region or environment tier (dev → staging promotion chain).
- An API-gateway or iPaaS front (e.g. APIM) in front of the MCP services.
- SharePoint/Graph API as a document store for policy PDFs.
- Contract-testing tooling (e.g. Pact) beyond the hand-rolled contract tests.

### NOT in scope

- Real customer, claimant or insurer data: the batch files, database rows and queue messages carry only generated synthetic content. The third-party API receives only synthetic, non-personal lookup values (fictional postcodes drawn from published test ranges, or public company numbers).
- Building an ESB, iPaaS, custom gateway or custom IdP.
- A self-managed Kafka cluster or streaming platform; a managed queue exercises the pattern at appropriate scale.
- Production load, availability or multi-region claims: staging demonstrates engineering controls, not commercial-scale operation.
- Multi-agent or A2A architecture (unchanged from the base plan).
- Autonomous consequential actions through any new seam: the third-party API and batch feed inform recommendations only; payment, denial and settlement remain authenticated human actions.
- Any public claim of integration into a pre-existing enterprise estate (see Claims discipline).

### Predeclared descope ladders

**`v1.1-integration-controls`:**

| Milestone | Minimum condition to exit the day | Deferred work and release effect |
|---|---|---|
| Day 23 — identity plane | All three MCP identities and the audit signer resolved through Entra; issuance revocation proven; active-token containment proven within the declared maximum window | CI OIDC federation may defer to Day 26. Until recovered, the "no stored cloud secrets" claim is withheld. |
| Day 24 — legacy and third party | Batch ingestion with reconciliation totals and at least one detected seeded drift; third-party client with timeout, retry-with-jitter and fail-degraded behavior under a forced outage | Duplicate-file and late-file handling may defer to Day 25 close or Day 27, with the reconciliation gate blocked until recovered. |
| Day 25 — async intake | Queue consumer proves idempotency under redelivery and routes a poison message to the DLQ with an alert | Outbox-pattern write coupling may defer to Day 27; the exactly-once-effect claim and the v1.1 tag are withheld until recovered. |

**`v1.2-cloud-operation`:**

| Milestone | Minimum condition to exit the day | Deferred work and release effect |
|---|---|---|
| Day 26 — cloud staging | `terraform/bicep apply` from a clean state produces a working environment; one CI-promoted deploy; one exercised rollback to the previous release | Environment-teardown/rebuild timing evidence may defer to Day 27. The reproducible-environment claim requires at least one clean rebuild before v1.2. |
| Day 27 — drill, re-verification and conversion | Combined incident drill executed with measured times; staging re-verification classified under the variance taxonomy; assessment, offer rows and published article 4 complete | No conversion artifact may defer past Day 27; if any is incomplete, v1.2 does not tag and the sixth proposition stays blocked. |

Slip order: stretch items first, additional failure scenarios second, non-evidentiary polish third. Deferred work enters `docs/evidence/deferred-work-register.md` with owner, receiving milestone, blocked gate and prohibited claim, exactly as in the base plan.

---

## The six milestones

### Day 22 `[S]` — Integration landscape, ADR, canonical updates and threat-model delta

Define Cotswold Mutual's system landscape (table above) and record the vendor choices, substitution rationale, subscription spending-limit eligibility, quota ceilings and the re-estimated effort budget in `docs/adr/002-enterprise-integration-architecture.md`. Extend the threat model with the new trust boundaries: compromised batch file, poisoned third-party response, queue replay, cloud-credential theft, IaC-state tampering and staging-environment drift. Each new threat gets a planned prevention/detection/recovery control and a named future test. Extend the capability manifests: the third-party API and batch feed are registered as tool domains with owner, data class, egress destination and decommission method, even though they are advisory-only. Configure the cloud-spend control package (alerts, quotas, teardown script skeleton, reconciliation log). **Append the sixth proposition row, marked blocked, to the base plan's "What AEGIS must prove" table and the README propositions section; add the corresponding competence-ledger chains; wire the six-row CI validation.** Add the Agent Integration Engineer role and fifth-chain skeleton to the delivery guide and service-to-artifact matrix.

**Deliverables:** `docs/adr/002-enterprise-integration-architecture.md`, threat-model delta, extended capability manifests, `controls/cloud-budget.yaml`, updated base-plan and README propositions tables with blocked sixth row, competence-ledger chains, six-row CI check, updated guide/matrix skeletons.

**Done when:** every new trust boundary has a threat row with a planned test; the spend-control package is active and evidenced; the six-row validation passes with the sixth row shown as blocked; no landscape component requires real personal data to function.

### Day 23 `[D]` — Real identity plane

Replace locally issued MCP workload tokens with Entra ID app registrations: one per MCP domain, minimum scopes, documented owner and lifecycle. Move the audit-signer key into Key Vault with access policies that exclude the agent and ordinary ledger writer, preserving the base plan's signer-separation invariant under a real custodian. Configure workload identity federation so GitHub Actions obtains short-lived cloud credentials via OIDC with no stored secrets.

Revocation is tested as **two distinct properties**, because continuous access evaluation does not cover a custom API that validates issued JWTs locally, and workload identity federation by itself gives no revocation awareness to the MCP servers:

1. **Issuance revocation:** disabling the service principal prevents acquisition of any new token, proven against the real IdP.
2. **Active-token containment:** an already-issued token is rejected within a **declared maximum containment window**, achieved by a named mechanism — short token lifetime, a resource-side denylist consulted by the MCP servers on each consequential call, or another mechanism recorded in the ADR. The window is published in the NHI register and the readiness assessment. If the achievable window is longer than the v1.0 local implementation's, that difference is classified under the variance taxonomy: a documented implementation variance if the containment objective still holds, a control regression (release blocker) if it does not.

Re-run the remaining Day 6 negative identity suite (expired, wrong-audience, wrong-scope) against the real IdP. Update the NHI register: each identity's provision/rotate/monitor/decommission entry names the real tenant object, and the register gains a variance column recording every difference the managed service imposes, with its taxonomy class.

**Deliverables:** Entra configuration as code (or scripted, exported and versioned), Key Vault signer integration, federated CI credential flow, issuance-revocation and active-token-containment test evidence with the declared window, re-executed negative identity tests, updated `security/nhi-register.yaml` with classified variance column.

**Done when:** no MCP identity or CI job uses a long-lived stored secret; issuance revocation and active-token containment both pass with captured evidence and a published window; expired, wrong-audience and wrong-scope tokens fail closed against the real IdP; signer-key custody exclusion is proven by a denied-access test; every variance is classified and no control regression is open.

### Day 24 `[D]` — Legacy batch integration and real third-party API

**Legacy seam:** stand up the "policy admin system" as a nightly synthetic CSV drop to object storage under a written file contract (`docs/contracts/policy-admin-batch.md`: schema, encoding, delivery window, sequence numbering, control totals). Build the ingestion pipeline into the policy-retrieval backing store with reconciliation: row counts and control totals must match, and mismatches quarantine the file rather than partially load it. Seed and prove detection of: schema drift (renamed and retyped column), late file, duplicate file, truncated file and a control-total mismatch. Migrate the claims-record MCP backing store to managed Postgres with versioned migrations and row-level scoping tests re-run against the real engine.

**Third-party seam:** integrate one genuinely external API on the fraud-enrichment path (address validation or company lookup) as advisory input only. The client implements timeout, bounded retry with jitter, response schema validation, and a circuit breaker that degrades to "enrichment unavailable — flagged for human note" rather than blocking triage or fabricating a value. Force a real failure (block egress to the API) and capture the degradation trace. Record the API's terms, rate limits and version in the capability manifest; only synthetic, non-personal lookup values are ever sent.

**Deliverables:** batch contract, ingestion and reconciliation code with quarantine path, seeded-drift evidence set, Postgres migration and re-run scoping tests, third-party client with outage drill trace, updated threat-to-test map.

**Done when:** all five seeded batch failures are detected and quarantined with alerts, none partially loads; the outage drill shows degraded-but-safe triage with the gap visible to the human reviewer; no consequential action depends on the third-party response; row-level scoping holds on the real engine.

### Day 25 `[D]` — Asynchronous intake and v1.1 verification

Replace the synchronous FNOL intake with an enterprise-shaped path: an inbound webhook validates and enqueues; an idempotent consumer starts the workflow. Prove: duplicate delivery produces exactly one workflow effect (idempotency key evidence); a poison message routes to the dead-letter queue with an alert and a runbook entry rather than a retry storm; replay from the DLQ after a fix is possible and audited; ordering assumptions are either not required or explicitly enforced. Couple queue consumption to the audit ledger through an outbox pattern so a crash between "consume" and "record" cannot produce an unaudited workflow start. Verify the kill switch stops queue consumption: after a global stop, messages accumulate safely and no consequential tool call occurs — extending the Day 12 race test to the async path.

Close the release: re-run the sealed behavioral suite, the adversarial suite and full audit-chain verification against the locally integrated environment (real identity, real backing stores, real third party, async intake). Classify every difference from the v1.0 results under the variance taxonomy. Tag `v1.1-integration-controls` only if all Day 22–25 gates are clear and no control regression is open.

**Deliverables:** webhook + queue + consumer implementation, idempotency and DLQ test evidence, outbox coupling tests, extended kill-switch test, `docs/runbooks/async-intake-operations.md`, locally-integrated re-verification results with classified variance record, conditional `v1.1-integration-controls`.

**Done when:** redelivery, poison-message, replay and crash-between-steps scenarios each have a passing test with captured traces; the stop test shows zero consequential calls after halt with messages preserved; audit completeness (100% correlation fields) holds across the async boundary; the sealed suites pass in the locally integrated environment with every variance classified and zero open control regressions.

### Day 26 `[D]` — Cloud staging from infrastructure-as-code

Author IaC (Bicep or Terraform) for the full staging environment: container runtime for the agent and MCP services, managed identity bindings, Postgres, queue, storage, Key Vault references, egress restrictions and the quota ceilings from the spend-control package. Provision from a clean state. Wire CI promotion: a release that passes all v1.0 gates deploys the signed container to staging using the Day 23 federated credentials; the deployed image digest must match the signed release evidence (provenance check at deploy time). Exercise a cloud rollback: deploy a release, deploy its successor, roll back using the runbook, and verify with the smoke suite. Tear down and rebuild once to prove reproducibility, exercising the automated-teardown control in the process. Runtime egress in staging is restricted to the declared allowlist (model API, third-party API, telemetry), re-proving the Day 6 egress control in a real network.

**Deliverables:** `infra/` IaC, CI deploy workflow with provenance check, deploy/rollback/rebuild evidence with timestamps, staging smoke suite, egress-restriction proof, exercised teardown evidence.

**Done when:** clean-state provision succeeds from documented commands; the deployed digest is verified against release provenance; rollback restores the prior release with smoke evidence; one full teardown/rebuild is captured; no credential is stored in CI or IaC state in plaintext; daily spend reconciliation shows no unexplained variance.

### Day 27 `[B]` — Integration drill, staging re-verification and commercial conversion

Run a scripted integration incident on staging combining three real seams: the third-party API becomes unavailable mid-run, a drifted batch file arrives, and one MCP credential is rotated live. Measure detection, containment and continued-safe-operation behavior; write the blameless report with follow-ups. Re-run the complete sealed behavioral suite, the adversarial suite and full audit-chain verification **in staging** and classify every difference from the v1.1 results under the variance taxonomy.

Assemble the commercial conversion package defined in the next section: the Enterprise Integration Readiness Assessment (using the defined instrument), the integration runbook, the contracting and consulting offer rows in `docs/service-to-artifact-matrix.md`, the finalized fifth chain in `docs/delivery-evidence-guide.md`, the updated `docs/advisory-evidence-guide.md`, the exact README entry-point text, and the service one-pager update. **Edit and publish article 4** — "Enterprise integration is the missing half of agent production-readiness" — and link it from the README and advisory guide; CI verifies the links resolve. Unblock the sixth proposition row in the base plan and README. Tag `v1.2-cloud-operation` only if every extension gate is clear.

**Deliverables:** integration incident report with measured times, staging re-verification results with classified variance record, `assessment/integration-readiness.md`, `docs/runbooks/integration-operations.md`, both offer rows, updated guides, README entry-point text, service one-pager, **published and link-checked article 4**, unblocked sixth proposition, conditional `v1.2-cloud-operation`.

**Done when:** the drill shows safe degradation with zero unauthorized consequential actions; the staging sealed-suite results carry zero open control regressions; article 4 is publicly published with resolving links, not a draft; both offer rows and the assessment instrument are complete; the six-row CI validation passes with the sixth row unblocked; the assessment claims only what the evidence shows.

---

## Commercial conversion

The base plan's rule holds: engineering produces facts once; commercial artifacts interpret them. Both offers below consume the **same six-seam evidence** produced on Days 22–27 — neither creates a second implementation or a second evidence store.

### Offer rows

These rows are added to `docs/service-to-artifact-matrix.md` and the corresponding guides, in the base plan's offer format.

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

**Consulting offer — Enterprise Integration Readiness Assessment** (added to `docs/advisory-evidence-guide.md` as a third current offer alongside the two in the base plan):

| Field | Content |
|---|---|
| Buyer | CTO, CISO, Head of AI, platform and integration leadership |
| Triggering problem | Leadership cannot tell whether the agent pilot's integration approach will survive contact with the estate, or what integration work stands between pilot and controlled production |
| Scope | Assessment of the six seams against the defined instrument below; findings, blockers, residual risks and a prioritized remediation plan |
| Inputs | Architecture documentation, identity model, interface contracts, deployment pipeline definitions, interviews |
| Outputs | Scored per-seam findings, release-blocker list, residual-risk register, prioritized remediation roadmap, executive decision recommendation |
| Exclusions | Compliance certification, production-scale attestation, vendor selection authority, legal opinions |
| Underlying tests/evidence | The worked assessment in `assessment/integration-readiness.md`, applied to AEGIS's own pilot-vs-integrated states, plus the six-seam evidence it cites |
| Likely remediation path | 90-day phased plan ordered by the prioritization rule in the instrument |

### README navigation contract (exact text)

The two entry-point blocks defined in the base plan are replaced with the following exact text on Day 27; CI checks both links and the propositions-table row count:

```markdown
## Hiring an engineer?

Start with the [Delivery Evidence Guide](docs/delivery-evidence-guide.md) to inspect the implementation, test commands, seeded failures and generated evidence for EvalOps, model migration, MCP security, release controls, cost attribution and enterprise integration.

## Assessing a consulting engagement?

Start with the [Advisory Evidence Guide](docs/advisory-evidence-guide.md) to review the readiness method, executive findings, release blockers, service scopes, the enterprise integration readiness method and the 90-day remediation path.
```

### The assessment instrument

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

## Quantitative acceptance gates (extension)

Thresholds are versioned in `controls/release-policy.yaml` under an `integration:` section, frozen at Day 22 exit. Gates 1–4 and the v1.1 half of gate 6 govern `v1.1-integration-controls`; gates 5, 7 and the staging half of gate 6 govern `v1.2-cloud-operation`.

| # | Gate | Minimum release condition |
|---|---|---|
| 1 | Identity | 0 long-lived stored secrets in code, CI or IaC; issuance revocation proven; active-token containment within the declared published window; expired/wrong-audience/wrong-scope fail closed against the real IdP; signer-key custody exclusion proven |
| 2 | Reconciliation | 100% of ingested batch rows reconcile to control totals; all five seeded batch failures detected and quarantined; 0 partial loads |
| 3 | Third party | Forced outage produces degraded-but-safe triage; 0 consequential actions depend on the third-party response; 0 fabricated enrichment values |
| 4 | Async | Duplicate delivery → exactly one workflow effect; poison message → DLQ + alert; crash between consume and record → no unaudited start; stop → 0 consequential calls with messages preserved |
| 5 | Deployment | Clean-state IaC provision, CI-promoted deploy with digest-provenance match, exercised rollback and one teardown/rebuild all evidenced |
| 6 | Control preservation | Sealed behavioral, adversarial and audit-verification suites pass in the integrated environment (locally for v1.1, staging for v1.2); every difference classified under the variance taxonomy; **0 open control regressions**; implementation variances dispositioned with dated records |
| 7 | Conversion | Both offer rows complete in the required format; assessment issued using the defined instrument; README entry-point text in place; article 4 published and link-checked; six-row propositions validation passes |
| 8 | Spend | Spend-control package fully configured and evidenced (eligibility record, tiered alerts, tested teardown, quota ceilings, daily reconciliation); no unexplained daily variance open at tag time; latency limitation disclosed in runbook and assessment |

A gate may not be weakened to make a release ship; the release-label invariants apply.

---

## Claims discipline

Permitted after `v1.1-integration-controls`:

- "Integrates with a real enterprise identity provider using per-workload identities, with issuance revocation and a declared active-token containment window proven by fail-closed tests."
- "Demonstrates legacy batch, managed-database, third-party API and asynchronous integration patterns with reconciliation, drift detection and safe degradation, on synthetic data."

Permitted only after **both** releases (`v1.2-cloud-operation`):

- "Demonstrates six enterprise integration patterns against a real identity provider, managed cloud services and an independent third-party API, using synthetic data."
- "Deploys to a cloud staging environment from infrastructure-as-code with provenance-verified promotion and an exercised rollback."
- The sixth proposition, asserted through the canonical table.

Prohibited (entered in the claims register as prohibited language):

- Any claim of production operation, commercial scale, real-data processing or availability guarantees.
- "Enterprise-proven" or any phrase implying operation inside a real client estate.
- **"Integrates with the identity, data and legacy systems the enterprise already runs" as a repository or article claim.** That sentence is service positioning for client delivery and may appear only in outreach/proposal material clearly framed as the service offered, never as a description of what AEGIS demonstrates.
- Any absolute cloud-spend guarantee; spend controls bound, detect and respond, they do not cap.
- Describing the third-party or batch integrations as consequential-action paths; they are advisory inputs under the unchanged human-decision boundary.
- Asserting the sixth proposition, in any channel, before both extension releases have shipped.

---

## Gap-closure delta

| Gap identified in v1.0 | How the extension closes it | Evidence of closure |
|---|---|---|
| All MCP backends are self-built mocks | Managed Postgres system of record, legacy batch feed and a genuinely external API | Migration tests, reconciliation report, outage drill trace |
| Identity integration is a paper mapping to Entra | Real Entra workload identities, Key Vault signer custody, federated secretless CI, revocation split into issuance and containment properties | Issuance-revocation and containment tests with declared window, NHI register with tenant objects and classified variances |
| No deployment beyond local/staging on one machine | IaC-provisioned cloud staging, CI promotion with provenance check, cloud rollback | Provision/deploy/rollback/rebuild evidence with timestamps |
| No heterogeneous-failure evidence | Combined third-party outage + batch drift + live credential rotation drill | Integration incident report with measured detect/contain times |
| Delivery guide names two roles; no integration offer exists on either buyer journey | Third role, fifth delivery chain, one contracting and one consulting offer row over the same six-seam evidence, and a defined assessment instrument | Updated delivery and advisory guides, service-to-artifact matrix rows, issued readiness assessment, published article 4 |
