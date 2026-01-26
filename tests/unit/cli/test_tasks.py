"""Tests for CLI task commands."""

from pathlib import Path

from click.testing import CliRunner

from sdp.cli import main


def test_task_enqueue_command(tmp_path: Path) -> None:
    """Test task enqueue command."""
    import os
    original_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        runner = CliRunner()
        result = runner.invoke(main, ["task", "enqueue", "00-012-01"])

        assert result.exit_code == 0
        assert "Enqueued: 00-012-01" in result.output
    finally:
        os.chdir(original_cwd)


def test_task_execute_dry_run() -> None:
    """Test task execute dry run."""
    runner = CliRunner()
    result = runner.invoke(main, ["task", "execute", "00-012-01", "--dry-run"])

    assert result.exit_code == 0
    assert "Would execute: 00-012-01" in result.output


def test_task_list_empty_queue(tmp_path: Path) -> None:
    """Test task list with empty queue."""
    import os
    original_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        runner = CliRunner()
        result = runner.invoke(main, ["task", "list"])

        assert result.exit_code == 0
        assert "No tasks in queue" in result.output
    finally:
        os.chdir(original_cwd)
