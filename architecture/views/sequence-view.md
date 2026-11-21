# Sequence view: one run, from trigger to review

> **Status: PLANNED.** The diagram below shows the designed message flow. Every `⟨…⟩` placeholder will be filled in from **one real run** after it happens: the run URL, PR number, timestamps, attempts and tokens. Values are copied from that run's `state.json` and its Actions log. Nothing here will be invented.

## Run record (filled in from the real run)

| Field | Value |
|---|---|
| Issue | ⟨#N title⟩ |
| Trigger | ⟨label `autose` / comment `/autose`⟩ by ⟨user⟩ at ⟨time⟩ |
| Build job run | ⟨https://github.com/…/actions/runs/…⟩ |
| Review job run | ⟨url⟩ |
| PR | ⟨#M url⟩ |
| Implement/test attempts | ⟨n⟩ |
| Review rounds | ⟨n⟩, final verdict ⟨approve / changes⟩ |
| Tokens (planner / judge / builder / reviewer) | ⟨…⟩ |
| Wall-clock time | ⟨mm:ss⟩ |

## Diagram

```mermaid
sequenceDiagram
  autonumber
  actor M as Maintainer
  participant GH as GitHub (issue / PR)
  participant WF as Actions: build job
  participant O as Orchestrator (code)
  participant P as Planner agent
  participant J as LLM judge
  participant B as Builder agent
  participant G as Groq API
  participant CI as CI (pytest)
  participant RJ as Actions: review job
  participant R as Reviewer agent
  participant PJ as Actions: post job

  M->>GH: add label "autose" (or comment /autose)
  GH->>WF: issues.labeled event
  WF->>WF: gate: author_association ∈ {OWNER, MEMBER, COLLABORATOR}
  WF->>O: start(issue N) and read state.json if present
  Note over O: concurrency group autose-issue-N

  rect rgba(120,160,255,0.12)
  Note over O,P: Stage 1: Requirements
  O->>P: <untrusted_issue> + A1 spec-writer skill
  P->>G: chat + tools (read_file, grep)
  P-->>O: spec.md
  O->>O: regex: AC-n has Given/When/Then
  O->>J: each AC: testable?
  J->>G: single completion (different model)
  J-->>O: {AC-1: yes, …}
  end

  rect rgba(120,160,255,0.12)
  Note over O,P: Stage 2: Design
  O->>P: spec.md + ARCHITECTURE.md
  P-->>O: design.md
  O->>O: script: named files and functions exist
  end

  rect rgba(120,220,160,0.12)
  Note over O,B: Stages 3–4: Implement ⇄ Test (≤3 attempts)
  O->>B: spec.md + design.md + target files
  loop until pytest passes or 3 attempts
    B->>G: chat + tools (read, write_file, run_tests)
    B-->>O: claims done
    O->>O: compileall + full pytest + AC-n mapped to tests
    alt tests fail
      O->>B: truncated failure log
    end
  end
  O->>O: save diff.patch, test_report.md, commit .autose/issue-N/
  end

  rect rgba(255,200,120,0.12)
  Note over O,CI: Stage 5: Release (no LLM)
  O->>GH: git push autose/issue-N, gh pr create (pr.md)
  GH->>CI: pull_request event
  CI-->>O: gh pr checks --watch → green
  end

  WF->>RJ: needs: build (outputs: PR number, head SHA)

  rect rgba(255,140,140,0.12)
  Note over RJ,R: Stage 6: Independent review (read-only token, fresh runner)
  RJ->>RJ: checkout PR head SHA
  RJ->>R: issue text + diff (excluding .autose/)
  R->>G: chat + tools (read_file, grep, run_tests)
  R-->>RJ: review.md + verdict.json
  end

  RJ->>PJ: verdict
  PJ->>GH: gh pr comment review.md
  alt verdict = changes and round < 2
    PJ->>WF: workflow_dispatch(issue N, round+1, start=design|implement)
  else approve or 2 rounds used
    PJ->>GH: comment "ready for human decision"
    GH-->>M: notification
    M->>GH: merge or close (human only)
  end
```
