"""Developer-facing P1 fixture entrypoint; not a real knowledge-base connector."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .contracts import ContractError, validate_task_input
from .fixture_adapter import FixtureAdapter, FixtureResolutionError
from .run_store import RunStore, RunStoreError
from .state_machine import StateMachine


def main() -> int:
    parser = argparse.ArgumentParser(description="Create or resume a fixture-backed P1 Run")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--catalog", required=True, type=Path)
    parser.add_argument("--store", required=True, type=Path)
    args = parser.parse_args()

    try:
        with args.input.open("r", encoding="utf-8") as handle:
            task_input = validate_task_input(json.load(handle))
        adapter = FixtureAdapter(args.catalog)
        knowledge_base, ip = adapter.resolve(task_input["knowledge_base"], task_input["ip"])
        result = RunStore(args.store).create_or_resume(task_input, knowledge_base, ip)
        output = {
            "outcome": "created" if result.created else "resumed",
            "run_id": result.run["run_id"],
            "status": result.run["status"],
            "next_states": sorted(StateMachine.next_states(result.run["status"])),
            "knowledge_base_backend": result.run["knowledge_base_identity"]["backend"],
            "ip_status": result.run["ip_identity"]["status"],
        }
        print(json.dumps(output, ensure_ascii=False, sort_keys=True))
        return 0
    except (
        OSError,
        json.JSONDecodeError,
        ContractError,
        FixtureResolutionError,
        RunStoreError,
    ) as exc:
        print(f"P1 fixture entry failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

