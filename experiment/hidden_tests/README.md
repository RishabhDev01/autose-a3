# Hidden acceptance tests

These are kept outside the fork, so no agent can read them. Each test runs on 3 storages: `memory`, `json`, and `caching` (`CachingMiddleware(MemoryStorage)`).

| Issue | File | Tests | Baseline at `edff96a` |
|---|---|---|---|
| 1 bug: partial update | `test_issue_1_partial_update.py` | 3 | fails on memory and caching; JSON already passes (the bug is the inconsistency) |
| 2 bug: string doc IDs | `test_issue_2_string_doc_ids.py` | 4 | 3 fail on all storages; `test_int_ids_still_work` passes (regression guard) |
| 3 feature: `pluck` | `test_issue_3_pluck.py` | 3 | all fail (no `pluck`) |
| 4 feature: `append` op | `test_issue_4_append.py` | 3 | all fail (no `append`) |
| 5 vague: result isolation | `test_issue_5_search_isolation.py` | 3 | all fail, except the `get` case on JSON |

Baseline: **39 failed, 9 passed** (48 = 16 tests × 3 storages).

## Run against an AutoSE branch
```bash
git -C tinydb checkout autose/issue-N
cp -r experiment/hidden_tests tinydb/hidden_tests_tmp
cd tinydb && python -m pytest -q -p no:cacheprovider -o addopts="" hidden_tests_tmp/test_issue_N_*.py
rm -rf hidden_tests_tmp
```

Issue 5 is deliberately vague. The hidden tests encode one reasonable reading: results are independent copies. An agent that picks a different reading, for example documenting the behaviour instead of changing it, will fail them. This is recorded as a limitation in the report.
