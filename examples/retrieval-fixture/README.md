# Retrieval fixture (SPIKE-001 T07)

Controlled mock project for SPIKE-001 retrieval A/B. Seeds `agent-context/memory/`
indexes with known rows so `resolve-agent-context.sh` output can be compared to a
gold file in CI.

**Spike branch only** — not installed into target projects.

## Layout

| Path | Role |
|------|------|
| `spdd/analysis/SPIKE-FIX-001-retrieval-fixture-analysis.md` | Domain keywords + code areas |
| `spdd/canvas/SPIKE-FIX-001-retrieval-fixture.md` | REASONS canvas |
| `agent-context/memory/context-index.md` | Indexed session, pitfall, decision rows |
| `src/billing/` | Code area referenced by analysis |

## Run baseline test (mode A — markdown resolver)

From repo root:

```bash
./tests/test-retrieval-fixture-resolver.sh
```

15 gold assertions across three cases: code+work-id, analysis+work-id, areas-only code.

## Guide ingest (mode B — local only)

Copy `templates/guide-profiles/application-menke-fixture.yml.example` into your
guide checkout, then:

```bash
./scripts/guide/append-retrieval-fixture.sh
```

Spot-check queries: `tests/fixtures/spike-001-mcp-queries.tsv`. Record chunk URIs in
`spdd/analysis/SPIKE-001-guide-ingest-agent-context-exploration.md`.
