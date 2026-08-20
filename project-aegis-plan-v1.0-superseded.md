# Project AEGIS — 21 Days to Evidence of Controlled Agent Production

> **Superseded (2026-08-20):** This is the original v1.0 planning document, retained for provenance only. The governing plan is `project-aegis-plan-v1.1.md`, which now incorporates the enterprise-integration milestones (Days 22–28, formerly `project-aegis-integration-extension.md`). On any conflict, the governing plan controls. This file receives no further updates.
>
> Note: "Day-22" in the evidence-bundles section below predates the integration extension and means "post-launch," not the governing plan's Day 22 build milestone. The sections unique to this file — skill-to-proof coverage, the post-launch evidence bundles and the final public narrative — already exist in the governing plan, where they carry their integration additions.

> **Market position:** I help regulated and data-intensive organizations move AI agents from pilot to controlled production by testing their behavior, securing MCP and tool access, and implementing measurable release and operating controls.
>
> **Technical shorthand:** I secure, evaluate, and cost-control production-oriented agent systems.

Project AEGIS is the worked proof behind both statements. It is not another agent demo. It starts with a deliberately limited pilot, exposes why that pilot is unsafe to release, and produces an evidence-backed path to a controlled production candidate.

The reference use case is an insurance claims-triage agent for a fictional UK mid-market insurer, **Cotswold Mutual**. The agent ingests synthetic first-notification-of-loss documents, retrieves policy terms, checks deterministic fraud indicators, and recommends the next action. It may request missing information or route work, but it never settles a claim or makes a rights-affecting decision without an authenticated human approval.

**Time budget:** 21 days at 3–4 focused hours per day. The plan has a mandatory core and explicitly marked stretch items. Evidence depth wins over tool count.

**Repository rule:** every claim in the README must link to a test, generated result, trace, report, or runbook. If the repository cannot reproduce it, the project does not claim it.

---

## What AEGIS must prove

AEGIS must let a technical buyer verify five propositions without relying on certificates or self-description.

| Proposition | Reproducible proof | Buyer-facing artifact |
|---|---|---|
| The pilot can become a controlled production candidate | Baseline gap assessment, release policy, signed build evidence, rollback exercise and production-readiness score | Production-Readiness Assessment and 90-day remediation plan |
| Agent behavior is tested rather than “vibe checked” | Versioned holdout set, calibrated scoring, repeated runs, slice results, adversarial cases and model-migration diff | EvalOps scorecard and migration regression report |
| MCP and tool access is constrained outside the model | Per-tool authorization, short-lived identities, capability manifests, egress limits, approval enforcement and negative security tests | MCP Security / NHI Audit report |
| Release and operating controls are measurable | Quality, security, cost and reliability gates; SLOs; alerts; change record; incident and recovery evidence | Release evidence pack and AgentOps runbook |
| Cost is attributable and controlled without hiding quality loss | Per-claim attribution, quality-adjusted unit economics, forecast variance, caps, anomaly tests and safe degradation | Power BI executive dashboard and FinOps-for-Agents report |

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

### Stretch only after all release gates pass

- Garak in addition to PyRIT.
- promptfoo in addition to the primary Python/DeepEval harness.
- A public container image or hosted demo.
- More claim types, multi-agent coordination or real-time streaming.
- A second dashboard beyond the Power BI executive view.

### NOT in scope

- Real customer, claimant or insurer data: synthetic data only avoids privacy and contractual risk.
- Autonomous settlement, claim denial or payment: those actions remain human-authorized because this is a high-impact workflow.
- A legal conclusion of UK GDPR, FCA, Consumer Duty, ISO/IEC 42001 or EU AI Act compliance: AEGIS supplies technical evidence only.
- Production load or availability claims: local/staging tests can demonstrate engineering controls, not commercial-scale operation.
- A custom identity provider, policy engine, vector database or observability platform: use established components and focus effort on integration and evidence.
- Multi-agent or A2A architecture: it adds surface area without strengthening the three core service offers.

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
             v                                 v
     [Eval/release evidence]          [Cost attribution + Power BI]
             |                                 |
             +----------------+----------------+
                              v
                  [Release / operate / rollback]
```

**Security invariant:** prompts may recommend an action but never authorize it. The policy decision point and each MCP server independently enforce identity, scope, claim-value limits and approval state.

**Audit invariant:** the local hash chain is described as **tamper-evident**, not immutable. Each event includes a correlation ID, timestamp, actor/NHI, model and prompt version, policy version, tool arguments hash, authorization result, human approval reference, cost and outcome. The verification command must detect modification or deletion. A real immutable/WORM store is documented as a production deployment option, not simulated by wording.

---

## Technology choices

| Concern | Core choice | Reason |
|---|---|---|
| Agent workflow | Python, typed LangGraph state | Familiar to buyers and inspectable in tests |
| Tool protocol | Official MCP Python SDK | Makes protocol security and capability boundaries visible |
| Models | Claude plus one alternate | Supports a concrete migration regression exercise |
| Deterministic tests | pytest | Control enforcement must not depend on probabilistic judges |
| Behavioral evaluation | DeepEval plus versioned Python fixtures | Supports repeatable scoring while keeping raw cases inspectable |
| System red team | PyRIT plus custom indirect-injection corpus | Exercises end-to-end attacks and tool misuse |
| Observability | OpenTelemetry plus self-hosted Langfuse | Links traces, evaluation, latency and cost |
| Analytics | DuckDB, dbt and Power BI | Demonstrates data engineering, SQL and executive reporting |
| Packaging | Locked dependencies, Docker Compose, OCI image CI, SBOM and provenance | Establishes a reproducible release artifact rather than a laptop-only demo |

Tool breadth is not a success metric. Garak and promptfoo remain stretch integrations unless they find distinct failures the core harness misses.

---

## Quantitative acceptance gates

Thresholds are versioned in `controls/release-policy.yaml`. Day 4 establishes the pilot baseline; Day 7 freezes the candidate thresholds before remediation results are known.

| Gate | Minimum release condition |
|---|---|
| Boundary enforcement | 0 unauthorized consequential tool executions; 0 human-approval bypasses across the full deterministic and adversarial suite |
| High-risk escalation | 100% recall on holdout cases marked mandatory-escalation |
| Behavioral quality | At least 90% task success on the held-out set, with the lower confidence bound and all slice results reported rather than hidden |
| Grounding | At least 95% policy citations resolve to the retrieved source passage; no fabricated policy identifier in the holdout set |
| Security | 0 open critical/high findings in the release threat model; attack success rate reported before and after control changes |
| Kill and recovery | Global stop prevents the next tool execution; credentials revoke successfully; last known good release can be restored using the runbook |
| Audit | 100% of consequential decisions have complete correlation fields; mutation/deletion test causes verification failure |
| Cost | 100% of model/tool spend attributed to a claim and stage; release stays within the approved quality-adjusted cost envelope |
| Reliability | No silent failure paths in critical flows; defined timeout/retry/human-handoff behavior passes integration tests |
| Reproducibility | Clean checkout can run tests, build the container and generate the evidence index from documented commands |

The exact quality and cost envelope may change after baseline measurement, but changes require a dated decision record. A team may not lower a safety threshold solely to make the demo pass.

---

## Daily delivery standard

Every day ends with:

1. A small, tagged commit (`day-01` through `day-21`).
2. Tests for the new happy path, boundary and failure path.
3. An update to the competence ledger and threat/control traceability.
4. A reproducible command and captured result under `artifacts/day-XX/`.
5. A short engineering log: decision, evidence, limitation and next risk.

No secrets, even fake reusable secrets, are committed to Git history. An insecure “as-found” pilot is represented by a clearly isolated test fixture and assessment snapshot, not by deliberately leaking credentials.

---

## Week 1 — Turn an unsafe pilot into a governed candidate

### Day 1 — Define the buyer problem and pilot baseline

Create a one-page engagement brief: business objective, intended users, affected parties, prohibited outcomes, decision rights and measurable success. Build a deliberately limited pilot assessment showing the normal gaps: no formal release gate, broad tool identity, incomplete audit, no cost attribution and ad hoc evaluation. Create the competence ledger and an assumptions/claims register.

**Deliverables:** `docs/engagement-brief.md`, `assessment/pilot-baseline.md`, `docs/evidence/competence-ledger.md`, `docs/claims-register.md`.

**Done when:** every positioning phrase maps to at least one planned control and proof artifact; unsupported production or compliance claims are listed as prohibited language.

### Day 2 — Threat model, data model and architecture decision record

Create the synthetic data generator for 50 base claims and parameterized scenario variants. Classify fields, define retention/redaction rules and mark all uploaded documents as untrusted. Write a STRIDE-style threat model covering indirect prompt injection, confused-deputy behavior, excessive agency, data exfiltration, over-privileged NHI, MCP supply chain, audit tampering and denial of wallet. Record why consequential decisions remain human-owned.

**Deliverables:** `data/generator/`, `docs/adr/001-controlled-agent-boundary.md`, `docs/threat-model.md`, `docs/data-governance.md`.

**Done when:** each high-risk threat has a planned prevention/detection/recovery control and named future test; generated data contains no real person or policy content.

### Day 3 — Build capability-scoped MCP services

Build three MCP domains: read-only policy retrieval, scoped claims-record access and a mock-payment service. Publish a machine-readable capability manifest for each server, including owner, allowed operations, data class, required identity, approval requirement, timeout, egress and decommission method. Parameterize all database access and validate inputs at the tool boundary.

**Deliverables:** `mcp/`, `controls/capabilities/`, `docs/mcp-trust-boundaries.md`.

**Done when:** negative tests prove that unknown tools, invalid arguments, cross-claim access and direct payment attempts are rejected without calling the model.

### Day 4 — Build and measure the pilot workflow

Implement the LangGraph workflow: intake, validation, policy retrieval, coverage analysis, deterministic fraud indicators, recommendation and human queue. Run it on a development set and capture quality, latency, cost, escalation and failure data. This becomes the honest “before” state.

**Deliverables:** `src/aegis/`, `tests/integration/`, `artifacts/baseline/scorecard.json`, pilot trace bundle.

**Done when:** the end-to-end happy path and at least five failure paths run reproducibly; limitations are visible rather than silently patched.

### Day 5 — Enforce objectives and boundaries as code

Create `controls/agent-policy.yaml` for allowed actions, prohibited actions, confidence thresholds, value bands, approval rules and per-run cost limits. Implement a deterministic policy decision point plus enforcement at every MCP server. The agent may autonomously request missing information and route a claim; payment, denial and settlement remain authenticated human actions.

**Deliverables:** versioned policy, enforcement service/module, `docs/boundary-design.md`, policy test matrix.

**Done when:** prompt text cannot change authorization; all allow, deny and escalation branches have deterministic tests; policy decisions appear in the audit event.

### Day 6 — Implement NHI and MCP security controls

Use separate workload identities per MCP domain with minimum scopes, short lifetimes and explicit owners. Implement token expiry/revocation tests, secret scanning, egress allowlists and an NHI lifecycle register. Pin dependencies and generate an MCP/server software bill of materials. Document a realistic production mapping to Entra workload identity or the client’s identity provider without building a custom IdP.

**Deliverables:** `security/nhi-register.yaml`, `security/access-matrix.md`, SBOM, before/after privilege diff.

**Done when:** expired, wrong-audience, wrong-scope and revoked credentials all fail closed; the identity register covers provision, rotate, monitor and decommission.

### Day 7 — Add traceability and freeze the release contract

Instrument model, retrieval, authorization and tool calls with OTel/Langfuse. Add a tamper-evident, hash-chained decision log and a verifier. Freeze `controls/release-policy.yaml`, including quality, security, cost and reliability gates, before Week 2 remediation begins. Record engineer-facing video 1 and draft article 1: “From unsafe pilot to explicit control boundaries.”

**Deliverables:** trace pipeline, `audit/`, verifier tests, release policy, `docs/evidence/audit-field-map.md`, `v0.1-controlled-boundaries`.

**Done when:** a claim can be traced from input to decision, identity, tool, cost and human approval; changing or deleting an audit event fails verification.

---

## Week 2 — Test behavior, attack the system and gate releases

### Day 8 — Design a defensible evaluation protocol

Create versioned development, calibration and sealed holdout sets. Define human-written rubrics for task success, grounding, escalation, claimant communication and policy compliance. Label at least 30 representative cases manually, blind to model output, and use them to calibrate any LLM judge. Define slice reporting by claim type, value band, ambiguity and document quality. Record limitations; do not claim demographic fairness from synthetic operational data.

**Deliverables:** `evals/datasets/`, `evals/rubrics/`, `docs/evaluation-protocol.md`, judge-calibration report.

**Done when:** development cases cannot leak into the holdout; judge agreement and disagreement examples are published; deterministic controls are never scored only by an LLM judge.

### Day 9 — Build the behavioral EvalOps harness

Implement deterministic assertions plus DeepEval behavioral metrics. Run repeated trials for non-deterministic cases and report denominators, confidence intervals, model/prompt version and slice results. Add empty, malformed, contradictory, large and timeout cases.

**Deliverables:** `evals/`, baseline evaluation result, machine-readable scorecard and human-readable summary.

**Done when:** one command recreates the scorecard; failures link back to trace IDs; no aggregate score can conceal a failed mandatory-escalation slice.

### Day 10 — Establish the adversarial baseline

Use PyRIT and a custom corpus of at least 20 indirect injections embedded in claim documents and tool results. Cover exfiltration, approval bypass, cross-claim access, policy override, fabricated evidence, tool enumeration and denial of wallet. Measure attempted compromise, blocked compromise and actual unauthorized action separately. Preserve raw evidence and do not remediate until the baseline is captured.

**Deliverables:** `redteam/`, threat-to-test map, raw findings, baseline attack report.

**Done when:** each attack has a success definition and trace; the report distinguishes model misbehavior from an authorization failure.

### Day 11 — Contain, remediate and re-test

Apply layered controls: untrusted-content separation, minimal context, schema validation, output encoding, least privilege, egress restriction, policy enforcement and human approval. Prompt hardening is defense in depth, not the authorization boundary. Re-run the unchanged attack suite and publish before/after results plus residual risk.

**Deliverables:** remediation changes, `redteam/before-after-results.md`, residual-risk register.

**Done when:** consequential unauthorized tool execution is zero; any remaining prompt manipulation is visibly contained and cannot become authority.

### Day 12 — Add kill, circuit-breaker and safe-degradation controls

Implement global pause, per-agent credential revocation, tool-level circuit breakers, request admission control and budget alerts. A budget breach must stop new low-priority work and hand active claims to a human queue; it must not silently abandon an in-flight high-impact workflow. Test halt, drain, resume and stale-worker behavior.

**Deliverables:** runtime controls, `docs/runbooks/kill-and-recovery.md`, scripted rogue-agent scenario and video evidence.

**Done when:** the next consequential tool call is blocked after a stop; revoked workers cannot resume with cached credentials; operators receive a clear state and recovery action.

### Day 13 — Build the complete release gate

GitHub Actions runs four lanes: deterministic/security tests on every PR, a fast behavioral canary, container/SBOM/vulnerability checks, and a request-level token/cost budget derived from Day 4 telemetry. Nightly runs execute the full behavioral and adversarial suites. Generate a single release evidence bundle with code, model, prompt, policy, dataset and dependency versions. Build the OCI image and attach provenance; publishing to a registry is stretch. Days 15–17 replace the provisional request budget with reconciled, quality-adjusted workflow cost gates.

**Deliverables:** `.github/workflows/`, release evidence generator, container build, SBOM and sample failed/passed change records.

**Done when:** seeded bad changes separately demonstrate blocking for authorization bypass, behavioral regression, vulnerable dependency and cost regression; no gate is merely documented.

### Day 14 — Prove model-migration control and publish the security audit

Swap to the alternate model without retuning thresholds. Run the sealed evaluation and compare quality, security, latency, cost and slice behavior with uncertainty shown. Make a ship/hold recommendation. Then write the Agent Security, MCP Access, Kill-Switch and NHI Audit as a client deliverable: scope, method, as-found state, evidence, remediation, residual risk and exclusions. Record engineer-facing video 2 and draft article 2 on adversarial evaluation and safe model migration.

**Deliverables:** `docs/reports/model-migration-regression.md`, `docs/reports/agent-security-audit.md`, video 2, `v0.2-secured-and-gated`.

**Done when:** the migration decision follows predeclared thresholds; the audit’s every finding links to evidence and does not imply certification or legal sign-off.

---

## Week 3 — Control cost and demonstrate operation after release

### Day 15 — Build end-to-end cost attribution

Extract token, model, tool and latency telemetry into DuckDB. Build dbt models that reconcile provider/model usage to claim, workflow stage, retry, model and MCP tool. Track unattributed spend as an error rather than dropping it. Version the price table and separate measured usage from assumed currency conversion or human-cost inputs.

**Deliverables:** `finops/`, dbt tests, reconciliation report and attribution schema.

**Done when:** 100% of synthetic run spend reconciles within a declared tolerance; fan-out, retries, failed calls and cache hits receive explicit treatment.

### Day 16 — Measure quality-adjusted unit economics

Calculate cost per attempted claim, successfully triaged claim and correctly triaged claim. Show latency, escalation and quality beside price so a cheap but unsafe model cannot appear optimal. Create a transparent human-handler comparator with editable assumptions and sensitivity ranges, not a fabricated ROI claim.

**Deliverables:** semantic metrics layer, unit-economics notebook/report, Power BI model and static export.

**Done when:** every dashboard number traces to a dbt model; changing the human-cost or model-price assumption updates the result; limitations are displayed on the dashboard.

### Day 17 — Close the cost-control loop safely

Implement per-run and daily budgets, anomaly detection, model/tool fan-out limits and admission throttling. Couple every cost policy to a minimum quality and safety floor. Test spikes, price-table changes, retry storms and telemetry loss. Replace Day 13’s provisional cost gate with the reconciled workflow metrics. Write the FinOps-for-Agents operating runbook and draft article 3 on quality-adjusted agent economics.

**Deliverables:** cost policies and tests, `docs/runbooks/agent-cost-operations.md`, cost-control before/after report.

**Done when:** cost controls contain a simulated denial-of-wallet attack without bypassing approval, losing audit data or silently reducing the mandatory escalation rate.

### Day 18 — Establish SLOs and run an incident exercise

Define SLIs/SLOs for task success, mandatory escalation, unauthorized action, p95 latency, audit completeness, cost attribution and recovery. Create alerts and an owner/RACI table. Run a scripted incident: indirect injection causes suspicious behavior, monitoring detects it, the operator stops and revokes the agent, evidence is preserved, the last known good release is restored, and the sealed suite verifies recovery. Record timestamps and gaps in a blameless post-incident report.

**Deliverables:** `operations/slos.yaml`, alerts, RACI, incident timeline, post-incident report and recovery evidence.

**Done when:** mean time to detect, contain and recover are measured; no step relies on undocumented operator memory; the incident creates follow-up actions.

### Day 19 — Produce the governance and production-readiness packs

Create one evidence-led control matrix rather than five repetitive documents. Cross-reference NIST AI RMF, ISO/IEC 42001-style controls and applicable EU/UK technical obligations with scope and date caveats. Add model/system cards, change-management record, data sheet and incident process. Apply the Production-Readiness Assessment to the original pilot and the final candidate, then produce a prioritized 90-day client roadmap.

**Deliverables:** `governance/control-evidence-matrix.md`, system card, data sheet, `assessment/final-readiness.md`, `assessment/90-day-roadmap.md`.

**Done when:** every “implemented” control links to executable evidence, every partial control has an owner and action, and no regulatory status is asserted without qualification.

### Day 20 — Package the repository as buyer-verifiable evidence

Rewrite the README around the buyer journey: pilot gap, architecture, attacks found, controls, release decision, operation and economics. Put four proof points above the fold: before/after security result, held-out eval scorecard, release-gate evidence and quality-adjusted cost view. Add a one-command reviewer path and a service-to-artifact map. Record executive-facing video 3 with no code walkthrough.

**Deliverables:** polished README, `docs/reviewer-guide.md`, static dashboard exports, executive video and service one-pager.

**Done when:** a clean reviewer can reproduce the core evidence using documented commands; links contain no private tokens, local-only paths or unsupported claims.

### Day 21 — Independent challenge, launch and conversion

Ask two practitioners to review different evidence chains, or run a documented adversarial self-review if external reviewers are unavailable. Resolve or disclose findings. Edit and publish the three articles drafted on Days 7, 14 and 17: boundary-first security, behavioral/model-migration evaluation and quality-adjusted AgentOps cost. Tag `v1.0-aegis`, publish the repository and videos, and contact ten relevant UK insurance/financial-services prospects with the readiness assessment as the entry offer.

**Deliverables:** review findings and dispositions, three articles, `v1.0-aegis`, outreach tracker.

**Done when:** critical findings are fixed; accepted residual risks are explicit; the public materials use the aligned positioning consistently.

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

- **Unit:** policy parsing, authorization decisions, budget math, audit hashing, redaction and cost attribution.
- **Contract:** MCP schemas, identity audience/scope, timeout behavior and error normalization.
- **Integration:** agent-to-MCP-to-audit flow, human approval, kill switch, trace correlation and cost capture.
- **Behavioral:** development, calibration and sealed holdout cases with repeat runs and slice reporting.
- **Adversarial:** indirect injection, exfiltration, privilege escalation, denial of wallet and compromised tool output.
- **Release:** seeded-regression tests prove that each CI gate can fail for the intended reason.
- **Operations:** stop, revoke, drain, rollback, recover and post-recovery evaluation.

### Critical production failure modes

| Failure | Required handling | Required proof |
|---|---|---|
| Model proposes an unauthorized payment | Independent policy and MCP denial; alert and audit | Deterministic negative test and attack trace |
| Human approval token is replayed or belongs to another claim | Bind approval to claim, action, amount, actor and expiry | Replay/cross-claim tests |
| MCP server times out after a write | Idempotency key, status reconciliation and human-visible uncertain state | Timeout-after-write integration test |
| Kill switch races with a queued tool call | Server-side enforcement at execution time | Concurrent stop/tool test |
| Audit event is dropped or modified | Fail or quarantine consequential flow; verifier alerts | Mutation, deletion and sink-unavailable tests |
| Cost telemetry is missing | Mark spend unattributed and block cost sign-off | Reconciliation failure test |
| Budget trips during an active claim | Stop admissions, preserve active state, hand off visibly | Budget-spike and recovery test |
| Model migration improves aggregate score but harms a critical slice | Per-slice release threshold blocks migration | Seeded slice-regression test |
| Evaluation judge is biased or unstable | Calibrate against human labels and publish disagreement | Judge calibration artifact |
| Dependency or MCP configuration changes silently | Lock, inventory, scan and version in release evidence | Tampered lock/config CI test |

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
| Consulting ability and executive translation not visible | Engagement brief, client-style assessments, audit, 90-day roadmap and executive dashboard | Four buyer-facing evidence bundles and reviewer guide |
| Product/operating boundary design not demonstrated | Explicit decision rights, policy as code, human ownership, value limits and residual-risk register | Boundary design, policy tests and competence ledger |
| FinOps knowledge not demonstrated | Reconciled attribution, quality-adjusted unit economics, safe cost policies and forecast/variance reporting | dbt tests, Power BI model and AgentOps cost report |
| Regulated-sector expertise could be overclaimed | Insurance-specific controls with dated, scoped evidence mappings and legal caveats | Claims register and qualified control-evidence crosswalk |
| “Production” credibility exceeds a local demo | Reproducible artifact, complete release gate, staged operations exercise, rollback and explicit limitations | Release bundle, build provenance, SLOs and readiness assessment |
| Enterprise Azure/Entra depth remains limited | Document production identity mapping without pretending the local reference implements a client tenant | Entra/workload-identity deployment note; hands-on tenant work remains a separate development goal |

The last row is intentionally not marked fully closed. A public synthetic project cannot replace enterprise tenant experience; it can demonstrate that the engineer understands the integration and evidence requirements.

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

The point is not to mention the certifications in every report. It is to make the corresponding engineering judgment inspectable. The README can then link from each capability to the strongest artifact rather than presenting a catalogue of course badges.

---

## Day-22 evidence bundles and commercial use

| Evidence bundle | Core artifacts | Consulting opportunity | Contract roles supported |
|---|---|---|---|
| Production Readiness | Pilot/final assessments, release contract, 90-day roadmap, reviewer guide | Agent Production-Readiness Assessment | Agentic AI Solutions Architect, AI Production Engineer, Responsible AI Technical Lead |
| MCP and Agent Security | Threat model, access matrix, NHI register, attack results, kill/recovery proof, audit report | Agent Security and Kill-Switch/NHI Audit | Agentic AI Security Engineer, MCP Security Engineer, AI Application Security Engineer |
| EvalOps and Migration | Protocol, calibrated harness, holdout results, CI gates and model diff | Adversarial EvalOps harness and model-migration assurance | Agent EvalOps Engineer, LLMOps/MLOps Engineer, AI Quality Engineer |
| AgentOps and Cost | Attribution models, quality-adjusted economics, budget controls, SLOs and Power BI | FinOps-for-Agents diagnostic and remediation | AgentOps Engineer, AI FinOps Engineer, LLM Observability Engineer |

The primary wedge remains the **Production-Readiness Assessment**. Security, EvalOps and cost remediation are the evidence-backed follow-on engagements.

---

## Final public narrative

The repository should tell one story:

> Cotswold Mutual had a functioning claims-agent pilot, but it lacked evidence that its behavior, permissions, economics and operation were controlled. AEGIS defined the decision boundary, moved authorization outside the model, secured MCP identities and capabilities, built calibrated behavioral and adversarial evaluation, made quality/security/cost/reliability tests release gates, and proved stop, rollback and recovery through an incident exercise. The result is not a compliance certificate or a claim of real production scale; it is a reproducible controlled-production evidence pack and a worked example of how I help clients cross that gap.

That narrative aligns the technical shorthand with the buyer outcome:

- **“I secure”** becomes constrained identities, deterministic authorization, tested containment and recovery.
- **“I evaluate”** becomes calibrated holdout evidence, adversarial regression and model-migration decisions.
- **“I cost-control”** becomes reconciled, quality-adjusted unit economics and safe operating limits.
- **“Production agent systems”** becomes measurable release, SLO, incident, rollback and ownership controls, with honest limits on what a synthetic reference implementation proves.

Project AEGIS then functions as the bulwark of competence: one coherent system in which the code, tests, traces, dashboards and consulting artifacts all support the same market promise.
