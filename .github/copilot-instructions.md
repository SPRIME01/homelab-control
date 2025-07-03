# Copilot Instructions for homelab-control

This document provides context for GitHub Copilot to better understand the `homelab-control` project.

## Project Overview

`homelab-control` is a unified Nx monorepo designed to provision, deploy, and manage a homelab control plane. It emphasizes security, self-healing, and GitOps principles.

## Key Technologies & Tools

*   **Infrastructure as Code:** Pulumi (TypeScript), Ansible
*   **Container Orchestration:** K3s (Kubernetes)
*   **Ingress:** Traefik, Cloudflare Tunnels
*   **Authentication:** Authelia, Bitwarden, HashiCorp Vault
*   **Observability:** OpenTelemetry, InfluxDB, Prometheus, Loki, Jaeger, Grafana
*   **GitOps CD:** ArgoCD
*   **Backup & DR:** Velero, Vault snapshots
*   **Monorepo Management:** Nx (TypeScript/Node.js)
*   **Build System:** Make, pnpm (Node.js), uv (Python)
*   **Python Development:** pyenv, uv, ruff, mypy, pytest

## Repository Layout Highlights

*   `apps/`: Contains Pulumi infrastructure, Ansible playbooks, ArgoCD Helm charts, OpenTelemetry collector config.
*   `libs/`: Shared TypeScript and Python libraries (e.g., `shared-types`, `kube-utils`, `ci-scripts`).
*   `tools/`: Custom Nx executors and generators.
*   `Makefile`: Main orchestration for common tasks.
*   `package.json`: Node.js and Nx dependencies.
*   `pyproject.toml`: Python development dependencies (managed by `uv`).

## Common Workflows & Commands

The project uses `make` for common operations. Here are some frequently used commands:

*   `make setup`: One-time setup to install all dependencies and tools (pnpm, pyenv, uv, pre-commit hooks).
*   `make app NAME=<app-name>`: Generate a new Python application.
*   `make lib NAME=<lib-name>`: Generate a new Python library.
*   `make lint`: Lint all affected projects.
*   `make typecheck`: Type-check all affected projects.
*   `make test`: Run tests for affected projects.
*   `make build`: Build all affected projects.
*   `make infra-plan TARGET=<target>`: Plan infrastructure changes (e.g., `vpc`, `control-plane`).
*   `make infra-apply TARGET=<target>`: Apply infrastructure changes.
*   `make ansible-run PLAYBOOK=<playbook>`: Run Ansible playbooks.
*   `make containerize PROJECT=<project-name>`: Build Docker image for a project.
*   `make graph`: Open Nx dependency graph.
*   `make help`: Get help with all available commands.

## Pre-commit Hooks

Pre-commit hooks are configured to run:
*   Code formatting (ruff)
*   Type checking (mypy)
*   Linting (ruff, Nx affected)
*   Testing (pytest, Nx affected)

## Important Files for Context

*   `Makefile`
*   `nx.json`
*   `package.json`
*   `pnpm-lock.yaml`
*   `pyproject.toml`
*   `.github/workflows/ci.yml`
*   `.make_assets/.pre-commit-config.yaml`
*   `scripts/setup.py`
