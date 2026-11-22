# A3: AutoSE, Issue In, Pull Request Out

A GitHub Actions workflow on a fork of TinyDB. It takes an issue through requirements, design, implementation, testing and release, then has an independent reviewer check the pull request. A person always makes the merge decision. The report is in [`report.pdf`](report.pdf).

## Fork
- Upstream: https://github.com/msiemens/tinydb
- Fork: https://github.com/RishabhDev01/tinydb
- Base commit: `edff96aeb2616402e9489d46e90a592c05565621` (`edff96a`)
- Workflow code at the end of the project: fork `master` at `d04b1e4` (after PR #35)
- Branch protection on `master`: PR required, no bypass, no force push, no deletion

## Models
| Role | Model | Provider |
|---|---|---|
| Planner (stages 1–2) | `gemini-3.8-flash` (fallback `openai/gpt-oss-120b`, then `openai/gpt-oss-20b`) | Google Gemini API, paid Tier 1 (fallback: Groq free tier) |
| Builder (stages 3–4) | `gemini-3.8-flash` (same fallback) | Google Gemini API, paid Tier 1 |
| Judge (stage 1 check) | `qwen/qwen3.8-27b` | Groq free tier |
| Reviewer (stage 6) | `gemini-4-hydrogen` (fallback `qwen/qwen3.8-27b`) | Google Gemini API, paid Tier 1 |
| Injection screen | `meta-llama/llama-prompt-guard-2-86m` | Groq free tier |

Each model is set by a repository variable (`PLANNER_MODEL`, `BUILDER_MODEL`, `JUDGE_MODEL`, `REVIEWER_MODEL`, `GUARD_MODEL`). Runs 1 to 14 used `gpt-oss-120b`/`-20b` on Groq for the planner and builder; later runs use Gemini (ADR-019). Each run records its models in `state.json`.

API keys are stored only as repository secrets (`GEMINI_API_KEY`, `GROQ_API_KEY`). Total recorded use: 2.37 M tokens, about US$2.1 on Gemini; Groq was free.

## How to trigger the workflow
A collaborator (owner, member or collaborator) can start a run on an issue in the fork in any of these ways:
- add the label `autose` to the issue;
- comment `/autose` on the issue;
- open Actions, choose **AutoSE**, then **Run workflow** with the issue number (optional: round, and the stage to start at).

The run ends with a pull request and a review comment. If the reviewer requests changes, the comment shows the command for a second round (`/autose round 2 implement` or `/autose round 2 design`), and a person decides whether to type it. The workflow never merges.

Two further workflows, also started by hand, were used for the evaluation:
- **AutoSE review only** runs the reviewer on any pull request. It was used for the seeded PRs and experiment E1.
- **AutoSE experiment E2** runs the builder alone, with the full or summarised hand-off.

## Decisions D1–D10 from the assignment
| D1 Splitting the work | D2 Control flow | D3 Hand-offs | D4 State | D5 Tools | D6 Models | D7 Checks | D8 Reviewer independence | D9 Safety and failures | D10 Triggers |
|---|---|---|---|---|---|---|---|---|---|
| ADR-001 | ADR-002 | ADR-003, 028 | ADR-004, 017, 029 | ADR-005, 014, 016, 025 | ADR-006 (superseded), 011, 019, 021 | ADR-007, 024, 026 | ADR-008, 021, 027 | ADR-009, 013, 015, 020, 022, 023, 026 | ADR-010, 026, 029 |

## Layout
```
report.pdf               the report
demo.mp4                 the demo video
architecture/views/      component view, sequence view (real runs), stage map
architecture/decisions/  ADR-001 ... ADR-029 (ADR-006 superseded, ADR-018 rejected; both kept)
workflow/                copy of the fork's .github/workflows/, autose/ (agent code and prompts),
                         skills/ and ARCHITECTURE.md
experiment/issues/       the 5 issue texts (2 bugs, 2 features, 1 vague)
experiment/hidden_tests/ acceptance tests kept outside the fork
experiment/seeded_prs/   the 5 reviewer-check PRs: diffs, labels.csv and answer key
experiment/variants.md   what each variant of experiments E1 and E2 changes, and the results
results/results.csv      one row per issue: outcome, hidden tests, tokens, runs
results/runs.md          links to every Actions run, pull request and review
results/seeded_reviews.csv, results/e2_handoff.csv   per-run data for the experiments
```

## Demo video
[`demo.mp4`](demo.mp4) (3 min 8 s, narrated). Direct link: https://github.com/RishabhDev01/autose-a3/blob/main/demo.mp4
Backup link (Google Drive): https://drive.google.com/file/d/1bTlspmt7U8KSJB5e7vj05uGFJsFw81Om/view?usp=sharing

It shows one complete real run on issue #5: the issue page, the `autose` label, the run log, pull request #23 and the independent review posted on it. It also shows the comment trigger on issue #6, three design decisions (patch-mode builder, the test-gaming check added after PR #26, designing around rate limits) and the evaluation results.
