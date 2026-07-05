# REASONS Canvas: SPIKE-001-guide-rag-context-backend - Guide as a DICE hybrid context backend

## Metadata

- Work ID: SPIKE-001-guide-rag-context-backend
- Work Type: Spike
- Status: In Progress
- Readiness: Needs Analysis
- Created: 2026-06-19
- Updated: 2026-07-05 (SPDD analysis + branch policy; menke-5 scaffold on spike branch)
- Owner:
- Target Project: sdlc-spdd-orchestrator (self / dogfood)
- Stack: Bash + Markdown harness ↔ JVM (Embabel guide) + Neo4j graph + RAG, over MCP (SSE)
- Source System: Roadmap
- Roadmap: ROADMAP.md
- Milestone:
- Delivery stage: make it fast (optimization) — **spike, parked behind FEAT-004/005**
- Time-box: 1–2 focused sessions
- Branch: `cursor/spike-guide-ingest-agent-context-17f4` — **off `main` until T06 go/no-go**
- Related PR: #24 (draft)

## R - Requirements

### User Goal

Find out whether a **DICE-style hybrid** retrieval over guide's Neo4j — combining our
existing lexical index, embedding discovery, and a typed **domain graph** — selects
better prompt context than today's markdown lookup, before committing to the dependency.

### Business / Product Goal

De-risk the make-it-fast retrieval direction with evidence. Produce a go / no-go
decision and, if go, the shape of the follow-on feature(s).

### Framing: the three retrieval legs (Domain-Integrated Context Engineering)

Per Rod Johnson's **DICE (Domain-Integrated Context Engineering)** — typed domain
objects, not generic chunks, should drive context. The SDLC-SPDD domain already exists
(Work ID, Operation, Canvas, REASONS sections, Decision, Pitfall, Pattern, code-area,
phase, metric Kind). The hybrid uses three complementary legs over one join key (the
domain model):

1. **Lexical/area index (current)** — deterministic, auditable, exact identifiers.
2. **Embedding discovery (guide RAG)** — synonym/paraphrase reach to find entry points.
3. **Domain graph (DICE)** — typed `Spdd*` entities + relationships in Neo4j; retrieve by
   following domain structure. Requires **designing DICE-compatible entity types and an
   ingest projection** before leg 3 works — RAG chunk ingest alone leaves `__Entity__`
   empty (confirmed 2026-06-19). **Verified: fork work** — guide MCP exposes no generic
   domain-graph traversal (see Confirmational Research).

### Hypothesis

A domain-graph-led hybrid (lexical + embedding + DICE relationships) surfaces more
relevant prior decisions, pitfalls, patterns, and canvases than markdown
`context-index.md` lookup, at comparable or lower context cost — while staying
auditable (retrieval explained by domain links, not opaque cosine). **Research guard
(2026-06-19):** the embedding leg alone cannot satisfy auditability — use it for
discovery; legs 1 + 3 must justify what stays in context.

### Decision Criteria (what "done" means)

- [ ] SDLC-SPDD DICE entity schema designed and reviewed (`spdd/analysis/SPIKE-001-dice-entity-schema.md`).
- [ ] Entity projection ingest loads at least one real Work ID subgraph into Neo4j `__Entity__`.
- [ ] One real Work ID run across the modes: (a) current resolver, (b) embedding-only RAG, (c) DICE hybrid (graph + lexical + embedding).
- [ ] Outcomes compared on the FEAT-004 ledger (rework count, review-result) + approximate context tokens.
- [ ] Auditability check: can each included item be explained by a domain link / matched term (not just a similarity score)?
- [ ] Written go / no-go with trade-offs (retrieval value vs. JVM+Neo4j+domain-modeling cost).
- [ ] If go: a sketch of follow-on FEAT(s) — domain-graph schema, corpus/ingest wiring, retrieval seam, optional live write tool.

### Non-Goals

- No production integration; no required dependency; default markdown-first path unchanged.
- No new guide features beyond what a throwaway experiment needs.

### Assumptions

- guide can ingest arbitrary directories (`guide.directories` + `guide.git-ingestion`) — confirmed in its `DataManager.loadReferences()`.
- guide exposes semantic-search MCP tools (`docs_*`: `textSearch`, `vectorSearch`, `broadenChunk`, `zoomOut`) over its Neo4j `ContentElement` store — **confirmed live 2026-06-19**. It does **not** expose generic domain-graph traversal (that leg is fork work).
- Neo4j (guide's store) is a graph DB, so it can hold a DICE domain graph alongside RAG chunks — confirmed it is Neo4j.
- The SDLC-SPDD domain model is implicit in our artifacts; leg 3 requires explicit **DICE entity types** (`SpddWorkId`, `SpddCanvas`, etc.) and a projection ingest — RAG directory ingest alone does not populate `__Entity__`.
- FEAT-004 ledger is available as the scoreboard (or co-stubbed for the experiment).

### Open Questions

- ~~Does retrieval plug in at the assistant layer (Cursor calls guide MCP mid-session) or via a resolver shim?~~ **Resolved 2026-06-19: assistant layer.** Context-engineering corpus + Embabel MCP client autoconfig align with per-turn agent retrieval, not a one-time resolver shim.
- Store-as-we-go via batch append-ingest of `agent-context/memory/` vs. a live `remember()` write tool in the fork? (Lean: batch append for spike; DICE proposition extraction is the live-write alternative — defer.)
- Minimal DICE domain slice worth modeling first (likely Work ID ↔ Area ↔ Decision/Pitfall/Pattern) vs. full model. **Draft schema:** `spdd/analysis/SPIKE-001-dice-entity-schema.md` — finalize in T02.
- Kotlin `NamedEntity` classes vs. Cypher-only `NamedEntityData` load for spike speed? (Resolve in T02.)
- ~~Does Embabel/guide already expose domain-graph retrieval, or is that fork work?~~ **Resolved 2026-06-19: fork work.** MCP exposes `docs_*` + code signatures only; `SearchOperations` entity/graph APIs exist in the library layer but not on guide MCP.

### Confirmational Research (2026-06-19)

Full notes: `spdd/analysis/SPIKE-001-guide-rag-context-backend-research.md`

Design verification against live guide MCP (`:21337`) + Neo4j + Embabel/DICE corpus
(menke code ~1,416 docs + menke-2 reference 24 URLs; 9,664 chunks; 384-dim ONNX).
**Goal:** validate spike **architecture**, not merely confirm ingest completeness.

| Design element | Verdict |
|----------------|---------|
| Three-leg hybrid over one Neo4j store | ✅ Confirmed — `SearchOperations` dual search + DICE dual-role graph |
| MCP = legs 1–2; leg 3 fork | ✅ Confirmed |
| Assistant-layer integration | ✅ Confirmed |
| FEAT-004 ledger / evals scoreboard | ✅ Confirmed (Hamel evals corpus in store) |
| GOAP as optional policy layer | ✅ Confirmed native to Embabel; not retrieval substitute |
| Auditability via domain links | ⚠️ Partial — embedding leg opaque; legs 1+3 justify inclusions |
| DICE leg = our SDLC-SPDD slice | ⚠️ Refined — requires `Spdd*` entity design + projection ingest; see entity schema draft |
| Hybrid beats markdown (hypothesis) | ⏳ Plausible; A/B still required |

**MCP connectivity (post menke-2 ingest):** `helloBanner` → 0.4.0-SNAPSHOT. Leg 1
`docs_textSearch` and leg 2 `docs_vectorSearch` return strong hits on SPDD, context
engineering, evals, DICE proposition pipeline. `broadenChunk` surfaces Fowler "decision
memory" passages. Leg 3: `__Entity__` count = 0. Indexes ONLINE (underscore names).

**Not yet in store (expected until menke-5):** orchestrator `agent-context/` +
`spdd/canvas/` — needed for Work-ID A/B. Exploration branch
`cursor/spike-guide-ingest-agent-context-17f4` adds menke-5 profile + runbook; guide
branch `ingest-to-hub` for git incremental ingest.

## E - Entities

### Application Components

- guide (Embabel): RAG ingestion + `docs_*` semantic-search MCP tools, SSE at `http://localhost:21337/sse` (this instance; guide's in-app default port is 1337)
- Orchestrator memory: `agent-context/memory/`, `spdd/canvas/`, `spdd/analysis/`
- Cursor as the MCP client; FEAT-004 ledger as the measurement

### External Systems

- Neo4j (local docker compose `embabel-neo4j`, or Embabel Hub)

### Data / Persistence

- Neo4j `ContentElement` RAG store (chunks + ONNX embeddings)
- Reference corpus (curated reading) cataloged in `spdd/analysis/SPIKE-retrieval-reference-corpus.md`, ingested via guide profile `menke-2`
- DICE domain graph: typed `Spdd*` entities in Neo4j (`__Entity__` layer) — schema in `spdd/analysis/SPIKE-001-dice-entity-schema.md`
- Throwaway / local only for the spike

### Domain Entities (DICE slice — Embabel conventions)

See `spdd/analysis/SPIKE-001-dice-entity-schema.md`. Package `com.embabel.spdd.domain`;
labels = class simple names + `__Entity__`; relationships via `@Semantics` property refs.

- **WorkId**, **Canvas**, **Operation**, **Area**, **Decision**, **Pitfall**, **Pattern**
- Persist via `NamedEntityDataRepository`; schema via `DataDictionary.fromClasses("sdlc-spdd", …)`

## A - Approach

### Proposed Approach (experiment)

1. Stand up a local guide; set `guide.directories` to orchestrator `agent-context/memory/` (+ `spdd/`); append-ingest for **leg 2** (RAG chunks).
2. **Design SDLC-SPDD DICE entities** per Embabel conventions (`NamedEntity`, `@Semantics`, `DataDictionary`); finalize `SPIKE-001-dice-entity-schema.md`.
3. **Implement entity projection ingest** via `NamedEntityDataRepository` + `mergeRelationship` (not proposition pipeline).
4. Connect Cursor to guide MCP; sanity-check legs 1–2 on corpus; add fork tool for leg 3 domain traversal by Work ID / Area.
5. Pick one real Work ID. Run across modes: (a) lexical resolver, (b) embedding-only RAG, (c) DICE hybrid (graph-led + lexical + embedding).
6. Record on FEAT-004 ledger + auditability (every item explainable by domain link/term).
7. Write go / no-go; if go, sketch follow-on FEAT(s) including production entity ingest + retrieval seam.

### Alternatives Considered

- Stay markdown-first only (the no-go baseline).
- Live `remember()` write tool now (deferred — only if the spike says go).

### Risks

- Entity schema design underestimated — leg 3 blocked until `Spdd*` types and projection ingest exist.
- Embabel MCP / Hub setup friction (the server has errored before — verify connection first).
- Small-sample A/B is indicative, not conclusive — treat as directional evidence.

## S - Structure

### Files To Add

- Confirmational research (done): `spdd/analysis/SPIKE-001-guide-rag-context-backend-research.md`
- DICE entity schema (draft): `spdd/analysis/SPIKE-001-dice-entity-schema.md`
- Spike analysis (done): `spdd/analysis/SPIKE-001-guide-rag-context-backend-analysis.md`
- T01 exploration log: `spdd/analysis/SPIKE-001-guide-ingest-agent-context-exploration.md`
- A/B findings note (pending): extend analysis artifact T06 section
- Feature workspace (done): `agent-context/features/SPIKE-001-guide-rag-context-backend/`
- Mock fixture (pending T07): `examples/retrieval-fixture/`, `tests/test-retrieval-fixture-resolver.sh`

### Files To Modify

- None in the framework (spike is exploratory; no production wiring).

### Documentation Structure

- Findings + decision recorded in the analysis note and this canvas's Sync Notes.

## O - Operations

### T01 - Stand up guide + ingest orchestrator memory (leg 2 — RAG chunks)

- Status: In Progress
- Description: Local guide instance on branch `ingest-to-hub`; menke-5 profile points
  `guide.directories` at `agent-context/memory/`, `spdd/canvas/`, `spdd/analysis/`; append-ingest
  with git incremental; verify MCP spot-checks.
- Files: `templates/guide-profiles/application-menke-5-orchestrator-context.yml.example`,
  `scripts/guide/append-orchestrator-context.sh`, `docs/spike-guide-ingest-agent-context.md`,
  `spdd/analysis/SPIKE-001-guide-ingest-agent-context-exploration.md`
- Validation: Ingestion summary shows orchestrator memory loaded as chunks; MCP returns Work ID hits
- Research: menke code + menke-2 reference corpus ingested; menke-5 exploration scaffold on
  `cursor/spike-guide-ingest-agent-context-17f4`

### T02 - Design SDLC-SPDD DICE entity schema (Embabel conventions)

- Status: In Progress
- Description: Define `NamedEntity` types per Embabel conventions (`id`/`name`/`description`, `@Semantics` relationships, `DataDictionary.fromClasses` or `dataDictionaryFromPackages`). Review against `dice/README.md` and `embabel-agent-rag` `NamedEntity`/`NamedEntityDataRepository` APIs. Finalize draft against one real Work ID.
- Files: `spdd/analysis/SPIKE-001-dice-entity-schema.md`
- Validation: Convention alignment table complete; ingest mapping uses `NamedEntityDataRepository`, not proposition pipeline

### T03 - Implement entity projection ingest (leg 3 — domain graph)

- Status: Not Started
- Description: Fork loader: parse orchestrator artifacts → populate Neo4j `__Entity__` subgraph; register `Spdd*` for DICE `entityPackages` / `SearchOperations`; optional fork MCP domain-query tool.
- Files: (guide fork; projection script)
- Validation: `__Entity__` count > 0; domain query by Work ID returns linked Canvas, Operations, Decision/Pitfall/Pattern

### T04 - Connect Cursor to guide MCP + sanity retrieval (all legs)

- Status: In Progress
- Description: Link guide SSE MCP into Cursor; confirm legs 1–2 on corpus; leg 3 via fork domain-query tool on projected entities.
- Files: (Cursor MCP config; fork tool)
- Validation: Relevant results for a known Work ID/area via each leg
- Research: MCP connected; legs 1+2 verified; leg 3 blocked on T02/T03

### T05 - Compare modes on one real Work ID and record on the ledger

- Status: Not Started
- Description: Run a session across (a) lexical resolver, (b) embedding-only, (c) DICE hybrid; capture rework/review-result/tokens + auditability.
- Files: spdd/analysis/SPIKE-001-guide-rag-context-backend-analysis.md
- Validation: All modes recorded; metrics comparable

### T06 - Write go / no-go recommendation

- Status: Not Started
- Description: Summarize evidence + trade-offs; if go, sketch follow-on FEAT(s) including production entity ingest + retrieval seam.
- Files: `spdd/analysis/SPIKE-001-guide-rag-context-backend-analysis.md` (T06 section), this canvas Sync Notes
- Validation: Clear decision with rationale; only then consider merging research notes to `main`

### T07 - Mock retrieval fixture + resolver gold test

- Status: Not Started
- Description: Add `examples/retrieval-fixture/` with seeded indexes, canvas, analysis, and tiny
  `src/` tree; `tests/test-retrieval-fixture-resolver.sh` diffs `resolve-agent-context.sh`
  output against gold TSV. Optional `menke-fixture` Guide profile for MCP spot-checks (local only).
- Files: `examples/retrieval-fixture/`, `tests/test-retrieval-fixture-resolver.sh`,
  `templates/guide-profiles/application-menke-fixture.yml.example`
- Validation: CI passes resolver gold test; MCP spot-check doc in exploration log

### T08 - SPDD workspace documentation

- Status: In Progress
- Description: Feature workspace under `agent-context/features/SPIKE-001-guide-rag-context-backend/`;
  analysis artifact with branch policy and experiment protocol; operator runbook links analysis.
- Files: `agent-context/features/SPIKE-001-guide-rag-context-backend/*`,
  `spdd/analysis/SPIKE-001-guide-rag-context-backend-analysis.md`
- Validation: requirement → analysis → canvas → feature workspace chain complete on spike branch

## N - Norms

### General

- Time-boxed: stop at the decision, do not slide into building the integration.
- No production dependency added during the spike.
- Markdown-first default path stays intact.

## S - Safeguards

- This is exploratory: do not wire guide into the default resolver or installers under this Work ID.
- **Stay off `main`:** all spike implementation and docs on `cursor/spike-*` branches until T06
  go/no-go. **All PRs for this Work ID must remain draft** until T06 — never mark ready for review
  or merge to `main` during the experiment. Markdown-first default on `main` unchanged.
- Keep all Neo4j/guide setup local/throwaway; no secrets committed.
- Operator docs and Guide profiles are orchestrator-only — never ship to target projects.
- If the spike says "go", the real integration is a separate FEAT with its own canvas on a new branch.
- Posture/optimization framing stays internal; nothing ships to target projects from this spike.

## Review Checklist

- [ ] Question answered with evidence
- [ ] Decision criteria met
- [ ] Trade-offs documented
- [ ] Go / no-go recorded
- [ ] Follow-on FEAT(s) sketched if go
- [ ] No production wiring left behind
- [ ] No secrets committed

## Sync Notes

Spike to de-risk the make-it-fast retrieval direction via a **DICE (Domain-Integrated
Context Engineering)** hybrid over guide/Neo4j: lexical index + embedding discovery +
typed domain graph, with the domain model as the shared join key. Converges with the
Embabel GOAP idea: guide/Neo4j = retrieval substrate, the DICE domain graph = structure,
FEAT-004 ledger = scoreboard, GOAP = optional selection policy. Keeps retrieval
auditable (domain links, not opaque similarity).

**Confirmational research 2026-06-19:** design validated against live MCP store —
architecture sound; proceed. Refinements: explicit `Spdd*` DICE entity design + projection
ingest required for leg 3 (RAG alone leaves `__Entity__` empty); auditability via legs
1+3; embedding for discovery only. Entity schema draft:
`spdd/analysis/SPIKE-001-dice-entity-schema.md`. A/B + go/no-go still pending.

**SPDD documentation 2026-07-05:** analysis artifact + feature workspace on spike branch
`cursor/spike-guide-ingest-agent-context-17f4` (PR #24). Branch stays off `main` until T06.
Mock fixture (T07) planned for scriptable A/B. See
`spdd/analysis/SPIKE-001-guide-rag-context-backend-analysis.md`.

## Final Status

- Status:
- Completed Date:
- PR:
- Follow-Up Tasks:
