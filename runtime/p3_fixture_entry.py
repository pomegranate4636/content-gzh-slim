"""Fixture or explicitly authorized temporary-bundle P3 entry; no real backend adapter."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .p3_pipeline import P3Pipeline


def main() -> int:
    parser = argparse.ArgumentParser(description="Build one P3 Article Context Pack")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--catalog", required=True, type=Path)
    parser.add_argument("--selection", required=True, type=Path)
    parser.add_argument("--store", required=True, type=Path)
    args = parser.parse_args()
    try:
        result = P3Pipeline(args.store, args.catalog).run(args.run_id, args.selection)
        context = result["context"]
        output = {
            "run_id": context["run_identity"]["run_id"],
            "status": "context_ready",
            "outcome": "resumed" if result["resumed"] else "created",
            "context_file": "article_context_v1.json",
            "writer_input_files": 1,
        }
        print(json.dumps(output, ensure_ascii=False, sort_keys=True))
        return 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"P3 Context build failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
