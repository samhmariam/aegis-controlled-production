# AEGIS Resource & Reference Guide

A companion to the Project AEGIS build plan. This guide separates authority from implementation so that a useful current tool is not mistaken for a durable standard. Every entry belongs to one of five classes:

1. **Citable control authority [N]** — law, regulation, an RFC, or recognised regulatory, standards, assurance, or control guidance. These sources define legal obligations or accepted language for defining, assessing, and mapping controls.
2. **Interoperability standard [I]** — a governed protocol, schema, or data format such as MCP, OpenTelemetry, CycloneDX, or FOCUS. These provide portable boundaries.
3. **Preferred implementation [P]** — a selected framework or tool. Selection requires active maintenance, a suitable licence, exportable data, version compatibility, a documented security posture, and a replacement boundary; foundation ownership is helpful but not mandatory.
4. **Supporting research or practitioner analysis [R]** — papers, benchmarks, and expert commentary that inform design and test coverage but do not define compliance.
5. **Deep-dive reference [D]** — books, long-form treatments, and structured courses held as *lookup* references for a named weakness. A `[D]` entry is a place to go when a specific decision is blocked; it is never a syllabus, a prerequisite, or a queue to work through. Listing is not activation (§10).

`[N]` denotes citable control authority—accepted language for defining, assessing, and mapping controls—not necessarily a legally binding obligation. Legal obligations arise only from applicable regulatory instruments and binding legal requirements.

The **staying-power test** therefore varies by class. Authorities are checked for provenance and currency; standards for governance, adoption, and versioned compatibility; implementations for maintenance health, licence, portability, security, and replaceability; research for methodological relevance and reproducibility; and deep-dive references for whether the edition is current and whether the weakness they resolve is one AEGIS actually has. No implementation is treated as permanent merely because it is popular.

**Linking policy:** deep links are given where URLs are canonical and stable (specs, GitHub repos, arXiv, RFCs); fast-moving pages (regulatory guidance, vendor doc trees) get the authoritative root plus what to navigate to, because a root that always works beats a deep link that 404s in week three.

Rule of use: **pin every package version in the lockfile, record every specification revision and model identifier in the release evidence bundle, and follow the three watchlist cadences in §11 — automated, weekly-while-in-use, and phase-entry.** A listed alternative is not assumed to be drop-in compatible: the retained interface, exported data, conversion work, invariant tests, and acceptance gate must be recorded before migration.

**Learning-resource boundary:** this guide is not a syllabus. Books, courses, and credentials remain governed by the [Just-in-Time Development Register](docs/development-register.md) under the principle “build by default; learn only when a named weakness blocks a decision, artifact, or commercial interaction; stop when that weakness is resolved well enough to continue.” A learning resource does not enter the Resource Decision Register unless it becomes a cited input to release evidence or a client-facing claim.

§10 exists to serve that principle rather than to bypass it. The register answers *whether* to spend time on a resource and for how long; §10 answers *which* resource to reach for once that decision has already been made, so a blocked decision does not also become a search problem. **Listing a `[D]` resource creates no obligation to read it, no reading order, and no prerequisite for any milestone.** Activation still requires the register's four-gate decision, timebox, validation, and stop rule, and consulting a chapter to settle one question is the expected mode — not working through a book.

---

## Start here — the minimum viable reference path

This guide catalogues roughly 120 sources. Consumed at that volume it becomes the syllabus it says it is not, and the project never starts. **The default path is small; everything else waits for a question.**

### Preflight — four to six hours, once, before Day 1

| # | Read | Scope limit |
|---|---|---|
| 1 | The governing plan and this guide's use rules — resource classes, staying-power test, register, development-register principle | The rules, not the catalogue |
| 2 | [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | The ten categories and their mitigation summaries, to seed the Day 2 threat model — not every linked OWASP paper |
| 3 | [MCP `2026-07-28`](https://modelcontextprotocol.io/specification/2026-07-28) — [release notes](https://blog.modelcontextprotocol.io/posts/2026-07-28/), tools, transport, authorization and security sections; then the SDK protocol-versions page and the [conformance suite](https://github.com/modelcontextprotocol/conformance) README | Those sections only; the OAuth RFCs come later and only where the spec invokes them |
| 4 | Anthropic on [building effective agents](https://www.anthropic.com/engineering/building-effective-agents) and [effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Both are short and directly validate the constrained-workflow architecture |
| 5 | **Environment preflight** — Python compatibility, model API access for both providers, Azure subscription and region availability, **Entra administration rights**, GitHub OIDC capability, expected cloud cost | Operational validation, not study. This is a Day 0 gate in the governing plan: access has procurement lead time, and nothing on Days 22–28 can begin without it |
| 6 | A concise STRIDE treatment, or the relevant Shostack chapter — **only if the method is unfamiliar** | One chapter before Day 2, never the whole book |

Then begin Day 1.

### Consult at the consuming milestone

| Phase | Primary sources only |
|---|---|
| Threat model (Day 2) | OWASP ASI 2026; one STRIDE chapter if needed |
| MCP and identity (Days 3, 6, 23a–23b) | Pinned MCP revision; SDK docs; conformance suite; OWASP MCP guidance; only the RFC/JWT sections the spec invokes |
| Workflow (Days 4–5) | LangGraph docs; the two Anthropic articles |
| Evaluation (Days 8a–9) | DeepEval docs; Brown/Cai/DasGupta; the statsmodels fixture; PyRIT docs |
| Audit and release (Days 7a–7b, 13a–13b, 20) | OTel conventions; SLSA verification model; GitHub attestations; CycloneDX |
| Cost (Days 15–17) | Provider usage/billing docs; DuckDB; dbt-duckdb; Power BI only once metric definitions and totals are frozen |
| Incident operations (Days 12, 18, 27a) | The relevant SRE Workbook chapters; NIST SP 800-61r3 |
| Governance (Days 19a–19b) | NIST AI RMF and GenAI Profile; official Commission, EUR-Lex, ICO and FCA sources |
| Integration (Days 22–28) | The official Azure, Entra, PostgreSQL, Service Bus and Bicep documentation **for the seam currently being built** — §9, one subsection at a time |

### The research rule

One primary reference per blocked decision. Timebox the research to 60–120 minutes. Require it to produce or change a named artifact, test, or decision. Stop when that validation passes. Anything larger is a development-register decision with its own four gates, timebox, and stop rule — not a reading session.

### Deferred from the base v1.0 critical path

Later, not never. Each of these is catalogued in full below, and each has a named activation point:

| Deferred | Activate at |
|---|---|
| FOCUS implementation (§7) | Day 22, as a narrow 1.4 bridge once Azure billing exists |
| Separate CycloneDX AI/ML-BOM generation (§6) | Post-v1.0; the small model register carries v1.0's model-inventory requirement |
| Pandera or Great Expectations (§9.2) | Only if the batch seam needs tabular expectations pydantic and dbt tests cannot express |
| promptfoo and garak (§4) | Only on a recorded migration decision; they stay out of routine review until then |
| OpenTofu or Terraform evaluation (§9.6) | Only if Bicep proves genuinely unsuitable for the staging estate |
| Commercial and consulting books (§10) | Only once a market trigger fires — a qualified proposal, repeated role requirement, recruiter screen, or prospect objection |
| Full ISO, NIST, RFC or regulatory reading | Never in full; read the section a specific artifact requires |

---

## 1. Security standards & threat frameworks (Days 2, 10–11, 14, 19a–19b, 22)

These are the authorities your threat model, red-team scoping, and audit report must cite. Buyers recognise them; auditors expect them.

| Resource | What it is | Use in AEGIS |
|---|---|---|
| [N] [OWASP Top 10 for Agentic Applications 2026 (ASI01–ASI10)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | The peer-reviewed agentic risk taxonomy (goal hijack, tool misuse, identity abuse, supply chain, memory, inter-agent comms, cascading failures, rogue agents), published Dec 2025 by the [OWASP GenAI Security Project](https://genai.owasp.org/) | Primary structure for the Day 2 threat model and the threat-to-test matrix; cite ASI IDs in the security audit findings |
| [N] [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) | The model-layer risk list (prompt injection LLM01 remains #1) | Covers the model-layer rows of the threat model that the agentic list assumes |
| [N] [OWASP Agentic Security Initiative MCP guidance](https://genai.owasp.org/initiatives/agentic-security-initiative/) (navigate to the practical guides for secure MCP server development and third-party MCP servers) | Official MCP-specific guidance from the OWASP GenAI Security Project; do not cite an "OWASP MCP Top 10" unless OWASP publishes a canonical document with that title | The checklist behind the Day 3 capability manifests and Day 6 MCP controls; pairs directly with your CMCPSE |
| [N] [MITRE ATLAS](https://atlas.mitre.org/) | Adversarial ML/AI tactics-and-techniques matrix, the AI sibling of ATT&CK | **Selective mapping, not corpus design.** Every attack carries a stable internal AEGIS test ID and exactly one primary OWASP ASI category; add an LLM Top 10 ID only where it clarifies a model-layer failure, and an ATLAS technique ID only for material findings, clean technique matches, or the SOC-facing section of the report. Blanket ATLAS tagging creates taxonomy work without improving the test, and some agentic cases do not map cleanly to a matrix built around model-centric techniques |
| [N] [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) + [Generative AI Profile, NIST AI 600-1 (PDF)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) | The govern/map/measure/manage risk framework US-aligned enterprises anchor to; AI RMF 1.0 is under revision, so record the cited version and publication date | Backbone of the Day 19 control-evidence crosswalk |
| [N] [ISO/IEC 42001](https://www.iso.org/standard/81230.html) | AI management-system standard (certifiable); pair with ISO/IEC 23894 (AI risk guidance, findable via [iso.org](https://www.iso.org/)) | Crosswalk rows in the governance pack; do not claim certification — map controls only |
| [R] [Cloud Security Alliance — AI research](https://cloudsecurityalliance.org/research/topics/artificial-intelligence) | CSA research on agentic AI, identity and governance (incl. the 2026 agent-incident survey used in your market research) | Citable statistics and control patterns for the audit's context section; verify the underlying study before repeating a statistic |
| [R] [Simon Willison — prompt-injection tag](https://simonwillison.net/tags/prompt-injection/) and [the lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) | Practitioner analysis of why injection remains difficult and why containment is a necessary defence | Grounding for the Day 11 remediation philosophy; clearly attribute it as practitioner analysis rather than a control authority |
| [R] ["Design Patterns for Securing LLM Agents against Prompt Injections" (arXiv:2506.08837)](https://arxiv.org/abs/2506.08837) | The pattern catalogue (plan-then-execute, context-minimisation, dual-LLM, action-selector) | Justifies the AEGIS architecture choice: deterministic authorization outside the model |

**[N] UK/EU regulatory sources (Day 19 crosswalk):** use the [European Commission's AI Act FAQ and implementation timeline](https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act), [AI Omnibus entry-into-force notice](https://digital-strategy.ec.europa.eu/en/news/ai-omnibus-enters-force), and [Article 50 transparency guidance](https://digital-strategy.ec.europa.eu/en/policies/guidelines-ai-transparency-obligations) as the primary authorities. As of 13 August 2026, the Commission identifies 2 December 2027 for Annex III high-risk-system rules, 2 August 2028 for high-risk systems embedded in regulated products, and 2 August 2026 for Article 50 transparency obligations. Treat the [EU AI Act Explorer](https://artificialintelligenceact.eu/) as a secondary navigation aid, not the control authority; verify dates against Commission guidance and EUR-Lex on the day a client-facing crosswalk is issued. UK: [ICO — AI guidance hub](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/) and [FCA — innovation & AI](https://www.fca.org.uk/firms/innovation) (navigate to AI Lab).

The Day 19 crosswalk must include a dated, counsel-reviewable AI Act classification determination recording the system boundary, intended purpose, provider/deployer role, Article 6 classification route, applicable Annex III entry or reason none applies, any Article 6(3) exception relied upon, and the independently applicable Article 50 transparency analysis. For AEGIS's motor/property claims-triage reference scope, the documented working hypothesis is that Annex III point 5(c) does not apply because that entry concerns individual risk assessment and pricing for life and health insurance, while current [Commission draft classification guidance](https://ai-act-service-desk.ec.europa.eu/en/essential-services) treats claims validation and payment determination as distinct claims-management activities; the guidance and this project determination are not legal advice, and the conclusion must be reassessed if the product line, intended purpose, decision authority, deployment context, or controlling guidance changes.

**Day 19 classification determination — minimum record:**

1. Decide whether the system is an AI system within the Act and cite the definition and facts relied upon.
2. Test the Article 6(1) Annex I regulated-product route.
3. Test the intended purpose against every plausibly relevant Annex III use case; record both positive and negative reasoning.
4. If the system falls within Annex III, assess and evidence any Article 6(3) exception separately rather than using an exception as the initial classification test.
5. Assess Article 50 independently of high-risk status, including whether a claimant interacts directly with AI or receives generated content; do not imply that Article 50 automatically applies to every non-high-risk system.
6. Identify other applicable regimes, including data-protection, automated-decision, consumer, and insurance requirements; an out-of-scope Annex III conclusion is not an unregulated-system conclusion.
7. Record the conclusion, owner, evidence, legal-review status, decision date, and reclassification triggers. At minimum, triggers include a change to product line, intended purpose, autonomy or decision authority, affected population, deployment jurisdiction, model capability, or controlling law/guidance.

---

## 2. Agent framework & models (Days 4–5)

| Choice | Selection basis | Pre-evaluated alternative (not drop-in) |
|---|---|---|
| [P] [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview) | Open orchestration framework with typed state graphs, first-class human-in-the-loop interrupts, durable execution, and checkpointing for resume-after-stop; these capabilities directly support the Day 5 approval and recovery controls | [Claude Agent SDK](https://docs.claude.com/) (navigate: Agent SDK) for a Claude-centred stack, or [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) for Azure-centric clients. Either requires an adapter and invariant-test migration; neither is a drop-in replacement |
| [P] [Claude API docs](https://docs.claude.com/) | Baseline model; strong tool-use and long-context behaviour; platform docs include agent and tool-use patterns worth reading regardless of framework | Any second provider serves the Day 14 migration exercise — that's the point |
| [P] Alternate model (one only) | Required for the model-migration regression demo; pick a provider with a published deprecation/versioning policy so the exercise mirrors real client pain | — |

**[R] Read before Day 4:** Anthropic's engineering posts on [building effective agents](https://www.anthropic.com/engineering/building-effective-agents) and [effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — the "workflows vs agents" distinction and context-minimisation guidance directly justify keeping AEGIS a constrained workflow with narrow autonomy, which is the defensible design for a claims use case.

**[P] Python toolchain:** Python 3.12+, [uv](https://docs.astral.sh/uv/) (Astral) for dependency management and locking; [ruff](https://docs.astral.sh/ruff/) for lint/format; [pydantic v2](https://docs.pydantic.dev/) for schemas at every trust boundary; and [pytest](https://docs.pytest.org/) for deterministic tests. The selection is based on active releases, supported Python versions, reproducible locking, typed boundaries, open licences, and CI suitability. Record those observable signals in the Resource Decision Register rather than relying on popularity claims.

---

## 3. MCP layer (Days 3, 6)

| Resource | Use |
|---|---|
| [I] [MCP specification `2026-07-28`](https://modelcontextprotocol.io/specification/2026-07-28) — the **default target**, subject to explicit confirmation in `docs/adr/002-mcp-protocol-contract.md` (governed by the Agentic AI Foundation under the Linux Foundation since Dec 2025) | The normative protocol reference for your three servers. This revision introduced a stateless protocol core, multi-round-trip requests, header-based routing, cacheable list results, authorization hardening and a formal extensions framework, so a pre-`2026-07-28` implementation demonstrates a superseded deployment model. Pin the dated revision independently of the SDK version and read the **security best practices**, **authorization** and [release notes](https://blog.modelcontextprotocol.io/posts/2026-07-28/) first |
| [P] [Official MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) — current line supporting `2026-07-28`; confirm the major version and read its protocol-versions documentation before pinning | Build servers with the reference SDK, not a wrapper — protocol-level fluency is the CMCPSE differentiator. The SDK's protocol-version documentation distinguishes the legacy handshake era from the stateless era, which is the compatibility-window evidence the ADR needs |
| [I]/[P] [Official MCP conformance suite](https://github.com/modelcontextprotocol/conformance) | Automated client and server conformance against a chosen spec version, with CI integration and the SDK tier assessment. **Pin the package version and record an expected-failure baseline** — the suite carries scenarios for several dated revisions and coverage for the newest one can lag the specification itself. Run it alongside the AEGIS authorization and capability-invariant tests, never instead of them |
| [P] [MCP Inspector](https://github.com/modelcontextprotocol/inspector) | Exploratory and manual inspection during Days 3 and 6; capture sessions as supplementary evidence. Inspector does not substitute for automated conformance or the AEGIS invariant suite |
| [N] [OAuth 2.1 Internet-Draft](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/) · [RFC 9700 — OAuth Security BCP](https://datatracker.ietf.org/doc/html/rfc9700) · [RFC 8414 — Authorization Server Metadata](https://datatracker.ietf.org/doc/html/rfc8414) · [RFC 7636 — PKCE](https://datatracker.ietf.org/doc/html/rfc7636) · [RFC 8707 — Resource Indicators](https://datatracker.ietf.org/doc/html/rfc8707) · [RFC 9728 — Protected Resource Metadata](https://datatracker.ietf.org/doc/html/rfc9728) · [RFC 9207 — Authorization Server Issuer Identification](https://datatracker.ietf.org/doc/html/rfc9207) | **Do not read these front to back.** Start from the pinned MCP revision's authorization requirements and consult only the RFC sections those requirements actually invoke; the stable RFCs are the control authorities the spec defers to. OAuth 2.1 remains an evolving Internet-Draft consolidation and must never be represented as a completed RFC |

| [I] [JSON Schema 2020-12](https://json-schema.org/specification) | The schema dialect MCP tool definitions are expressed in. The Day 2 protocol ADR must bound schema depth and decide how external `$ref` values are handled — an unbounded or remotely-resolvable schema is a denial-of-service and SSRF surface at the tool boundary, not merely a validation detail |

Design rule the spec supports: **capability manifests are contracts, not documentation** — Day 3's negative tests (unknown tool, invalid arguments, cross-claim access, direct payment) enforce the manifest at runtime.

---

## 4. Evaluation & testing (Days 8a–9, 12, 13a–13b, 14)

| Choice | Why | Pre-evaluated alternative (not drop-in) |
|---|---|---|
| [P] [DeepEval](https://github.com/confident-ai/deepeval) ([docs](https://deepeval.com/)) | Pytest-native LLM evaluation — the behavioural suite can run beside deterministic tests while exporting machine-readable results | [promptfoo](https://www.promptfoo.dev/) provides declarative YAML evals and CI integration, but requires a test-definition and result-schema mapping. The sealed cases, scoring policy, thresholds, and release decision must remain invariant during migration |
| [P] [PyRIT](https://github.com/microsoft/PyRIT) | Microsoft's open red-team orchestration framework; attack strategies as composable code make the Day 10 corpus reproducible evidence rather than a manual exercise. **Use `microsoft/PyRIT`** — the former `Azure/PyRIT` repository was archived on 27 March 2026 and is read-only. Recent releases have redesigned core abstractions, so pin the version and keep the corpus behind a thin adapter | [garak](https://github.com/NVIDIA/garak) is a vulnerability scanner with a different execution model. Preserve attack IDs, inputs, expected control outcomes, evidence fields, and pass/fail policy rather than assuming configuration compatibility |
| [R] [InjecAgent (arXiv:2403.02691)](https://arxiv.org/abs/2403.02691) · [dataset repo](https://github.com/uiuc-kang-lab/InjecAgent) | The reference benchmark design for *indirect* injection against tool-using agents | Model your custom 20-case corpus on its structure so reviewers recognise the methodology |
| [R] Wilson score interval and Cohen's kappa — primary sources: [Brown, Cai & DasGupta, "Interval Estimation for a Binomial Proportion", *Statistical Science* 16(2), 2001](https://projecteuclid.org/euclid.ss/1009213286) for Wilson-over-Wald, and Fleiss/Levin/Paik for kappa | Named statistical methods for holdout uncertainty and Day 8 judge calibration | Cite the method, assumptions, sample size, confidence level, and interpretation in the evaluation protocol; a named method with a primary source is auditable, while “we computed a confidence interval” is not. The thirty-case manual set is a **calibration floor** — sufficient to detect gross judge miscalibration on the primary rubrics, not to establish judge reliability broadly — and every agreement figure states that limitation beside its denominator |
| [P] [statsmodels `proportion_confint`](https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportion_confint.html) (`method="wilson"`) and sklearn/statsmodels agreement metrics | Reproducible implementations of the declared methods | Pin the libraries, test them against hand-checked fixtures, and preserve the method and expected numeric result if the implementation changes |

Principles the plan already encodes, sourced here so you can cite them: deterministic controls are never scored by an LLM judge (OWASP agentic guidance); judges must be calibrated against human labels before their scores gate anything (standard ML evaluation practice — document agreement *and* disagreement examples).

**Evaluation migration contract:** framework-specific test definitions are adapters around a versioned AEGIS case schema and result schema. A replacement is accepted only when the same sealed holdout, deterministic-control tests, scoring policy, thresholds, and release decision run successfully and any result deltas are disclosed.

---

## 5. Observability & audit (Days 5, 7a–7b)

| Choice | Why | Pre-evaluated alternative or continuity control |
|---|---|---|
| [I] [OpenTelemetry](https://opentelemetry.io/) + [GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) | Vendor-neutral telemetry boundary. GenAI attributes remain under development, so pin the semantic-convention revision and do not expose those attributes as AEGIS's canonical domain schema | Maintain a versioned internal event schema and one tested OTel mapping adapter. Contract tests must prove required fields survive exporter changes and semantic-convention attribute renames |
| [P] [Langfuse (self-hosted)](https://langfuse.com/) — **start on v4**, GA 29 July 2026; v3 cloud ingestion is retired 16 November 2026 and self-hosted v3 receives security patches only through January 2027 ([compatibility](https://langfuse.com/docs/compatibility)) | Open-source LLM observability with OTel ingestion, cost fields, exports, and self-hosting. **Four-hour stop rule on initial Docker Compose setup:** if it overruns, preserve the OTel export and canonical JSON evidence path first and return to the presentation store later — Langfuse is presentation, never the system of record | [Arize Phoenix](https://phoenix.arize.com/) or [LangSmith](https://www.langchain.com/langsmith) may replace the presentation and trace-store layer. Acceptance requires replaying a representative trace fixture and reproducing the required AEGIS fields and cost totals through the OTel boundary |
| [I]/[P] Audit chain — [Sigstore](https://www.sigstore.dev/) / [cosign](https://github.com/sigstore/cosign) for signing, [Rekor](https://docs.sigstore.dev/logging/overview/) as transparency log, [GitHub artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations) as the CI anchor | Build on SHA-256 content hashing, monotonic sequence numbers, separately controlled signer identity, signed heads, and external anchoring. Public GitHub repositories can use the Sigstore Public Good transparency log; private/internal repositories require GitHub Enterprise Cloud and have a different trust model without the same public-log property | SSH-key signing is permitted only as the local signer-verification fallback; it is **not** an external anchor. v1.0 requires a signed head anchored by separately controlled CI attestation or a transparency service, with the repository visibility, trust assumptions, verification command, expected mutation failure, and alternate anchor recorded |

**Telemetry schema rule:** AEGIS owns a small canonical event envelope for workflow, model, tool, policy-decision, token, latency, and cost identifiers. OTel and any observability product receive mapped copies. The release bundle records the internal schema version, OTel semantic-convention revision, exporter version, mapping tests, and a fixture proving that a convention change cannot silently alter the dashboard or gate metrics.

**Audit-anchor rule:** signing proves who endorsed a head; independent anchoring proves that a particular head existed outside the mutable local chain. Both properties are mandatory for v1.0. Day 7 may use the local anchor adapter as defined in the build plan, but the Day 13/20 provenance work must wire and verify the external anchor before release.

---

## 6. Supply chain & release engineering (Days 13a–13b, 20, 26a–26b)

| Resource | Use |
|---|---|
| [N] [SLSA](https://slsa.dev/) | Provenance framework. Describe the controls as **SLSA-aligned** until the builder, isolation, provenance, distribution, and verification requirements for a specific level have all been checked against the [SLSA verification model](https://slsa.dev/spec/v1.2/verifying-artifacts); an attestation alone does not establish a level |
| [P] [Sigstore](https://www.sigstore.dev/) / [cosign](https://github.com/sigstore/cosign) | Sign the container image and audit-chain heads; OpenSSF/Linux Foundation governance |
| [P] [Syft](https://github.com/anchore/syft) + [Grype](https://github.com/anchore/grype) | Generate the software-component inventory and scan it for known vulnerabilities; pin both implementations and retain their machine-readable reports |
| [I] [CycloneDX](https://cyclonedx.org/) SBOM and [AI/ML-BOM](https://cyclonedx.org/guides/OWASP_CycloneDX-Authoritative-Guide-to-AI-ML-BOM-en.pdf) | Portable inventory formats. Syft may emit a CycloneDX software SBOM, but its output must not be assumed to populate the model-specific AI/ML-BOM fields |
| [P] [pip-audit](https://github.com/pypa/pip-audit) | Python dependency vulnerability checks in the PR lane (PyPA-governed) |
| [P] [GitHub Actions](https://docs.github.com/en/actions) | The four CI lanes; use OIDC-based auth for anything that needs credentials (no long-lived secrets — practising what the NHI register preaches) |
| [P] [Docker Compose](https://docs.docker.com/compose/) | Local/staging reproducibility; the reviewer's one-command path depends on this being boring and reliable |

**Model-inventory rule:** generate and validate a separate ML-BOM or model register containing provider, immutable model identifier or dated alias, endpoint/deployment, intended use, data classifications transmitted, evaluation-suite version, limitations, model-card/provider reference, and deprecation status. Link it to—but do not conflate it with—the software SBOM.

---

## 7. Cost, analytics & the executive layer (Days 15–17)

| Choice | Why | Pre-evaluated alternative or continuity control |
|---|---|---|
| [P] [DuckDB](https://duckdb.org/) | In-process analytical SQL with a zero-service local path, open data formats, active releases, and reproducible execution for a public repository | SQLite plus [Polars](https://pola.rs/) is a pre-evaluated alternative, not a transparent substitution. The canonical input/output schemas, decimal and timestamp semantics, dbt tests, and cost totals must remain invariant |
| [P] [dbt-core](https://docs.getdbt.com/) with the [dbt-duckdb adapter](https://github.com/duckdb/dbt-duckdb) | Versioned SQL transformations, lineage, documentation, and executable tests make attribution numbers reproducible evidence | [SQLMesh](https://sqlmesh.com/) is a credible alternative, but migration requires reproducing model dependencies, tests, snapshots/incremental semantics, and published tables before acceptance |
| [P] [Power BI](https://learn.microsoft.com/en-us/power-bi/) | Advisory presentation layer and visible use of the Microsoft certification; it is not the system of record | The repository retains versioned source fixtures, dbt models/tests, DuckDB outputs, machine-readable metric definitions, and static dashboard exports. A reviewer must be able to reproduce every headline metric without Power BI or a commercial licence |
| [I] [FinOps Foundation](https://www.finops.org/) · [FOCUS billing-data specification](https://focus.finops.org/focus-specification/) — **deferred out of base v1.0**; FOCUS 1.4 was ratified 4 June 2026 | FOCUS normalizes *provider billing*, and base v1.0 has no cloud bill to normalize: Days 15–17 attribute model and tool usage from provider APIs. Building a full FOCUS layer there is specification work that does not improve the v1.0 cost proposition | **Base v1.0:** the canonical AEGIS operational-cost schema plus a provider billing adapter, carrying the three labelled layers. **Days 22–26:** add a narrow FOCUS 1.4 bridge once Azure infrastructure billing exists, implementing only the columns exercised by the reconciliation and unit-economics tests. FOCUS 1.4's invoice-reconciliation additions map closely to the three-layer model, which is what makes the bridge worth building *then*. Do not model commitments, discounts, marketplace purchases or multi-provider allocation unless the evidence uses them |
| [P] Provider usage/billing APIs — [Anthropic docs](https://docs.claude.com/) (navigate: usage & cost / admin API) plus the alternate provider's equivalent | Invoice-level reconciliation target for Day 15. Billing feeds may lag, aggregate, or differ from request-time estimates, so they cannot always provide event-level attribution | Preserve three labelled layers—request-time estimate, metered/provider usage, and billed/invoiced amount—and disclose reconciliation windows, residuals, credits, and allocation assumptions |

**Canonical analytics path:** versioned fixture or source extract → dbt transformations and tests → DuckDB evidence tables → machine-readable metric definitions → Power BI presentation → static PDF/image export. The dashboard may fail or become unavailable without invalidating the reproducible evidence path.

**Cost attribution boundary:** use the FOCUS-aligned layer for normalized provider billing and reconciliation. Use the AEGIS extension for claim/workflow ID, agent step, model route, tool call, retry reason, evaluation run, control outcome, prevented/wasted cost, and human-review cost. Never present allocated event-level cost as directly billed cost.

---

## 8. Governance & operations references (Days 12, 18, 19a–19b, 27a–27b)

- **[R]** [Google SRE Book & Workbook](https://sre.google/books/) — the SLO/error-budget vocabulary for Day 18; free online and widely understood by platform teams.
- **[N]/[R]** Incident response structure — blameless postmortem format from the SRE Workbook; [NIST SP 800-61r3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) for IR phase vocabulary so the Day 18 report reads like security IR, not improvisation.
- **[R]** Model cards & datasheets — ["Model Cards for Model Reporting" (arXiv:1810.03993)](https://arxiv.org/abs/1810.03993) and ["Datasheets for Datasets" (arXiv:1803.09010)](https://arxiv.org/abs/1803.09010); the Day 19 system card should visibly descend from them.
- **[R]** UK market context for pricing/positioning — [FCA innovation pages](https://www.fca.org.uk/firms/innovation) for sandbox cohort announcements as prospecting triggers; [ITJobsWatch](https://www.itjobswatch.co.uk/) for live day-rate benchmarks when quoting. Treat market data as dated evidence, not a durable control source.

---

## 9. Enterprise integration & cloud platform (Days 22–28)

Azure and Entra are the **mandatory reference implementation** for the integration releases, not one option among several: the build plan's downstream milestones, gates, claims, and closure rows all name them, and the AWS/GCP equivalents are documented future ports rather than build-time alternatives. Vendor documentation trees move faster than this guide, so entries give the authoritative root plus what to navigate to, per the linking policy.

### 9.1 Identity, key custody, and federation (Days 23a–23b)

| Resource | Class | Use in AEGIS |
|---|---|---|
| [Microsoft Entra docs root](https://learn.microsoft.com/en-us/entra/) — navigate to: workload identities, app registrations and service principals, workload identity federation, Conditional Access and continuous access evaluation | [P] | One app registration per MCP domain with minimum scopes; the federation pages are the reference for the secretless CI credential flow |
| [Azure Key Vault docs root](https://learn.microsoft.com/en-us/azure/key-vault/) — navigate to: keys, the RBAC-versus-access-policy permission models, soft-delete and purge protection | [P] | Audit-signer key custody with the agent and ordinary ledger writer excluded; purge protection matters because a deleted signer key destroys chain verifiability |
| [Azure Database for PostgreSQL docs root](https://learn.microsoft.com/en-us/azure/postgresql/) — navigate to: security and access control | [P] | Managed-identity connection path and the platform's role-privilege specifics |
| [RFC 7519 — JWT](https://datatracker.ietf.org/doc/html/rfc7519) · [RFC 8725 — JWT Best Current Practices](https://datatracker.ietf.org/doc/html/rfc8725) · [RFC 9068 — JWT Profile for OAuth 2.0 Access Tokens](https://datatracker.ietf.org/doc/html/rfc9068) | [N] | Control authority for the issuer, audience, expiry, and algorithm validation the MCP servers perform; §3 carries the broader OAuth RFC suite |
| [NIST SP 800-207 — Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final) | [N] | Vocabulary for per-request verification and the "never trust a token because it was valid once" position the containment window encodes |

**Revocation rule the platform imposes:** continuous access evaluation covers a supported set of service-principal and resource combinations and requires both sides to participate in the claims-challenge flow; it does not extend automatically to a custom MCP server that validates a JWT locally, and managed identities are outside its support. That is precisely why the build plan splits revocation into **issuance revocation** (a disabled principal cannot acquire a new token) and **active-token containment** (an already-issued token is rejected on every authenticated request within a declared window, protected reads included). Verify the current CAE support matrix against the Entra docs before writing the ADR; if the achievable window comes from token lifetime plus a resource-side denylist rather than CAE, record that as the named mechanism and test the cache TTL at its expiry boundary.

### 9.2 Asynchronous intake (Days 25a–25b)

| Resource | Class | Use in AEGIS |
|---|---|---|
| [Azure Service Bus docs root](https://learn.microsoft.com/en-us/azure/service-bus-messaging/) — navigate to: message transfers/locks/settlement, delivery guarantees and duplicate handling, dead-lettering, sessions, and duplicate detection | [P] | PeekLock and manual settlement semantics; the delivery-guarantee pages are the citation for why the claim is effectively-once *effect*, not exactly-once delivery |
| [Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/) (Hohpe & Woolf) — idempotent receiver, guaranteed delivery, dead letter channel, message store | [D]/[R] | The pattern vocabulary a reviewer will expect the async design to speak |
| [microservices.io patterns](https://microservices.io/patterns/) (Richardson) — transactional outbox, idempotent consumer | [R] | The canonical statement of what an outbox is for, and therefore of what it is not for |
| [Pandera](https://pandera.readthedocs.io/) or [Great Expectations](https://greatexpectations.io/) | [P] | Optional declarative validation for message and batch payload schemas; pydantic already covers the trust-boundary case, so adopt only if the batch work needs tabular expectations |

**Outbox-versus-inbox rule:** a transactional outbox makes a database state change and an *outgoing publication* atomic. It does **not** make a broker dequeue and a database write one transaction, and it is not the control that prevents an unaudited workflow start. The consumer-side design is an inbox: receive under PeekLock with manual settlement, commit the inbox/idempotency record, workflow state, and audit event in one Postgres transaction, settle the message only after that commit, and abandon on failure so redelivery deduplicates against the unique constraint. Reserve the outbox for the case where processing must emit a downstream message. Because PeekLock delivery is at-least-once by design, the published claim is an **effectively-once business effect under tested at-least-once redelivery**.

### 9.3 System of record and row-level security (Days 24a–24b)

| Resource | Class | Use in AEGIS |
|---|---|---|
| [PostgreSQL — Row Security Policies](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) · [CREATE POLICY](https://www.postgresql.org/docs/current/sql-createpolicy.html) · [CREATE ROLE](https://www.postgresql.org/docs/current/sql-createrole.html) (role attributes including `BYPASSRLS`) · [ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html) (`FORCE ROW LEVEL SECURITY`) | [N]/[P] | The normative reference for the role-topology contract: non-owner runtime role, `NOBYPASSRLS`, forced row security where the owner would otherwise bypass |
| [Alembic](https://alembic.sqlalchemy.org/) | [P] | Versioned, reversible migrations with the migration role distinct from the runtime role |
| [SQLAlchemy](https://docs.sqlalchemy.org/) | [P] | Parameterised access at the tool boundary; the session's role and connection identity are what the RLS tests must assert against |

**Role-topology rule:** RLS is proven through the role, not only through policy behaviour. A suite that connects as a well-behaved test role passes while an over-powered runtime role silently bypasses row security in the deployed system, so every assertion runs against the credentials the runtime actually uses. Table owners bypass RLS unless `FORCE ROW LEVEL SECURITY` is set, and `BYPASSRLS` defeats it outright — both are tested explicitly and excluded from runtime credentials. The scoping predicate is derived server-side from the validated workload identity, never from a client-supplied field: a model-influenced tenant predicate would widen the agent's own data access through the ORM without ever reaching the policy decision point.

### 9.4 Legacy batch interfaces and data contracts (Day 24a)

| Resource | Class | Use in AEGIS |
|---|---|---|
| *Driving Data Quality with Data Contracts* — Andrew Jones | [D] | Structure for `docs/contracts/policy-admin-batch.md`: schema, ownership, delivery expectations, and change process |
| [dbt tests](https://docs.getdbt.com/docs/build/data-tests) and [dbt-expectations](https://github.com/metaplane/dbt-expectations) | [P] | Reconciliation assertions — row counts, control totals, uniqueness, referential integrity — as executable evidence rather than a spreadsheet check |
| [RFC 4180 — Common Format and MIME Type for CSV](https://datatracker.ietf.org/doc/html/rfc4180) | [N] | Cite an actual format authority in the file contract; ambiguity about quoting and line endings is a real source of drift |
| [Azure Blob Storage docs root](https://learn.microsoft.com/en-us/azure/storage/blobs/) — navigate to: lifecycle management, immutability policies, event triggers | [P] | Batch drop location, quarantine container, and the trigger that starts ingestion |

**Reconciliation rule:** control totals and row counts are the contract's enforcement mechanism. A mismatch quarantines the whole file rather than partially loading it, because a partial load is the failure mode that silently corrupts downstream policy retrieval. Schema drift, late, duplicate, truncated, and control-total failures each get a seeded test.

### 9.5 Third-party dependency resilience (Day 24b)

| Resource | Class | Use in AEGIS |
|---|---|---|
| *Release It!* (2nd ed) — Michael Nygard | [D] | The canonical treatment of circuit breaker, timeout, bulkhead, and steady-state patterns behind the degradation design |
| [Amazon Builders' Library — timeouts, retries, and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) | [R] | The reference for why bounded retry needs jitter; vendor-published but vendor-neutral in substance |
| [Google SRE Book — Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) | [R] | Why an unbounded retry against a failing dependency is itself an outage amplifier |
| [postcodes.io](https://postcodes.io/) (Open Government Licence) or [Companies House API](https://developer.company-information.service.gov.uk/) (free, key required, rate-limited) | [P] | Candidate enrichment dependencies; record terms, rate limits, and API version in the capability manifest before first call |

**Advisory-path rule:** the third-party response informs a recommendation and never authorises an action. A forced outage must produce degraded-but-safe triage — "enrichment unavailable, flagged for human note" — rather than a blocked workflow or, worse, a fabricated value. Only synthetic, non-personal lookup values are ever sent.

### 9.6 Infrastructure as code and cloud deployment (Days 26a–26b)

| Resource | Class | Use in AEGIS |
|---|---|---|
| [Bicep docs root](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/) | [P] | Azure-native IaC with no separate state file to secure — the lower-friction default for a single-cloud reference implementation |
| [OpenTofu](https://opentofu.org/) (MPL-2.0, Linux Foundation) · [Terraform](https://developer.hashicorp.com/terraform) (BUSL-1.1 since August 2023) | [P] | If HCL is preferred over Bicep, **record the licence class in the Resource Decision Register**: the `[P]` selection criteria require a suitable licence, and BUSL is not an open-source licence. OpenTofu is the open-governance fork and the defensible choice for a public repository |
| [Azure Container Apps docs root](https://learn.microsoft.com/en-us/azure/container-apps/) — navigate to: managed identity, ingress and egress restrictions, revisions and rollback | [P] | Container runtime for the agent and MCP services, with revision-based rollback matching the runbook |
| [GitHub Actions — OIDC hardening](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments) and [Azure login action](https://github.com/Azure/login) | [P] | The federated, secretless promotion path; pin the action by full commit SHA as §6 requires |

**Promotion rule:** CI promotes the signed `v1.1-integration-controls` artifact only after the inherited v1.0 gates *and* the applicable integration gates pass, and the deployed image digest is verified against that release's signed provenance at deploy time. A build that clears only the v1.0 gates is not promotable, because the artifact carries every integration change.

### 9.7 Cloud spend, quota, and policy controls (Days 22, 26b)

| Resource | Class | Use in AEGIS |
|---|---|---|
| [Azure Cost Management docs root](https://learn.microsoft.com/en-us/azure/cost-management-billing/) — navigate to: create and manage budgets, cost alerts, exports | [N]/[P] | Tiered alerts at 50/75/90 percent; the budget pages are also the citation for the limitation below |
| Azure spending limit — same docs root, navigate to: spending limit | [P] | Offer-dependent hard stop; record subscription eligibility in the Day 22 ADR and enable it where supported |
| [Azure Quotas docs root](https://learn.microsoft.com/en-us/azure/quotas/) | [P] | Quotas are subscription-scoped and often further divided by provider and region — a resource group is **not** a quota boundary |
| [Azure Policy docs root](https://learn.microsoft.com/en-us/azure/governance/policy/) — navigate to: definition structure, assignment scopes, the deny effect | [P] | Resource-group-scoped deny rules for allowed resource types, regions, and SKUs — a policy restriction, which is a different mechanism from a numeric quota |
| [FinOps Foundation](https://www.finops.org/) FinOps-for-AI working group | [I]/[R] | Cross-reference to §7; cloud infrastructure cost enters the attribution model as a visible infrastructure class, never mixed into per-claim model or tool cost |

**Spend-control rule:** Azure budgets trigger notifications but do not stop consumption, and cost data arrives with latency, so an absolute "spend stays under cap" release gate is not implementable and is not claimed. The implementable package is: recorded spending-limit eligibility, tiered alerts, a scripted and tested teardown, capacity restrictions (recorded subscription/provider/region quotas plus resource-group-scoped Azure Policy deny rules plus explicit IaC replica and capacity limits, with an oversized deployment proven to be rejected), daily observed-spend reconciliation, and an explicit statement that billing latency prevents a universal cap. The controls bound, detect, and respond to spend; they do not guarantee a ceiling.

---

## 10. Deep-dive reference library `[D]`

**How to use this section.** These are lookup references, held so that a blocked decision does not also become a search problem. Listing creates no obligation to read, no order, and no prerequisite for any milestone. The [Just-in-Time Development Register](docs/development-register.md) still governs whether time is spent — four-gate admission, timebox, validation, stop rule — and consulting one chapter to settle one question is the expected mode. Nothing here is on the v1.0 critical path.

Each entry names the **weakness it resolves**, because that is the register's admission test.

**Triage.** Six entries earn first-lookup status within their domain: *Designing Data-Intensive Applications* (2nd ed), *Release It!*, *Threat Modeling*, the *SRE Workbook*, *Building Secure and Reliable Systems*, and *Driving Data Quality with Data Contracts*. Everything else here is worth opening only when a precise blocker names it — they are catalogued for findability, not for breadth of reading.

### Distributed systems, messaging, and integration

| Reference | Resolves |
|---|---|
| Martin Kleppmann & Chris Riccomini, [*Designing Data-Intensive Applications* (2nd ed, O'Reilly, March 2026)](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/) | Delivery semantics, idempotence, and why exactly-once is a property of effects rather than of message delivery — the reasoning behind the §9.2 rule. Read the transactions, consistency and stream-processing chapters; it is ~670 pages and is not read sequentially |
| Gregor Hohpe & Bobby Woolf, *Enterprise Integration Patterns* ([site](https://www.enterpriseintegrationpatterns.com/)) | Naming and structuring the async design in vocabulary a reviewer already knows |
| Chris Richardson, *Microservices Patterns* ([site](https://microservices.io/)) | The outbox/inbox distinction and transactional messaging boundaries |

### Reliability and operations

| Reference | Resolves |
|---|---|
| Michael Nygard, *Release It!* (2nd ed) | Circuit breakers, timeouts, and stability patterns for the third-party seam |
| [Google SRE Book & Workbook](https://sre.google/books/) | SLO and error-budget vocabulary, blameless postmortem structure (also cited in §8) |
| [Beyer et al., *Building Secure and Reliable Systems*](https://sre.google/books/building-secure-reliable-systems/) (free) | Where security and reliability controls conflict — directly relevant to kill-switch and degradation design |

### Security, threat modelling, and identity

| Reference | Resolves |
|---|---|
| Adam Shostack, *Threat Modeling: Designing for Security* | STRIDE technique for Day 2 — the canonical source for the method the plan names |
| [Ross Anderson, *Security Engineering* (3rd ed)](https://www.cl.cam.ac.uk/~rja14/book.html) (free) | Broad control reasoning; useful when an audit finding needs a principled rather than a checklist justification |
| Justin Richer & Antonio Sanso, *OAuth 2 in Action* | **Conceptual background only.** Token validation, audience restriction and delegation reasoning; published 2017, so it predates RFC 9700 and the current MCP authorization model. The pinned MCP revision and the stable RFCs are the implementation authorities — never this book |
| [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final) | Per-request verification vocabulary for the NHI and containment design |

### Statistics for evaluation

| Reference | Resolves |
|---|---|
| Brown, Cai & DasGupta, ["Interval Estimation for a Binomial Proportion", *Statistical Science* 16(2), 2001](https://projecteuclid.org/euclid.ss/1009213286) | **The** citation for preferring Wilson over Wald — defend the Day 8 gate choice with a source, not a preference |
| Fleiss, Levin & Paik, *Statistical Methods for Rates and Proportions* (3rd ed) | Cohen's kappa, agreement interpretation, and the sample-size reasoning behind the thirty-case calibration floor |
| Alan Agresti, *Categorical Data Analysis* | Slice comparisons and small-denominator caution when a primary slice sits near its minimum |

### Data engineering and analytics

| Reference | Resolves |
|---|---|
| Joe Reis & Matt Housley, *Fundamentals of Data Engineering* | Pipeline and ingestion design vocabulary for the batch seam |
| Ralph Kimball & Margy Ross, *The Data Warehouse Toolkit* (3rd ed) | Grain and dimensional modelling decisions in the dbt cost-attribution layer |
| Andrew Jones, *Driving Data Quality with Data Contracts* | Structuring the batch file contract and its change process |

### Cloud platform and infrastructure as code

| Reference | Resolves |
|---|---|
| Yevgeniy Brikman, *Terraform: Up & Running* (3rd ed) | State, module, and environment-promotion design if HCL is chosen over Bicep |
| Kief Morris, [*Infrastructure as Code* (3rd ed, O'Reilly, March 2025)](https://www.oreilly.com/library/view/infrastructure-as-code/9781098150341/) | Reproducibility, teardown/rebuild, and environment-parity reasoning |
| [Microsoft Learn](https://learn.microsoft.com/en-us/training/) — free structured paths for Entra workload identities, Key Vault, Service Bus, Bicep fundamentals, and Azure cost management | Fastest route through a specific platform mechanism when the docs alone are not landing; scoped to one module, not a certification path |

### Commercial and consulting craft (post-v1.0, register-gated)

The build plan is explicit that no pricing course or credential starts before market evidence — a qualified proposal, a repeated role requirement, a recruiter screen, or a prospect objection — supplies the activation trigger. These are named so that, when a trigger fires, the choice is already scoped.

| Reference | Resolves |
|---|---|
| David C. Baker, *The Business of Expertise* | Positioning and specialisation depth — the question behind the two-register market-position split |
| Blair Enns, *The Win Without Pitching Manifesto* and *Pricing Creativity* | Scoping and pricing fixed-scope diagnostics without competing on day rate |

**Activate one commercial book, not several.** The register's three-active-resource cap applies, and these overlap heavily; a single reference chosen against the specific trigger that fired beats a shelf.

---

## 11. Watchlist — three review cadences

Eleven fast-moving domains cannot be reviewed meaningfully in one weekly sitting, and most do not need weekly review. Currency is preserved by matching the cadence to how the item actually changes and to when AEGIS actually consumes it. **A weekly manual sweep across everything is not the control; these three cadences are.**

### Cadence A — automated, continuous (no manual time)

Configure once, then respond to what it reports. This replaces manual dependency vigilance entirely.

| Signal | Mechanism |
|---|---|
| Package and transitive-dependency advisories | Dependabot or Renovate on the lockfile, plus the [pip-audit](https://github.com/pypa/pip-audit) PR lane |
| Container and image vulnerabilities | [Grype](https://github.com/anchore/grype) in the supply-chain CI lane |
| GitHub Actions releases and pinned-SHA drift | Dependabot on the workflow files |
| Cloud spend variance | Tiered budget alerts plus the daily reconciliation log (§9.7) |

### Cadence B — weekly, but only while the item is actively in use

Roughly ten minutes, and only for the areas the current build phase touches.

1. **MCP specification releases and SDK line** — [modelcontextprotocol.io](https://modelcontextprotocol.io/), the [spec repo releases](https://github.com/modelcontextprotocol/modelcontextprotocol/releases) and the [conformance suite](https://github.com/modelcontextprotocol/conformance). Check while Days 3, 6 and 22 work is live. A revision landing mid-project is an *opportunity*: write the migration note, and that is article material.
2. **Model deprecation pages for both providers** — check while Days 4–14 are live ([Anthropic docs](https://docs.claude.com/), navigate: model deprecations). A mid-project deprecation is a free, real migration exercise for Day 14.
3. **Langfuse and OTel GenAI semantic-convention compatibility** — check while Days 7a–7b and 15–17 are live. Attribute renames are the classic breakage; the mapping adapter plus contract fixture must absorb them. Note the v3 retirement dates in §5 if self-hosting decisions are still open.

### Cadence C — at phase entry and again at release only

These change slowly but matter absolutely when they change. Re-verify when the consuming milestone begins, and again on the date any client-facing document is issued.

| Item | Verify at |
|---|---|
| **EU AI Act implementation status** — [Commission implementation FAQ](https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act), [AI Omnibus notice](https://digital-strategy.ec.europa.eu/en/news/ai-omnibus-enters-force) and EUR-Lex first; the AI Act Explorer is a secondary navigation aid only | Day 19a entry, and the issue date of every client-facing deliverable |
| **NIST AI RMF revision** — [programme page](https://www.nist.gov/itl/ai-risk-management-framework); AI RMF 1.0 is under revision, so keep the crosswalk versioned and disclose changed mappings before adopting a successor | Day 19a entry and release |
| **OWASP GenAI Security Project** — [genai.owasp.org](https://genai.owasp.org/); track releases by canonical title and never promote a community label into an OWASP publication name | Day 2 entry, Day 10 entry, and the security-audit issue dates (14, 19b) |
| **Entra continuous access evaluation support matrix** — [Entra docs root](https://learn.microsoft.com/en-us/entra/) | Day 23a entry; a widened matrix could shorten the declared containment window, a narrowed one could invalidate a published figure, and either way the window is republished with a dated decision |
| **PostgreSQL major version and managed-service role behaviour** — [release notes](https://www.postgresql.org/docs/release/) and the Azure version-support pages | Day 24b entry; row-security semantics are stable, managed-service role privileges are not guaranteed to be |
| **Third-party enrichment API terms, rate limits and version** | Day 24b entry and before launch; a terms change can retire the seam, a rate-limit change alters what the degradation test means |
| **FOCUS ratified version and provider adoption** — [focus.finops.org](https://focus.finops.org/focus-specification/) | Day 22 entry only, since FOCUS is deferred out of base v1.0 (§7) |
| **IaC licensing** — [opentofu.org](https://opentofu.org/) | Day 26a entry, and only if HCL was chosen over Bicep |

---

## 12. Resource Decision Register

This compact register is the control point for resource selection. It covers resources that enter the runtime, CI/CD path, evidence-production chain, or client-facing deliverables; supporting `[R]` references do not require individual rows unless they become inputs to a release or compliance claim. Before first use, replace every “pin before use” entry with the exact package version, specification date, model identifier, or publication revision. Update the row when a watchlist trigger fires; keep the superseded decision in version control.

| Resource | Class | AEGIS role | Version/specification record | Licence or governance | Canonical output/evidence | Replacement boundary | Review trigger |
|---|---|---|---|---|---|---|---|
| OWASP Agentic/LLM and MCP guidance; NIST AI RMF; ISO 42001/23894 | [N] | Threat taxonomy and control-evidence crosswalk | Record publication title, edition/date, and accessed date | OWASP, NIST, ISO | Versioned threat/control crosswalk with source IDs | Re-map controls; never silently overwrite IDs | New edition, withdrawal, or regulatory guidance change |
| MCP specification | [I] | Tool protocol and capability contract | Pin dated MCP revision separately from SDK | Agentic AI Foundation/Linux Foundation | Protocol conformance, negative authorization tests, and captured Inspector evidence | MCP adapter plus invariant test suite | Spec/SDK release, authorization change, or deprecation |
| OAuth Internet-Draft and stable RFC suite | [N] | Identity and authorization control authority used by the pinned MCP revision | Record the Internet-Draft version and every stable RFC revision cited | IETF | Authorization design, cited-RFC matrix, and negative identity/token tests | Authorization adapter plus unchanged identity and token invariants | MCP authorization change, Internet-Draft update, new/revised RFC, or security guidance change |
| MCP Python SDK and Inspector | [P] | Reference server implementation and protocol inspection | Pin SDK and Inspector versions before use | Record licences, owners, security policies, compatibility, and release dates | Server fixtures, captured Inspector sessions, and conformance results | Protocol-facing adapter; the tests and manifest contracts survive an SDK/tool replacement | Breaking SDK/spec incompatibility, security issue, or inactivity |
| LangGraph | [P] | Durable constrained workflow, checkpoints, and human approval | Pin package and Python compatibility before use | Record package licence, owner, security policy, and release date | State-transition, interruption, resume, and recovery tests | Workflow port plus unchanged state-machine invariants | Breaking release, unsupported runtime, licence/security change, or inactivity |
| Python data/test toolchain: uv, ruff, pydantic, pytest, statsmodels/sklearn | [P] | Reproducible environment, typed boundaries, deterministic tests, and statistical calculations | Pin packages and Python runtime before use | Record licences, owners, supported runtimes, security policies, and release dates | Lockfile, schema validation, lint/test reports, and reproduced Wilson/kappa calculations | Standard Python package/data boundaries; preserve schemas, test semantics, and statistical methods | Runtime incompatibility, security/licence change, or calculation regression |
| DeepEval | [P] | Behavioural evaluation runner | Pin package before use | Record package licence, owner, security policy, and release date | Versioned AEGIS result schema, JUnit/JSON output, sealed-holdout report | Eval-runner adapter; same cases, policy, thresholds, and release decision | Breaking result semantics, inactivity, licence/security change |
| PyRIT | [P] | Reproducible adversarial orchestration | Pin package before use | Microsoft open-source project; record exact licence/release | Attack corpus with IDs, transcripts, expected controls, and outcomes | Attack-runner adapter; preserve corpus and evidence schema | Breaking strategy API, inactivity, or coverage gap |
| promptfoo and garak | [P] | Pre-evaluated evaluation and scanning alternatives; inactive unless a migration decision is recorded | Record assessed versions; pin only when activated | Record licences, owners, security policies, and releases | Migration comparison against the canonical AEGIS case, attack, and result schemas | May replace a runner, never the sealed cases, expected controls, policy, thresholds, or release decision | Primary-tool migration, alternative inactivity, or incompatible evidence semantics |
| OpenTelemetry GenAI conventions | [I] | Vendor-neutral trace export | Pin OTel packages and semantic-convention revision | CNCF/OpenTelemetry governance | Canonical AEGIS event fixture plus adapter-contract results | Replace exporter/store without changing internal schema or metrics | Attribute stability change, rename, or exporter incompatibility |
| Langfuse | [P] | Trace inspection and observability presentation | Pin self-hosted release and database schema | Record licence, owner, security policy, and export support | Exported representative traces and cost totals | OTel boundary; replay fixture in replacement and reproduce required fields | Export/licence change, schema break, or unsupported release |
| Sigstore/cosign, Rekor, GitHub attestations | [I]/[P] | Sign artifacts and externally anchor audit heads/provenance | Pin actions by commit SHA and tools by version | OpenSSF/Linux Foundation plus GitHub; record public/private trust model | Signature, attestation, transparency/anchor proof, verifier output, mutation failures | Alternate independently controlled transparency or CI anchor; SSH signing is local-only | Repo visibility change, trust-root change, action/tool release, or verification failure |
| SLSA | [N] | Provenance assessment vocabulary | Record specification version | OpenSSF | Requirement-by-requirement assessment and provenance evidence | Continue as “SLSA-aligned” unless every claimed level requirement passes | Specification revision or builder/provenance change |
| CycloneDX SBOM and AI/ML-BOM | [I] | Portable software and model inventories | Pin schema/specification version and generators | OWASP Foundation | Validated SBOM plus separately populated ML-BOM/model register | Preserve identifiers and required fields in another open format | Schema/generator release or validation failure |
| Syft, Grype, pip-audit, GitHub Actions, and Docker Compose | [P] | Inventory generation, vulnerability checks, CI execution, and reproducible local staging | Pin tools and actions; pin third-party actions by full commit SHA | Record licences, owners, security policies, supported runtimes, and releases | SBOM source report, vulnerability reports, CI logs/attestations, and one-command staging result | Preserve CycloneDX output, policy thresholds, CI lane contracts, credentials boundary, and reviewer command | Security advisory, action/tool release, unsupported runtime, or evidence/reproduction failure |
| DuckDB and dbt-duckdb | [P] | Canonical cost transformation, tests, and evidence tables | Pin packages and SQL/schema compatibility | Record licences, owners, security policies, and releases | Reproducible database, manifest/docs, test results, and metric tables | Input/output schemas, numeric semantics, lineage, tests, and totals | Adapter incompatibility, unsupported version, licence/security change |
| Power BI | [P] | Executive/advisory presentation only | Record Desktop/service version and export date | Microsoft proprietary product | Dashboard plus static PDF/images linked to metric definitions | Open dbt/DuckDB path must reproduce all headline metrics without Power BI | Licence/service change, refresh failure, or metric mismatch |
| FOCUS | [I] | Provider billing normalization and reconciliation | Pin exact ratified specification version | FinOps Foundation | FOCUS-aligned billing table, validation result, and reconciliation report | Versioned bridge to AEGIS operational-cost extension | New ratified version, provider mapping change, or residual breach |
| Model providers and model versions | [P] | Baseline execution and migration regression | Record immutable model ID/date, API version, region, and deprecation policy | Provider terms and documentation | Model inventory entry, eval result, usage record, and migration comparison | Provider adapter plus unchanged safety, behaviour, latency, and cost gates | Deprecation, silent alias change, policy change, or gate regression |
| Microsoft Entra ID and Azure Key Vault | [P] | Per-domain workload identity, federated CI credentials, and audit-signer key custody | Record tenant/app object IDs, federation subject claims, key identifiers and versions, and the declared containment window with its mechanism | Microsoft proprietary service; record terms and regional scope | Issuance-revocation and active-token-containment evidence, NHI register rows with tenant objects, denied signer-access test | Identity adapter plus unchanged fail-closed invariants; a longer achievable window is a variance or a control regression, never a silent change | CAE support-matrix change, token-lifetime policy change, service deprecation, or containment-test regression |
| Azure Service Bus (or the selected managed queue) | [P] | Asynchronous FNOL intake with at-least-once delivery | Pin SDK version; record lock duration, max delivery count, and dead-letter configuration | Microsoft proprietary service | Inbox/idempotency schema, redelivery and DLQ evidence, both crash-window tests | Broker adapter; the inbox transaction, settlement ordering, and effectively-once effect must survive replacement | Delivery-semantics or settlement-API change, SDK break, or duplicate-effect regression |
| PostgreSQL (managed) with Alembic and SQLAlchemy | [P] | Claims-record system of record under row-level security | Pin engine major version, driver, and migration revision; record runtime and migration role names separately | PostgreSQL licence; Azure service terms | Role-topology assertions, four-command cross-claim denial, identity-derived predicate tests, migration history | Preserve role separation, `NOBYPASSRLS`, forced row security, and server-derived predicates across any engine or driver change | Engine major upgrade, managed-service privilege change, driver break, or any RLS test regression |
| Bicep, or OpenTofu/Terraform if HCL is chosen | [P] | Reproducible cloud staging, promotion, rollback, and teardown | Pin tool version and provider/module versions; **record the licence class explicitly** (BUSL-1.1 is not an open-source licence) | Microsoft (Bicep) · Linux Foundation MPL-2.0 (OpenTofu) · BUSL-1.1 (Terraform) | Clean-state provision, CI-promoted deploy with digest-provenance match, rollback and teardown/rebuild evidence | Environment definition may port; reproducibility, provenance verification, and rollback evidence must not weaken | Licence or governance change, provider break, or a failed clean rebuild |
| Third-party enrichment API | [P] | Advisory fraud-enrichment input on a non-consequential path | Record provider, API version, rate limits, terms, and licence of returned data | External provider terms | Forced-outage degradation trace, circuit-breaker configuration, capability-manifest entry | Any equivalent advisory source; degradation behaviour and the no-fabricated-value rule are invariant | Terms, pricing, rate-limit, version, or availability change |
| Azure Cost Management, spending limit, Quotas, and Policy | [N]/[P] | Bounded, observable cloud spend for the integration releases | Record subscription-offer eligibility, budget thresholds, quota figures by provider and region, and policy assignment scopes | Microsoft proprietary service | Alert configuration, tested teardown, oversized-deployment rejection test, daily reconciliation log | Equivalent cloud controls; the disclosure that billing latency prevents an absolute cap is invariant | Offer or eligibility change, quota revision, policy-effect change, or unexplained daily variance |

---

## 13. Day-to-resource quick map

| Build phase | Primary references |
|---|---|
| Days 1–2 (brief, threat model, data) | [OWASP ASI 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) · [MITRE ATLAS](https://atlas.mitre.org/) · [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) · [ICO AI guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/) |
| Days 3, 6 (MCP, NHI) | Pinned [MCP spec](https://modelcontextprotocol.io/) revision (security/authorization sections) · [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) · [OWASP ASI MCP guidance](https://genai.owasp.org/initiatives/agentic-security-initiative/) · stable OAuth RFCs including [RFC 9700](https://datatracker.ietf.org/doc/html/rfc9700), [RFC 8707](https://datatracker.ietf.org/doc/html/rfc8707), and [RFC 9728](https://datatracker.ietf.org/doc/html/rfc9728) · [Syft](https://github.com/anchore/syft) |
| Days 4–5 (workflow, boundaries) | [LangGraph](https://langchain-ai.github.io/langgraph/) (interrupts, checkpointing) · [building effective agents](https://www.anthropic.com/engineering/building-effective-agents) · [context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) · [pydantic](https://docs.pydantic.dev/) |
| Days 7a–7b (traceability, release contract) | Pinned [OTel GenAI semconv](https://opentelemetry.io/docs/specs/semconv/gen-ai/) plus mapping adapter and telemetry-redaction tests · [Langfuse self-hosting](https://langfuse.com/) · [cosign](https://github.com/sigstore/cosign) · local anchor adapter; external [GitHub attestation](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations) wired by Days 13/20 |
| Days 8a–8b, 9 (eval protocol, harness) | [DeepEval](https://github.com/confident-ai/deepeval) · [Wilson interval](https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportion_confint.html) with the [Brown/Cai/DasGupta](https://projecteuclid.org/euclid.ss/1009213286) rationale · Cohen's kappa · [InjecAgent](https://arxiv.org/abs/2403.02691) |
| Days 10–11 (attack, remediate) | [PyRIT](https://github.com/microsoft/PyRIT) · [OWASP ASI](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) + [LLM Top 10](https://genai.owasp.org/llm-top-10/) · [lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) · [securing-agents patterns](https://arxiv.org/abs/2506.08837) |
| Days 12, 13a–13b, 14 (kill, gates, migration, audit draft) | [SRE Workbook](https://sre.google/books/) (runbooks) · [SLSA](https://slsa.dev/) verification requirements · [pip-audit](https://github.com/pypa/pip-audit)/[Grype](https://github.com/anchore/grype) · provider deprecation policies |
| Days 15–17 (cost) | [Langfuse](https://langfuse.com/) cost fields · provider estimate/usage/billing APIs ([Anthropic](https://docs.claude.com/)) · [DuckDB](https://duckdb.org/) + [dbt-duckdb](https://github.com/duckdb/dbt-duckdb) canonical evidence path · pinned [FOCUS](https://focus.finops.org/focus-specification/) billing layer + AEGIS operational-cost extension · [Power BI](https://learn.microsoft.com/en-us/power-bi/) presentation |
| Days 18, 19a–19b (SLOs, incident, governance) | [SRE Book](https://sre.google/books/) (SLOs) · [NIST SP 800-61r3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) · versioned [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) + [GenAI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) · [ISO 42001](https://www.iso.org/standard/81230.html) · official [European Commission AI Act timeline](https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act) · [Model Cards](https://arxiv.org/abs/1810.03993) |
| Days 20–21 (package, launch) | [GitHub attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations) with documented trust model · [CycloneDX](https://cyclonedx.org/) SBOM + separate AI/ML-BOM · reviewer-guide conventions from any CNCF project's CONTRIBUTING.md as a template |
| Day 22 (integration landscape, ADR) | §9 in full for the vendor confirmations · [Azure Cost Management](https://learn.microsoft.com/en-us/azure/cost-management-billing/) + [Quotas](https://learn.microsoft.com/en-us/azure/quotas/) + [Policy](https://learn.microsoft.com/en-us/azure/governance/policy/) for the spend package · OWASP agentic taxonomy for the threat-model delta |
| Days 23a–23b (identity plane) | [Entra docs root](https://learn.microsoft.com/en-us/entra/) (workload identities, federation, CAE) · [Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/) · [RFC 8725](https://datatracker.ietf.org/doc/html/rfc8725) + [RFC 9068](https://datatracker.ietf.org/doc/html/rfc9068) · [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final) |
| Days 24a–24b (batch, system of record, third party) | [PostgreSQL RLS](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) + [CREATE ROLE](https://www.postgresql.org/docs/current/sql-createrole.html) · [Alembic](https://alembic.sqlalchemy.org/) · [RFC 4180](https://datatracker.ietf.org/doc/html/rfc4180) · dbt tests for reconciliation · *Release It!* + [backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) |
| Days 25a–25b (async intake, v1.1 tag) | [Service Bus docs root](https://learn.microsoft.com/en-us/azure/service-bus-messaging/) (locks, settlement, dead-lettering) · [Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/) (idempotent receiver) · [microservices.io](https://microservices.io/patterns/) (outbox versus inbox) · Kleppmann on delivery semantics |
| Days 26a–26b (cloud staging) | [Bicep](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/) or [OpenTofu](https://opentofu.org/) · [Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/) (revisions, egress) · [GitHub OIDC hardening](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments) · [SLSA verification](https://slsa.dev/spec/v1.2/verifying-artifacts) for the deploy-time digest check |
| Days 27a–27b (drill, staging re-verification) | [SRE Workbook](https://sre.google/books/) (postmortem) · [NIST SP 800-61r3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) · [Building Secure and Reliable Systems](https://sre.google/books/building-secure-reliable-systems/) for degradation-under-attack reasoning |
| Days 28a–28b (challenge, conversion, launch) | Day 21 reviewer conventions reused for the integration chain · §10 commercial references, register-gated and only once a market trigger has fired |

---

## Anti-recommendations (deliberate exclusions, so future-you doesn't relitigate)

- **No custom vector database, policy engine, or IdP** — the plan's NOT-in-scope list already forbids these; effort goes to integration and evidence.
- **No framework-of-the-week orchestrators** without documented ownership, licence, maintenance health, security policy, portable boundaries, and a tested replacement contract. Evaluate implementations against the class-specific staying-power test and Resource Decision Register before they enter the lockfile.
- **No closed eval SaaS as the only harness** — managed platforms may supplement, but the reproducible path a reviewer runs must be open source end to end, or the repository rule ("if the repository cannot reproduce it, the project does not claim it") breaks.
- **No LLM-judge-only scoring of deterministic controls** — restating the plan's own rule here because it is the one most tempting to violate under time pressure.
- **No general reading list or course backlog on the v1.0 critical path** — use the separate development register, four-gate admission decision, timebox, validation and stop rule. Course completion never substitutes for tested judgment or buyer-verifiable evidence. §10 names *which* reference resolves a given weakness; it does not authorise spending time on any of them.
- **No self-managed Kafka or streaming platform** — a managed queue exercises the async pattern at the scale this reference implementation needs, and operating a broker is effort spent away from evidence.
- **No multi-cloud abstraction layer** — Azure and Entra are the mandatory reference implementation. AWS and GCP equivalents are documented future ports; an abstraction built to keep both open would dilute the platform-depth evidence that motivated the integration work.
- **No BUSL- or otherwise source-available-licensed tool entering the lockfile without a recorded licence decision** — the `[P]` criteria require a suitable licence, and a public reference repository that a reviewer must be able to reproduce is exactly where that distinction bites. Where an open-governance fork exists, it is the default.
- **No transactional outbox presented as the consumer-side crash control** — it makes a state change and an outgoing publication atomic; it does not span a broker dequeue and a database write. The inbox-plus-post-commit-settlement design in §9.2 is the control, and conflating the two is the error most likely to survive review unnoticed.
