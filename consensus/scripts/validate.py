#!/usr/bin/env python3
"""
UPC Protocol v2.0 Validator

Validates consensus artifacts against JSON schemas.
Works with standard library only (jsonschema optional for full validation).
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Optional

# Try to import jsonschema, fall back to basic validation
try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


def load_json(path: Path) -> Optional[dict]:
    """Load and parse a JSON file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON in {path}: {e.msg} at line {e.lineno}")
        return None
    except FileNotFoundError:
        print(f"⚠ File not found: {path}")
        return None


def validate_json_syntax(epic_dir: Path) -> bool:
    """Check all JSON files for syntax errors."""
    consensus_dir = epic_dir / "consensus"
    if not consensus_dir.exists():
        print(f"⚠ No consensus directory found in {epic_dir}")
        return True
    
    all_valid = True
    for json_file in consensus_dir.rglob("*.json"):
        data = load_json(json_file)
        if data is None and json_file.exists():
            all_valid = False
        elif data is not None:
            print(f"✓ {json_file.relative_to(epic_dir)}")
    
    return all_valid


def validate_against_schema(data: dict, schema: dict, file_path: str) -> bool:
    """Validate data against JSON schema using jsonschema library."""
    if not HAS_JSONSCHEMA:
        print(f"⚠ jsonschema not installed, skipping schema validation for {file_path}")
        return True
    
    try:
        jsonschema.validate(data, schema)
        print(f"✓ {file_path} (schema valid)")
        return True
    except jsonschema.ValidationError as e:
        print(f"✗ {file_path}: {e.message}")
        if e.path:
            print(f"  Field: {'.'.join(str(p) for p in e.path)}")
        return False


def validate_status(epic_dir: Path, schema_dir: Path) -> bool:
    """Validate status.json against schema."""
    status_path = epic_dir / "consensus" / "status.json"
    schema_path = schema_dir / "status.schema.json"
    
    status = load_json(status_path)
    schema = load_json(schema_path)
    
    if status is None:
        print(f"⚠ No status.json found in {epic_dir}")
        return True  # Not an error for starter tier
    
    if schema is None:
        print(f"✗ Schema not found: {schema_path}")
        return False
    
    return validate_against_schema(status, schema, "status.json")


def validate_phase_requirements(epic_dir: Path, tier: str) -> bool:
    """Check that required artifacts exist for the current phase."""
    status_path = epic_dir / "consensus" / "status.json"
    status = load_json(status_path)
    
    if status is None:
        return True  # No status = starter tier, no requirements
    
    phase = status.get("phase", "requirements")
    artifacts_dir = epic_dir / "consensus" / "artifacts"
    
    # Phase artifact requirements (Standard tier+)
    requirements_map = {
        "architecture": ["requirements.json"],
        "planning": ["requirements.json", "architecture.json"],
        "implementation": ["plan.json"],
        "testing": ["implementation.json"],
        "deployment": ["test_results.json"],
        "done": ["requirements.json", "architecture.json", "plan.json", "implementation.json", "test_results.json"],
    }
    
    if tier == "starter":
        return True  # No strict requirements for starter
    
    required = requirements_map.get(phase, [])
    all_present = True
    
    for artifact in required:
        artifact_path = artifacts_dir / artifact
        if not artifact_path.exists():
            print(f"⚠ Missing required artifact for phase '{phase}': {artifact}")
            all_present = False
    
    if all_present and required:
        print(f"✓ All required artifacts present for phase '{phase}'")
    
    return all_present


def main():
    parser = argparse.ArgumentParser(description="UPC Protocol v2.0 Validator")
    parser.add_argument(
        "epic_dir",
        type=Path,
        nargs="?",
        default=Path("."),
        help="Epic directory (default: current directory)"
    )
    parser.add_argument(
        "--tier",
        choices=["starter", "standard", "enterprise"],
        default="standard",
        help="Validation tier (default: standard)"
    )
    parser.add_argument(
        "--schema-dir",
        type=Path,
        default=None,
        help="Schema directory (default: auto-detect)"
    )
    
    args = parser.parse_args()
    epic_dir = args.epic_dir.resolve()
    tier = args.tier
    
    # Auto-detect schema directory
    if args.schema_dir:
        schema_dir = args.schema_dir.resolve()
    else:
        # Try relative to script, then relative to epic
        script_dir = Path(__file__).parent.parent
        schema_dir = script_dir / "schema"
        if not schema_dir.exists():
            schema_dir = epic_dir / "consensus" / "schema"
    
    print(f"=== UPC Protocol Validation (Tier: {tier}) ===")
    print(f"Epic: {epic_dir}")
    print(f"Schemas: {schema_dir}")
    print()
    
    all_valid = True
    
    # Step 1: JSON syntax (all tiers)
    print("--- JSON Syntax Check ---")
    if not validate_json_syntax(epic_dir):
        all_valid = False
    print()
    
    # Step 2: Schema validation (standard+)
    if tier in ("standard", "enterprise"):
        print("--- Schema Validation ---")
        if not validate_status(epic_dir, schema_dir):
            all_valid = False
        print()
        
        # Step 3: Phase requirements (standard+)
        print("--- Phase Requirements ---")
        if not validate_phase_requirements(epic_dir, tier):
            all_valid = False
        print()
    
    print("=== Validation Complete ===")
    
    if all_valid:
        print("✓ All checks passed")
        sys.exit(0)
    else:
        print("✗ Some checks failed")
        sys.exit(1)


if __name__ == "__main__":
    main()

