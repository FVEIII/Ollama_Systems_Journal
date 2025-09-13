# ADR-001 Edge Control Plane
Date: 2025-09-13
Status: Accepted (v1)
Decision Drivers: simplicity, centralized auth/policy, low cost

## Context
Two services (`users`, `analytics`) behind a single public edge. We need authentication (OIDC/JWT), request validation, throttling, and a stable place to version/retire APIs. Traffic is modest; team size is small.

## Decision
Use a single **API Gateway** at the edge. Do **not** add a separate load balancer in v1.

## Consequences
+ Centralized auth, rate limits, request/response validation, versioning.
+ Simpler routing and operations; one ingress to observe and secure.
- Less per-service L7 tuning or independent edge scaling.

## Alternatives Considered
- **LB only (ALB/NLB):** simpler/cheaper but lacks policy features we want at the edge.
- **Gateway + per-service LB:** adds flexibility but more moving parts for v1.

## Migration Path
If per-service policies or scaling diverge, introduce internal LBs later and keep the gateway as the stable north–south control plane.

## Verification / Guardrails
- IaC tests check required gateway features (auth, rate limit, schema validation) are enabled.
- Canary deployments through the gateway; automatic rollback on SLO breach.
