# AEGIS Just-in-Time Development Register

## Operating principle

> **Build by default. Learn just in time when a named weakness blocks the quality of a decision, artifact, or commercial interaction. Stop learning when that weakness has been resolved well enough to continue building.**

This is not a reading list, syllabus, or credential plan. It controls scarce development time that may be used to close gaps AEGIS cannot efficiently supply through implementation alone. A resource is an input to practice; completion is not evidence of competence unless the changed judgment or behaviour is validated.

## Admission gate

A book, course, workshop, or extended reference enters active work only through a dated decision record that passes all four gates:

1. **Specific weakness** — name the decision, behaviour, artifact, or buyer expectation that is presently below standard. “Useful background” is not a weakness.
2. **Near-term conversion** — identify the current milestone or real commercial interaction that will improve. Draft or attempt the work first unless doing so would be unsafe or legally inappropriate.
3. **Timebox and opportunity cost** — set a maximum duration and name the build work it must not displace. No full course is a v1.0 prerequisite unless a dated re-plan explicitly changes scope and schedule.
4. **Validation and stop rule** — state the observable test of improvement and the condition that ends consumption. Finishing a chapter or video is not the validation.

## Capacity controls

- Maximum **three active resources** across the project and maximum **four focused learning hours per build week**.
- Activated learning time is recorded in `docs/evidence/effort-log.csv` and counts toward the 75/100-hour controls.
- At 75 hours, no new resource is activated without including it in the remaining-effort forecast. At 100 hours with a mandatory gate blocked, all development activity stops unless the dated re-plan identifies it as the shortest safe path to clearing that gate.
- Reading stops at the declared stop rule. Unfinished material returns to the post-v1.0 backlog; it does not expand to fill available time.
- Credentials require separate market evidence. The existing certification portfolio raises the threshold for another credential: it must unlock screening, buyer vocabulary, or access that AEGIS evidence does not already supply.
- Resource notes may be private. Only decisions, methods, limitations, or artifacts that support an AEGIS claim enter the evidence chain.

## Activation record

Copy this row for any activated resource. Keep completed and rejected decisions so the same resource is not repeatedly reconsidered.

| Decision date | Status | Named weakness and evidence | Resource portion | Milestone/interaction | Timebox | Build work protected | Changed output or behaviour | Validation | Stop rule | Actual time/outcome |
|---|---|---|---|---|---:|---|---|---|---|---|
| — | No active resource | No demonstrated blocker yet; build first | — | — | 0 h | All v1.0 work | — | — | Activate only through all four gates | — |

Allowed statuses: `candidate`, `active`, `complete`, `rejected`, or `post-v1.0`.

## Pre-authorized candidates — inactive until triggered

These rows define narrow responses to anticipated gaps. They are **not assigned reading** and consume no time until their activation test is met.

| Candidate gap | Narrow resource portion | Activation test | Earliest conversion point | Maximum initial timebox | Required change | Validation and stop rule |
|---|---|---|---|---:|---|---|
| Evaluation-statistics reasoning cannot be defended without relying on a library call | Targeted material on Wilson intervals, integer thresholds, sample-size effects, Cohen's kappa, judge calibration, slice uncertainty and multiple comparisons; use a reputable statistical reference and the selected implementation docs, not a general statistics course | The first Day 8 protocol draft or hand calculation contains an unexplained method choice, inconsistent result, or reviewer challenge the engineer cannot resolve | Before the Day 8 protocol and pre-result gate manifest freeze | 2 h | Revise the method rationale; add hand-checked fixtures for the declared Wilson and agreement calculations; state assumptions, limitations and slice interpretation | Fixtures agree with the pinned implementation and a reviewer can reproduce the threshold. Stop immediately; broader study is post-v1.0 |
| Discovery, scope, or executive framing is too technical or ambiguous | Selected sections of Peter Block's *Flawless Consulting* on contracting, discovery, resistance and feedback, or an equivalent consulting-craft source; do not read cover-to-cover during the build | After the initial Day 1 engagement brief/advisory skeleton is attempted, a checklist or reviewer finds unclear buyer outcome, decision rights, assumptions, exclusions, or next decision | Day 1 revision; revisit the notes before Day 19 issuance | 1.5 h | Improve discovery questions, engagement boundaries, assumptions/exclusions and the executive recommendation structure | Advisory reviewer finds no critical scope ambiguity and can identify the buyer decision without reading code. Stop; value-pricing and negotiation study waits until before the first paid proposal |
| Governance crosswalk copies control language but lacks an auditor's management-system reasoning | A short structured ISO/IEC 42001 primer or selected training modules covering management-system boundaries, roles, risk treatment, documented information, internal assurance and continual improvement; use the licensed standard and official/recognized guidance for actual mappings | The first Day 19 crosswalk draft cannot explain system boundary, control objective, owner, evidence, residual gap and review cadence, or an advisor flags checklist-style mapping | Before Day 19 final issuance | 2.5 h | Revise the crosswalk and readiness assessment to distinguish implemented, partial and planned controls without implying certification or legal sign-off | Each mapped control has scope, owner, evidence, gap and action; reviewer accepts the reasoning. Stop; a full ISO course/certification remains post-v1.0 |
| FinOps buyer vocabulary or screening signal is demonstrably missing | FinOps Certified Practitioner or a narrower recognized FinOps-for-AI learning path | After v1.0, at least two relevant role descriptions, recruiter screens, or prospect conversations show the credential/vocabulary would materially improve access; AEGIS cost artifacts alone did not resolve the objection | Post-v1.0 commercial phase; never a Days 15–17 prerequisite | Dated re-plan required | Earn the credential if justified and update the diagnostic language only where it improves buyer comprehension | Record the market evidence and a resulting screening, proposal or buyer-language improvement. Cancel if the evidence is absent or the course duplicates AEGIS proof |
| Value pricing, negotiation and proposal conversion are weak in a real opportunity | Selected material on value-based fees, negotiation and proposal structure, paired with a real proposal review | A qualified prospect reaches proposal stage and the engineer cannot clearly connect scope, value, risk allocation and fee structure | After v1.0 and before the first paid proposal | 3 h initial study/practice | Produce a concise proposal with outcomes, scope, exclusions, responsibilities, evidence, options and commercial assumptions | Independent commercial review finds no critical ambiguity and the proposal is usable. Stop; continue learning from actual proposal outcomes |

## Rejected by default

- General “AI mastery” curricula, broad reading challenges, and cover-to-cover study without a current blocker.
- Another agent-framework course when the required capability can be learned through the pinned documentation and the current milestone.
- A credential added only to make the credential list longer.
- Any resource whose completion becomes a substitute for an executable test, decision record, reviewer challenge, or buyer conversation.
- Passive consumption after the declared validation has passed.

## Post-v1.0 review

At release, review the rejected, completed, and post-v1.0 rows against actual reviewer findings, role descriptions, recruiter screens, prospect conversations, and proposal outcomes. Promote only the smallest resource that addresses a repeated observed gap. The default remains no new course.
