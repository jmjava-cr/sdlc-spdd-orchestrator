# SDLC-SPDD Orchestrator

A multi-assistant scaffold for disciplined AI-assisted delivery.

## Work in progress

**SPIKE-001 — Guide as an optional DICE context backend** (spike branch
`cursor/spike-guide-ingest-agent-context-17f4`). Flow overview:

[docs/guide-flow.md](https://github.com/jmjava/sdlc-spdd-orchestrator/blob/cursor/spike-guide-ingest-agent-context-17f4/docs/guide-flow.md)

Paired PRs: [orchestrator #24](https://github.com/jmjava/sdlc-spdd-orchestrator/pull/24) · [guide #2](https://github.com/jmjava/guide/pull/2). Experimental work stays on the spike branch until T06 go/no-go; `main` keeps shipping cleanup without merging the spike yet.

**Demo videos:** [Watch three narrated intro segments on GitHub Pages](https://jmjava.github.io/sdlc-spdd-orchestrator/) — SDLC-SPDD overview, install/workflow, and Guide RAG dogfooding.

## Recent highlights

New agent coordination shipped in [#19](https://github.com/jmjava/sdlc-spdd-orchestrator/issues/19) via [#20](https://github.com/jmjava/sdlc-spdd-orchestrator/pull/20) and [#21](https://github.com/jmjava/sdlc-spdd-orchestrator/pull/21) and [#21](https://github.com/jmjava/sdlc-spdd-orchestrator/pull/21)

| What | Why it matters | Try it |
| ---- | -------------- | ------ |
| **SDLC pointer** ([#20](https://github.com/jmjava/sdlc-spdd-orchestrator/pull/20)) | Persistent Work ID on your machine; guarded wrappers refuse commands aimed at the wrong chore | `agent-context/sdlc-pointer.sh` |
| **Workflow CLI** ([#21](https://github.com/jmjava/sdlc-spdd-orchestrator/pull/21)) | Phase/gate tracking, canvas-op inference, and safe session capture | `./scripts/sdlc.sh` or `./scripts/sdlc-spdd/sdlc.sh` |
| **Team registry** ([#21](https://github.com/jmjava/sdlc-spdd-orchestrator/pull/21)) | Shared claims in git so teammates see who owns which Work ID | `./scripts/sdlc.sh team`, `./scripts/sdlc.sh claim …` |
| **Agent grounding** ([#21](https://github.com/jmjava/sdlc-spdd-orchestrator/pull/21)) | `/sdlc-spdd-whereami` in Cursor, Copilot, and Claude — same “what now?” answer as the shell CLI | `/sdlc-spdd-whereami` |

Pointer and workflow state stay local (`.sdlc/pointer`, `.sdlc/workflows/`); team claims live in `agent-context/work-registry.tsv` and sync through git. Details: [agent-context/README.md](agent-context/README.md)

> **Project status: Milestone 1 make-it-right track is largely complete; make-it-fast measurement landed.**
> We develop this framework through Kent Beck's progression — *make it work → make it
> right → make it fast*. **Make it work** is done. **Make it right** refactors
> (shared libs, command-spec generation, extension manifest, analysis Scope Lock,
> Jira requirements format, milestone subdirs, session-brief archive) are Complete
> on the integration line. **Make it fast** measurement (prompt-optimization ledger +
> canvas readiness indicators) is also Complete; remaining make-it-fast work is
> SPIKE-001/002 (Guide / local models), shelved until Guide MCP is available.
> See the [ROADMAP](ROADMAP.md) and
> [milestone-1](requirements/milestones/milestone-1/MILESTONE-1.md) (root
> [`milestone-1.md`](milestone-1.md) is a compatibility stub).
>
> **We dogfood the framework on itself.** Improvements are governed Work IDs with
> REASONS Canvases under [`spdd/canvas/`](spdd/canvas/) and requirements under
> [`requirements/milestones/`](requirements/milestones/) — the same workflow this
> repo asks target projects to use.

Note: Guide integration spike details (including the flow diagram) live in the
[Work in progress](#work-in-progress) section above and on the spike branch.

It is built from **three parts** that work together:

| Part         | Answers                                   | Artifacts                                                         |
| ------------ | ----------------------------------------- | ----------------------------------------------------------------- |
| **Planning** | _Why_ the work matters                    | `ROADMAP.md`, `milestone-*.md`, `requirements/`, `session-notes/` |
| **SPDD**     | _What_ to build (and what not to)         | `spdd/canvas/<WORK-ID>.md` (REASONS Canvas)                       |
| **SDLC**     | _Who acts when_ and how sessions hand off | phase commands, session briefs, `agent-context/` memory           |

## How Commands Work

This repo uses **two kinds** of commands. They run in different places — do not mix them up.

| Kind                       | Looks like                                                  | Where you run it                                                             |
| -------------------------- | ----------------------------------------------------------- | ---------------------------------------------------------------------------- |
| **Assistant** (AI chat)    | `/sdlc-spdd-init`, `/sdlc-spdd-plan @requirements/foo.md`   | **Cursor Chat**, **Copilot Chat**, or **Claude Code** in your target project |
| **Shell — install** (once) | `./scripts/setup-agent-prompts.sh --target ...`             | Terminal in the **orchestrator repo** clone                                  |
| **Shell — daily use**      | `./scripts/sdlc-spdd/sdlc.sh next`, `./scripts/sdlc-spdd/sdlc.sh claim …` | Terminal in your **installed target project**                                |
| **Shell — orchestrator**   | `./scripts/sdlc.sh next` (same CLI, orchestrator repo layout)             | Terminal in the **orchestrator repo** clone (dogfooding)                     |

Install/upgrade/verify from the orchestrator clone use `./scripts/<name>.sh`. After install, runtime scripts live in the target at `./scripts/sdlc-spdd/`. See [Script paths](CONTRIBUTING.md#script-paths)

**`/sdlc-spdd-*` is not a terminal command.** Open your target app in Cursor, Copilot, or Claude Code, open **AI chat**, then:

- **Cursor:** type `/sdlc-spdd-init` (or `/` → pick `sdlc-spdd-init`)
- **Copilot:** type `/sdlc-spdd-init`, or `#prompt:sdlc-spdd-init` if slash commands are missing
- **Claude Code:** type `/sdlc-spdd-init` (or `/` → pick `sdlc-spdd-init`)

Full detail: [How to run assistant commands](docs/initialization-and-invocation.md#how-to-run-assistant-commands).

## The Adoption Path

Five steps take you from install to confident daily use. Follow them in order — each step points to one doc.

```mermaid
flowchart TD
    S1["1 - Install and verify<br/>(~5 min)"]
    S2["2 - Run your first session<br/>hands-on walkthrough"]
    S3["3 - Learn the model<br/>how the 3 parts connect"]
    S4["4 - Work day to day<br/>copy-paste prompts and rhythm"]
    S5["5 - Go deeper<br/>per-part value and prompts"]

    S1 --> S2 --> S3 --> S4 --> S5

    S1 -.-> D1["setup-agent-prompts.sh --all<br/>verify-project-install.sh"]
    S2 -.-> D2["First day with SDLC-SPDD"]
    S3 -.-> D3["Three-part operating path"]
    S4 -.-> D4["Session prompt standard<br/>Daily runbook"]
    S5 -.-> D5["What X brings + SPDD/Planning<br/>prompt standards"]

    classDef step fill:#1f6feb,stroke:#0b3a8a,color:#ffffff;
    classDef doc fill:#eef2f7,stroke:#9aa7b8,color:#1b2733;
    class S1,S2,S3,S4,S5 step;
    class D1,D2,D3,D4,D5 doc;
```

| Step                | Do this                                                                                      | Read this                                                                    [...]

[rest of file unchanged]
