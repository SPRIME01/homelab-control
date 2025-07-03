import pytest
from unittest.mock import patch, mock_open
import os
import sys
import subprocess # Import subprocess

# Add the scripts directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from setup import run_command, init_nx, init_python_env, install_custom_py_generator, install_pre_commit

@patch('subprocess.run')
def test_run_command_success(mock_run):
    mock_run.return_value = subprocess.CompletedProcess(args=['echo', 'hello'], returncode=0)
    mock_run.return_value.stdout = "Success"
    mock_run.return_value.stderr = ""
    result = run_command(["echo", "hello"], "Test command")
    mock_run.assert_called_once_with(["echo", "hello"], check=True, capture_output=False, text=True)
    assert result.stdout == "Success"

@patch('subprocess.run')
def test_run_command_failure(mock_run):
    mock_run.side_effect = subprocess.CalledProcessError(1, ["bad", "command"])
    mock_run.side_effect.stdout = ""
    mock_run.side_effect.stderr = "Error"
    with pytest.raises(SystemExit):
        run_command(["bad", "command"], "Test command failure")
    mock_run.assert_called_once_with(["bad", "command"], check=True, capture_output=False, text=True)

@patch('os.path.exists', return_value=False)
@patch('subprocess.run')
def test_init_nx_new_workspace(mock_run, mock_exists):
    init_nx("1.0.0")
    assert mock_run.call_count == 2
    mock_run.call_args_list[0].assert_called_with(
        ["npx", "create-nx-workspace@latest", ".", "--nxCloud=skip", "--preset=react-standalone", "--pm=pnpm"],
        check=True, capture_output=False, text=True
    )
    mock_run.call_args_list[1].assert_called_with(
        ["pnpm", "add", "-D", "@nxlv/python@1.0.0"],
        check=True, capture_output=False, text=True
    )

@patch('os.path.exists', return_value=True)
@patch('subprocess.run')
def test_init_nx_existing_workspace(mock_run, mock_exists):
    init_nx("1.0.0")
    mock_run.assert_not_called()

@patch('subprocess.run')
@patch('os.path.exists', return_value=True)
@patch('builtins.open', new_callable=mock_open)
def test_init_python_env(mock_open_file, mock_exists, mock_run):
    # Mock pyenv --version and uv --version to indicate they are installed
    mock_run.side_effect = [
        subprocess.CompletedProcess(args=['pyenv', '--version'], returncode=0, stdout='pyenv 1.2.3', stderr=''),
        subprocess.CompletedProcess(args=['pyenv', 'install', '3.9.5'], returncode=0, stdout='', stderr=''),
        subprocess.CompletedProcess(args=['pyenv', 'local', '3.9.5'], returncode=0, stdout='', stderr=''),
        subprocess.CompletedProcess(args=['uv', '--version'], returncode=0, stdout='uv 0.1.0', stderr='')
    ]

    init_python_env("3.9.5", False, "/path/to/pyproject.toml", "/path/to/monorepo")

    assert mock_run.call_count == 4
    mock_open_file.assert_called_once_with("/path/to/pyproject.toml", "w")
    handle = mock_open_file()
    handle.write.assert_called_once()
    assert "name = \"monorepo-dev-env\"" in handle.write.call_args[0][0]

@patch('subprocess.run')
@patch('os.path.exists', return_value=False)
@patch('builtins.open', new_callable=mock_open)
def test_init_python_env_install_uv(mock_open_file, mock_exists, mock_run):
    # Mock pyenv --version and uv --version to indicate uv is NOT installed
    error_uv_not_found = subprocess.CalledProcessError(1, ['uv', '--version'])
    error_uv_not_found.stdout = ""
    error_uv_not_found.stderr = "uv not found"

    mock_run.side_effect = [
        subprocess.CompletedProcess(args=['pyenv', '--version'], returncode=0, stdout='pyenv 1.2.3', stderr=''),
        subprocess.CompletedProcess(args=['pyenv', 'install', '3.9.5'], returncode=0, stdout='', stderr=''),
        subprocess.CompletedProcess(args=['pyenv', 'local', '3.9.5'], returncode=0, stdout='', stderr=''),
        error_uv_not_found,
        subprocess.CompletedProcess(args=['pip', 'install', 'uv'], returncode=0, stdout='', stderr='')
    ]

    init_python_env("3.9.5", False, "/path/to/pyproject.toml", "/path/to/monorepo")

    assert mock_run.call_count == 5
    mock_run.call_args_list[4].assert_called_with(
        [os.path.join("/path/to/monorepo", ".venv", "bin", "pip"), 'install', 'uv'],
        check=True, capture_output=False, text=True
    )

@patch('subprocess.run')
def test_install_custom_py_generator(mock_run):
    install_custom_py_generator("my-generator")
    mock_run.assert_not_called() # No actual commands are run for this placeholder function

@patch('subprocess.run')
def test_install_pre_commit(mock_run):
    # Mock pre-commit --version to indicate it's not installed
    error_pre_commit_not_found = subprocess.CalledProcessError(1, ['pre-commit', '--version'])
    error_pre_commit_not_found.stdout = ""
    error_pre_commit_not_found.stderr = "pre-commit not found"

    mock_run.side_effect = [
        error_pre_commit_not_found,
        subprocess.CompletedProcess(args=['pip', 'install', 'pre-commit'], returncode=0, stdout='', stderr=''),
        subprocess.CompletedProcess(args=['pre-commit', 'install', '--config', '.make_assets/.pre-commit-config.yaml'], returncode=0, stdout='', stderr='')
    ]

    install_pre_commit()
    assert mock_run.call_count == 3
    mock_run.call_args_list[1].assert_called_with(
        [sys.executable, "-m", "pip", "install", "pre-commit"],
        check=True, capture_output=False, text=True
    )
    mock_run.call_args_list[2].assert_called_with(
        ['pre-commit', 'install', '--config', '.make_assets/.pre-commit-config.yaml'],
        check=True, capture_output=False, text=True
    )
