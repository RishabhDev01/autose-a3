# A3 — AutoSE: Issue In, Pull Request Out

> Status: design phase. The ADRs and component view were committed before any agent code.

## Fork
- Upstream: https://github.com/msiemens/tinydb
- Fork: https://github.com/RishabhDev01/tinydb
- Pinned commit: `edff96aeb2616402e9489d46e90a592c05565621` (`edff96a`)
- Branch protection on `master`: PR required, no bypass, no force push, no deletion

## Models
| Role | Model | Provider |
|---|---|---|
| Planner (stages 1–2) | `gemini-3.8-flash` (fallback: `openai/gpt-oss-120b`, then `openai/gpt-oss-20b`) | Google Gemini API, paid Tier 1 (fallback: Groq free) |
| Builder (stages 3–4) | `gemini-3.8-flash` (same fallback) | Google Gemini API, paid Tier 1 (fallback: Groq free) |
| LLM judge (stage 1 check) | `qwen/qwen3.8-27b` | Groq free tier |
| Reviewer (stage 6) | `gemini-4-hydrogen` (fallback: `qwen/qwen3.8-27b`) | Google Gemini API, paid Tier 1; a different series from the builder (ADR-021) |
| Injection screen | `meta-llama/llama-prompt-guard-2-86m` | Groq free tier |

Each model is set by a repository variable (see ADR-011, which supersedes ADR-006). Runs 1–14 used `openai/gpt-oss-120b`/`-20b` on Groq's free tier for the planner and builder. Later runs use Gemini (ADR-019). `state.json` in each run records the models used.

## How to trigger
On an issue in the fork, a collaborator either:
- adds the label `autose`, or
- comments `/autose`.

## Layout
```
architecture/views/      component view, sequence view, stage map
architecture/decisions/  ADR-001 … ADR-027 (ADR-006 superseded)
workflow/                copy of the fork's .github/workflows + autose/ agent code
experiment/              issues, hidden tests, seeded PRs, variants.md
results/                 results.csv, runs.md
```

## Demo video
TODO
