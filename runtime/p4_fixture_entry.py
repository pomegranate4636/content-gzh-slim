"""Fixture or authorized temporary-bundle P4 entry; no source or save adapter."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .p4_pipeline import P4Pipeline


def main() -> int:
    parser = argparse.ArgumentParser(description="Build one P4 draft, Top 3, and Gate B")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--draft-output", required=True, type=Path)
    parser.add_argument("--headline-output", required=True, type=Path)
    parser.add_argument("--store", required=True, type=Path)
    args = parser.parse_args()
    try:
        body = args.draft_output.read_text(encoding="utf-8")
        headline_candidate = json.loads(args.headline_output.read_text(encoding="utf-8"))
        result = P4Pipeline(args.store).run_initial(args.run_id, body, headline_candidate)
        print(
            json.dumps(
                {
                    "run_id": args.run_id,
                    "status": "waiting_final",
                    "draft_file": result["draft_file"],
                    "headline_file": result["headline_file"],
                    "writer_input_files": 1,
                    "saved": False,
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"P4 build failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
