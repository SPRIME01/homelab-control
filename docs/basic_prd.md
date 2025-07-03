# HomeStation control‐plane

## WHY – Vision & Purpose

### What problem are we solving and for whom?

*   **Problem:** Disparate self‑hosted services, secrets, CI/CD, and observability scattered across devices and the cloud.
*   **Target users:**

    *   **Home Lab Enthusiasts** who need a single pane to manage edge AI nodes, IoT, and home automation.
    *   **Small DevOps Teams** experimenting with distributed compute, secure remote access, and GitOps.

### What does HomeStation do?

*   Provides a **central control plane** that:

    1. **Provisions** and **updates** infrastructure (WSL2 host, K3s control, Jetsons) via Pulumi & Ansible.
    2. **Exposes** services (ArgoCD, Authelia, Vault, Guacamole, Homepage) behind Traefik + Cloudflare Tunnels.
    3. **Orchestrates** self‑healing, backups, and GitOps deployments.
    4. **Unifies** logging, metrics, tracing with an OpenTelemetry–Grafana stack.
    5. **Secures** everything with centralized SSO/MFA, secrets vaulting, and network‑wide ACLs.

### Who will use it?

* **Primary personas:**

    * 🧑‍💻 **Edge AI Engineer**: deploys MLOps workloads on Jetsons; needs seamless CI/CD and secrets.
    * 🏠 **Smart‑Home Admin**: configures HomeAssistant integrations, MQTT topics, device access.
    * 🔐 **Security‑Focused Hobbyist**: demands MFA, Vault‑backed secrets, encrypted tunnels.
    * 🚀 **DevOps Learner**: experiments with Pulumi, ArgoCD, NX, and wants a turnkey homelab.

### Why will they use it instead of alternatives?

* **Uniquely** integrates edge AI and homelab under one GitOps umbrella.
* **All‑in‑one**: infra, secrets, ingress, observability, remote‑desktop, captive‑portal.
* **Loosely coupled & modular**: swap out any component (e.g., replace Home Assistant with Node‑RED).
* **Self‑healing** and **auto‑documentation** reduce maintenance overhead.

---

## WHAT – Core Requirements

### What must HomeStation do?

*   **System must** provision and configure K3s control in WSL2 on Windows 11.
*   **System must** deploy and manage Traefik, Authelia, Bitwarden, Vault, ArgoCD, Guacamole, Homepage.
*   **System must** integrate with Cloudflare Tunnels and Tailscale for secure remote access.
*   **Systems must** collect logs, metrics, traces via OpenTelemetry → Loki, Prometheus, InfluxDB, Jaeger, Grafana.
*   **System must** schedule regular backups (Velero, Vault snapshots, DB dumps) to S3‑compatible storage.
*   **Users must be able to** add a new containerized service via Helm and have it auto‑deployed by ArgoCD.

### What actions need to happen?

1. **Bootstrap**: `make setup` initializes development environment; Ansible configures host; Pulumi spins up K3s + Vault + tunnels.
2. **Develop**: `make app/lib NAME=...` generates projects; daily workflow uses `make lint/typecheck/test/build`.
3. **Deploy apps**: ArgoCD syncs Helm charts for all control‑plane services.
4. **Monitor**: OTEL Collector ingests data; Grafana dashboards surface health.
5. **Backup**: Velero and cronjobs snapshot state; object storage ingestion.
6. **Scale**: Add new K3s actors (Jetsons) via Tailscale; auto‐join cluster.
7. **Maintain secrets**: Vault Agent injects dynamic creds; Ansible Vault for playbooks.
8. **Quality assurance**: Pre‑commit hooks validate all changes before commits.

### What should the outcomes be?

* **Reliable up‑time**: Services recover within 2 minutes of failure.
* **Unified view**: Single dashboard for infra health, logs, metrics, and traces.
* **Rapid provisioning**: New services go live < 5 minutes after commit.
* **Secure posture**: All external access MFA‑protected; secrets never hard‑coded.

---

## HOW – Planning & Implementation

### What are the required stack components?

*   **Infrastructure:** Windows 11 WSL2, Docker, K3s (control), Tailscale mesh, Cloudflare Tunnel.
*   **Provisioning:** Pulumi (TypeScript), Ansible (Ubuntu roles).
*   **Development Environment:** Python 3.12.1 (pyenv), uv package manager, ruff linter/formatter, mypy type checker, pytest testing, Nx workspace, pnpm, custom Python generators, Make orchestration, pre-commit hooks.
*   **CI/CD & GitOps:** Nx monorepo, GitHub Actions, ArgoCD, Harbor registry.
*   **Ingress & Security:** Traefik, Cert‑Manager (Vault issuer), Authelia, Bitwarden, Vault Raft.
*   **Observability:** OpenTelemetry Collector, Prometheus, Loki, InfluxDB, Jaeger, Grafana.
*   **Backup/DR:** Velero+Restic, Vault snapshots, DB cronjobs → S3‑compatible.
*   **Integrations:** Home Assistant (MQTT), OpenWRT router (MQTT), Guacamole, Homepage captive portal.

### What are the system requirements?

*   **Performance:**

    *   Control node: 32 GB RAM, SSD, 4‑core CPU.
    *   Jetsons: GPU‑accelerated inference, K3s actor connectivity via Tailscale.
*   **Security:**

    *   TLS everywhere, Vault‑driven secrets, SSO/MFA, network ACLs.
    *   Cloudflare Tunnel termination, no open inbound ports.
*   **Scalability:**

    *   Add/remove K3s actors dynamically.
    *   Harbor for image snapshots; ArgoCD multi‑cluster.
*   **Reliability:**

    *   99.9% service availability; self‑healing pods and automatic rollbacks.
*   **Integration constraints:**

    *   WSL2 network quirks (use host‑network for K3s).
    *   Tailscale handles inter‑device mesh.
    *   Ansible Vault for playbook variables.

### What are the key user flows?

1. **First‑time setup**

    *   Clone Nx repo → `make setup` → `make infra-apply TARGET=control-plane` → Cloudflare Tunnel live.
2. **Adding a new service**

    *   `make app NAME=my‑service` → write Helm chart → push to Git → ArgoCD auto‑deploy.
3. **Adding a new library**

    *   `make lib NAME=shared‑utils` → implement functionality → `make test` → publish for reuse.
4. **Daily development workflow**

    *   `make lint` → `make typecheck` → `make test` → `make build` → commit with pre‑commit hooks.
5. **Edge node onboarding**

    *   On Jetson: `tailscale up` → auto‑join cluster → ZenML pipelines appear in control Grafana.
6. **Infrastructure changes**

    *   `make infra-plan TARGET=vpc` → review → `make infra-apply TARGET=vpc` → ArgoCD sync.
7. **Configuration management**

    *   `make ansible-run PLAYBOOK=bootstrap-wsl2` → host configuration applied.
8. **Viewing observability**

    *   Open Grafana (metrics), Loki (logs), Jaeger (traces) via Homepage portal.
9. **Secrets rotation**

    *   Vault rotation cron → apps automatically pick up new creds via Vault Agent.
10. **Containerization**

    *   `make containerize PROJECT=my‑service` → Docker image built and pushed to Harbor.

### What are the core interfaces?

| Interface       | Purpose                         | Key Functionality                             |
| --------------- | ------------------------------- | --------------------------------------------- |
| **Homepage UI** | Entry portal for all dashboards | Links to Grafana, ArgoCD, Guacamole, Vault UI |
| **Traefik UI**  | Ingress rules & health          | Route creation, Let’s Encrypt cert status     |
| **ArgoCD UI**   | GitOps app management           | Sync status, rollbacks, diff view             |
| **Grafana**     | Metrics dashboards & alerts     | Pre‑built homelab + AI dashboards             |
| **Guacamole**   | RDP/SSH browser access          | Connect to WSL2, Jetsons, other VMs           |
| **Vault UI**    | Secrets management              | Policy creation, secret viewer, audit logs    |

---

## BUSINESS REQUIREMENTS

### What are HomeStation's access and authentication needs?

* **User types:**

    * **Admins** (full access via Authelia+Vault policies)
    * **Developers** (deploy rights to dev namespaces)
    * **Viewers** (Grafana‑only access)
* **Auth mechanisms:**

    * SSO via Authelia (LDAP or OIDC backend) + 2FA
    * Vault tokens & policies per role
    * Tailscale ACLs for network segmentation

### What business rules must be followed?

* **Encryption at rest** for all backups and Vault data.
* **Immutable commits**: infra changes only via PR & ArgoCD sync.
* **Backup retention**:

    * Velero snapshots ≥ 30 days
    * Vault snapshots ≥ 7 days
* **SLA:** 99.9% uptime for control‑plane services.
* **Compliance:** No hard‑coded credentials; secrets in Vault only.

### What are HomeStation's implementation priorities?

| Priority   | Feature                                        |
| ---------- | ---------------------------------------------- |
| **High**   | K3s control plane + Traefik ingress + Vault    |
| **High**   | Pulumi & Ansible bootstrap + ArgoCD GitOps     |
| **High**   | Observability stack (OTEL → Grafana/Prom/Loki) |
| **Medium** | Harbor registry + CI automation                |
| **Medium** | Backup/DR jobs (Velero, DB dumps)              |
| **Medium** | Guacamole & Homepage captive portal            |
| **Low**    | Advanced RLHF feedback integration             |
| **Low**    | Auto‑documentation generator                   |
