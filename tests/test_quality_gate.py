"""Tests for quality gate configuration and validation."""

import pytest
from pathlib import Path
from sdp.quality import QualityGateConfigLoader, QualityGateValidator
from sdp.quality.config import ConfigValidationError


def test_default_config_loading():
    """Test loading default configuration."""
    validator = QualityGateValidator()
    assert validator._config.coverage.minimum == 80
    assert validator._config.complexity.max_cc == 10
    assert validator._config.file_size.max_lines == 200


def test_custom_config_loading(tmp_path):
    """Test loading custom configuration file."""
    config_file = tmp_path / "custom-gate.toml"
    config_file.write_text("""
[coverage]
minimum = 90
fail_under = 85

[complexity]
max_cc = 15
""")
    validator = QualityGateValidator(config_path=str(config_file))
    assert validator._config.coverage.minimum == 90
    assert validator._config.complexity.max_cc == 15


def test_config_validation_errors(tmp_path):
    """Test configuration validation."""
    # Invalid coverage values
    config_file = tmp_path / "invalid-gate.toml"
    config_file.write_text("""
[coverage]
minimum = 150
fail_under = -10
""")
    with pytest.raises(ValueError, match="Invalid configuration"):
        QualityGateValidator(config_path=str(config_file))


def test_file_size_validation(tmp_path):
    """Test file size validation."""
    # Create a file that exceeds max_lines
    test_file = tmp_path / "large_file.py"
    lines = ["pass\n"] * 250  # 250 lines
    test_file.write_text("".join(lines))

    validator = QualityGateValidator()
    violations = validator.validate_file(test_file)

    assert len(violations) > 0
    assert any(v.category == "file_size" for v in violations)


def test_complexity_validation(tmp_path):
    """Test complexity validation."""
    test_file = tmp_path / "complex.py"
    test_file.write_text("""
def complex_function(x):
    if x > 0:
        if x > 10:
            if x > 20:
                if x > 30:
                    if x > 40:
                        if x > 50:
                            if x > 60:
                                if x > 70:
                                    if x > 80:
                                        if x > 90:
                                            return x
    for i in range(10):
        if i > 5:
            if i > 7:
                pass
    try:
        pass
    except:
        pass
    except:
        pass
""")
    validator = QualityGateValidator()
    violations = validator.validate_file(test_file)

    # Should detect high complexity function
    assert any(v.category == "complexity" for v in violations)


def test_type_hints_validation(tmp_path):
    """Test type hints validation."""
    test_file = tmp_path / "no_hints.py"
    test_file.write_text("""
def add(x, y):
    return x + y
""")
    validator = QualityGateValidator()
    violations = validator.validate_file(test_file)

    assert any(v.category == "type_hints" for v in violations)


def test_error_handling_validation(tmp_path):
    """Test error handling validation."""
    test_file = tmp_path / "bad_except.py"
    test_file.write_text("""
try:
    risky_operation()
except:
    pass
""")
    validator = QualityGateValidator()
    violations = validator.validate_file(test_file)

    assert any(v.category == "error_handling" for v in violations)


def test_security_validation(tmp_path):
    """Test security validation."""
    test_file = tmp_path / "secrets.py"
    test_file.write_text("""
password = "SuperSecret123"
api_key = "sk-1234567890"
""")
    validator = QualityGateValidator()
    violations = validator.validate_file(test_file)

    assert any(v.category == "security" for v in violations)


def test_directory_validation(tmp_path):
    """Test directory validation."""
    # Create multiple test files
    (tmp_path / "file1.py").write_text("pass\n" * 250)
    (tmp_path / "file2.py").write_text("pass\n" * 300)
    (tmp_path / "good.py").write_text("x = 1\n")

    validator = QualityGateValidator()
    violations = validator.validate_directory(tmp_path)

    # Should find violations in large files
    assert len(violations) > 0


def test_validation_summary(tmp_path):
    """Test validation summary."""
    test_file = tmp_path / "mixed.py"
    test_file.write_text("""
password = "secret"
def bad_func(x):
    try:
        pass
    except:
        pass
    if x:
        if x:
            if x:
                if x:
                    if x:
                        return x
""")
    validator = QualityGateValidator()
    validator.validate_file(test_file)
    summary = validator.get_summary()

    assert summary["total"] > 0
    assert summary["by_category"]["security"] >= 1
    assert summary["by_category"]["error_handling"] >= 1


def test_performance_nesting_depth(tmp_path):
    """Test performance nesting depth check."""
    test_file = tmp_path / "nested.py"
    test_file.write_text("""
def deeply_nested():
    if True:
        if True:
            if True:
                if True:
                    if True:
                        if True:
                            if True:
                                pass
""")
    validator = QualityGateValidator()
    violations = validator.validate_file(test_file)

    # Should detect excessive nesting (max is 5)
    assert any(v.category == "performance" for v in violations)


def test_config_optional_sections(tmp_path):
    """Test that optional config sections work."""
    config_file = tmp_path / "minimal-gate.toml"
    config_file.write_text("""
[coverage]
enabled = true
minimum = 80

[complexity]
enabled = true
max_cc = 10

[file_size]
enabled = true
max_lines = 200

[type_hints]
enabled = true
require_return_types = true

[error_handling]
enabled = true
forbid_bare_except = true

[architecture]
enabled = true
enforce_layer_separation = true
""")
    # Should not raise error even without optional sections
    validator = QualityGateValidator(config_path=str(config_file))
    assert validator._config.documentation is None
    assert validator._config.testing is None
