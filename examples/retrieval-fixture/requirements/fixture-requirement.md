# Requirement: SPIKE-FIX-001-retrieval-fixture

## Summary

Mock project for SPIKE-001 retrieval experiments. Provides seeded indexes and a
tiny `src/billing/` code area so mode (a) resolver output is gold-testable in CI.

## User Story

As a spike researcher, I want a controlled fixture so I can compare markdown
resolver paths against Guide MCP hits without noise from the live orchestrator corpus.

## Acceptance Criteria

- [ ] `resolve-agent-context.sh` gold test passes (`tests/test-retrieval-fixture-resolver.sh`)
- [ ] Domain keyword `billing` maps to `src/billing` in `domain-index.md`
- [ ] Unrelated area `src/payments` is indexed but excluded when resolving SPIKE-FIX-001

## Non-Goals

- Not a real application; no production code
- Not shipped to target projects
