# Incident Runbook RB-402: Ingress Gateway 504 Timeout

## 1. Overview
This runbook governs HTTP 504 (Gateway Timeout) errors occurring on the `/api/v2/` ingress mesh.

## 2. Thresholds & Trigger Conditions
- **Hard Timeout Limit**: Ingress proxies terminate unfulfilled connections at exactly **45.0 seconds**.
- **Auto-Retry Policy**: Downstream clients must NOT retry requests immediately. A client-side exponential backoff jitter of `base=2s, max=30s` is strictly required.
- **Worker Drain Threshold**: When queue depth exceeds 250 pending jobs per partition, the load balancer initiates 504 fast-fails.

## 3. Remediation & Routing Protocol
- **Action for Incomplete Telemetry**: If the customer request does not include transaction correlation IDs (`X-Correlation-ID`), request the header immediately (routing: **CLARIFY**).
- **Action for Confirmed Timeout with Header**: If transaction correlation ID is present and payload exceeds 5MB, route to Database Infrastructure (routing: **ESCALATE**) citing `RB-402-SEC3`.
