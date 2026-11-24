# Self-Healing Cloud Web System

High-availability replicated web architecture with automated load balancing, failover, and container recovery.

## Architecture
- **Load Balancer:** Nginx Reverse Proxy (`:5050` -> `:80`) with `proxy_next_upstream` auto-failover
- **Compute Nodes:** 3 replicated Python Flask web containers
- **State & Logs:** Redis in-memory database for shared node metrics and event logs
- **Self-Healing:** Docker health checks (3s interval) + `restart: always` policy
- **CI/CD:** Jenkins automated build and health verification pipeline

## Quick Start
```bash
docker compose up -d --build