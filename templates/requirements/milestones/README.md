# Milestone-Derived Requirements

This folder holds requirement stubs created from milestone checklist items.

## Purpose

When you run `create-work-from-milestone.sh`, each unchecked milestone item becomes:

- a Work ID
- a requirement file here: `requirements/milestones/<WORK-ID>.md`
- a draft REASONS Canvas under `spdd/canvas/<WORK-ID>.md`
- a **Linked Work** row in the source `milestone-*.md` file

Use these files in plan prompts:

    /sdlc-spdd-plan @requirements/milestones/<WORK-ID>.md @ROADMAP.md @milestone-1.md

## Jira issue drafts

Each milestone requirement file is the **natural place to store Jira syntax** before and after
issue creation. Keep copy-paste-ready fields under `## Jira`:

- **Before create** — fill Summary, Description, acceptance criteria, labels, components
- **After create** — set `- Key: ABC-123` and commit
- **On claim** — `./scripts/sdlc.sh claim <WORK-ID>` (or `SDLC_ENGINE=python`) auto-reads the Key into the team registry
  `jira:` note token (disable with `SDLC_TEAM_AUTO_JIRA=0`)

Engine helpers (v2):

```bash
SDLC_ENGINE=python ./scripts/sdlc.sh issues draft <WORK-ID> --system jira
SDLC_ENGINE=python ./scripts/sdlc.sh issues draft <WORK-ID> --system jira --format adf  # Cloud payload preview
SDLC_ENGINE=python ./scripts/sdlc.sh issues push <WORK-ID> --system jira          # dry-run
SDLC_ENGINE=python ./scripts/sdlc.sh issues push <WORK-ID> --system jira --apply  # ADF on Jira Cloud
SDLC_ENGINE=python ./scripts/sdlc.sh sync-links --repair
```

Jira Cloud needs ADF for descriptions — the engine converts this markdown
automatically on push (see [jira-runbook.md](../../docs/jira-runbook.md)).

See [jira-runbook.md](../../docs/jira-runbook.md) and [engine-v2.md](../../docs/engine-v2.md).

## GitHub issue drafts

Optional `## GitHub` section for teams that track delivery in GitHub Issues:

```markdown
## GitHub

- Number: TBD
- Title: …
- Labels: feature
- URL:
```

After create, set `Number` / `URL`. Claim auto-links `github:#N` (disable with `SDLC_TEAM_AUTO_GITHUB=0`).

```bash
SDLC_ENGINE=python ./scripts/sdlc.sh issues push <WORK-ID> --system github --apply   # uses gh CLI
```

## Relationship to other planning artifacts

| Artifact | Role |
|----------|------|
| `milestone-*.md` | Goal, scope checklist, linked Work IDs |
| `requirements/milestones/` | Per-item requirement stubs + Jira draft syntax |
| `session-notes/` | Daily agent-session narrative |
| `ROADMAP.md` | Milestone progress and current focus |

Ad-hoc requirements (not from a milestone) live directly under `requirements/` instead.
Use the same `## Jira` section there when the work will be tracked in Jira.
