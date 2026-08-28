"""Explicitly fixture-only P2 Gate A entry; real backends are intentionally unavailable."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .contracts import validate_task_input
from .fixture_adapter import FixtureAdapter
from .p2_pipeline import P2Pipeline
from .run_store import RunStore


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a fixture-only P2 Gate A card")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--catalog", required=True, type=Path)
    parser.add_argument("--analysis", required=True, type=Path)
    parser.add_argument("--direction", required=True, type=Path)
    parser.add_argument("--store", required=True, type=Path)
    args = parser.parse_args()

    try:
        with args.input.open("r", encoding="utf-8") as handle:
            task = validate_task_input(json.load(handle))
        adapter = FixtureAdapter(args.catalog)
        knowledge_base, ip = adapter.resolve(task["knowledge_base"], task["ip"])
        run_result = RunStore(args.store).create_or_resume(task, knowledge_base, ip)
        result = P2Pipeline(args.store, args.catalog).run(
            run_result.run["run_id"], args.analysis, args.direction
        )
        print(result["gate_a"])
        return 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"P2 fixture Gate A failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
