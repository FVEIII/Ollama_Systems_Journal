# ADR-002 Data Isolation
Date: 2025-09-13
Status: Accepted (v1)
Decision Drivers: cost, operational simplicity, evolution path

## Context
Two services writing to Postgres. We want clear ownership and low coupling, without the overhead of DB-per-service at v1 scale.

## Decision
Use **schemas per service** within a single Postgres cluster, plus a **read replica** to offload analytics reads.

## Consequences
+ Lower cost/ops overhead than DB-per-service.
+ Clear ownership boundaries via schemas and per-service roles.
- Larger failure/blast radius than fully isolated databases.
- Risk of noisy neighbors if one service misbehaves.

## Alternatives Considered
- **DB-per-service:** strongest isolation and autonomy; higher cost and admin overhead.
- **Single shared schema:** simplest short-term; highest coupling and migration pain.

## Migration Path
If isolation or scale needs increase: enable **logical replication** and split a service to its own DB with minimal downtime.

## Verification / Guardrails
- Separate DB roles and connection strings per service.
- Query budgets and statement timeouts to reduce noisy-neighbor effects.
- Backups, restore drills, and replica health alerts.
