"""Fixture-only P2 orchestration that stops at the unapproved Gate A card."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .analysis_contract import validate_analysis
from .artifact_store import ArtifactStore
from .gate_a import build_direction, render_gate_a
from .reference_prep import FixtureReferencePreparer
from .retrieval_receipt import build_retrieval_receipt
from .retrieval_search import ControlledFixtureRetriever
from .run_store import RunStore, RunStoreError


class P2Pipeline:
    def __init__(self, store_root: str | Path, catalog_path: str | Path) -> None:
        self.run_store = RunStore(store_root)
        self.artifacts = ArtifactStore(store_root)
        self.retriever = ControlledFixtureRetriever(catalog_path)
        self.reference_preparer = FixtureReferencePreparer(catalog_path)

    @staticmethod
    def _read_object(path: str | Path) -> dict[str, Any]:
        with Path(path).open("r", encoding="utf-8") as handle:
            value = json.load(handle)
        if not isinstance(value, dict):
            raise ValueError("fixture Analyzer output must be an object")
        return value

    def run(
        self,
        run_id: str,
        analysis_path: str | Path,
        direction_template_path: str | Path,
    ) -> dict[str, Any]:
        run = self.run_store.load(run_id)
        if run["status"] == "waiting_direction":
            direction = self.artifacts.read_json(run_id, "direction_v1.json")
            return {"direction": direction, "gate_a": render_gate_a(direction), "resumed": True}
        if run["status"] == "created":
            run = self.run_store.advance(run_id, "direction_working")
        elif run["status"] != "direction_working":
            raise RunStoreError("P2 may only start from created or resume direction_working")

        retrieval = self.retriever.prepare(
            run["task_input"], run["knowledge_base_identity"], run["ip_identity"]
        )
        snapshots = self.reference_preparer.prepare(run["task_input"]["references"])
        analysis = validate_analysis(self._read_object(analysis_path), snapshots)
        direction = build_direction(
            self._read_object(direction_template_path), run, retrieval, analysis
        )
        receipt = build_retrieval_receipt(run, retrieval, snapshots, direction)

        self.artifacts.write_json_once_or_verify(run_id, "reference_snapshot_v1.json", snapshots)
        self.artifacts.write_json_once_or_verify(run_id, "analysis_v1.json", analysis)
        self.artifacts.write_json_once_or_verify(run_id, "direction_v1.json", direction)
        self.artifacts.write_json_once_or_verify(run_id, "retrieval_receipt.json", receipt)
        self.run_store.advance(run_id, "waiting_direction")
        return {
            "direction": direction,
            "gate_a": render_gate_a(direction),
            "retrieval_receipt": receipt,
            "resumed": False,
        }
