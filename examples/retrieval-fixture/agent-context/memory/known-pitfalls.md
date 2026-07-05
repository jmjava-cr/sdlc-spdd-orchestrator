# Known Pitfalls

## Billing

### 2026-07-05 - SPIKE-FIX-001 - Do not retry without idempotency key

Charge retries must include an idempotency key or duplicate charges may post.
