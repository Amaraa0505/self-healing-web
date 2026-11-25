# Self-Healing Cloud Web System (Kubernetes)

High-availability replicated web architecture orchestrated by Kubernetes with automated load balancing, failover, and self-healing pod recovery.

## Architecture
- **Orchestration:** Kubernetes (`Deployment` with 3 replicas + `LoadBalancer` Service)
- **Compute Nodes:** 3 replicated Python Flask web pods
- **State & Logs:** Redis in-memory database for shared node metrics and cluster event logs
- **Self-Healing:** Kubernetes HTTP `livenessProbe` (3s interval) + automatic pod restart policy

## Quick Start
```bash
docker build -t self-healing-web-web:latest .
kubectl apply -f k8s.yaml
kubectl get pods