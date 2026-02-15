#!/usr/bin/env python3
"""
Reorder YAML frontmatter in vault markdown notes to match Second Brain rules.

Order: top = categories, title, name, aliases; middle = rest (alphabetical);
       bottom = published, created, tags.

Usage:
  python reorder_frontmatter.py [--dry-run] [--path PATH]
"""

from collections import OrderedDict
import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("This script requires PyYAML. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

TOP_KEYS = ["categories", "title", "name", "aliases"]
BOTTOM_KEYS = ["published", "created", "tags"]


def find_vault_root(start: Path) -> Path:
    """Assume script is in .cursor/skills/frontmatter-order/scripts/; vault root is 4 levels up."""
    p = start.resolve()
    for _ in range(4):
        p = p.parent
    return p


def extract_frontmatter(content: str):
    """Return (frontmatter_str, body_str) or (None, content) if no frontmatter."""
    if not content.startswith("---"):
        return None, content
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)", content, re.DOTALL)
    if not match:
        return None, content
    return match.group(1).strip(), match.group(2)


def reorder_keys(data: dict) -> OrderedDict:
    """Return an OrderedDict with keys in canonical order."""
    top_set = set(TOP_KEYS)
    bottom_set = set(BOTTOM_KEYS)
    top_ordered = [k for k in TOP_KEYS if k in data]
    bottom_ordered = [k for k in BOTTOM_KEYS if k in data]
    middle = sorted(k for k in data if k not in top_set and k not in bottom_set)
    ordered = OrderedDict()
    for k in top_ordered + middle + bottom_ordered:
        ordered[k] = data[k]
    return ordered


def main():
    parser = argparse.ArgumentParser(description="Reorder frontmatter in vault notes")
    parser.add_argument("--dry-run", action="store_true", help="Only print what would be changed")
    parser.add_argument("--path", type=str, default="", help="Limit to this path under vault (e.g. Daily)")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    vault_root = find_vault_root(script_dir)
    if args.path:
        search_root = vault_root / args.path
        if not search_root.is_dir():
            print(f"Path not found: {search_root}", file=sys.stderr)
            sys.exit(1)
    else:
        search_root = vault_root

    edited = 0
    errors = []

    for path in sorted(search_root.rglob("*.md")):
        # Skip .cursor and Templates (templates often have {{placeholders}} that aren't valid YAML until filled)
        if ".cursor" in path.parts or "Templates" in path.parts:
            continue
        rel = path.relative_to(vault_root)
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            errors.append((str(rel), str(e)))
            continue

        fm_str, body = extract_frontmatter(content)
        if fm_str is None:
            continue

        try:
            data = yaml.safe_load(fm_str)
        except yaml.YAMLError as e:
            errors.append((str(rel), f"YAML: {e}"))
            continue

        if not isinstance(data, dict):
            continue

        ordered = reorder_keys(data)
        # Check if order actually changed (compare key order)
        orig_keys = list(data.keys())
        new_keys = list(ordered.keys())
        if orig_keys == new_keys:
            continue

        # Use plain dict so PyYAML outputs standard YAML (order preserved in 3.7+).
        # OrderedDict would be serialized as !!python/object/apply and break Obsidian.
        plain = dict(ordered)
        new_fm = yaml.dump(
            plain,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            width=1000,
        ).strip()
        new_content = "---\n" + new_fm + "\n---\n" + body

        if args.dry_run:
            print(f"Would reorder: {rel}")
            edited += 1
        else:
            path.write_text(new_content, encoding="utf-8")
            print(f"Reordered: {rel}")
            edited += 1

    if errors:
        print("\nErrors:", file=sys.stderr)
        for rel, err in errors:
            print(f"  {rel}: {err}", file=sys.stderr)
    print(f"\nDone. {edited} file(s) {'would be ' if args.dry_run else ''}updated.")


if __name__ == "__main__":
    main()
