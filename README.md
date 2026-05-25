# DevOps Engineer - Infrastructure Challenge

This repository contains the infrastructure and application code for a complete CI/CD and Kubernetes deployment challenge.

## Architecture
- **Application**: A simple Python Flask backend that connects to a Redis database to increment a visitor counter.
- **Containerization**: Docker multi-stage build.
- **Kubernetes Environment**: AWS EKS (Elastic Kubernetes Service).
- **CI/CD**: GitHub Actions.

## Requirements Fulfilled

### 1. Working Deployment
The application stack is fully containerized and deployed to an AWS EKS cluster. It consists of:
- 1 Backend Service (Python Flask)
- 1 Database Dependency (Redis)
- Kubernetes Services (LoadBalancer for the app, ClusterIP for Redis)

### 2. CI/CD Pipeline
A GitHub Actions workflow (`.github/workflows/deploy.yml`) is configured to run automatically on pushes to the `main` branch. It performs the following:
- Checks out the source code.
- Logs into Docker Hub.
- Builds the Docker image and pushes it to the registry.
- Authenticates securely with AWS.
- Deploys the updated Kubernetes manifests directly to the EKS cluster.

### 3. Reliability Improvement
**Readiness and Liveness Probes** have been implemented on the Python application deployment (`k8s/app-deployment.yaml`).
- **Why**: To prevent Kubernetes from routing traffic to pods that are starting up or temporarily overloaded, and to automatically restart frozen containers.
- **Tradeoffs**: Probes introduce a small amount of overhead on the application. Misconfigured timeouts or checking database health in the liveness probe could lead to endless restart loops (cascading failures).

### 4. Intentional Failure Simulation
This deployment includes a documented intentional failure scenario for debugging purposes.
**Scenario**: Bad Environment Variable
1. In `k8s/app-deployment.yaml`, change the `REDIS_HOST` environment variable to `"wrong-redis"`.
2. Apply the manifest: `kubectl apply -f k8s/app-deployment.yaml`
3. Observe the failure: `kubectl get pods` will show the app pods failing their readiness probes (or entering CrashLoopBackOff).
4. Debug: `kubectl logs <pod-name>` will reveal the `Connection refused` error to the Redis host.
5. Fix: Revert the environment variable back to `"redis"` and reapply the manifest.

## Running Locally / Deployment Instructions

1. **Provision Cluster**:
   ```bash
   eksctl create cluster --name devops-challenge-cluster --region us-east-1 --nodegroup-name standard-workers --node-type t3.medium --nodes 2
   ```
2. **Apply Manifests**:
   ```bash
   kubectl apply -f k8s/redis-deployment.yaml
   kubectl apply -f k8s/app-deployment.yaml
   ```
3. **Access Application**:
   ```bash
   kubectl get svc devops-app-service
   ```
   Open the `EXTERNAL-IP` in your web browser.

4. **Teardown**:
   ```bash
   eksctl delete cluster --name devops-challenge-cluster --region us-east-1
   ```
