#!/usr/bin/env python3
"""Promote a repetition-log entry to a playbook file."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REGISTRY_DEFAULT = Path(".app-workflow/repetition-log.json")
TEMPLATE = Path(__file__).resolve().parents[1] / "assets/playbook.template.md"

PHASE_SKILL_HINT = {
    "prd": "01_PRD/creating-app-product-docs/SKILL.md",
    "ip": "02_IP/generate-app-brand-ip/SKILL.md",
    "prototype": "03_UI_UX/creating-app-prototypes/SKILL.md",
    "scaffold": "04_Dev/create-flutter-app/SKILL.md",
    "features": "05_Feature/implement-flutter-features/SKILL.md",
    "qa": "06_QA/polish-app-quality/SKILL.md",
    "app_store": "07_AppStore/release-to-app-store/SKILL.md",
}


def slugify(text: str) -> str:
    return re.sub(r"[^\w]+", "_", text.casefold()).strip("_")[:60]


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote repetition to playbook")
    parser.add_argument("--pattern-id", required=True)
    parser.add_argument("--title", default="", help="Playbook title; defaults to pattern text")
    parser.add_argument("--registry", type=Path, default=REGISTRY_DEFAULT)
    args = parser.parse_args()

    registry_path = args.registry.resolve()
    if not registry_path.is_file():
        print(f"FAIL: registry not found: {registry_path}", file=sys.stderr)
        return 1

    data = json.loads(registry_path.read_text(encoding="utf-8"))
    entry = next((e for e in data.get("entries", []) if e.get("id") == args.pattern_id), None)
    if not entry:
        print(f"FAIL: pattern id not found: {args.pattern_id}", file=sys.stderr)
        return 1

    state_dir = registry_path.parent
    relative_path = entry.get("playbook_path")
    if relative_path and (state_dir / relative_path).is_file():
        print(f"ALREADY_PROMOTED: {entry['playbook_path']}")
        return 0

    phase = entry.get("phase", "general")
    title = args.title or entry.get("pattern", "Untitled")
    slug = slugify(title)
    playbooks_dir = state_dir / "playbooks"
    phase_dir = playbooks_dir / phase
    phase_dir.mkdir(parents=True, exist_ok=True)
    playbook_path = phase_dir / f"{slug}.md"

    if playbook_path.exists():
        playbook_path = phase_dir / f"{slug}_{entry.get('count', 3)}.md"

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    template = TEMPLATE.read_text(encoding="utf-8")
    body = template.replace("<title>", title)
    front = (
        f"---\nphase: {phase}\npattern_id: {entry['id']}\n"
        f"title: {title}\ncount_at_promotion: {entry.get('count', 3)}\n"
        f"promoted_at: {now}\npromoted_to: []\n---\n\n"
    )
    contexts = entry.get("contexts", [])
    ctx_block = contexts[-1]["text"] if contexts else entry.get("pattern", "")
    body = body.replace("repetition-log id: ", f"repetition-log id: {entry['id']}")
    body = body.replace("典型 context: ", f"典型 context: {ctx_block}")

    playbook_path.write_text(front + body.split("---\n\n", 1)[-1], encoding="utf-8")

    entry["status"] = "promoted"
    entry["playbook_path"] = str(playbook_path.relative_to(state_dir))
    registry_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    index_path = playbooks_dir / "INDEX.md"
    if not index_path.is_file():
        index_path.write_text("# Playbook Index\n\n| Phase | Title | Path | Count |\n|-------|-------|------|-------|\n", encoding="utf-8")
    row = f"| {phase} | {title} | `{entry['playbook_path']}` | {entry.get('count', 3)} |\n"
    with index_path.open("a", encoding="utf-8") as f:
        f.write(row)

    hint = PHASE_SKILL_HINT.get(phase, "00_Orchestrator/app-workflow/SKILL.md")
    print(f"PLAYBOOK={playbook_path}")
    print(f"SUGGEST_MERGE_INTO={hint}")
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
