# ADR-003 Caching Strategy
Date: 2025-09-13
Status: Accepted (v1)
Decision Drivers: read-heavy analytics, latency targets, DB protection

## Context
Chart endpoints are read-heavy and repeat similar aggregations. We want fast p95 latency (<300ms for cached paths) and to avoid hammering Postgres.

## Decision
Use **Redis cache-aside** for analytics responses:
- Short TTL (60–300s) for freshness.
- Explicit invalidation on writes via SNS events consumed by SQS workers.
- Request coalescing (single-flight) to avoid stampedes.

## Consequences
+ Lower DB load; predictable latency for hot paths.
- Potential staleness between writes and invalidation.
- Complexity for key versioning and jittered TTLs.

## Alternatives Considered
- **Materialized views only:** good for heavy pre-aggregation; still needs caching for bursty access.
- **No cache:** simpler, but risks DB saturation and slower p95.

## Migration Path
If cache hit-rates are low or data is wide: precompute aggregates into materialized tables on a schedule, then cache those results.

## Verification / Guardrails
- Dashboards: cache hit ratio, p95 latency, error rates, cost/request.
- Circuit breaker to DB with backoff; alert on stampede patterns.
- Keys are namespaced (`analytics:v1:<query-fingerprint>`), with TTL jitter to avoid synchronized expiry.
