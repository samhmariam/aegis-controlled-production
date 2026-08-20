# Update Plan: Incorporating the Integration Extension into `project-aegis-plan-v1.1.md`

**Date:** 2026-08-20
**Objective:** One governing plan document covering all milestones (Days 1–28), after which `project-aegis-integration-extension.md` is marked superseded and no separately maintained plan can drift. `project-aegis-plan-v1.0-superseded.md` is already banner-marked and renamed.

---

## Design decisions (settled before editing)

1. **Filename stays `project-aegis-plan-v1.1.md`.** The document's own revision-record convention tracks versions; renaming the file would break the reference in the v1.0 supersession banner and any external links. The merge is recorded as a new dated revision entry, not a new filename. (If a versionless `project-aegis-plan.md` is ever preferred, do it as a separate, single rename with both banners updated in the same commit.)

2. **The extension's six milestones become seven: Days 22–28.** The extension's Day 27 bundled a staging drill, full re-verification, the entire commercial assembly and article publication — the same overload pattern the external review flagged on the original budget. Split it:
   - **Day 27 `[B]`** — integration incident drill + staging re-verification (technical fact).
   - **Day 28 `[A]`** — commercial conversion: assessment issuance, offer rows, guide/README updates, article 4 publication, sixth-proposition unblock, `v1.2-cloud-operation` tag, integration outreach.
   This also restores the base plan's track grammar: `[B]` bridges technical evidence, `[A]` converts it. Budgets are unchanged in total: `v1.1-integration-controls` = Days 22–25 (30 h, triggers 22/30); `v1.2-cloud-operation` = Days 26–28 (25 h, triggers 18/25).

3. **Sequencing dependency is explicit.** Day 22 may not start until `v1.0-aegis` is tagged. The v1.0 release contract, its mandatory gates and its 75/100-hour controls are untouched by the merge; the extension budgets and triggers are additional and separate.

4. **The merge simplifies the canonical-table mechanics.** With the extension folded in, the sixth proposition row is added to this document's "What AEGIS must prove" table *during the merge edit itself*, marked **blocked until `v1.2-cloud-operation`**. Day 22's job shrinks to wiring the README, competence ledger and six-row CI validation — the awkward "extension edits the base plan" step disappears.

5. **The three sections stranded in the v1.0 plan migrate here in the same revision** (skill-to-proof coverage, post-launch evidence bundles, final public narrative), each extended with its integration row/bullet. One revision, one commit, no second migration pass.

---

## Section-by-section edits to `project-aegis-plan-v1.1.md`

Ordered top-to-bottom through the document.

### 1. Title and header

- Title → `# Project AEGIS — 28 Build Milestones to Evidence of Controlled Agent Production and Enterprise Integration`.
- Replace the market-position block with the extension's **two-register** form: *service positioning (client delivery only)* — may include "systems the enterprise already runs"; *demonstrated claim (repository)* — "demonstrates six enterprise integration patterns against a real identity provider, managed cloud services and an independent third-party API, using synthetic data"; *technical shorthand* — "I secure, evaluate, cost-control and enterprise-integrate production-oriented agent systems." Include the one-paragraph explanation of why the registers differ.
- Add a new revision-record entry (2026-08-20): incorporation of the integration extension as Days 22–28 in two releases; Day 27/28 split; sixth proposition added blocked; variance taxonomy, cloud-spend control package, commercial conversion section and claims additions; migration of the three v1.0-plan sections; supersession of both companion documents.

### 2. "What AEGIS must prove"

- Append the sixth row (proposition / reproducible proof / buyer-facing artifact exactly as in the extension), with a status marker: **blocked until `v1.2-cloud-operation`**.
- Add below the table: the CI validation rule — README propositions table must contain exactly six rows, each proof column resolving to at least one competence-ledger chain with a runnable test command; a row without a chain fails the build.

### 3. Contracting-to-consulting continuum

- No structural change. Add one sentence noting the track labels extend to Days 22–28 (Day 22 `[S]`, Days 23–26 `[D]`, Day 27 `[B]`, Day 28 `[A]`).
- In the delivery/advisory guide description that follows, update the role list: the delivery guide now supports **three** roles (add Agent Integration Engineer) and **five** traceable delivery chains (add enterprise integration); the advisory guide gains the Enterprise Integration Readiness Assessment as a third offer.

### 4. Scope guardrails

- **Mandatory core:** append the extension's two release cores as a labelled sub-list ("Integration extension — `v1.1-integration-controls`" and "— `v1.2-cloud-operation`"), with article 4 publication and the commercial artifacts under v1.2.
- **Stretch:** append the extension's four stretch items.
- **NOT in scope:** append the extension's exclusions. Reconcile the existing "custom identity provider" line so it reads: *build* no custom IdP/policy engine/observability platform — *integrating* the real managed IdP (Days 23, 26) is in scope and is the point.
- **Descope ladder:** append the extension's ladder rows for Days 23, 24, 25, 26 and a revised Day 27/28 row pair: Day 27's minimum is the executed drill plus classified staging re-verification; Day 28's row states that no conversion artifact may defer — if any is incomplete, v1.2 does not tag and the sixth proposition stays blocked.

### 5. Effort-control triggers

- Keep the v1.0 75/100-hour text verbatim. Append: the integration releases carry their own budgets and triggers (30 h @ 22/30; 25 h @ 18/25), re-estimated in the Day 22 ADR after vendor selection; all extension time logs into the same `docs/evidence/effort-log.csv` with labels `day-22`…`day-28`; the release-label invariants (v1.1 blocked by any Day 22–25 gate; v1.2 blocked by any extension gate; sixth proposition blocked until both; `-rc` labelling for partials).

### 6. New section: "Enterprise integration (Days 22–28): landscape, releases and controls"

Insert after the effort-control section, containing (moved from the extension, lightly edited for the Day 27/28 split):

1. **Why the extension exists** (condensed to one paragraph — the full argument stays in the revision record and article 4).
2. **Target enterprise landscape**: the ASCII estate diagram, the six-seam table, and the vendor-substitution note (ADR-recorded, with re-estimated budget).
3. **Release structure table** (two releases, milestones, budgets, triggers).
4. **Control-preservation rule: variance taxonomy** — the two-class table (implementation variance = disposition; control regression = release blocker, never dispositionable), plus the rule that sealed suites re-run locally-integrated before the v1.1 tag and in staging before the v1.2 tag.
5. **Cloud spend controls** — the six-item implementable package (eligibility record, 50/75/90% alerts, tested teardown, quota ceilings, daily reconciliation, latency disclosure) and the rule that cloud cost is a visible infrastructure class in the attribution model.

### 7. Non-slippable executive conversion layer

- v1.0's four artifacts stay as-is. Append: after the integration releases, the **Enterprise Integration Readiness Assessment** and **published article 4** join the non-slippable set for `v1.2-cloud-operation` — they may not be traded away for engineering scope, and if underlying evidence is incomplete the artifact states the gap and v1.2 waits.

### 8. Preparation schedule table

Append rows:

| Preparation starts | Incremental work | Final assembly milestone |
|---|---|---|
| Day 22 | Readiness-assessment skeleton from the instrument; offer-row skeletons; article 4 outline | Day 28 |
| Days 23–25 | Capture variance records, seeded-failure traces and containment-window evidence as each seam lands | Days 25 and 28 |
| Day 26 | Capture provision/deploy/rollback timestamps and spend-reconciliation extracts | Day 27 |
| Day 27 | Fold drill timeline and staging variance record into the assessment draft | Day 28 |

### 9. Buyer-navigation artifacts

- Delivery-guide requirements: change "four traceable delivery chains" to **five**, adding the enterprise-integration chain (problem → integration ADR → code → contract/reconciliation tests → seeded failure → generated result → limitation → client-team ownership).
- Advisory-guide requirements: add the Enterprise Integration Readiness Assessment as a third current offer (assessment-type, like the Production-Readiness Assessment — not assurance), with its full offer row (buyer, trigger, scope, inputs, outputs, exclusions, evidence, remediation path) copied from the extension.
- Add the **assessment instrument** subsection verbatim from the extension: per-seam minimum evidence, finding scale + severities, release-blocker rules (no averaging), residual-risk register, prioritization order, forced Ship/Hold/Conditional-ship decision.
- README navigation contract: note the two-stage text — Day 20 ships the v1.0 wording; Day 28 replaces both entry-point blocks with the extension's exact six-area wording (kept verbatim in this section) and CI re-checks links and the six-row table.

### 10. Reference architecture

- Keep the v1.0 diagram. Add a pointer line: "Days 22–28 replace the mocked seams with the real estate defined in the enterprise-integration section" (avoids maintaining two full diagrams).

### 11. Technology choices

Append rows: Identity — Entra ID workload identities + Key Vault (real IdP integration, secretless CI); Legacy interface — object-storage CSV drop under a written file contract; System of record — managed Postgres; Async — managed queue (Service Bus/Storage Queue); Third party — one genuinely external enrichment API; Infrastructure — Bicep/Terraform IaC with CI promotion. Note vendor substitution is ADR-governed.

### 12. Quantitative acceptance gates

- Keep the v1.0 gate table untouched.
- Append the extension's eight integration gates as a second table under an `integration:` heading, frozen at Day 22 exit, with the gate-to-release mapping (gates 1–4 + local half of 6 → v1.1; gates 5, 7, 8 + staging half of 6 → v1.2) and the no-weakening rule.

### 13. Daily delivery standard

- Extend the tag range: `day-01` through `day-28`.
- Rule 7's guide-update duty now includes the integration chain and offer rows.

### 14. Week 4 and Week 5 milestone sections

Insert after Day 21:

- **"Week 4 — Integrate with the enterprise estate (Days 22–25)"** — opening note: begins only after `v1.0-aegis` is tagged; "week" remains a build phase. Then Days 22, 23, 24, 25 copied from the extension (Day 22's update-target list rewritten to README + ledger + matrix + CI check, since the plan table is edited in this merge; Day 25 keeps the local re-verification and conditional `v1.1-integration-controls` tag).
- **"Week 5 — Operate in the cloud and convert (Days 26–28)"** — Day 26 unchanged from the extension. Day 27 `[B]` reduced to: combined incident drill (third-party outage + drifted batch + live credential rotation), blameless report, staging re-run of sealed/adversarial/audit suites with taxonomy-classified variances. Day 28 `[A]`: assessment issuance via the instrument, integration runbook, both offer rows, guide finalization, README entry-point replacement, service one-pager, article 4 **edited and published** with CI-checked links, sixth-proposition unblock, conditional `v1.2-cloud-operation` tag, and a second outreach wave adding the integration assessment to the follow-on offer set. Done-when for each day carried from the extension, re-split accordingly.

### 15. Test and evidence strategy

- **Test layers:** extend Contract with batch file contracts and third-party response schemas; add reconciliation tests to Unit/Integration; extend Operations with cloud rollback, teardown/rebuild and spend reconciliation.
- **Critical production failure modes table:** append rows — batch file partially loads (quarantine, zero partial loads / seeded truncation test); revoked identity's issued token still accepted (declared containment window / issuance + containment tests); consumer crashes between consume and record (outbox pattern / crash test); deployed image differs from signed release (deploy-time provenance check / mismatch test); cloud spend variance unexplained (daily reconciliation blocks tag / reconciliation test).

### 16. Gap-closure matrix

Append the extension's five gap-closure delta rows.

### 17. Migrated v1.0 sections (new, near the end)

1. **Skill-to-proof coverage** — table as in the v1.0 plan, plus one row: *Enterprise integration engineering* → real-IdP identity tests, batch reconciliation, third-party degradation evidence, async intake proofs, IaC deployment and rollback evidence (the fifth chain).
2. **Post-launch evidence bundles and commercial use** — the four-bundle table retitled (no "Day-22" label), plus a fifth row: *Enterprise Integration* — readiness assessment, integration runbook, variance records, seam evidence → Enterprise Integration Readiness Assessment (consulting) → Agent Integration Engineer, Platform/Integration Engineer (contracting). Wedge note updated: the Production-Readiness Assessment remains the primary wedge; the integration assessment is the second assessment-type offer.
3. **Final public narrative** — the Cotswold Mutual paragraph extended with one sentence on integrating the estate, and a fifth shorthand bullet: **"I enterprise-integrate"** becomes real workload identity, reconciled batch interfaces, resilient third-party clients, audited async intake and provenance-verified cloud deployment — claimable only after both integration releases ship.

### 18. Claims discipline

Merge the extension's permitted/prohibited claims into the plan's claims-register guidance: the two-stage permitted list (post-v1.1 vs post-v1.2), and the prohibited list (production/scale/real-data claims, "enterprise-proven", the service-positioning sentence as a repository claim, absolute spend guarantees, consequential-path descriptions of advisory seams, premature sixth-proposition assertion).

---

## Post-merge cleanup (same working session)

1. Add a supersession banner to `project-aegis-integration-extension.md`: superseded 2026-08-20, incorporated into `project-aegis-plan-v1.1.md` as Days 22–28 (with the Day 27/28 split noted); retained for provenance; no further updates.
2. Verify the v1.0 file's banner still describes the arrangement accurately (it references the extension "being incorporated" — update its parenthetical to past tense).
3. Confirm no document besides the governing plan presents a propositions table, milestone schedule, gate table or descope ladder as current.

## Verification checklist (run after editing)

- [ ] Title says 28 build milestones; revision record has the 2026-08-20 merge entry.
- [ ] "What AEGIS must prove" has exactly six rows; the sixth is marked blocked until `v1.2-cloud-operation`.
- [ ] Two market-position registers present; the "already runs" sentence appears only in the service register.
- [ ] Days 22–28 all present with track labels, deliverables and done-when; Day 22 starts only after `v1.0-aegis`.
- [ ] Two release-label invariants and both budget/trigger pairs present; effort-log labels `day-22`…`day-28` specified.
- [ ] Variance taxonomy present and referenced by Day 25, Day 27 and integration gate 6.
- [ ] Cloud-spend package present; no absolute spend cap stated anywhere.
- [ ] Issuance-revocation and active-token-containment both specified in Day 23 with a declared window.
- [ ] Both offer rows, the assessment instrument and the exact Day 28 README text present.
- [ ] Article 4 appears as *published, link-checked* in Day 28, the non-slippable layer, the v1.2 mandatory core and gate 7 — nowhere as "draft".
- [ ] Migrated sections present with their integration additions; no "Day-22 = post-launch" wording survives.
- [ ] Both companion files carry accurate supersession banners.
