# Component view

Two repositories are involved:

| Repo | Contents | Why separate |
|---|---|---|
| **Fork** `tinydb` (pinned at `edff96a`) | `.github/workflows/autose.yml`, `autose/` (orchestrator, agents, prompts, tools), `ARCHITECTURE.md`, `skills/spec-writer/` | The workflow must live where it runs. |
| **Submission repo** `autose-a3` | report, ADRs, views, issues, **hidden tests**, seeded PRs, results | Hidden tests must never be visible to the agents. If they lived in the fork, the builder could read them. |

```mermaid
flowchart LR
  subgraph GH[GitHub]
    ISSUE[Issue / comment<br/>label 'autose' or '/autose']
    PR[Pull request]
    CI[CI workflow<br/>pytest]
    ART[(Actions artifacts<br/>.autose/issue-N/*)]
  end

  subgraph JOB1["Job: build  (contents:write, pull-requests:write)"]
    GATE[Gate<br/>author_association check]
    ORCH[Orchestrator<br/>Python state machine<br/>NO LLM]
    PLAN[Planner agent<br/>stages 1-2<br/>model: PLANNER_MODEL]
    JUDGE[LLM judge<br/>testability check<br/>model: JUDGE_MODEL]
    BUILD[Builder agent<br/>stages 3-4<br/>model: BUILDER_MODEL]
    REL[Release script<br/>stage 5, NO LLM<br/>git push + gh pr create]
    CHK[Deterministic checks<br/>regex, file-exists,<br/>compileall, pytest]
  end

  subgraph JOB2["Job: review  (contents:read, pull-requests:read)"]
    REV[Reviewer agent<br/>stage 6<br/>model: REVIEWER_MODEL<br/>qwen, a different family]
  end

  subgraph JOB3["Job: post  (pull-requests:write, no LLM)"]
    POST[Post review.md<br/>as PR comment<br/>route verdict]
  end

  GROQ[(Groq API<br/>OpenAI-compatible<br/>function calling)]

  ISSUE --> GATE --> ORCH
  ORCH -->|issue text in &lt;untrusted&gt;| PLAN
  PLAN -->|spec.md| JUDGE
  ORCH --> CHK
  ORCH -->|spec.md + design.md| BUILD
  BUILD -->|diff.patch, test_report.md| ORCH
  ORCH --> REL --> PR --> CI
  ORCH --> ART
  PR -->|issue + diff + repo @ PR head ONLY| REV
  REV -->|review.md + verdict.json| POST
  POST -->|changes requested, round < 2:<br/>re-dispatch with target stage| ORCH
  POST -->|approve or rounds used| HUMAN[Human merges or closes]

  PLAN & JUDGE & BUILD & REV -.-> GROQ
```

## Tools per agent

The planner and reviewer run on one small in-house tool loop (`autose/agent.py`)
over Groq's OpenAI-compatible chat API. Each gets an explicit allow-list of
Python functions; anything not on the list does not exist for it. Since
ADR-016, the builder has **no tools**. The orchestrator gives it the code it
needs (`autose/patcher.py`), and it answers once per attempt.

| Agent | Tools | Cannot |
|---|---|---|
| Planner | `read_file`, `list_dir`, `grep`, `write_artifact` (only `.autose/`) | edit source, run shell, use network |
| LLM judge | none (single completion, JSON out) | anything |
| Builder | none (ADR-016). It receives the definitions the design names and answers with whole replacement definitions and one new test file. The orchestrator applies them by name, only to `tinydb/*.py` and `tests/test_autose_issue_N.py`, then runs the fixed pytest command. (`BUILDER_MODE=agent` restores the earlier tool loop: `read_file`, `grep`, `replace_lines`, `edit_file`, `write_file`, `run_tests`.) | read files on its own, write outside those paths, push, call `gh`, run shell, read secrets |
| Reviewer | `read_file`, `list_dir`, `grep`, `run_tests` | write any file, push, comment (its job token is read-only) |
| Orchestrator / release / post | `git`, `gh` CLI | — (code, not an LLM) |
