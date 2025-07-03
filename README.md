# 🏠 Home Station Control

> A unified Nx monorepo to provision, deploy, and manage your entire homelab control plane—secure, self‑healing, and GitOps‑driven! 🚀

---

## 📖 Table of Contents

1. [✨ Features](#-features)
2. [👥 Who Is This For?](#-who-is-this-for)
3. [🚀 Quickstart](#-quickstart)
4. [🏗️ Architecture](#️-architecture)
5. [📂 Repo Layout](#-repo-layout)
6. [🔧 Prerequisites](#-prerequisites)
7. [⚙️ Usage](#️-usage)
8. [️ Security & Secrets](#️-security--secrets)
9. [💾 Backups & DR](#-backups--dr)
10. [🛠️ CI/CD & GitOps](#️-cicd--gitops)
11. [🏢 Business Requirements & Compliance](#-business-requirements--compliance)
12. [🔧 Build System Details](#-build-system-details)
13. [🤝 Contributing](#-contributing)
14. [📄 License](#-license)

---

## ✨ Features

- **🏗️ Infrastructure as Code** with Pulumi (TypeScript) + Ansible
- **🛡️ Secure Ingress** via Traefik + Cloudflare Tunnels
- **🔐 Central Auth**: Authelia SSO + Bitwarden + HashiCorp Vault
- **📊 Observability**: OpenTelemetry → InfluxDB, Prometheus, Loki, Jaeger, Grafana
- **🚁 GitOps CD** powered by ArgoCD
- **🔄 Self‑healing & Backups** with Velero, Vault snapshots, DB dumps
- **🧩 Modular Nx Monorepo**: generate, test, and deploy any service with Nx CLI
- **⚡ Hybrid Build System**: Make orchestration + pnpm/Nx + uv for Python

---

## 👥 Who Is This For?

### Primary User Personas

* 🧑‍💻 **Edge AI Engineer**: deploys MLOps workloads on Jetsons; needs seamless CI/CD and secrets.
* 🏠 **Smart‑Home Admin**: configures HomeAssistant integrations, MQTT topics, device access.
* 🔐 **Security‑Focused Hobbyist**: demands MFA, Vault‑backed secrets, encrypted tunnels.
* 🚀 **DevOps Learner**: experiments with Pulumi, ArgoCD, Nx, and wants a turnkey homelab.

### Why HomeStation vs Alternatives?

* **Uniquely** integrates edge AI and homelab under one GitOps umbrella
* **All‑in‑one**: infra, secrets, ingress, observability, remote‑desktop, captive‑portal
* **Loosely coupled & modular**: swap out any component (e.g., replace Home Assistant with Node‑RED)
* **Self‑healing** and **auto‑documentation** reduce maintenance overhead

---

## 🚀 Quickstart

```bash
# 1. Clone repo
git clone https://github.com/SPRIME01/homelab-control.git
cd homelab-control

# 2. One-time setup (installs all dependencies & tools)
make setup

# 3. Deploy infrastructure
make infra-apply TARGET=control-plane

# 4. Apply configuration management
make ansible-run PLAYBOOK=bootstrap-wsl2

# 5. Deploy applications via GitOps
make infra-apply TARGET=argocd-apps

# 6. Verify services → https://traefik.home.local
```

> 📋 **Complete workflow diagram**: See [docs/diagrams/user-workflows.mmd](docs/diagrams/user-workflows.mmd) for detailed user flow visualization.

---

## 🏗️ Architecture

```mermaid
flowchart LR
  subgraph Home Station (WSL2: 182.168.0.51)
    Pulumi --> K3s[🖥️ K3s Control Plane]
    Ansible --> K3s
    K3s -- Ingress --> Traefik[🌐 Traefik Ingress]
    Traefik --> Authelia[🔒 Authelia]
    Traefik --> Bitwarden[🔑 Bitwarden]
    Traefik --> ArgoCD[🔄 ArgoCD]
    Traefik --> Guacamole[🖥️ Guacamole]
    Traefik --> Homepage[🏠 Homepage Portal]
    Traefik --> Vault[🗝️ Vault]
    K3s --> Observability[📊 OTEL → InfluxDB, Loki, Prom, Jaeger, Grafana]
  end

  subgraph LAN (192.168.0.0/24)
    Router[🛡️ OpenWRT + AdGuard + Tailscale]
    HomeAssistant[🏡 HA Yellow (MQTT & InfluxDB)]
  end

  HomeStation -- MQTT --> HomeAssistant
  HomeStation -- MQTT --> Router
  Router -- Tailscale --> Jetsons[🚀 Jetson Actor Nodes]
```

---

## 📂 Repo Layout

```
/
├── apps/                         # Nx Applications
│   ├── pulumi-control/           # Pulumi TS infra (K3s, Traefik, Vault, Cloudflare)
│   ├── ansible-playbooks/        # WSL2 host bootstrap & config
│   ├── argocd-helm-charts/       # Helm charts for Authelia, Bitwarden, Vault, Homepage, Guacamole
│   └── otel-collector/           # OpenTelemetry Collector config
│
├── libs/                         # Nx Libraries (Shared Code)
│   ├── shared-types/             # Pydantic & TS interfaces for shared configs
│   ├── kube-utils/               # Kubernetes helper functions
│   └── ci-scripts/               # Reusable Bash/TS scripts for CI
│
├── tools/                        # Nx Tooling & Custom Generators
│   ├── nx-plugins/               # Custom Nx executors & generators
│   └── generators/               # Schematic templates (e.g., new Helm chart)
│
├── .make_assets/                 # Make orchestration helpers
│   ├── shared-python-app/        # Python app generator templates
│   ├── shared-python-lib/        # Python lib generator templates
│   └── .pre-commit-config.yaml   # Git hooks configuration
│
├── backups/                      # Velero, Vault snapshots, DB dump jobs
├── docker/                       # Harbor & local dev stack values
├── scripts/                      # Setup automation scripts
├── Makefile                      # Main orchestration (⭐ start here!)
├── nx.json                       # Nx workspace config
├── package.json                  # Node.js + Nx dependencies
├── pyproject.toml               # Python dev dependencies (uv managed)
└── README.md                     # ← you are here!
```

---

## 🔧 Prerequisites

* **Windows 11 Pro** with WSL2 (Ubuntu)
* **Python 3.12.1** (managed via pyenv)
* **Node.js ≥ 16** + **pnpm**
* **uv** (Python package manager)
* **Pulumi CLI** & **Ansible**
* **Docker** (for local dev & Harbor)
* **kubectl** & **Helm**
* **Tailscale** & **Cloudflare** account + tunnel credentials

---

## ⚙️ Usage

### 🚀 Initial Setup

```bash
# Run this once to set up the entire development environment
make setup
```

This will:
- Initialize Nx workspace with pnpm
- Set up Python environment with pyenv + uv
- Install custom Python generators
- Configure pre-commit hooks

### 🏗️ Generate New Projects

```bash
# Create a new Python application
make app NAME=my-fastapi-service

# Create a new Python library
make lib NAME=my-shared-utils
```

### 🔧 Daily Development Workflow

```bash
# Lint all affected projects
make lint

# Type-check all affected projects
make typecheck

# Run tests for affected projects
make test

# Build all affected projects
make build

# Serve a specific application
make serve PROJECT=my-react-app
```

### 🏗️ Infrastructure Management

```bash
# Plan infrastructure changes
make infra-plan TARGET=vpc

# Apply infrastructure changes
make infra-apply TARGET=control-plane

# Run Ansible playbooks
make ansible-run PLAYBOOK=bootstrap-wsl2 HOSTS=production
```

### 🐳 Containerization

```bash
# Build Docker image for any project
make containerize PROJECT=my-fastapi-service
```

### 📊 Monitoring & Visualization

```bash
# Open Nx dependency graph
make graph

# Access dashboards:
# - Grafana → https://grafana.home.local
# - Jaeger → https://jaeger.home.local
# - Traefik → https://traefik.home.local
```

### 🛠️ Utilities

```bash
# Get help with all available commands
make help

# Clean build artifacts and caches (use with caution!)
make clean
```

---

## 🛡️ Security & Secrets

* **Vault**: central secret store (auto‑unseal via Tailscale)
* **Bitwarden**: user‑facing credentials & 2FA
* **Ansible Vault**: encrypt playbook variables via [.make_assets/.pre-commit-config.yaml](.make_assets/.pre-commit-config.yaml)
* **Harbor**: private container registry with RBAC & image signing

---

## 💾 Backups & DR

* **Velero**: Kubernetes cluster snapshots → S3-compatible storage
* **Vault snapshots**: hourly → object storage
* **DB dumps** (Postgres, InfluxDB, Loki, Prometheus): cronjobs → object storage
* **Test restores** monthly in staging environment 🔄

---

## 🛠️ CI/CD & GitOps

* **GitHub Actions** ([.github/workflows/ci.yml](.github/workflows/ci.yml)) + **Nx Cloud** for building, testing, and publishing container images
* **ArgoCD Image Updater** for automatic image promotion
* **Pulumi** GitHub checks for infra drift detection
* **Pre‑commit** hooks ([.make_assets/.pre-commit-config.yaml](.make_assets/.pre-commit-config.yaml)): lint, security scans, type checking, testing

---

## 🏢 Business Requirements & Compliance

### Access & Authentication
* **User Roles**: Admins (full access), Developers (deploy rights), Viewers (Grafana-only)
* **Auth Mechanisms**: SSO via Authelia + 2FA, Vault tokens & policies, Tailscale ACLs

### Security & Compliance Rules
* **🔒 Encryption at rest** for all backups and Vault data
* **📝 Immutable commits**: infrastructure changes only via PR & ArgoCD sync
* **📦 Backup retention**: Velero ≥ 30 days, Vault snapshots ≥ 7 days
* **⚡ SLA**: 99.9% uptime for control‑plane services
* **🔐 Zero hardcoded secrets**: all credentials in Vault only

### Implementation Priorities
| Priority   | Feature                                        |
| ---------- | ---------------------------------------------- |
| **High**   | K3s control plane + Traefik ingress + Vault    |
| **High**   | Pulumi & Ansible bootstrap + ArgoCD GitOps     |
| **High**   | Observability stack (OTEL → Grafana/Prom/Loki) |
| **Medium** | Harbor registry + CI automation                |
| **Medium** | Backup/DR jobs (Velero, DB dumps)              |
| **Medium** | Guacamole & Homepage captive portal            |

---

## 🔧 Build System Details

This project uses a **hybrid build approach** optimized for homelab infrastructure and development:

### Core Components
- **Make** ([Makefile](Makefile)) - Main orchestration and workflow commands for all operations
- **Nx + pnpm** ([package.json](package.json), [pnpm-lock.yaml](pnpm-lock.yaml)) - JavaScript/TypeScript project management and monorepo structure
- **uv** ([pyproject.toml](pyproject.toml)) - Fast Python dependency management and virtual environments
- **Custom Nx Generators** ([.make_assets/shared-python-app/](.make_assets/shared-python-app/), [.make_assets/shared-python-lib/](.make_assets/shared-python-lib/)) - Python project scaffolding with modern tooling

### Development Toolchain
- **Python 3.12.1** via pyenv for version consistency
- **ruff** for fast linting and code formatting
- **mypy** for static type checking
- **pytest** for comprehensive testing
- **pre-commit hooks** for automated quality gates

### Infrastructure Integration
The build system seamlessly integrates with infrastructure deployment:
- `make setup` → Environment initialization
- `make app/lib NAME=...` → Rapid project generation
- `make lint/typecheck/test` → Quality assurance
- `make infra-plan/apply TARGET=...` → Infrastructure deployment
- `make ansible-run PLAYBOOK=...` → Configuration management
- `make containerize PROJECT=...` → Service deployment

Key files:
- [scripts/setup.py](scripts/setup.py) - Automated environment setup
- [.make_assets/.pre-commit-config.yaml](.make_assets/.pre-commit-config.yaml) - Git hooks configuration
- [.make_assets/setup_helper.sh](.make_assets/setup_helper.sh) - Custom generator installation

---

## 🤝 Contributing

1. 🌱 **Fork** the repo
2. ✏️ Create a **feature branch** (`git checkout -b feat/new-service`)
3. ✅ **Lint & test** (`make lint && make test`)
4. 🔄 **Push** and open a **PR**
5. 🎉 **Celebrate** once merged!

Pre-commit hooks will automatically run:
- Code formatting (ruff)
- Type checking (mypy)
- Linting (ruff, Nx affected)
- Testing (pytest, Nx affected)

---

## 📄 License

© 2025 SPRIME01 • [MIT License](./LICENSE)

---

🚀 **Happy homelabbing!** 🚀
````
---

🚀 **Happy homelabbing!** 🚀
````
