#!/usr/bin/env python3
"""Validate frontmatter of skills/*/SKILL.md and agents/*.md.

Rules:
- File must start with `---\n...\n---` YAML frontmatter.
- Required fields: `name`, `description`.
- `name` must be kebab-case ([a-z0-9-]+).
- For skills: `name` must equal the parent directory name.
- For agents: `name` must equal the filename (without .md).
- `description` must be non-empty and ideally describe trigger conditions.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is not installed. Run `pip install pyyaml`.", file=sys.stderr)
    sys.exit(2)

KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
REPO_ROOT = Path(__file__).resolve().parents[2]


def parse_frontmatter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    match = FM_RE.match(text)
    if not match:
        return None
    return yaml.safe_load(match.group(1)) or {}


def validate(path: Path, expected_name: str, kind: str) -> list[str]:
    errors: list[str] = []
    fm = parse_frontmatter(path)
    if fm is None:
        return [f"{path}: missing YAML frontmatter (file must start with `---`)"]
    if not isinstance(fm, dict):
        return [f"{path}: frontmatter must be a YAML mapping, got {type(fm).__name__}"]

    name = fm.get("name")
    description = fm.get("description")

    if not name:
        errors.append(f"{path}: missing required field `name`")
    elif not isinstance(name, str):
        errors.append(f"{path}: `name` must be a string")
    else:
        if not KEBAB.match(name):
            errors.append(f"{path}: `name` ({name!r}) must be kebab-case ([a-z0-9-]+)")
        if name != expected_name:
            errors.append(
                f"{path}: `name` ({name!r}) must match {kind} identifier "
                f"({expected_name!r})"
            )

    if not description:
        errors.append(f"{path}: missing required field `description`")
    elif not isinstance(description, str):
        errors.append(f"{path}: `description` must be a string")
    elif len(description.strip()) < 20:
        errors.append(
            f"{path}: `description` is too short ({len(description.strip())} chars); "
            "describe when this should trigger"
        )

    return errors


def main() -> int:
    errors: list[str] = []

    skills_dir = REPO_ROOT / "skills"
    if skills_dir.is_dir():
        for skill_dir in sorted(skills_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_file = skill_dir / "SKILL.md"
            if not skill_file.is_file():
                errors.append(f"{skill_dir}: missing SKILL.md")
                continue
            errors.extend(validate(skill_file, skill_dir.name, "skill directory"))

    agents_dir = REPO_ROOT / "agents"
    if agents_dir.is_dir():
        for agent_file in sorted(agents_dir.glob("*.md")):
            errors.extend(validate(agent_file, agent_file.stem, "agent filename"))

    if errors:
        print("Frontmatter validation FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print("Frontmatter validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
