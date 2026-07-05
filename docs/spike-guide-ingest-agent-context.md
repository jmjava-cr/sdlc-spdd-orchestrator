# SPIKE — Guide ingest for agent-context store

> **Operator supplement** to the SPDD analysis artifact — not a substitute.  
> **Canonical:** `spdd/analysis/SPIKE-001-guide-rag-context-backend-analysis.md`  
> **Branch:** `cursor/spike-guide-ingest-agent-context-17f4` only. Do not merge to `main` until T06 go/no-go.

Exploration branch for [SPIKE-001](../spdd/canvas/SPIKE-001-guide-rag-context-backend.md)
**T01**: ingest orchestrator `agent-context/` and `spdd/` into the existing Guide/Neo4j
store (leg 2 — RAG chunks) so MCP search can reach Work IDs, indexes, and analysis artifacts
already indexed in markdown.

This is **throwaway / local-only**. Target projects never receive Guide profiles or Neo4j data.

## Guide branch

Use the **`ingest-to-hub`** branch on [jmjava/guide](https://github.com/jmjava/guide) (not
upstream `main` alone). That branch adds:

- **Git incremental ingestion** — `guide.git-ingestion.enabled` re-ingests only files changed
  since the last successful run per directory (stores HEAD in a local JSON state file).
- **Operator purge API** — preview/delete chunks by `directory` or `uriPrefix`; reset git
  revision state for one directory before a full re-ingest.

```bash
cd ~/github/jmjava/guide
git fetch origin ingest-to-hub
git checkout ingest-to-hub
```

MCP is bundled with Guide on the same process (`/sse` on `GUIDE_PORT`, default `1337`; this
repo's research stack uses `21337` to avoid clashing with other local services).

## Corpus layering (append, do not wipe)

| Profile | Layer | Content |
|---------|-------|---------|
| `menke` | Code | Local Embabel/DICE fork repos |
| `menke-2` | Reference | SPDD, context engineering, evals URLs |
| `menke-3` | Framework depth | Scripts, manifests, harness, craft |
| `menke-4` | Docgen consumer | documentation-generator + course-builder docs |
| **`menke-5`** | **Orchestrator context** | `agent-context/memory/`, `spdd/canvas/`, `spdd/analysis/` |

Run **one profile at a time** on the same Neo4j store. See
[guide-rag-research-and-dogfooding](guide-rag-research-and-dogfooding.md) for menke-1–4.

## One-time setup

1. Ensure menke-1–4 (or the subset you need) are already ingested on port `21337`.
2. Copy the profile template into guide (paths are gitignored in guide):

   ```bash
   cp templates/guide-profiles/application-menke-5-orchestrator-context.yml.example \
      ~/github/jmjava/guide/scripts/user-config/application-menke-5.yml
   ```

3. Edit `application-menke-5.yml` if your orchestrator clone is not at
   `~/github/jmjava/sdlc-spdd-orchestrator`.

## Append ingest (leg 2)

From the orchestrator repo (this spike branch):

```bash
./scripts/guide/append-orchestrator-context.sh
```

Or manually from guide:

```bash
cd ~/github/jmjava/guide
GUIDE_PROFILE=menke-5 GUIDE_PORT=21337 SERVER_PORT=21337 \
  GUIDE_INGEST_LOG=/tmp/menke-5-ingest.log ./scripts/append-ingest.sh
```

Wait for the **INGESTION COMPLETE** banner. First run ingests the full trees; subsequent
appends with `git-ingestion.enabled` only process changed files (for example after
`sdlc.sh capture` updates `agent-context/memory/`).

### Re-ingest one directory after a bad partial run

With Guide running on `:21337`:

```bash
curl -s -X POST http://localhost:21337/api/v1/data/git-ingestion/revision/reset \
  -H 'Content-Type: application/json' \
  -d '{"directory":"~/github/jmjava/sdlc-spdd-orchestrator/agent-context/memory"}' | jq .
```

Then re-run `append-orchestrator-context.sh`.

## Verify MCP (legs 1–2)

Connect **embabel-dev MCP** in Cursor to `http://localhost:21337/sse`.

| Check | Tool | Example query |
|-------|------|---------------|
| Work ID in store | `docs_vectorSearch` | `SPIKE-001 guide RAG context backend` |
| Index rows | `docs_textSearch` | `+context-index +agent-context/memory` |
| Canvas prose | `docs_vectorSearch` | `FEAT-004 prompt optimization ledger` |
| Prior decision memory | `docs_vectorSearch` | `decision memory Fowler SPDD` |

**Before menke-5:** orchestrator Work IDs return no hits (confirmed in SPIKE-001 research).
**After menke-5:** expect hits on `spdd/canvas/SPIKE-001-*.md`, `agent-context/memory/context-index.md`,
and analysis files under `spdd/analysis/`.

Record spot-check results in
`spdd/analysis/SPIKE-001-guide-ingest-agent-context-exploration.md`.

## Verify setup (T01 + T07)

```bash
./scripts/guide/verify-spike-guide-setup.sh
./tests/test-retrieval-fixture-resolver.sh
```

## T05 A/B fixture drill

```bash
# Mode (a) resolver baseline
./scripts/guide/run-retrieval-ab-fixture.sh --capture-a

# Mode (b) after menke-fixture MCP queries — save URIs, then:
./scripts/guide/run-retrieval-ab-fixture.sh --check-mcp path/to/mcp-results.tsv
```

Record metrics in `spdd/analysis/SPIKE-001-retrieval-ab-ledger.md`.

## What this spike does not cover

- **Leg 3 (DICE domain graph)** — RAG directory ingest leaves `__Entity__` empty. Entity
  projection is T02/T03 in SPIKE-001 (`spdd/analysis/SPIKE-001-dice-entity-schema.md`).
- **Production wiring** — no changes to `resolve-agent-context.sh` or default installers.
- **A/B vs markdown resolver** — T05; run after ingest is stable.

## Related

| Doc | Role |
|-----|------|
| [SPIKE-001 canvas](../spdd/canvas/SPIKE-001-guide-rag-context-backend.md) | Full hybrid retrieval experiment |
| [guide-rag-research-and-dogfooding](guide-rag-research-and-dogfooding.md) | menke-1–4 operator guide |
| [Context loading and scaling](context-loading-and-scaling.md) | Tier-1 vs on-demand markdown path (baseline) |
