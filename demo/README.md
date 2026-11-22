# Demo video: shot list and script (target 4:30, limit 5:00)

The video follows one complete run, from the issue page to the posted review. That is **run 30**: the `autose` label on issue #5, [Actions run 45005311148](https://github.com/RishabhDev01/tinydb/actions/runs/45005311148), PR [#23](https://github.com/RishabhDev01/tinydb/pull/23). After it, a shorter second run shows the comment trigger: **run 31**, `/autose` on issue #6, [45005712745](https://github.com/RishabhDev01/tinydb/actions/runs/45005712745), PR [#25](https://github.com/RishabhDev01/tinydb/pull/25).

The screenshots in `screenshots/` were captured during these real runs and can be used as stills. A screen recording of a fresh run is better, though: re-run it the same way (remove and re-add the label) while recording, and use the stills as backup.

| Time | Screenshot(s) | What to show | What to say (plain, short) |
|---|---|---|---|
| 0:00–0:20 | `19-pr23-review-approve.jpg` (as a teaser) | The end result first | "This is a pull request that no person wrote, and a review that no person wrote. In the next four minutes I will show how an issue becomes this, and where we stop the agents." |
| 0:20–0:45 | `01-issue5-page.jpg` | The issue: a user asks for `db.pluck('name')` | "The input is an ordinary GitHub issue on our fork of TinyDB. It is treated as untrusted text." |
| 0:45–1:05 | `02-issue5-label-menu.jpg`, `03-issue5-label-applied.jpg` (or `06-issue5-relabeled.jpg`) | Adding the `autose` label | "A collaborator adds the autose label. Only owners, members and collaborators can start a run, and events from bots are ignored." |
| 1:05–1:20 | `07-actions-run30-started.jpg`, `08-run30-gate-passed.jpg` | The run starts; the gate passes | "The gate job checks who triggered it. Gate: run equals true, labeled by the owner." |
| 1:20–2:05 | `09-run30-log-guard-spec.jpg`, `10-run30-log-design-build-retry.jpg`, `11-run30-log-pass-release.jpg` | The live log, stage by stage | "A Python state machine runs the stages. A classifier screens the issue for prompt injection. The planner reads the code and writes a specification with five testable criteria, then a design. The builder gets only the code it needs. Its first attempt fails the build check, because it used a type that was not imported. The error goes back, and attempt two passes all tests. Code decides every pass or fail, not the model." |
| 2:05–2:40 | `12-pr23-body-artifacts.jpg`, `13-pr23-files-audit-trail-design.jpg`, `14-pr23-spec-md.jpg`, `15-pr23-code-diff-pluck.jpg` | PR body, audit trail, spec, code | "Release is a script, not a model. The pull request links every artifact: spec, design, patch and test report are in the branch, so anyone can follow the run. Here is the code: twelve lines." |
| 2:40–3:15 | `16-run30-all-jobs-green.jpg`, `17-run30-stage-timeline.jpg`, `18-run30-tokens-review-summary.jpg` | Jobs, timeline, tokens | "Four jobs, 2 minutes 40 seconds. The review runs in a separate job, with a different model and a read-only token, and it sees only the issue and the diff, never the spec or the builder's reasoning." |
| 3:15–3:50 | `19-pr23-review-approve.jpg`, `20-pr23-review-evidence-risks.jpg`, `21-pr23-ready-for-human.jpg` | The posted review | "The reviewer maps each requirement to code and tests, checks risks, and approves. Then AutoSE hands over: ready for a human decision. It never merges." |
| 3:50–4:15 | `23-issue6-typing-autose.jpg`, `25-issue6-bot-started-guard.jpg`, `27-run31-log-full-pipeline.jpg`, `29-pr25-review-approve.jpg` | The second trigger: a comment | "The same works with a comment. The bot replies with a link, and the whole pipeline runs in about a minute to an approved review." |
| 4:15–4:45 | (optional) PR #26 review, from run 27 | What we learned | "Two things surprised us. On a vague issue, the builder passed every test by detecting one test's name, and only the independent reviewer caught it, so we added a check for that. And while recording this demo, the label trigger skipped the early stages; we found the cause and fixed it (ADR-029). Thank you." |

## Tips
- Zoom the browser to 125% before recording, so the logs are readable.
- Cut the waiting: the real run takes about 2 to 3 minutes, so speed up the log scrolling.
- Show the run link in the corner (`actions/runs/45005311148`) so viewers can check that it is real.
- Keep the narration to the facts on screen; numbers are in `results/runs.md`.

## Screenshot index
| File | Content |
|---|---|
| 01–05 | Issue #5, label menu, label applied, run 29 started, gate (run 29 resumed at release; see ADR-029) |
| 06–21 | Run 30, the full run: label re-added, run started, gate, live logs, PR body, audit trail, spec, code diff, jobs green, stage timeline, tokens, review, hand-over |
| 22–30 | Run 31: issue #6, typing `/autose`, comment posted, bot reply, gate, full log, jobs green, review, hand-over |
