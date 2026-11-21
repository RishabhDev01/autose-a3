# Sequence view: what one run looks like, from trigger to review

This walk-through follows one issue through the whole workflow, message by message. It shows the concrete inputs and outputs at every hop, including a test retry and one review round that sends work back. Links to actual Actions runs are listed in `results/runs.md`.

**Example issue: #3 "Feature: get a list of one field from all documents"**

> I often need just the `name` of every document. Right now I write
> `[d['name'] for d in db.all()]`, which breaks when some docs have no `name`.
> Could tinydb have something like `db.pluck('name')`?

```mermaid
sequenceDiagram
  autonumber
  actor M as Maintainer
  participant GH as GitHub
  participant WF as build job
  participant O as Orchestrator (code)
  participant P as Planner (gpt-oss-120b)
  participant J as Judge (qwen3.8-27b)
  participant B as Builder (gpt-oss-120b)
  participant CI as CI (pytest)
  participant RJ as review job (read-only)
  participant R as Reviewer (qwen3.8-27b)
  participant PJ as post job

  M->>GH: adds label "autose" to issue #3
  GH->>WF: event issues.labeled
  WF->>WF: gate: author_association = OWNER ✔
  WF->>O: run(issue=3), no state.json, so start at SPEC

  Note over O,J: Stage 1: Requirements
  O->>P: <untrusted_issue>#3 text</untrusted_issue> + spec-writer skill
  P->>P: read_file(README.md), grep("def all")
  P-->>O: spec.md (AC-1 list of values, AC-2 skip docs without field,<br/>AC-3 "should be fast")
  O->>O: regex check ✔ (3 ACs, Given/When/Then present)
  O->>J: is each AC testable?
  J-->>O: AC-1 yes, AC-2 yes, AC-3 NO ("fast" has no threshold)
  O->>P: redo 1/1: AC-3 not testable
  P-->>O: spec.md v2 (AC-3: empty table returns [])
  O->>J: re-check
  J-->>O: all yes ✔. Stage 1 PASS

  Note over O,P: Stage 2: Design
  O->>P: spec.md + ARCHITECTURE.md
  P-->>O: design.md: tinydb/table.py → Table.pluck (NEW),<br/>tinydb/database.py → forwarded via __getattr__,<br/>tests/test_tables.py → new tests
  O->>O: files exist ✔, Table class found by grep ✔. Stage 2 PASS

  Note over O,B: Stages 3–4: Implement ⇄ Test
  O->>B: spec.md + design.md + table.py
  B->>B: write_file(table.py), write_file(test_tables.py), run_tests
  B-->>O: done (attempt 1)
  O->>O: compileall ✔, pytest ✘ test_pluck_missing_field: KeyError
  O->>B: attempt 2/3 + failure log (truncated)
  B->>B: fix: skip docs where field not in doc
  B-->>O: done (attempt 2)
  O->>O: compileall ✔, full pytest ✔, AC-1/2/3 each have a test ✔
  O->>O: write diff.patch, test_report.md, commit .autose/issue-3/

  Note over O,CI: Stage 5: Release (no LLM)
  O->>GH: git push autose/issue-3, gh pr create, opens PR #6 (body = pr.md)
  GH->>CI: pull_request event
  CI-->>O: gh pr checks: all green ✔. Stage 5 PASS

  WF->>RJ: needs: build (pr=6, sha=abc123)

  Note over RJ,R: Stage 6: Review round 1 (fresh runner, sees issue + diff + repo only)
  RJ->>R: issue #3 text + diff (without .autose/)
  R->>R: read_file(table.py), run_tests ✔
  R->>R: tries edge case: nested field "a.b", not handled
  R-->>RJ: verdict changes, target implement,<br/>finding "issue says 'one field', but nested keys silently return nothing"
  RJ->>PJ: verdict.json
  PJ->>GH: comments review-r1.md on PR #6
  PJ->>WF: workflow_dispatch(issue=3, round=2, start=implement)

  Note over O,B: Round 2: back to stage 3, resumes from state.json
  O->>B: spec + design + review finding
  B-->>O: raise a clear ValueError for dotted keys + test
  O->>O: pytest ✔, push to PR #6, CI ✔

  Note over RJ,R: Stage 6: Review round 2
  RJ->>R: issue + new diff
  R-->>RJ: verdict approve, findings: none blocking
  RJ->>PJ: verdict.json
  PJ->>GH: comments review-r2.md + "Ready for human decision"
  GH-->>M: notification
  M->>GH: reviews PR #6 and merges or closes (human only)
```

## The same run as a timeline

| Step | Stage | Who | Output on GitHub | Check result |
|---|---|---|---|---|
| 1 | Trigger | Maintainer | label `autose` on issue #3 | gate ✔ |
| 2 | Requirements | Planner + Judge | `.autose/issue-3/spec.md` | 1 redo (AC-3 untestable), then ✔ |
| 3 | Design | Planner | `design.md` | files and functions exist ✔ |
| 4 | Implement | Builder | `diff.patch` | builds ✔ |
| 5 | Test | Builder | `test_report.md` | attempt 1 ✘, attempt 2 ✔ |
| 6 | Release | Script | PR #6 + `pr.md` | CI green ✔ |
| 7 | Review r1 | Reviewer | PR comment `review-r1.md` | changes → implement |
| 8 | Implement/Test r2 | Builder | new commit on PR #6 | pytest ✔, CI ✔ |
| 9 | Review r2 | Reviewer | PR comment `review-r2.md` | approve |
| 10 | Decision | Human | merge or close | — |
