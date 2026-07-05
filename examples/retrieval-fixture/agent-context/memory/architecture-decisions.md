# Architecture Decisions

## Billing

### 2026-07-05 - SPIKE-FIX-001 - Use exponential backoff

Billing retry policy uses exponential backoff with a 30s cap for transient gateway errors.
