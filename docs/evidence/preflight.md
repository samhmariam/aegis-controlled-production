# Sprint 1 preflight record

**Checked on:** 2026-09-05
**Checked by:** Samuel H. Mariam
**Host:** Windows 11 Home 10.0.26200
**Repository:** C:\Users\samue\Downloads\GTMS at commit 29a6c7a

| Capability | Command | Observed output | Verdict | Blocks Day 1? |
| --- | --- | --- | --- | --- |
| uv | `uv --version` | uv 0.9.9 | available | — |
| Python 3.12 | `uv python find 3.12` | <fill in> | <fill in> | yes if missing |
| Git | `git --version` | 2.50.0.windows.1 | available | — |
| Docker CLI | `docker --version` | 28.5.1 | available | no |
| Docker daemon | `docker info` | <fill in> | <fill in> | no |
| GitHub CLI | `gh auth status` | command not found | unavailable — gh not installed | no |
| GitHub Actions | n/a | not attempted — no gh CLI; visibility from `git remote -v` | not attempted | no |
| Model provider | n/a | <fill in> | <fill in> | no — Sprint 1 uses ScriptedModelGateway |
| Azure / Entra | `az account show` | <fill in> | <fill in> | no — Sprint 1 is local |
| Secrets tracked | `git ls-files` review | none | clean | yes if dirty |

## Limitations carried into Sprint 1

- <one line per unavailable capability, naming the day it first matters>

## Consequence

Only Python/uv and local package installation block Day 1. Every other unavailable capability is
recorded as a limitation and does not stop the sprint.
