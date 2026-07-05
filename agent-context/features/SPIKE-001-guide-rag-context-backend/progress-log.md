# Progress Log: SPIKE-001-guide-rag-context-backend

## 2026-07-05 — T03 leg 3 entity projection (guide spike branch)

- Dual ingest doc: `spdd/analysis/SPIKE-001-dual-ingest-model.md`
- Orchestrator helper: `scripts/guide/project-spdd-entities.sh`
- Guide implementation on `cursor/spike-spdd-dice-projection-17f4` (local; push requires repo access)
- **Not** DICE proposition pipeline — structured markdown projection via `NamedEntityDataRepository`
- **Next:** push guide branch + local verify `__Entity__` > 0; T04 MCP entity traversal fork

## 2026-07-05 — T05 A/B harness

- Ledger stub: `spdd/analysis/SPIKE-001-retrieval-ab-ledger.md`
- Scripts: `run-retrieval-ab-fixture.sh`, `capture-mode-a-baseline.sh`, `verify-spike-guide-setup.sh`
- Mode (a) baseline committed: `tests/fixtures/spike-001-mode-a-baseline.tsv` (3 cases)
- **Next:** local menke-5/menke-fixture ingest; fill ledger mode (b) rows

## 2026-07-05 — T07 retrieval fixture harness

- Added `examples/retrieval-fixture/` mock project (SPIKE-FIX-001)
- Gold test: `tests/test-retrieval-fixture-resolver.sh` (15 assertions, mode A baseline)
- CI: `.github/workflows/test-retrieval-fixture-resolver.yml`
- menke-fixture Guide profile + `append-retrieval-fixture.sh` for mode B (local)
- **Next:** T01 menke-5 ingest + MCP spot-checks; T05 A/B using fixture

## 2026-07-05 — Draft PR policy

- PR #24 confirmed **draft**; policy: all SPIKE-001 PRs stay draft until T06 go/no-go

## 2026-07-05 — SPDD documentation + branch policy

- Confirmed spike stays off `main`; active branch `cursor/spike-guide-ingest-agent-context-17f4`
- Draft PR #24 opened (menke-5 scaffold — T01)
- `/sdlc-spdd-analysis` updated: `spdd/analysis/SPIKE-001-guide-rag-context-backend-analysis.md`
  (branch isolation, three-mode experiment, mock fixture plan T07)
- Feature workspace created under `agent-context/features/SPIKE-001-guide-rag-context-backend/`
- **Next:** local menke-5 ingest + MCP spot-checks; then T07 mock fixture

## 2026-06-19 — Confirmational research

- Live MCP store validated (legs 1–2); leg 3 = fork work
- Notes: `spdd/analysis/SPIKE-001-guide-rag-context-backend-research.md`
- DICE entity schema draft started: `spdd/analysis/SPIKE-001-dice-entity-schema.md`

## 2026-06-19 — Spike opened

- Requirement + canvas drafted (ROADMAP make-it-fast, parked behind FEAT-004/005)
