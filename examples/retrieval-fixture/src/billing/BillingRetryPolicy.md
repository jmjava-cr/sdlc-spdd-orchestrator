# Billing retry policy (fixture)

Area: `src/billing`

Retry transient billing gateway failures with exponential backoff (cap 30s).
Requires idempotency key on every retry attempt.
