"""Unified installed-host CLI for one content-gzh-slim candidate bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from .contracts import validate_task_input
from .distribution_service import DistributionService
from .feishu_adapter import FeishuAdapter
from .fixture_adapter import FixtureAdapter
from .lark_cli_client import LarkCliFeishuClient
from .obsidian_adapter import ObsidianAdapter
from .p2_pipeline import P2Pipeline
from .p3_pipeline import P3Pipeline
from .p4_pipeline import P4Pipeline
from .run_store import RunStore
from .save_service import SaveService


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON input must be an object: {path}")
    return value


def _emit(value: dict[str, Any]) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True))


def _bundle_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _probe() -> dict[str, Any]:
    root = _bundle_root()
    manifest_path = root / "PACKAGE-MANIFEST.json"
    manifest = _read_json(manifest_path)
    files = manifest.get("files")
    if not isinstance(files, dict) or not files:
        raise ValueError("package manifest contains no files")
    for relative, expected in files.items():
        path = root / relative
        if not path.is_file():
            raise ValueError(f"package file is missing: {relative}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"package checksum mismatch: {relative}")
    skill_root = root / ".agents" / "skills"
    names = sorted(path.parent.name for path in skill_root.glob("*/SKILL.md"))
    if names != sorted(manifest.get("skills", [])):
        raise ValueError("installed skill list differs from package manifest")
    return {
        "status": "ready",
        "package": manifest.get("package"),
        "source_revision": manifest.get("source_revision"),
        "skills": names,
        "credentials_copied": False,
        "legacy_v1_replaced": False,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="content-gzh-slim installed-host runtime")
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("probe")

    start = commands.add_parser("start")
    start.add_argument("--input", required=True, type=Path)
    start.add_argument("--catalog", required=True, type=Path)
    start.add_argument("--store", required=True, type=Path)

    gate_a = commands.add_parser("prepare-gate-a")
    gate_a.add_argument("--input", required=True, type=Path)
    gate_a.add_argument("--catalog", required=True, type=Path)
    gate_a.add_argument("--analysis", required=True, type=Path)
    gate_a.add_argument("--direction", required=True, type=Path)
    gate_a.add_argument("--store", required=True, type=Path)

    approve_a = commands.add_parser("approve-gate-a")
    approve_a.add_argument("--run-id", required=True)
    approve_a.add_argument("--store", required=True, type=Path)
    approve_a.add_argument("--option-id", required=True)
    approve_a.add_argument("--decision", required=True)

    context = commands.add_parser("build-context")
    context.add_argument("--run-id", required=True)
    context.add_argument("--catalog", required=True, type=Path)
    context.add_argument("--selection", required=True, type=Path)
    context.add_argument("--store", required=True, type=Path)

    gate_b = commands.add_parser("prepare-gate-b")
    gate_b.add_argument("--run-id", required=True)
    gate_b.add_argument("--draft-output", required=True, type=Path)
    gate_b.add_argument("--headline-output", required=True, type=Path)
    gate_b.add_argument("--store", required=True, type=Path)

    approve_b = commands.add_parser("approve-gate-b")
    approve_b.add_argument("--run-id", required=True)
    approve_b.add_argument("--store", required=True, type=Path)
    approve_b.add_argument("--decision", required=True)

    obsidian = commands.add_parser("save-obsidian")
    obsidian.add_argument("--run-id", required=True)
    obsidian.add_argument("--store", required=True, type=Path)
    obsidian.add_argument("--isolated-root", required=True, type=Path)
    obsidian.add_argument("--target-ref", required=True)
    obsidian.add_argument("--relative-dir", required=True)

    feishu = commands.add_parser("save-feishu")
    feishu.add_argument("--run-id", required=True)
    feishu.add_argument("--store", required=True, type=Path)
    feishu.add_argument("--target-ref", required=True)
    feishu.add_argument("--parent-ref", required=True)
    feishu.add_argument("--client-state", required=True, type=Path)
    feishu.add_argument("--identity", choices=("user", "bot"), default="user")

    distribution = commands.add_parser("generate-distribution")
    distribution.add_argument("--run-id", required=True)
    distribution.add_argument("--store", required=True, type=Path)
    distribution.add_argument("--candidate", required=True, type=Path)
    distribution.add_argument("--request", required=True)

    status = commands.add_parser("status")
    status.add_argument("--run-id", required=True)
    status.add_argument("--store", required=True, type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "probe":
            _emit(_probe())
        elif args.command == "start":
            task = validate_task_input(_read_json(args.input))
            knowledge_base, ip = FixtureAdapter(args.catalog).resolve(
                task["knowledge_base"], task["ip"]
            )
            result = RunStore(args.store).create_or_resume(task, knowledge_base, ip)
            _emit(
                {
                    "outcome": "created" if result.created else "resumed",
                    "run_id": result.run["run_id"],
                    "status": result.run["status"],
                }
            )
        elif args.command == "prepare-gate-a":
            task = validate_task_input(_read_json(args.input))
            knowledge_base, ip = FixtureAdapter(args.catalog).resolve(
                task["knowledge_base"], task["ip"]
            )
            run = RunStore(args.store).create_or_resume(task, knowledge_base, ip).run
            result = P2Pipeline(args.store, args.catalog).run(
                run["run_id"], args.analysis, args.direction
            )
            print(result["gate_a"])
        elif args.command == "approve-gate-a":
            store = RunStore(args.store)
            store.select_gate_a_option(args.run_id, args.option_id)
            run = store.approve_gate(args.run_id, "A", args.decision)
            _emit({"run_id": args.run_id, "status": run["status"]})
        elif args.command == "build-context":
            result = P3Pipeline(args.store, args.catalog).run(args.run_id, args.selection)
            _emit(
                {
                    "run_id": args.run_id,
                    "status": "context_ready",
                    "context_file": "article_context_v1.json",
                    "writer_input_files": 1,
                    "resumed": result["resumed"],
                }
            )
        elif args.command == "prepare-gate-b":
            result = P4Pipeline(args.store).run_initial(
                args.run_id,
                args.draft_output.read_text(encoding="utf-8"),
                _read_json(args.headline_output),
            )
            print(result["gate_b"])
        elif args.command == "approve-gate-b":
            run = RunStore(args.store).approve_gate(args.run_id, "B", args.decision)
            _emit({"run_id": args.run_id, "status": run["status"]})
        elif args.command == "save-obsidian":
            adapter = ObsidianAdapter(
                args.isolated_root, {args.target_ref: args.relative_dir}
            )
            result = SaveService(args.store, {"obsidian": adapter}).save(args.run_id)
            _emit(result["save_receipt"])
        elif args.command == "save-feishu":
            client = LarkCliFeishuClient(
                args.client_state, identity=args.identity
            )
            adapter = FeishuAdapter(client, {args.target_ref: args.parent_ref})
            result = SaveService(args.store, {"feishu": adapter}).save(args.run_id)
            _emit(result["save_receipt"])
        elif args.command == "generate-distribution":
            result = DistributionService(args.store).generate(
                args.run_id,
                explicit_request=args.request,
                candidate=_read_json(args.candidate),
            )
            _emit(result["distribution"])
        elif args.command == "status":
            run = RunStore(args.store).load(args.run_id)
            _emit(
                {
                    "run_id": args.run_id,
                    "status": run["status"],
                    "gate_count": len(run.get("gate_approvals", [])),
                    "draftbox": False,
                    "published": False,
                }
            )
        return 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"content-gzh-slim failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
