# Day 0 — Environment and Access Preflight

**Date started:** YYYY-MM-DD
**Status:** in progress | closed | blocked

| # | Item | Result | Verified against | Date | Notes |
|---|---|---|---|---|---|
| 1 | Python runtime and toolchain | | | | Python / uv / git versions |
| 2a | Baseline model API + billing | | | | provider, models available |
| 2b | Alternate model API + billing | | | | provider chosen, deprecation policy URL |
| 3 | Azure subscription, region, offer | | | | offer type; spending-limit eligible Y/N; region |
| 4 | Entra app registration rights | | | | app create succeeded Y/N |
| 4b | Entra federated credential rights | | | | credential create succeeded Y/N |
| 5 | GitHub OIDC + repo visibility | | | | public/private; Actions enabled |
| 6 | Expected cloud cost estimate | | | | monthly figure + SKUs assumed |

## Decisions recorded

- **Alternate model provider:** (feeds Day 14 migration regression)
- **Azure region:** (feeds Day 26 IaC)
- **Spending-limit eligibility:** (feeds Day 22 spend-control package)
- **Repository visibility and anchor trust model:** (feeds Day 7b)

## Blocked items

| Item | Owner | Request raised | Expected resolution | Blocks |
|---|---|---|---|---|

## Privacy note

Identifiers (tenant ID, subscription ID, app object IDs) are deliberately not recorded here; this file is public. They are held locally in an untracked file.