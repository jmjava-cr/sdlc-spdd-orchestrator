# REASONS Canvas: SPIKE-FIX-001-retrieval-fixture - Retrieval experiment fixture

## Metadata

- Work ID: SPIKE-FIX-001-retrieval-fixture
- Work Type: Spike
- Status: Complete
- Readiness: Ready For Coding
- Created: 2026-07-05
- Updated: 2026-07-05
- Owner: fixture
- Target Project: retrieval-fixture (mock)
- Stack: Markdown + minimal src tree
- Parent spike: SPIKE-001-guide-rag-context-backend

## R - Requirements

### User Goal

Provide a controlled project for retrieval A/B gold tests.

### Business / Product Goal

De-risk SPIKE-001 T05 by making mode (a) resolver output deterministic in CI.

### Acceptance Criteria

- [x] Seeded indexes for `src/billing`
- [x] Unrelated `src/payments` row for negative assertions
- [x] Gold test harness in `tests/test-retrieval-fixture-resolver.sh`

## E - Entities

### Domain Entities

- BillingRetryPolicy (fixture documentation in `src/billing/`)

## A - Approach

Seed memory indexes; run `resolve-agent-context.sh` against gold TSV.

## S - Structure

See `examples/retrieval-fixture/README.md`.

## O - Operations

### T01 - Seed fixture indexes

- Status: Complete

## N - Norms

Fixture only — spike branch.

## S - Safeguards

Do not merge fixture into target project installers.
