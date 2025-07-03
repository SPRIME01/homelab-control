# ==============================================================================
# Makefile: Monorepo Orchestration for AI-Native Projects
# Built for a streamlined, one-person dev workflow.
# Uses pyenv, uv, ruff, mypy, pytest, pnpm, and Nx.
# ==============================================================================

.PHONY: help setup init-python-env generate-python-app generate-python-lib \
        install-pre-commit lint typecheck test build serve graph deploy-k8s-dev \
        containerize clean

# ==============================================================================
# Configuration Variables - Adjust as needed
# ==============================================================================
PYTHON_VERSION ?= 3.11.9
NX_PYTHON_PLUGIN_VERSION ?= 21.0.3 # Updated to latest stable for @nxlv/python
RUST_TOOLCHAIN_UV_INSTALL ?= false # Set to true to install uv via rustup for a self-contained install
# Add your custom Nx generator details
CUSTOM_PY_GEN_PLUGIN_NAME ?= shared-python-tools
CUSTOM_PY_APP_GENERATOR ?= $(CUSTOM_PY_GEN_PLUGIN_NAME):shared-python-app
CUSTOM_PY_LIB_GENERATOR ?= $(CUSTOM_PY_GEN_PLUGIN_NAME):shared-python-lib

# Root paths (relative to Makefile)
MONOREPO_ROOT := $(CURDIR)
PYTHON_VENV_PATH := $(MONOREPO_ROOT)/.venv
ROOT_PYPROJECT_TOML := $(MONOREPO_ROOT)/pyproject.toml

# ==============================================================================
# Help and Setup Targets
# ==============================================================================

help:
	@echo "=============================================================================="
	@echo "Nx Monorepo Management - Quick Start & Daily Workflow"
	@echo "=============================================================================="
	@echo "Usage:"
	@echo "  make setup                - Initial one-time setup of the monorepo."
	@echo "  make init-python-env      - Initializes/updates the root Python dev environment (.venv)."
	@echo ""
	@echo "  make app NAME=<name>      - Generates a new Python application (e.g., make app NAME=my-fastapi-service)"
	@echo "  make lib NAME=<name>      - Generates a new Python library (e.g., make lib NAME=my-shared-utils)"
	@echo ""
	@echo "  make install-pre-commit   - Installs git pre-commit hooks."
	@echo ""
	@echo "  make lint                 - Lints all affected projects (JS/TS, Python)."
	@echo "  make typecheck            - Type-checks all affected projects (JS/TS, Python)."
	@echo "  make test                 - Runs tests for all affected projects."
	@echo "  make build                - Builds all affected projects (JS/TS apps/libs)."
	@echo ""
	@echo "  make serve PROJECT=<name> - Serves a specific application (e.g., React frontend, Python API)."
	@echo "                              Example: make serve PROJECT=my-react-app"
	@echo "  make graph                - Opens the Nx dependency graph visualizer."
	@echo ""
	@echo "  make infra-plan TARGET=<name>  - Runs 'terraform plan' or similar for IaC project (e.g., TARGET=vpc)."
	@echo "  make infra-apply TARGET=<name> - Runs 'terraform apply' or similar for IaC project (e.g., TARGET=vpc)."
	@echo "  make ansible-run PLAYBOOK=<name> HOSTS=<hosts> - Runs an Ansible playbook."
	@echo ""
	@echo "  make containerize PROJECT=<name> - Builds a Docker image for a given project."
	@echo ""
	@echo "  make clean                - Cleans build artifacts and caches (use with caution)."
	@echo "=============================================================================="

setup: init-nx init-python-env install-custom-py-generator install-pre-commit
	@echo "🚀 Monorepo setup complete! Run 'make help' for available commands."

init-nx:
	@python scripts/setup.py init_nx --nx-python-plugin-version=$(NX_PYTHON_PLUGIN_VERSION)

init-python-env:
	@python scripts/setup.py init_python_env --python-version=$(PYTHON_VERSION) --rust-toolchain-uv-install=$(RUST_TOOLCHAIN_UV_INSTALL) --root-pyproject-toml=$(ROOT_PYPROJECT_TOML) --monorepo-root=$(MONOREPO_ROOT)

install-custom-py-generator:
	@bash ./.make_assets/setup_helper.sh install_custom_py_generator $(CUSTOM_PY_GEN_PLUGIN_NAME)

install-pre-commit:
	@python scripts/setup.py install_pre_commit


# ==============================================================================
# Project Generation Targets
# ==============================================================================

app:
	@sh -c 'if [ -z "$(NAME)" ]; then echo "Error: Please provide a project name. Usage: make app NAME=my-new-api"; exit 1; fi'
	@echo "✨ Generating Python application '$(NAME)' with custom settings..."
	pnpm nx generate $(CUSTOM_PY_APP_GENERATOR) $(NAME) --directory=apps
	@echo "Installing project-specific Python dependencies for $(NAME)..."
	pnpm nx run $(NAME):install-deps # Automatically install deps for the new app
	@echo "🎉 Python application '$(NAME)' generated and dependencies installed successfully."

lib:
	@sh -c 'if [ -z "$(NAME)" ]; then echo "Error: Please provide a project name. Usage: make lib NAME=my-shared-lib"; exit 1; fi'
	@echo "✨ Generating Python library '$(NAME)' with custom settings..."
	pnpm nx generate $(CUSTOM_PY_LIB_GENERATOR) $(NAME) --directory=libs
	@echo "Installing project-specific Python dependencies for $(NAME)..."
	pnpm nx run $(NAME):install-deps # Automatically install deps for the new lib
	@echo "🎉 Python library '$(NAME)' generated and dependencies installed successfully."

# ==============================================================================
# Daily Workflow Targets (Using Nx Affected)
# ==============================================================================

lint:
	@echo "🔎 Linting affected projects..."
	pnpm nx affected --target=lint --base=main --parallel=3

typecheck:
	@echo "🧐 Type-checking affected projects..."
	pnpm nx affected --target=typecheck --base=main --parallel=3

test:
	@echo "🧪 Running tests for affected projects..."
	pnpm nx affected --target=test --base=main --parallel=3

build:
	@echo "📦 Building affected projects..."
	pnpm nx affected --target=build --base=main --parallel=3

serve:
	@sh -c 'if [ -z "$(PROJECT)" ]; then echo "Error: Please provide a project name to serve. Usage: make serve PROJECT=my-react-app or make serve PROJECT=my-fastapi-service"; exit 1; fi'
	@echo "🚀 Serving '$(PROJECT)'..."
	pnpm nx serve $(PROJECT)

graph:
	@echo "📊 Opening Nx dependency graph..."
	pnpm nx graph

# ==============================================================================
# Infrastructure as Code (IaC) Targets
# ==============================================================================

# Generic target for Terraform, Pulumi, etc.
# Assumes you have an Nx project named 'infrastructure' that contains sub-directories
# for different environments/stacks (e.g., 'infrastructure/terraform/vpc')
# and a 'plan' or 'apply' target defined in its project.json.
# Example usage: make infra-plan TARGET=vpc
infra-plan:
	@sh -c 'if [ -z "$(TARGET)" ]; then echo "Error: Please specify the IaC target (e.g., 'vpc', 'kubernetes-cluster'). Usage: make infra-plan TARGET=vpc"; exit 1; fi'
	@echo "🗺️ Running IaC plan for '$(TARGET)'..."
	pnpm nx run infrastructure:plan-$(TARGET) # Assumes target name is plan-<TARGET>

infra-apply:
	@sh -c 'if [ -z "$(TARGET)" ]; then echo "Error: Please specify the IaC target. Usage: make infra-apply TARGET=vpc"; exit 1; fi'
	@echo "🚀 Applying IaC changes for '$(TARGET)'..."
	pnpm nx run infrastructure:apply-$(TARGET) # Assumes target name is apply-<TARGET>

# Specific target for Ansible
# Assumes an Nx project named 'ansible-playbooks' or similar, with targets
# configured for specific playbooks.
# Example usage: make ansible-run PLAYBOOK=deploy-web-servers HOSTS=production
ansible-run:
	@sh -c 'if [ -z "$(PLAYBOOK)" ]; then echo "Error: Please specify the Ansible playbook name. Usage: make ansible-run PLAYBOOK=deploy-web-servers"; exit 1; fi'
	@echo "⚙️ Running Ansible playbook '$(PLAYBOOK)' on hosts '$(HOSTS)'..."
	pnpm nx run ansible-playbooks:run-$(PLAYBOOK) --args="--inventory $(HOSTS)" # Assumes target name is run-<PLAYBOOK>

# ==============================================================================
# Containerization Targets (Microservices Transformation)
# ==============================================================================

# Assumes that each application project (e.g., apps/my-fastapi-service) has a Dockerfile
# in its root and a 'container' target defined in its project.json to build the image.
# This target is designed to make "transforming any monorepo into a microservice architecture
# without fuss at will" a reality at the build step.
containerize:
	@sh -c 'if [ -z "$(PROJECT)" ]; then echo "Error: Please specify the project to containerize. Usage: make containerize PROJECT=my-fastapi-service"; exit 1; fi'
	@echo "🐳 Building Docker image for '$(PROJECT)'..."
	pnpm nx run $(PROJECT):container # Assumes a 'container' target in project.json
	@echo "✅ Docker image for '$(PROJECT)' built successfully."

# ==============================================================================
# Cleanup (Use with Caution!)
# ==============================================================================
clean:
	@echo "🗑️ Cleaning Nx cache, node_modules, and Python environments..."
	pnpm nx reset
	rm -rf node_modules
	rm -rf .venv
	find . -name ".nx" -type d -exec rm -rf {} +
	find . -name "dist" -type d -exec rm -rf {} +
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name ".pytest_cache" -type d -exec rm -rf {} +
	@echo "Cleanup complete. You may need to run 'make setup' again."

.DEFAULT_GOAL := help
