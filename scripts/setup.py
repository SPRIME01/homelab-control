import subprocess
import os
import sys
import shutil
import argparse

def run_command(command: list[str], description: str = "", check: bool = True, capture_output: bool = False):
    """Runs a shell command and prints its output. Raises an exception if the command fails."""
    print(f"Executing: {description} {' '.join(command)}")
    try:
        result = subprocess.run(command, check=check, capture_output=capture_output, text=True)
        if capture_output:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        if e.stdout:
            print(f"Stdout: {e.stdout}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Command not found. Please ensure '{command[0]}' is installed and in your PATH.")
        sys.exit(1)

def init_nx(nx_python_plugin_version: str):
    print("🏗️ Initializing Nx workspace with pnpm...")
    if not os.path.exists("pnpm-lock.yaml"):
        run_command(["npx", "create-nx-workspace@latest", ".", "--nxCloud=skip", "--preset=react-standalone", "--pm=pnpm"],
                    "Running npx create-nx-workspace...")
        run_command(["pnpm", "add", "-D", f"@nxlv/python@{nx_python_plugin_version}"],
                    "Adding @nxlv/python plugin...")
    else:
        print("Nx workspace already initialized. Skipping.")
    print("✅ Nx workspace ready.")

def init_python_env(python_version: str, rust_toolchain_uv_install: bool, root_pyproject_toml: str, monorepo_root: str):
    print("🐍 Setting up Python environment with pyenv and uv...")

    # Check for pyenv
    try:
        run_command(["pyenv", "--version"], "Checking pyenv installation...", check=True)
    except SystemExit: # run_command exits if pyenv is not found
        print("pyenv not found. Please install pyenv first: https://github.com/pyenv/pyenv#installation")
        sys.exit(1)

    # Install Python version
    print(f"Installing Python {python_version}...")
    run_command(["pyenv", "install", python_version], check=False) # pyenv install returns 0 even if already installed

    # Set local Python version
    print(f"Setting local Python version to {python_version}...")
    run_command(["pyenv", "local", python_version])

    # Check for uv installation
    print("Checking for uv installation...")
    try:
        run_command(["uv", "--version"], "Checking uv installation...", check=True)
        print("uv already installed. Skipping.")
    except SystemExit: # run_command exits if uv is not found
        if rust_toolchain_uv_install:
            print("Installing uv via cargo (Rust toolchain required)...")
            run_command(["cargo", "install", "uv"])
        else:
            print("Installing uv via pip...")
            run_command([os.path.join(monorepo_root, ".venv", "bin", "pip"), "install", "uv"]) # Use venv pip

    # Create/update root pyproject.toml
    print("Creating/updating root pyproject.toml...")
    pyproject_content = f"""
[project]
name = "monorepo-dev-env"
version = "0.0.1"

[project.optional-dependencies]
dev = [
    "ruff",
    "mypy",
    "pytest",
    "uv"
]

[build-system]
requires = ["uv>=0.1.0"]
build-backend = "setuptools.build_meta"
"""
    with open(root_pyproject_toml, "w") as f:
        f.write(pyproject_content)
    print("✅ Python environment setup complete.")

def install_custom_py_generator(custom_py_gen_plugin_name: str):
    print("📦 Installing custom Python generator plugin...")
    print("Custom Python generator installation skipped (assuming Nx handles it).")
    print("✅ Custom Python generator plugin ready.")

def install_pre_commit():
    print("🎣 Installing pre-commit hooks...")
    try:
        run_command(["pre-commit", "--version"], "Checking pre-commit installation...", check=True)
    except SystemExit:
        print("pre-commit not found. Installing...")
        run_command([sys.executable, "-m", "pip", "install", "pre-commit"]) # Use current python's pip

    run_command(["pre-commit", "install", "--config", ".make_assets/.pre-commit-config.yaml"])
    print("✅ Pre-commit hooks installed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monorepo setup script.")
    parser.add_argument("action", help="Action to perform (e.g., init_nx, init_python_env, install_pre_commit)")
    parser.add_argument("--python-version", default="3.11.9", help="Python version to install via pyenv.")
    parser.add_argument("--nx-python-plugin-version", default="21.0.3", help="Version of @nxlv/python Nx plugin.")
    parser.add_argument("--rust-toolchain-uv-install", action="store_true", help="Install uv via rustup/cargo.")
    parser.add_argument("--root-pyproject-toml", default=os.path.join(os.getcwd(), "pyproject.toml"),
                        help="Path to the root pyproject.toml file.")
    parser.add_argument("--monorepo-root", default=os.getcwd(), help="Path to the monorepo root directory.")
    parser.add_argument("--custom-py-gen-plugin-name", default="shared-python-tools",
                        help="Name of the custom Python generator plugin.")

    args = parser.parse_args()

    if args.action == "init_nx":
        init_nx(args.nx_python_plugin_version)
    elif args.action == "init_python_env":
        init_python_env(args.python_version, args.rust_toolchain_uv_install, args.root_pyproject_toml, args.monorepo_root)
    elif args.action == "install_custom_py_generator":
        install_custom_py_generator(args.custom_py_gen_plugin_name)
    elif args.action == "install_pre_commit":
        install_pre_commit()
    else:
        print(f"Unknown action: {args.action}")
        parser.print_help()
        exit(1)