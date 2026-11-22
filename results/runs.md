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
| [#10](https://github.com/RishabhDev01/tinydb/pull/10) | Tolerant builder tools, `replace_lines` (ADR-014), after run #10 below |
| [#11](https://github.com/RishabhDev01/tinydb/pull/11) | Daily-quota fallback to gpt-oss-20b or stop fast (ADR-015), after run #11 below |
| [#12](https://github.com/RishabhDev01/tinydb/pull/12) | Patch-mode builder: localize → one-shot patch → validate; quota-stop resume; clean restart (ADR-016), after run #12 below |
| [#13](https://github.com/RishabhDev01/tinydb/pull/13) | Prompts, skill and ARCHITECTURE.md read from master at import; issue branch merged with master each run; complete reset with `--no-overlay` (ADR-017), after run #13 below |
| [#14](https://github.com/RishabhDev01/tinydb/pull/14) | **Closed, not merged.** Scheduled auto-resume (ADR-018, rejected): the maintainer keeps every run human-triggered |
| [#15](https://github.com/RishabhDev01/tinydb/pull/15) | Planner and builder on **Gemini 3.8 Flash (paid Tier 1)**; judge and reviewer stay on Groq qwen; fallback to Groq gpt-oss (ADR-019). Groq's Developer tier was closed to upgrades |

## AutoSE runs

| # | Run | Trigger | Issue | Result | Notes |
|---|---|---|---|---|---|
| 1 | [44937097207](https://github.com/RishabhDev01/tinydb/actions/runs/44937097207) | label `duplicate` | #3 | skipped | gate pre-filter: wrong label (ADR-010 evidence) |
| 2 | [44937234625](https://github.com/RishabhDev01/tinydb/actions/runs/44937234625) | label `autose` | #3 | **stopped at spec** | guard pass (0.0007); baseline 227; planner HTTP 413, 8033/8000 TPM, which led to **ADR-013**. Stop reason posted on the issue and in `state.json` |
| 3–8 | AutoSE #3–#8 | labels `bug`/`enhancement`/`question` | #3–#7 | skipped | type labels do not trigger runs (ADR-010) |
| 9 | [44938351640](https://github.com/RishabhDev01/tinydb/actions/runs/44938351640) | comment `/autose` | #3 | **stopped at spec** | 413 is gone (first call 1,692 tokens). New failure: HTTP 400 `output_parse_failed`, because gpt-oss emitted its reasoning ("We need spec. Identify behavior…") instead of a tool call. The retry code only handled `tool_use_failed`. Fix: resample on both, and drop the reasoning setting after 2 failures (fork [PR #9](https://github.com/RishabhDev01/tinydb/pull/9)) |
| 10 | [44939124496](https://github.com/RishabhDev01/tinydb/actions/runs/44939124496) | comment `/autose` | #3 | **stopped at implement** (19m27s) | guard ✔; **spec ✔** (4 ACs, judge passed on 1st attempt); **design ✔** (`Table.update` + tests). Builder used 40/40 turns with **0 edits applied**: 13 × `read_file(line_start/line_end)` rejected as "bad arguments", 9 × `edit_file` "not found" (indentation mismatch), the rest re-reading. The `output_parse_failed` resample fired and recovered. Tokens: planner 22.5k, judge 0.9k, builder 165k. Led to **ADR-014** (tolerant tools, `replace_lines`) |
| 11 | [44942070537](https://github.com/RishabhDev01/tinydb/actions/runs/44942070537) | comment `/autose` | #3 | **cancelled in implement** (2h30m job timeout) | guard ✔ (0.001); **spec ✔** (4 ACs, judge passed on 1st attempt, under 1 min); **design ✔** (3 rows) but took 87 min. Every gpt-oss-120b call got a 429 with `retry-after` of 423–1659 s, which means its **daily token quota** was spent (runs 9–10 used about 190k). The builder made 3 read-only turns in 80 min. The new tools were not exercised. Led to **ADR-015** (fallback to gpt-oss-20b or stop fast) |
| — | — | — | — | — | Actions were disabled on the fork after run 11. The `/autose` comments at 00:55 and 00:59 UTC started no run until the maintainer re-enabled workflows |
| 12 | [44969611049](https://github.com/RishabhDev01/tinydb/actions/runs/44969611049) | comment `/autose` | #3 | **stopped at implement** (22m38s) | **ADR-015 worked**: 120b hit `tokens per day (TPD): Limit 200000, Used 197443` in design, and the run fell back to gpt-oss-20b with no long sleeps. guard ✔; **spec ✔** (4 ACs, judge passed on 1st attempt); **design ✔** (`Table._update_table`). Builder (20b, 40/40 calls) hit max_turns again: read `_update_table` 4×, `conftest.py` 2×, rewrote its test file 3×, never finished. Tokens: builder 179k, planner 35k. Led to **ADR-016** (patch-mode builder) |
| 13 | [44972517581](https://github.com/RishabhDev01/tinydb/actions/runs/44972517581) | comment `/autose` | #3 | **crashed after design** (3m23s) | guard ✔; 120b still at its daily limit (`Used 197186`), so the planner fell back to 20b; **spec ✔** (4 ACs; the qwen judge needed six per-minute 429 retries); **design ✔** (2 rows). Then `FileNotFoundError: autose/prompts/builder_patch.md`: the orchestrator read its prompts from the stale issue branch (cut at `585c29b`, PR #2). So **runs 10–12 also ran with the PR #2 prompts** (e.g. run 12's builder prompt never mentioned `replace_lines`). Led to **ADR-017** |
| 14 | [44973325961](https://github.com/RishabhDev01/tinydb/actions/runs/44973325961) | comment `/autose` | #3 | **stopped at design, quota** (2m52s) | **ADR-017 worked**: the branch was synced with master (`422a4b9`), run 12's leftover test file was deleted, and the prompts came from master. guard ✔; **spec ✔** (3 ACs, judge passed on 1st attempt). Design: 120b at `Used 199449/200000`, fell back to 20b, then 20b at `Used 195763/200000`, so **`QuotaExhausted` stopped the run in seconds** (ADR-015). `state.json` has `resume_at: design`, so the next trigger skips guard and spec (ADR-016). Tokens: planner 22k (6 of 8 calls on 20b) |

> **Note on runs 10–12:** their code was current, but their prompts, skill and ARCHITECTURE.md came from the issue branch at `585c29b` (ADR-017). Their failures are real, but ADR-014's *prompt* change was never in effect.
