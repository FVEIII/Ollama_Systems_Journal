# Architecture Draft (v1)

**Edge:** API Gateway terminates auth (OIDC/JWT), validates requests, throttles abuse.

**Services (containers):**
- `users`: authentication, profiles, session management.
- `analytics`: chart data, pre-aggregations, cache population.

**Data:** 
- Postgres primary for writes.  
- Read-replica for analytics reads.  
- Separate schemas per service.

**Cache:** 
- Redis cache-aside for hot chart payloads.  
- Short TTL (60–300s) with explicit invalidation on writes.

**Async:** 
- SNS topic emits write events.  
- SQS workers handle cache invalidation and slow tasks like CSV imports or recomputation.

**Observability:** 
- Logs, metrics, and traces with correlation IDs.  
- Error budgets with automated rollback triggers.

**Security:** 
- Secrets manager for sensitive data.  
- Per-service database roles.  
- WAF at the gateway.

## Request Flow
Client → API Gateway → {users | analytics} → Postgres / Redis  
Writes → SNS → SQS workers → Cache invalidation or data refresh

## Evolution Path
- If analytics load spikes, migrate analytics service to serverless.
- If Postgres becomes a bottleneck, split databases using logical replication.
- For wide scans, consider adding a columnar sidecar like DuckDB or Athena.
