# Progress Log: SPIKE-001-guide-rag-context-backend

## 2026-07-11 — DICE contract formalized; guide spike branch build fixed; live run started

- **Contract (persist/retrieve) formalized:** `spdd/analysis/SPIKE-001-dice-entity-schema.md`
  rewritten as an explicit DICE contract (join key = Work ID; id rules per type; rel types
  `canvas`/`area`; merge-by-id idempotency; write API = projection load; read API = stats +
  new `GET /api/v1/data/spdd-projection/work/{workId}`; MCP domain traversal = T04 gap).
  `SPIKE-001-dual-ingest-model.md` updated with write/read surfaces per leg + chunk↔entity join.
- **Guide read API added (spike branch):** `subgraphForWorkId` on
  `SpddMarkdownProjectionService` + `/work/{workId}` endpoint — domain retrieval via
  `findRelated` typed edges, not cosine. Unit test extended.
- **Build fixes on guide spike branch:** pin `embabel-agent-rag-neo-drivine`
  `0.1.2-20260224.010659-19` (floating snapshot now needs agent 0.4.0); bump
  `drivine4j-spring-boot-starter` 0.0.29 → 0.0.45 (chat-store needs `SchemaCatalog`);
  test fixes for `InMemoryNamedEntityDataRepository` signature. Details in exploration log.
- **T05 mode (a) captured:** C01 6 paths/2579 B, C02 8/4026, C03 2/311 — ledger rows filled.
- **T01/T03 runtime:** menke-5 append-ingest running on :21337 (first attempt SIGKILLed
  mid-reference-reingest; restarted). Baseline store: 18083 chunks, 0 entities.
- `project-spdd-entities.sh` extended with optional Work ID subgraph fetch.

### Live-Neo4j contract exercise (same day, later)

- Leg 2 append grew the store 18083 → ~24.9k `ContentElement`. Repeated JVM deaths during
  startup re-ingest traced to a **native ONNX crash** (`libonnxruntime.so` SIGSEGV,
  `hs_err_pid2780387.log`); append mode is idempotent so re-runs resume.
- Leg 3 projection load on live Neo4j: **9 WorkId / 9 Canvas / 12 Area / 21 relationships**,
  `__Entity__` label confirmed. Cypher `MATCH (w:WorkId)-[r]->(x)` shows `canvas` edges for
  all 9 WorkIds + `area` edges where analysis declares code areas.
- Read API verified live: `GET /api/v1/data/spdd-projection/work/SPIKE-001-…` → 200 with
  WorkId + canvas neighbor (endpoint added to Guide security permit list after initial 403).
- MCP spot-checks (mode (b)) recorded in the A/B ledger: text/vector search retrieve the
  spike's own docs, but vector results tie the contract doc with unrelated framework source
  at 0.76 — auditability `mixed` vs domain-read `pass`.

## 2026-07-05 — T03 leg 3 entity projection (guide spike branch)

- Dual ingest doc: `spdd/analysis/SPIKE-001-dual-ingest-model.md`
- Orchestrator helper: `scripts/guide/project-spdd-entities.sh`
- Guide implementation on `cursor/spike-spdd-dice-projection-17f4` (**pushed**; draft PR on guide)
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
