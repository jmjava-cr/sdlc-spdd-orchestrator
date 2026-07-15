# Extension manifest

Declarative registry for SDLC-SPDD extension points. When this file exists,
`resolve-agent-context.sh` prefers it for phase-extension discovery; when it is
missing or unreadable, convention-based folder layout still applies.

Hooks are **declared only** in this MVP — no automatic hook execution.

## Phase extensions

| Folder | Phases | Description |
|--------|--------|-------------|
| `_all-agents` | * | Rules loaded for every phase |
| `initializer-agent` | init | Extensions for `/sdlc-spdd-init` |
| `planning-agent` | analysis, plan, prompt-update | Planning and analysis extensions |
| `architect-agent` | architect | Architecture phase extensions |
| `coding-agent` | code, api-test | Implementation and API-test extensions |
| `codereview-agent` | review | Review checklist extensions |
| `retro-agent` | retro | Retrospective extensions |
| `curator-agent` | sync | Sync and curation extensions |

## Skills

Skill files live under `skills/`. Reference them in prompts with `#SkillName`
(for example `#TDD`, `#java`). Exclude with `!SkillName`.

| Path | Skill | Description |
|------|-------|-------------|
| `skills/TDD.md` | TDD | Test-driven development workflow |
| `skills/security.md` | security | Security review checklist |

Playbooks under `agent-context/playbooks/` remain discoverable via `#name`
without listing them here.

## Hooks (declarative)

| Path | Trigger | Description |
|------|---------|-------------|
| `hooks/notify-team-registry.example.sh` | manual | Example script to notify team registry changes |

## Example extension

See `_all-agents/example-manifest-extension.md` for a minimal phase extension
that resolves when this manifest is present.
