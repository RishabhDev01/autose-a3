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
| [#16](https://github.com/RishabhDev01/tinydb/pull/16) | Stated turn budget and forced `finish` in the last 3 turns; spec prompt says behaviour, not implementation (ADR-020), after run #16 below |
| [#18](https://github.com/RishabhDev01/tinydb/pull/18) | Reviewer on **gemini-4-hydrogen** (a different series from the builder), fallback qwen (ADR-021), after run #17's slow Groq review |
| [#19](https://github.com/RishabhDev01/tinydb/pull/19) | Planner budget 150k → 400k tokens; budgets set by repo variables (ADR-022), after run #20 below |
| [#20](https://github.com/RishabhDev01/tinydb/pull/20) | Builder `max_tokens` 3000 → 12000, cut-off answers reported as cut-offs, builder budget 200k (ADR-023), after run #21 below; also resets code and counters on a restart at spec/design |
| [#21](https://github.com/RishabhDev01/tinydb/pull/21) | Failing tests named with line and error (`failure_digest`); helper code always shown by `localize`; ARCHITECTURE.md invariant 2 states the `str`/`int` doc-ID key forms, and the builder gets §4 (ADR-024), after run #22 below. **Human context edit**, see ADR-024 |
| [#24](https://github.com/RishabhDev01/tinydb/pull/24) | `localize` shows the module (full if small, else outline) for a new module-level function (ADR-025), after run #25 below |
| [#27](https://github.com/RishabhDev01/tinydb/pull/27) | Test-gaming check at stage 3; stop on a conflict with pinned behaviour; review round 2 started by `/autose round 2 <stage>` (ADR-026), after runs #27–#28 below |
| [#28](https://github.com/RishabhDev01/tinydb/pull/28) | Review-only workflow (`autose-review.yml`) for the seeded PRs and experiment E1; reviewer code from master (ADR-027) |
| [#34](https://github.com/RishabhDev01/tinydb/pull/34) | Experiment E2 harness: `HANDOFF=full|summary`, `autose/experiment.py`, matrix workflow `autose-e2.yml` (ADR-028) |
| [#35](https://github.com/RishabhDev01/tinydb/pull/35) | A label or `/autose` trigger after a released run starts fresh instead of resuming at release (ADR-029), after run #29 below |

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
| 15 | [44979414380](https://github.com/RishabhDev01/tinydb/actions/runs/44979414380) | comment `/autose` | #3 | **stopped at design** (~1 min) | First Gemini run (ADR-019). It **resumed at design** as saved (`start=design`) and synced with master (`2530478`). Then the planner's first Gemini call returned `HTTP 400: Invalid Auth key`: the `GEMINI_API_KEY` secret value was wrong. A setup error, not a code fault. Fix: re-enter the secret with the full key |
| 16 | [44979706645](https://github.com/RishabhDev01/tinydb/actions/runs/44979706645) | comment `/autose` | #3 | **stopped at spec** (~2 min) | **The Gemini key works**: the planner (gemini-3.8-flash) made 20 well-formed tool calls with no 429s. But it researched the *fix* (`copy`, `_read_table`, storage internals) instead of writing the spec, and never called `finish`, so `AgentStopped: max_turns=20`. Led to **ADR-020** (stated turn budget, forced finish) |
| 17 | [44980211177](https://github.com/RishabhDev01/tinydb/actions/runs/44980211177) | comment `/autose` | #3 | **build ✔, PR [#17](https://github.com/RishabhDev01/tinydb/pull/17) with green CI; review failed** (29m38s) | **First complete build** (2m28s on Gemini 3.8 Flash): guard ✔, spec ✔ (4 ACs, judge passed on 1st attempt), design ✔ (2 rows), **implement+test ✔ on attempt 1** (builder: 1 call, about 3k tokens), release ✔ (PR #17, CI green). Review (qwen on Groq free, 26m48s): about 50 s 429 waits per turn, read `table.py` chunk by chunk, and was **forced to finish at turn 23** (ADR-020 worked). The verdict was rejected by `validate()` (it never ran the full tests). The second attempt started, then hit qwen's daily limit (`Used 192412/200000`), so there is **no verdict**. The post job commented "review round 1 failed … handing over to a human" on PR #17, as designed. Tokens: planner 126k (29 calls), builder 3k. Led to **ADR-021** (reviewer on Gemini 4 Hydrogen) |
| 18 | [44982638273](https://github.com/RishabhDev01/tinydb/actions/runs/44982638273) | `workflow_dispatch` (issue 3, round 1, start=release) | #3 | **review failed: Google billing** (1m45s) | Release reused PR #17, synced with master, CI ✔. The reviewer's first Gemini call returned `HTTP 403: Your billing account has an outstanding balance`. AI Studio then showed "payment issue … billing account inactive, 0 projects, Unavailable Tier". An account problem, not a code fault; the maintainer must fix the payment in Cloud Console |
| 19 | [44990334394](https://github.com/RishabhDev01/tinydb/actions/runs/44990334394) | `workflow_dispatch` (issue 3, round 1, start=release) | #3 | **✔ complete: review APPROVE** (1m45s) | After the billing fix. Release reused PR #17, synced with master, CI ✔. **Review on gemini-4-hydrogen took 30 s** (vs 26m48s on Groq qwen in run 17): 3 calls, 10,763 prompt + 578 completion tokens. Ran the full suite (231 passed, 1 skipped), mapped both issue requirements to `table.py:838` (`copy.deepcopy` in `_update_table`) and the 4 AC tests, and checked 2 risks (nested mutables; existing `_update_table` callers). Verdict posted on PR #17; **not merged** (maintainer decides) |
| 20 | [44990628889](https://github.com/RishabhDev01/tinydb/actions/runs/44990628889) | `workflow_dispatch` (issue 4, round 1, start=auto) | #4 | **stopped at design: budget** (1m53s) | guard ✔ (0.001); **spec ✔** (5 ACs, judge passed on 1st attempt, 41 s). Design stopped with `BudgetExceeded: planner used 153744 tokens, budget 150000` (34 planner calls across spec and design). The 150k per-run planner budget was sized for Groq; on Gemini each turn carries about 4k tokens of context. Cost of the run was about $0.12. Led to **ADR-022** |
| 21 | [44990995937](https://github.com/RishabhDev01/tinydb/actions/runs/44990995937) | `workflow_dispatch` (issue 4, round 1, start=design) | #4 | **stopped at test** (3m59s) | After PR #19. **Design ✔** (4 rows: `Table.get`, `remove`, `update` + tests). The builder failed 3 attempts, went back to design (ADR-002), and failed 3 more. The **6 builder calls averaged 2,994 of `max_tokens` 3000 completion tokens**: Gemini counts thinking as output, so answers replacing 3 functions were cut off. 3 attempts were reported as format errors ("no python code block"); the others failed tests. The redesign, steered by that feedback, switched to `str(doc_id)` keys, which cannot match the int keys `_update_table` passes in. Tokens: planner 171k (36 calls), builder 26k in / 18k out. Led to **ADR-023** |
| 22 | [44991617605](https://github.com/RishabhDev01/tinydb/actions/runs/44991617605) | `workflow_dispatch` (issue 4, round 1, start=design) | #4 | **stopped at test** (7m14s) | After PR #20. **ADR-023 worked**: answers were complete or reported as cut off (2 of 6 hit even 12k: `truncated: 2`, builder 37k output tokens). Design ✔ twice, but **both designs were wrong about doc-ID key types**. `get()` reads `_read_table()`, whose keys are **str** (storage form), while the `_update_table` updater sees **int** keys. Run 21's redesign assumed str everywhere; run 22's designs assumed int everywhere, so `get()` looked up `table.get(1)` on str keys and returned `None`. Re-running the final branch locally: **19 failed, 214 passed** (`test_get_ids`, `test_get_multiple_ids`, `test_contains_ids`, `test_doc_ids_json`, `test_move_document_between_tables`, …, plus 2 of its own AC tests). The builder also deleted the docstrings and comments of the 3 functions it replaced. The feedback it got was the tail of the pytest output (19 one-line `assert None…` summaries) with no traceback, and `localize` sent no helper (`_read_table`) because the 3 large functions filled the budget. **No PR was opened** (the stage-4 check blocked broken code). Tokens: planner 160k (34 calls), builder 27k in / 37k out |
| 23 | [44992783565](https://github.com/RishabhDev01/tinydb/actions/runs/44992783565) | `workflow_dispatch` (issue 4, round 1, start=design) | #4 | **✔ complete: PR [#22](https://github.com/RishabhDev01/tinydb/pull/22), CI green, review APPROVE** (3m16s) | After PR #21 (ADR-024, including the human ARCHITECTURE.md edit). Restart reset the code and counters (ADR-023). **Design ✔ on attempt 1** (4 rows); **implement+test ✔ on attempt 1** (builder: 1 call, 4.7k in / 3.0k out; no truncation). The fix keeps `get`'s `str` lookup and only converts the returned ID with `document_id_class`; `update`/`remove` convert `doc_ids` to `document_id_class` and skip values that cannot be converted. Review (gemini-4-hydrogen, 44 s, 4 calls, 16k tokens): ran the suite (232 passed, 1 skipped), mapped 3 requirements to code lines and AC tests, checked 2 risks (non-convertible IDs; `get(doc_ids)`/`contains` consistency). Tokens: planner 85k (18 calls). **Not merged** (maintainer decides) |
| 24 | [44993182187](https://github.com/RishabhDev01/tinydb/actions/runs/44993182187) | `workflow_dispatch` (issue 5, round 1, start=auto) | #5 | **✔ complete: PR [#23](https://github.com/RishabhDev01/tinydb/pull/23), CI green, review APPROVE** (3m8s) | First full run straight from guard with no fix needed. guard ✔ (0.001). **Spec**: the judge rejected AC-5 on attempt 1 ("redundant, non-standard boolean list expression" in its Then clause); the planner fixed it, and attempt 2 passed (5 ACs). Design ✔ (2 rows). **Implement+test**: attempt 1 BUILD FAILED (stage-3 compile/import check), attempt 2 ✔. The change is a 12-line `Table.pluck(field)` over `_read_table().values()` that skips documents without the field and keeps `None` values. Review (gemini-4-hydrogen, 32 s, 3 calls): 232 passed, 1 skipped; 3 requirements mapped; 3 risks checked (empty table, `None` values, §4 invariants). Tokens: planner 88k (22 calls), judge 1.5k, builder 4.9k in / 1.3k out. **Not merged** |
| 25 | [44993561408](https://github.com/RishabhDev01/tinydb/actions/runs/44993561408) | `workflow_dispatch` (issue 6, round 1, start=auto) | #6 | **stopped at implement** (1m21s) | guard ✔ (0.001); **spec ✔** (4 ACs, judge passed on 1st attempt); **design ✔** (2 rows: `append (NEW)` in `tinydb/operations.py` + tests), correct. Then `the design names no existing definition or class under tinydb/ to change`: `localize` handled new methods (class outline) but not new **module-level** functions, so it returned no code blocks. A pipeline bug, not an agent error; no builder tokens spent. Tokens: planner 37k (10 calls). Led to **ADR-025** |
| 26 | [44993893882](https://github.com/RishabhDev01/tinydb/actions/runs/44993893882) | `workflow_dispatch` (issue 6, round 1, start=design) | #6 | **✔ complete: PR [#25](https://github.com/RishabhDev01/tinydb/pull/25), CI green, review APPROVE** (2m13s) | After PR #24 (ADR-025). Design ✔ on attempt 1 (2 rows); **implement+test ✔ on attempt 1** (builder: 1 call, 2.2k in / 0.6k out; it saw the whole `operations.py`). The change is `operations.append(field, val)`: it appends to a list field, or creates `[val]` if the field is missing, in the same style as `add`/`set`. Review (gemini-4-hydrogen, 31 s, 3 calls): 231 passed, 1 skipped; 2 requirements mapped; 2 risks checked (non-list field raises `AttributeError`; cache invalidation through `update`). Tokens: planner 14k (4 calls). **Not merged** |
| 27 | [44994263819](https://github.com/RishabhDev01/tinydb/actions/runs/44994263819) | `workflow_dispatch` (issue 7, round 1, start=auto) | #7 (vague) | **PR [#26](https://github.com/RishabhDev01/tinydb/pull/26), CI green, review CHANGES REQUESTED: the builder gamed the test** (7m40s) | guard ✔; spec ✔ (4 ACs, judge passed on 1st attempt; read as "search results must be independent copies"); design ✔. Every attempt failed **exactly 1 test** (the ADR-024 digest named it): `test_query_cache_documents_are_shared_with_cache`, an existing test that pins the documented behaviour (ARCHITECTURE.md invariant 3: cached documents are shared). The issue asks for the opposite. The builder may only write `tinydb/*.py` and its own new test file, so the legitimate fix (change that test) was out of its reach. After 3 attempts, a redesign and 2 more, **attempt 6 passed by special-casing the test**: `Table.search()` walks the call stack with `sys._getframe` and, if the caller is `test_query_cache_documents_are_shared_with_cache`, runs the old shared-cache code; everyone else gets deep copies. **All deterministic checks passed (231 tests, CI green). The independent reviewer (gemini-4-hydrogen, 5 calls) caught it**: risk "Legacy test special-casing in production code" = DEFECT; finding: remove the `sys._getframe` branch and update or remove the legacy test; route back to `implement`. Also: one attempt tried to edit a non-`tinydb/` file (blocked by `_check_path`), one hit the format/cut-off. Tokens: planner 217k (49 calls), builder 18k in / 21k out, reviewer 23k |
| 28 | [44994832774](https://github.com/RishabhDev01/tinydb/actions/runs/44994832774) | `workflow_dispatch` by `github-actions[bot]` (round 2) | #7 | **skipped by the gate** (12s) | The post job dispatched review round 2, but the gate rejects any event sent by a bot (ADR-010 loop guard): `run=false (event sent by a bot)`. The PR comment "Starting round 2 at stage implement" is therefore wrong; round 2 never ran. Inconsistency between the post job and the gate |
| 29 | [45004971036](https://github.com/RishabhDev01/tinydb/actions/runs/45004971036) | **label `autose`** on issue #5 (demo) | #5 | release + review only (1m51s) | Gate: `run=true (labeled by RishabhDev01)`. But setup logged `start=release`: the branch's `state.json` (committed before release) still said `next=release`, so the run reused PR #23, CI ✔, review approve (Hydrogen, 2 calls). Not a full run. Led to **ADR-029** |
| 30 | [45005311148](https://github.com/RishabhDev01/tinydb/actions/runs/45005311148) | **label `autose`** (removed and re-added) on issue #5 (demo) | #5 | **✔ complete: PR [#23](https://github.com/RishabhDev01/tinydb/pull/23), CI green, review APPROVE** (2m40s) | After PR #35. `start=guard`; guard 0.001; spec ✔ (5 ACs, first try); design ✔; builder attempt 1 BUILD FAILED, attempt 2 ✔; release, CI ✔ ([45005411616](https://github.com/RishabhDev01/tinydb/actions/runs/45005411616)); review approve (3 requirements, 3 risks). Hidden tests 9/9 (Python 3.12). Screenshots 06–21 in `demo/screenshots/` |
| 31 | [45005712745](https://github.com/RishabhDev01/tinydb/actions/runs/45005712745) | **comment `/autose`** on issue #6 (demo) | #6 | **✔ complete: PR [#25](https://github.com/RishabhDev01/tinydb/pull/25), CI green, review APPROVE** (2m18s) | Gate: `run=true (/autose by RishabhDev01)`; bot reply on the issue: "round 1 started at stage `guard`". Spec ✔ (4 ACs); design ✔; builder ✔ on attempt 1 (new module-level function, `blocks ['MODULE']`, ADR-025); release; review approve (3 requirements, 2 risks). Hidden tests 9/9. Screenshots 22–30 |

> **Note on runs 10–12:** their code was current, but their prompts, skill and ARCHITECTURE.md came from the issue branch at `585c29b` (ADR-017). Their failures are real, but ADR-014's *prompt* change was never in effect.

## Hidden acceptance tests (run locally, 2026-11-22)

Each AutoSE branch was checked out at its final state (re-run on **Python 3.12**, the CI version; results unchanged, suite counts are the 3.12 ones), `experiment/hidden_tests/` was copied in, and the relevant file was run (3 storages each). The fork's own suite was also run. Master baseline: **39 failed, 9 passed** (as documented in `experiment/hidden_tests/README.md`), 228 passed in the repo suite.

| Experiment issue | Branch (PR) | Hidden tests | Repo suite | Review |
|---|---|---|---|---|
| 1 bug: partial update | `autose/issue-3` ([#17](https://github.com/RishabhDev01/tinydb/pull/17)) | **9/9** | 232 passed | approve |
| 2 bug: string doc IDs | `autose/issue-4` ([#22](https://github.com/RishabhDev01/tinydb/pull/22)) | **12/12** | 233 passed | approve |
| 3 feature: `pluck` | `autose/issue-5` ([#23](https://github.com/RishabhDev01/tinydb/pull/23)) | **9/9** | 233 passed | approve |
| 4 feature: `append` | `autose/issue-6` ([#25](https://github.com/RishabhDev01/tinydb/pull/25)) | **9/9** | 232 passed | approve |
| 5 vague: result isolation | `autose/issue-7` ([#26](https://github.com/RishabhDev01/tinydb/pull/26)) | 7/9 | 232 passed | changes (test gaming) |

Issue 5: the change deep-copies `search()` results only; `test_get_result_mutation_does_not_leak` fails on `memory` and `caching`, because `get(cond)` still returns the stored object. The branch also contains the gamed `sys._getframe` branch, so it is not a valid solution regardless (ADR-026). The reviewer's verdict (changes) agrees with the hidden tests: every approved PR passes all its hidden tests, and the one PR it rejected does not. Per-run numbers are in `results.csv`.

## Reviewer calibration on 5 seeded PRs (ADR-008, ADR-027)

Five hand-written PRs (#29–#33; answer key in `experiment/seeded_prs/README.md`), all with green tests, reviewed by `gemini-4-hydrogen` through the review-only workflow. The reviewer saw only the issue and the diff.

| Seeded | PR | Truth | Verdict | Right reason? | Run |
|---|---|---|---|---|---|
| S1 | [#29](https://github.com/RishabhDev01/tinydb/pull/29) | buggy (swallows `KeyError`, keeps partial update) | **changes** → design | yes: "swallows KeyError/TypeError instead of failing atomically" | [44996163932](https://github.com/RishabhDev01/tinydb/actions/runs/44996163932) |
| S2 | [#30](https://github.com/RishabhDev01/tinydb/pull/30) | buggy (`remove` only) | **changes** → implement | yes: `update` not converted (line 465), `get` returns `str` doc_id (line 369) | [44996293421](https://github.com/RishabhDev01/tinydb/actions/runs/44996293421) |
| S3 | [#31](https://github.com/RishabhDev01/tinydb/pull/31) | buggy (`None` for missing field) | **changes** → implement | yes: "returns None ... rather than skipping"; no test for missing fields | [44996311924](https://github.com/RishabhDev01/tinydb/actions/runs/44996311924) |
| S4 | [#32](https://github.com/RishabhDev01/tinydb/pull/32) | buggy (shared mutable default) | **changes** → implement | yes: "mutable default argument ... share the same list instance" | [44996329084](https://github.com/RishabhDev01/tinydb/actions/runs/44996329084) |
| S5 | [#33](https://github.com/RishabhDev01/tinydb/pull/33) | correct | **approve** | yes, no findings | [44996347841](https://github.com/RishabhDev01/tinydb/actions/runs/44996347841) |

**Result: 4/4 seeded bugs caught for the right reason, 0/1 false alarms; approval rate on buggy PRs 0%.** About 30 s and 6–22k tokens per review. With the 4 AutoSE PRs (approved, all hidden tests pass) and PR #26 (rejected, gamed; fails 2 hidden tests), the reviewer agreed with ground truth on **10/10** PRs. Per-review numbers: `results/seeded_reviews.csv`.

## Experiment E1: reviewer model (same 5 seeded PRs)

The same five seeded PRs were reviewed by the **builder's model**, `gemini-3.8-flash`, through the same workflow and prompt (only `reviewer_model` changed). This is the "same model as the author" option that ADR-008 rejected.

| Reviewer | Bugs caught (right reason) | False alarms | LLM calls | Prompt / completion tokens | Cost (list price) |
|---|---|---|---|---|---|
| `gemini-4-hydrogen` (default, ADR-021) | **4/4** | **0/1** | 16 | 54,412 / 4,092 | **$0.11** |
| `gemini-3.8-flash` (builder's model) | **4/4** | **0/1** | 55 | 251,567 / 5,643 | $0.21 |

Per PR, Flash needed 5–18 calls (Hydrogen 2–5): for example, S5 took 18 calls and 91k prompt tokens with Flash vs 3 calls and 10k with Hydrogen. So **verdict quality was the same, but Flash cost about 1.9× more** despite half the per-token price, because it read far more code before deciding. Runs: `results/seeded_reviews.csv`.

**Limit of this test:** the seeded PRs were written by a human, not by the builder, so E1 measures each model's review skill, not the "shared blind spot" risk of a model reviewing *its own* output. The only builder-written defect so far is PR #26 (test gaming), which Hydrogen rejected.

**Follow-up: the builder's model reviewing its own gamed PR.** `gemini-3.8-flash` reviewed PR #26 (written by `gemini-3.8-flash` in run 27) in run [44996830372](https://github.com/RishabhDev01/tinydb/actions/runs/44996830372): **changes → design**, 7 calls, 28k tokens. It called the `sys._getframe` branch "test-tampering/cheating to bypass an existing test", and also recognised the real conflict: the PR "directly violates ARCHITECTURE.md Invariant 3", so the issue asks to change intended behaviour and should be rejected or decided by the maintainer. Hydrogen (run 27) also rejected the cheat but suggested updating the old test instead. So on this one builder-written defect, **the same model did not share the blind spot**. Its advice (route to design; a behaviour decision) even matches ADR-026's conflict stop more closely. One case is not enough to rule out the risk; the report should say so.

## Experiment E2: full vs 5-line summary hand-off (ADR-003, ADR-028)

One manual dispatch of `autose-e2.yml` ran 20 builder-only runs (issues #3–#7 × full/summary × 2 repetitions), with the spec and design frozen from each issue's AutoSE branch and no redesign. Results are on the `e2/*` branches; hidden tests were run on Python 3.12.

| | full | summary |
|---|---|---|
| Passed the orchestrator's checks | 8/10 | 7/10 |
| Passed all hidden tests | 8/10 | 7/10 |
| Hidden tests passed | **92/96** | 83/96 |
| Builder tokens in / out | 52.6k / 37.3k | 49.9k / 34.2k |

The summary arm lost one run (issue #5 rep 2: `list[Any]` without `Any` imported, so `import tinydb` fails on 3.12, three attempts in a row) and saved only about 5% of tokens. Issue #7 fails the same way in both arms (the pinned test, ADR-026). **Full artifacts stay (ADR-003).** Small sample: one run apart at n = 2 per cell. Full write-up: `experiment/variants.md`; per run: `results/e2_handoff.csv`.

> **Correction:** a first local pass of the hidden tests used Python 3.14, which evaluates annotations lazily and scored the broken issue-5 branch 9/9. All hidden-test results (issue branches, seeded PRs, E2) were re-run on Python 3.12: the issue and seeded results are unchanged; the repo-suite counts in `results.csv` were lowered by one (3.12 skips one test).

## Index of the other workflow runs

### CI run for each AutoSE pull request (stage 5)
| PR | Issue | CI run |
|---|---|---|
| [#17](https://github.com/RishabhDev01/tinydb/pull/17) | #3 | [44990369982](https://github.com/RishabhDev01/tinydb/actions/runs/44990369982) (re-run in run 19) |
| [#22](https://github.com/RishabhDev01/tinydb/pull/22) | #4 | [44992918065](https://github.com/RishabhDev01/tinydb/actions/runs/44992918065) |
| [#23](https://github.com/RishabhDev01/tinydb/pull/23) | #5 | [44993321665](https://github.com/RishabhDev01/tinydb/actions/runs/44993321665) |
| [#25](https://github.com/RishabhDev01/tinydb/pull/25) | #6 | [44993967530](https://github.com/RishabhDev01/tinydb/actions/runs/44993967530) |
| [#26](https://github.com/RishabhDev01/tinydb/pull/26) | #7 | [44994715480](https://github.com/RishabhDev01/tinydb/actions/runs/44994715480) |

### "AutoSE review only" runs (seeded PRs, E1)
| # | Run | PR reviewed | Reviewer model | Verdict |
|---|---|---|---|---|
| 1 | [44996163932](https://github.com/RishabhDev01/tinydb/actions/runs/44996163932) | [#29](https://github.com/RishabhDev01/tinydb/pull/29) S1 | gemini-4-hydrogen | changes |
| 2 | [44996293421](https://github.com/RishabhDev01/tinydb/actions/runs/44996293421) | [#30](https://github.com/RishabhDev01/tinydb/pull/30) S2 | gemini-4-hydrogen | changes |
| 3 | [44996311924](https://github.com/RishabhDev01/tinydb/actions/runs/44996311924) | [#31](https://github.com/RishabhDev01/tinydb/pull/31) S3 | gemini-4-hydrogen | changes |
| 4 | [44996329084](https://github.com/RishabhDev01/tinydb/actions/runs/44996329084) | [#32](https://github.com/RishabhDev01/tinydb/pull/32) S4 | gemini-4-hydrogen | changes |
| 5 | [44996347841](https://github.com/RishabhDev01/tinydb/actions/runs/44996347841) | [#33](https://github.com/RishabhDev01/tinydb/pull/33) S5 | gemini-4-hydrogen | approve |
| 6 | [44996533445](https://github.com/RishabhDev01/tinydb/actions/runs/44996533445) | [#29](https://github.com/RishabhDev01/tinydb/pull/29) S1 | gemini-3.8-flash | changes |
| 7 | [44996551796](https://github.com/RishabhDev01/tinydb/actions/runs/44996551796) | [#30](https://github.com/RishabhDev01/tinydb/pull/30) S2 | gemini-3.8-flash | changes |
| 8 | [44996572607](https://github.com/RishabhDev01/tinydb/actions/runs/44996572607) | [#31](https://github.com/RishabhDev01/tinydb/pull/31) S3 | gemini-3.8-flash | changes |
| 9 | [44996592925](https://github.com/RishabhDev01/tinydb/actions/runs/44996592925) | [#32](https://github.com/RishabhDev01/tinydb/pull/32) S4 | gemini-3.8-flash | changes |
| 10 | [44996619061](https://github.com/RishabhDev01/tinydb/actions/runs/44996619061) | [#33](https://github.com/RishabhDev01/tinydb/pull/33) S5 | gemini-3.8-flash | approve |
| 11 | [44996830372](https://github.com/RishabhDev01/tinydb/actions/runs/44996830372) | [#26](https://github.com/RishabhDev01/tinydb/pull/26) (AutoSE, gamed) | gemini-3.8-flash | changes |

Each verdict is in the run's job summary and in its `verdict.json` artifact.

### "AutoSE experiment E2" run
One dispatch, run [44997545427](https://github.com/RishabhDev01/tinydb/actions/runs/44997545427), with 20 builder jobs (issues #3–#7 × full/summary × 2 repetitions). Each job pushed its result to a branch `e2/<handoff>/issue-N-r<rep>` (for example [e2/full/issue-5-r1](https://github.com/RishabhDev01/tinydb/tree/e2/full/issue-5-r1)), with outcome, attempts and tokens in `.autose/issue-N/e2.json`. Per-job results: `results/e2_handoff.csv`.

## Maintainer decisions after review (2026-11-22)

The workflow never merges; these decisions were made by the maintainer after reading the reviews.

| PR | What | Decision | Why |
|---|---|---|---|
| [#26](https://github.com/RishabhDev01/tinydb/pull/26) | AutoSE PR for issue #7 (vague) | **open, not to be merged** (closed, then reopened so all five issue PRs are visible) | The reviewer requested changes: the builder special-cased an existing test (`sys._getframe`); it also fails 2 of 9 hidden tests. Changing the behaviour that invariant 3 pins is a product decision (ADR-026) |
| [#29](https://github.com/RishabhDev01/tinydb/pull/29)–[#33](https://github.com/RishabhDev01/tinydb/pull/33) | Seeded reviewer-calibration PRs S1–S5 | **closed, not merged** | They exist only to test the reviewer (ADR-027); the answer key and diffs are in `experiment/seeded_prs/` |
| [#17](https://github.com/RishabhDev01/tinydb/pull/17), [#22](https://github.com/RishabhDev01/tinydb/pull/22), [#23](https://github.com/RishabhDev01/tinydb/pull/23), [#25](https://github.com/RishabhDev01/tinydb/pull/25) | Approved AutoSE PRs for issues #3–#6 | left **open** for the maintainer | Approved, CI green, all hidden tests pass |

Closed PRs keep their diffs, reviews and branches, so every link above still opens.
