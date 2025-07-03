````markdown
# 🏠 Home Station Control

> A unified Nx monorepo to provision, deploy, and manage your entire homelab control plane—secure, self‑healing, and GitOps‑driven! 🚀

---

## 📖 Table of Contents

1. [✨ Features](#-features)
2. [🚀 Quickstart](#-quickstart)
3. [🏗️ Architecture](#️-architecture)
4. [📂 Repo Layout](#-repo-layout)
5. [🔧 Prerequisites](#-prerequisites)
6. [⚙️ Usage](#️-usage)
7. [🛡️ Security & Secrets](#️-security--secrets)
8. [💾 Backups & DR](#-backups--dr)
9. [🛠️ CI/CD & GitOps](#️-cicd--gitops)
10. [🤝 Contributing](#-contributing)
11. [📄 License](#-license)

---

## ✨ Features

- **🏗️ Infrastructure as Code** with Pulumi (TypeScript) + Ansible
- **🛡️ Secure Ingress** via Traefik + Cloudflare Tunnels
- **🔐 Central Auth**: Authelia SSO + Bitwarden + HashiCorp Vault
- **📊 Observability**: OpenTelemetry → InfluxDB, Prometheus, Loki, Jaeger, Grafana
- **🚁 GitOps CD** powered by ArgoCD
- **🔄 Self‑healing & Backups** with Velero, Vault snapshots, DB dumps
- **🧩 Modular Nx Monorepo**: generate, test, and deploy any service with Nx CLI

---

## 🚀 Quickstart

```bash
# 1. Clone repo
git clone https://github.com/your-org/home_station_infra_kit.git
cd home_station_infra_kit

# 2. Install dependencies
npm install
pip install -r apps/ansible-playbooks/requirements.txt

# 3. Bootstrap WSL2 host
nx run ansible-playbooks:bootstrap

# 4. Deploy control plane
nx run pulumi-control:deploy

# 5. Sync GitOps apps
nx run argocd-helm-charts:deploy

# 6. Verify services in Traefik dashboard → https://traefik.home.local
````

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
├── apps/
│   ├── pulumi-control/           # Pulumi TS infra (K3s, Traefik, Vault, Cloudflare)
│   ├── pulumi-jetson/            # Pulumi for Jetson cluster provisioning
│   ├── ansible-playbooks/        # WSL2 host bootstrap & config
│   ├── argocd-helm-charts/       # Helm charts for Authelia, Bitwarden, Vault, Homepage, Guacamole
│   ├── otel-collector/           # OpenTelemetry Collector config
│   └── fastapi-services/         # Any custom APIs (e.g., feedback, telemetry)
│
├── libs/
│   ├── shared-types/             # Pydantic & TS interfaces for shared configs
│   ├── kube-utils/               # Kubernetes helper functions
│   └── ci-scripts/               # Reusable Bash/TS scripts for CI
│
├── tools/
│   ├── nx-plugins/               # Custom Nx executors & generators
│   └── generators/               # Schematic templates (e.g., new Helm chart)
│
├── backups/                      # Velero, Vault snapshots, DB dump jobs
├── docker/                       # Harbor & local dev stack values
├── nx.json                       # Nx workspace config
├── workspace.json                # Nx projects config
├── package.json                  # Nx & dev dependencies
└── README.md                     # ← you are here!
```

---

## 🔧 Prerequisites

* **Windows 11 Pro** with WSL2 (Ubuntu)
* **Node.js ≥ 16**, **npm**
* **Pulumi CLI** & **Ansible**
* **Docker** (for local dev & Harbor)
* **kubectl** & **Helm**
* **Tailscale** & **Cloudflare** account + tunnel credentials

---

## ⚙️ Usage

1. **Generate new app or lib**

   ```bash
   nx g @nrwl/workspace:library shared-new-thing --directory=libs
   ```
2. **Deploy infra**

   ```bash
   nx run pulumi-control:deploy
   ```
3. **Apply Ansible playbooks**

   ```bash
   nx run ansible-playbooks:bootstrap
   ```
4. **Sync GitOps**

   ```bash
   nx run argocd-helm-charts:deploy
   ```
5. **Monitor & dashboards**

   * Grafana → `https://grafana.home.local`
   * Jaeger → `https://jaeger.home.local`

---

## 🛡️ Security & Secrets

* **Vault**: central secret store (auto‑unseal via Tailscale)
* **Bitwarden**: user‑facing credentials & 2FA
* **Ansible Vault**: encrypt playbook variables
* **Harbor**: private container registry with RBAC & image signing

---

## 💾 Backups & DR

* **Velero**: Kubernetes cluster snapshots → S3-compatible storage
* **Vault snapshots**: hourly → object storage
* **DB dumps** (Postgres, InfluxDB, Loki, Prometheus): cronjobs → object storage
* **Test restores** monthly in staging environment 🔄

---

## 🛠️ CI/CD & GitOps

* **GitHub Actions** + **Nx Cloud** for building, testing, and publishing container images to Harbor
* **ArgoCD Image Updater** for automatic image promotion
* **Pulumi** GitHub checks for infra drift detection
* **Pre‑commit** hooks (Lint, security scans, fmt)

---

## 🤝 Contributing

1. 🌱 **Fork** the repo
2. ✏️ Create a **feature branch** (`git checkout -b feat/new-service`)
3. ✅ **Lint & test** (`nx affected:test`)
4. 🔄 **Push** and open a **PR**
5. 🎉 **Celebrate** once merged!

---

## 📄 License

© 2025 Your Name or Organization • [MIT License](./LICENSE)

---

🚀 **Happy homelabbing!** 🚀

```
```
