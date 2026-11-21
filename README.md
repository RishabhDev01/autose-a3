# A3 — AutoSE: Issue In, Pull Request Out

> Status: design phase. The ADRs and component view were committed before any agent code.

## Fork
- Upstream: https://github.com/msiemens/tinydb
- Fork: https://github.com/RishabhDev01/tinydb
- Pinned commit: `edff96aeb2616402e9489d46e90a592c05565621` (`edff96a`)
- Branch protection on `master`: PR required, no bypass, no force push, no deletion

## Models (all on the Groq free tier)
| Role | Model |
|---|---|
| Planner (stages 1–2) | `openai/gpt-oss-120b` |
| Builder (stages 3–4) | `openai/gpt-oss-120b` |
| LLM judge (stage 1 check) | `qwen/qwen3.8-27b` |
| Reviewer (stage 6) | `qwen/qwen3.8-27b` |
| Injection screen | `meta-llama/llama-prompt-guard-2-86m` |

Each model is set by a repository variable (see ADR-011, which supersedes ADR-006).

## How to trigger
On an issue in the fork, a collaborator either:
- adds the label `autose`, or
- comments `/autose`.

## Layout
```
architecture/views/      component view, sequence view, stage map
architecture/decisions/  ADR-001 … ADR-015 (ADR-006 superseded)
workflow/                copy of the fork's .github/workflows + autose/ agent code
experiment/              issues, hidden tests, seeded PRs, variants.md
results/                 results.csv, runs.md
```

## Demo video
TODO
