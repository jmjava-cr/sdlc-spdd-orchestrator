# SDLC Engine v2 — Python orchestration

## Why

v1 orchestration is a constellation of bash scripts (`sdlc.sh`,
`sdlc-workflow.sh`, `sdlc-team-registry.sh`, session helpers). That worked for
the MVP, but reuse, testing, and embedding inside other tools is harder than it
should be.

**v2** introduces a Python package — `sdlc_engine` — as the reusable
orchestration core while keeping shell as a compatibility surface.

## Goals

- One importable API for pointer, workflow, team registry, and archive
- Stable CLI (`sdlc-engine` / `python -m sdlc_engine`) with the same command
  names humans already use
- Identical on-disk formats (`.sdlc/`, `work-registry.tsv`, canvas paths)
- Gradual migration: shell remains the default (`SDLC_ENGINE=shell`); opt into
  Python with `SDLC_ENGINE=python` or `auto`
- Stdlib-first package (no required third-party runtime deps)

## Non-goals (this slice)

- Rewriting install/upgrade/adapter generation in Python (still shell)
- Replacing assistant command packs
- Changing SPDD canvas semantics

## Layout

```
engine/
  pyproject.toml
  README.md
  src/sdlc_engine/
    cli.py          # argparse CLI
    project.py      # root + paths
    phases.py       # phase/gate tables
    pointer.py
    workflow.py
    registry.py
    archive.py
    canvas.py
  tests/            # pytest
```

## Usage

```bash
# From orchestrator checkout (no install)
PYTHONPATH=engine/src python3 -m sdlc_engine next --root .

# Opt into the Python engine via the existing wrapper (default remains shell)
SDLC_ENGINE=python ./scripts/sdlc.sh next
SDLC_ENGINE=python ./scripts/sdlc.sh claim FEAT-001-demo
SDLC_ENGINE=auto   ./scripts/sdlc.sh next   # python if importable, else shell
./scripts/sdlc.sh next                      # bash default

# Editable install
python3 -m pip install -e './engine[dev]'
sdlc-engine team
sdlc-engine archive --all --dry-run
```

## Bridge to remaining shell scripts

Commands not yet ported (init, upgrade, capture-session-memory, adapter
validators, etc.) stay in `scripts/*.sh`. Call them through:

```bash
python3 -m sdlc_engine shell setup-agent-prompts.sh -- --target /tmp/demo --all
```

## Migration plan

1. **Now** — engine owns claim/next/shelf/advance/archive/team/list-work; shell
   wrapper delegates when importable.
2. **Next** — port capture + resolve-agent-context helpers into Python modules.
3. **Later** — optional install of the engine into target projects via
   `upgrade-project.sh` (copy or pip install path).

## Tests

```bash
PYTHONPATH=engine/src python3 -m pytest -q engine/tests
```

CI: `.github/workflows/test-sdlc-engine.yml`

## Related

- Canvas: `spdd/canvas/FEAT-006-python-orchestration-engine.md`
- Package readme: `engine/README.md`
