# Runs: every Actions run, PR and review

Fork: https://github.com/RishabhDev01/tinydb (base `edff96a`)

## Issue ↔ experiment file map

| Fork issue | Experiment file | Type | Hidden tests |
|---|---|---|---|
| [#3](https://github.com/RishabhDev01/tinydb/issues/3) | `issue-1-bug-partial-update.md` | bug | `test_issue_1_partial_update.py` |
| [#4](https://github.com/RishabhDev01/tinydb/issues/4) | `issue-2-bug-string-doc-ids.md` | bug | `test_issue_2_string_doc_ids.py` |
| [#5](https://github.com/RishabhDev01/tinydb/issues/5) | `issue-3-feature-pluck.md` | feature | `test_issue_3_pluck.py` |
| [#6](https://github.com/RishabhDev01/tinydb/issues/6) | `issue-4-feature-append.md` | feature | `test_issue_4_append.py` |
| [#7](https://github.com/RishabhDev01/tinydb/issues/7) | `issue-5-vague-search-results.md` | vague | `test_issue_5_search_isolation.py` |

## Setup PRs (human-authored, merged by the maintainer)

| PR | What |
|---|---|
| [#1](https://github.com/RishabhDev01/tinydb/pull/1) | ARCHITECTURE.md, spec-writer skill, slim CI (ADR-012) |
| [#2](https://github.com/RishabhDev01/tinydb/pull/2) | AutoSE agents, orchestrator, workflow |
| [#8](https://github.com/RishabhDev01/tinydb/pull/8) | Fit requests to the Groq 8k-TPM limit (ADR-013), after run #2 below |
| [#9](https://github.com/RishabhDev01/tinydb/pull/9) | Resample on `output_parse_failed`, after run #9 below |

## AutoSE runs

| # | Run | Trigger | Issue | Result | Notes |
|---|---|---|---|---|---|
| 1 | [44937097207](https://github.com/RishabhDev01/tinydb/actions/runs/44937097207) | label `duplicate` | #3 | skipped | gate pre-filter: wrong label (ADR-010 evidence) |
| 2 | [44937234625](https://github.com/RishabhDev01/tinydb/actions/runs/44937234625) | label `autose` | #3 | **stopped at spec** | guard pass (0.0007); baseline 227; planner HTTP 413, 8033/8000 TPM, which led to **ADR-013**. Stop reason posted on the issue and in `state.json` |
| 3–8 | AutoSE #3–#8 | labels `bug`/`enhancement`/`question` | #3–#7 | skipped | type labels do not trigger runs (ADR-010) |
| 9 | [44938351640](https://github.com/RishabhDev01/tinydb/actions/runs/44938351640) | comment `/autose` | #3 | **stopped at spec** | 413 is gone (first call 1,692 tokens). New failure: HTTP 400 `output_parse_failed`, because gpt-oss emitted its reasoning ("We need spec. Identify behavior…") instead of a tool call. The retry code only handled `tool_use_failed`. Fix: resample on both, and drop the reasoning setting after 2 failures (fork [PR #9](https://github.com/RishabhDev01/tinydb/pull/9)) |
| 10 | [44939124496](https://github.com/RishabhDev01/tinydb/actions/runs/44939124496) | comment `/autose` | #3 | **stopped at implement** (19m27s) | guard ✔; **spec ✔** (4 ACs, judge passed on 1st attempt); **design ✔** (`Table.update` + tests). Builder used 40/40 turns with **0 edits applied**: 13 × `read_file(line_start/line_end)` rejected as "bad arguments", 9 × `edit_file` "not found" (indentation mismatch), the rest re-reading. The `output_parse_failed` resample fired and recovered. Tokens: planner 22.5k, judge 0.9k, builder 165k. Led to **ADR-014** (tolerant tools, `replace_lines`) |
