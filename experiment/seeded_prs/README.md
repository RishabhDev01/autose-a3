# Seeded PRs: answer key for the reviewer calibration (ADR-008, ADR-027)

Five hand-written PRs on the fork: four contain a known bug and one is correct. They are written like ordinary PRs, each with a passing test file, so **CI is green on all five** and only a review can tell them apart.

**The reviewer never sees this file.** It lives in the submission repo, and the reviewer sees only the issue and the diff (`autose/review.py`), not the PR title or description. The PR descriptions on the fork say only "seeded PR … Do not merge".

Fork base: `6766223` (master after PR #27).

| Id | PR | Branch | Issue | Truth | The seeded defect | What a good review says |
|---|---|---|---|---|---|---|
| S1 | [#29](https://github.com/RishabhDev01/tinydb/pull/29) | `seeded/s1-update-skip-missing` | #3 partial update | **buggy** | `perform_update` catches `KeyError`/`TypeError` and skips that document. `update(increment('count'))` no longer raises, and the documents before and after the bad one stay changed: the half-applied update now happens on **every** storage, and the error is hidden. The returned IDs include the skipped document. | The issue asks for a failed update to leave the database unchanged; this swallows the error and keeps the partial update. |
| S2 | [#30](https://github.com/RishabhDev01/tinydb/pull/30) | `seeded/s2-remove-string-ids` | #4 string doc IDs | **buggy** | Only `remove(doc_ids=...)` converts string IDs. `update(..., doc_ids=['1'])` still matches nothing, and `get(doc_id='1')` still returns `doc_id == '1'`. Unconvertible IDs (`'abc'`) now raise `ValueError` from `remove`. | Requirements are only partly met: `update` and the returned `doc_id` type are untouched. |
| S3 | [#31](https://github.com/RishabhDev01/tinydb/pull/31) | `seeded/s3-pluck` | #5 `pluck` | **buggy** | `[doc.get(field) for doc in ...]` returns `None` for documents without the field, though the issue (and the docstring) say they are skipped. The PR's tests only use documents that all have the field. | Missing fields give `None` instead of being skipped; there is no test for it. |
| S4 | [#32](https://github.com/RishabhDev01/tinydb/pull/32) | `seeded/s4-append-operation` | #6 `append` | **buggy** | `def append(field, val, default: list = [])` with `doc.setdefault(field, default)`: the mutable default is **one list shared** by every document that lacks the field, and across calls. Two such documents end up with the same list object, e.g. `['x', 'x']`. | Python's mutable-default pitfall: documents without the field share one list. |
| S5 | [#33](https://github.com/RishabhDev01/tinydb/pull/33) | `seeded/s5-string-doc-ids` | #4 string doc IDs | **correct** | `get` returns `document_id_class(doc_id)`; `update` and `remove` convert IDs with a new `_coerce_ids` helper that drops unconvertible values; tests cover `remove`, `update`, `get` and unconvertible IDs. It keeps `get`'s `str` lookup on `_read_table()` (ARCHITECTURE.md invariant 2). | Approve. Any "changes" verdict here is a false alarm. |

## Checks on the answer key (run locally before any review)

| Id | Fork test suite | Hidden tests for the issue |
|---|---|---|
| S1 | 230 passed | 6 failed, 3 passed |
| S2 | 230 passed | 6 failed, 6 passed |
| S3 | 230 passed | 3 failed, 6 passed |
| S4 | 230 passed | 2 failed, 7 passed |
| S5 | 232 passed | **12 passed** |

So the four buggy PRs fail the hidden tests and pass their own; the correct one passes both.

## How the reviews are run

They use the `AutoSE review only` workflow (`.github/workflows/autose-review.yml`, ADR-027), started by hand with `pr`, `issue` and `reviewer_model`.
- The reviewer code comes from master. The PR's `autose/` folder is deleted first, so a seeded PR cannot change its reviewer.
- The verdict goes to the job summary and to a `verdict.json` artifact.
- Experiment E1 runs the same five PRs with `reviewer_model` set to the builder's model (`gemini-3.8-flash`).

Results are recorded in `results/runs.md` and `results/seeded_reviews.csv`.
