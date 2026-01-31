"""Tests for platform adapter base interface."""

import pytest
from pathlib import Path

from sdp.adapters.base import (
    PlatformAdapter,
    PlatformType,
    detect_platform,
)


class TestPlatformType:
    """Test PlatformType enum."""

    def test_platform_types_exist(self) -> None:
        """Verify all expected platform types are defined."""
        assert PlatformType.CLAUDE_CODE.value == "claude_code"
        assert PlatformType.CODEX.value == "codex"
        assert PlatformType.OPENCODE.value == "opencode"


class TestPlatformAdapter:
    """Test PlatformAdapter abstract interface."""

    def test_adapter_has_required_methods(self) -> None:
        """Verify all adapters implement required interface."""
        from sdp.adapters.claude_code import ClaudeCodeAdapter
        from sdp.adapters.opencode import OpenCodeAdapter

        required_methods = ["install", "configure_hooks", "load_skill", "get_settings"]

        for adapter_class in [ClaudeCodeAdapter, OpenCodeAdapter]:
            for method in required_methods:
                assert hasattr(adapter_class, method)

    def test_platform_adapter_is_abstract(self) -> None:
        """Verify PlatformAdapter cannot be instantiated directly."""
        with pytest.raises(TypeError):
            PlatformAdapter()


class TestDetectPlatform:
    """Test platform detection."""

    def test_detect_claude_code(self, tmp_path: Path) -> None:
        """Verify Claude Code detected when .claude/settings.json exists."""
        (tmp_path / ".claude").mkdir()
        (tmp_path / ".claude" / "settings.json").write_text("{}")

        result = detect_platform(tmp_path)

        assert result == PlatformType.CLAUDE_CODE

    def test_detect_opencode(self, tmp_path: Path) -> None:
        """Verify OpenCode detected when .opencode/opencode.json exists."""
        (tmp_path / ".opencode").mkdir()
        (tmp_path / ".opencode" / "opencode.json").write_text("{}")

        result = detect_platform(tmp_path)

        assert result == PlatformType.OPENCODE

    def test_detect_codex_config_yaml(self, tmp_path: Path) -> None:
        """Verify Codex detected when .codex/config.yaml exists."""
        (tmp_path / ".codex").mkdir()
        (tmp_path / ".codex" / "config.yaml").write_text("")

        result = detect_platform(tmp_path)

        assert result == PlatformType.CODEX

    def test_detect_codex_install_md(self, tmp_path: Path) -> None:
        """Verify Codex detected when .codex/INSTALL.md exists."""
        (tmp_path / ".codex").mkdir()
        (tmp_path / ".codex" / "INSTALL.md").write_text("")

        result = detect_platform(tmp_path)

        assert result == PlatformType.CODEX

    def test_detect_none_when_no_platform(self, tmp_path: Path) -> None:
        """Verify None when no platform directory exists."""
        result = detect_platform(tmp_path)

        assert result is None
