#!/usr/bin/env python3
"""Example: Using the Quality Gate Validator

This script demonstrates how to use the Quality Gate Validator
to check code quality against configurable thresholds.
"""

from pathlib import Path
from sdp.quality import QualityGateValidator

# Example 1: Validate a single file
print("=" * 60)
print("Example 1: Validating a single file")
print("=" * 60)

validator = QualityGateValidator()
violations = validator.validate_file("src/sdp/quality/validator.py")

print(f"\nFound {len(violations)} violations in validator.py")
if violations:
    for v in violations[:5]:  # Show first 5
        print(f"  {v}")

# Example 2: Validate a directory
print("\n" + "=" * 60)
print("Example 2: Validating a directory")
print("=" * 60)

validator2 = QualityGateValidator()
violations2 = validator2.validate_directory("src/sdp/quality/")
summary2 = validator2.get_summary()

print(f"\nDirectory validation summary:")
print(f"  Total violations: {summary2['total']}")
print(f"  Errors: {summary2['errors']}")
print(f"  Warnings: {summary2['warnings']}")
print(f"\nBy category:")
for category, count in sorted(summary2['by_category'].items()):
    print(f"  {category}: {count}")

# Example 3: Print full report
print("\n" + "=" * 60)
print("Example 3: Full validation report")
print("=" * 60)

validator3 = QualityGateValidator()
validator3.validate_directory("src/sdp/quality/")
validator3.print_report()

# Example 4: Custom configuration
print("\n" + "=" * 60)
print("Example 4: Using custom configuration")
print("=" * 60)

validator4 = QualityGateValidator(config_path="quality-gate.toml")
violations4 = validator4.validate_directory("src/sdp/quality/")

print(f"\nUsing custom configuration from quality-gate.toml")
print(f"Found {len(violations4)} violations")

# Example 5: Filter by severity
print("\n" + "=" * 60)
print("Example 5: Filtering violations by severity")
print("=" * 60)

validator5 = QualityGateValidator()
validator5.validate_directory("src/sdp/quality/")

errors = [v for v in validator5.violations if v.severity == "error"]
warnings = [v for v in validator5.violations if v.severity == "warning"]

print(f"\nErrors: {len(errors)}")
print(f"Warnings: {len(warnings)}")

if errors:
    print("\nFirst 3 errors:")
    for e in errors[:3]:
        print(f"  {e}")
