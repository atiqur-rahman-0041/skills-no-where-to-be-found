#!/usr/bin/env python3
"""Check that every skill in skills/ is well formed and listed in the marketplace.

Run from the repo root:  python3 scripts/validate_skills.py
Exits non-zero if anything is wrong.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / ".claude-plugin" / "marketplace.json"
SKILLS_DIR = ROOT / "skills"

MAX_DESCRIPTION = 1024
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def parse_frontmatter(path):
    """Return the YAML frontmatter of a SKILL.md as a flat dict of str -> str."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("file does not start with a '---' frontmatter fence")
    end = text.find("\n---", 3)
    if end == -1:
        raise ValueError("frontmatter is not closed by a '---' line")

    fields, key = {}, None
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        if line[0] in " \t" and key:  # folded continuation line
            fields[key] += " " + line.strip()
            continue
        if ":" not in line:
            raise ValueError(f"malformed frontmatter line: {line!r}")
        key, _, value = line.partition(":")
        key = key.strip()
        fields[key] = value.strip().strip('"').strip("'")
    return fields


def main():
    if not SKILLS_DIR.is_dir():
        print("no skills/ directory found")
        return 1

    errors = []
    directories = [
        d for d in sorted(SKILLS_DIR.iterdir()) if d.is_dir() and not d.name.startswith(".")
    ]

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    plugins = manifest.get("plugins", [])
    if len(plugins) != 1:
        errors.append(
            f"{MANIFEST.name}: expected exactly one plugin entry, found {len(plugins)}"
        )
        listed = set()
    else:
        listed = {p.rstrip("/").removeprefix("./") for p in plugins[0].get("skills", [])}

    on_disk = {f"skills/{d.name}" for d in directories}
    for missing in sorted(on_disk - listed):
        errors.append(f"{missing}: exists on disk but is not in the marketplace 'skills' array")
    for dangling in sorted(listed - on_disk):
        errors.append(f"{dangling}: listed in the marketplace but has no directory")

    for directory in directories:
        rel = f"skills/{directory.name}"
        skill_md = directory / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"{rel}: has no SKILL.md")
            continue
        try:
            fm = parse_frontmatter(skill_md)
        except ValueError as exc:
            errors.append(f"{rel}/SKILL.md: {exc}")
            continue

        name = fm.get("name", "")
        description = fm.get("description", "")
        if not name:
            errors.append(f"{rel}/SKILL.md: missing 'name'")
        elif name != directory.name:
            errors.append(
                f"{rel}/SKILL.md: name {name!r} does not match directory {directory.name!r}"
            )
        elif not NAME_RE.match(name):
            errors.append(f"{rel}/SKILL.md: name {name!r} must be lowercase-kebab-case")

        if not description:
            errors.append(f"{rel}/SKILL.md: missing 'description'")
        elif len(description) > MAX_DESCRIPTION:
            errors.append(
                f"{rel}/SKILL.md: description is {len(description)} chars (max {MAX_DESCRIPTION})"
            )

    if errors:
        print(f"{len(errors)} problem(s) found:\n")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"OK: {len(directories)} skill(s) validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
