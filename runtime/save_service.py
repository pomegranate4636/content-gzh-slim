"""Deterministic P5 save orchestration with create-only write and verified readback."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .approved_direction import canonical_digest
from .artifact_store import ArtifactStore, ArtifactStoreError
from .obsidian_adapter import SaveAdapterError
from .run_store import RunStore, RunStoreError
from .save_contract import build_approved_final


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class SaveService:
    def __init__(self, store_root: str | Path, adapters: dict[str, Any]) -> None:
        self.run_store = RunStore(store_root)
        self.artifacts = ArtifactStore(store_root)
        self.adapters = dict(adapters)

    @staticmethod
    def _verify_readback(
        approved: dict[str, Any], target: dict[str, Any], readback: dict[str, Any]
    ) -> None:
        expected = {
            "backend": approved["save_target"]["backend"],
            "object_ref": target["object_ref"],
            "version": approved["draft"]["version"],
            "body_digest": approved["draft"]["digest"],
            "context_digest": approved["context_digest"],
            "title": approved["headline"]["final_title"],
            "body": approved["draft"]["body"],
        }
        if any(readback.get(key) != value for key, value in expected.items()):
            raise SaveAdapterError("save readback does not match approved final content")

    def save(self, run_id: str, *, final_title: str | None = None) -> dict[str, Any]:
        run = self.run_store.load(run_id)
        if run["status"] not in {"final_approved", "saving", "saved"}:
            raise RunStoreError("P5 requires final_approved and never approves Gate B itself")
        backend = run.get("knowledge_base_identity", {}).get("backend")
        adapter = self.adapters.get(backend)
        if adapter is None or getattr(adapter, "backend", None) != backend:
            raise SaveAdapterError("no injected adapter matches the frozen backend")
        approved = build_approved_final(
            run, self.artifacts, adapter_backend=backend, final_title=final_title
        )
        self.artifacts.write_json_once_or_verify(run_id, "approved_final.json", approved)
        if run["status"] == "final_approved":
            self.run_store.advance(run_id, "saving")
            run = self.run_store.load(run_id)

        if run["status"] == "saved":
            receipt = self.artifacts.read_json(run_id, "save_receipt.json")
            target = receipt.get("target", {})
            readback = adapter.read_back(target)
            self._verify_readback(approved, target, readback)
            return {"approved_final": approved, "save_receipt": receipt, "resumed": True}

        try:
            receipt = self.artifacts.read_json(run_id, "save_receipt.json")
        except ArtifactStoreError:
            receipt = None
        if receipt is None:
            target = adapter.write_create_only(approved)
            readback = adapter.read_back(target)
            self._verify_readback(approved, target, readback)
            receipt = {
                "schema_version": 1,
                "run_id": run_id,
                "approved_final_digest": canonical_digest(approved),
                "backend": backend,
                "target": {
                    "target_ref": approved["save_target"]["target_ref"],
                    "object_ref": target["object_ref"],
                },
                "version": approved["draft"]["version"],
                "title": approved["headline"]["final_title"],
                "body_digest": approved["draft"]["digest"],
                "context_digest": approved["context_digest"],
                "write_status": "created" if target.get("created", True) else "verified_existing",
                "readback_status": "verified",
                "saved_at": _utc_now(),
                "semantics": {
                    "saved": True,
                    "draftbox": False,
                    "published": False,
                    "distribution_generated": False,
                },
            }
            self.artifacts.write_json_once_or_verify(run_id, "save_receipt.json", receipt)
        else:
            target = receipt.get("target", {})
            if receipt.get("approved_final_digest") != canonical_digest(approved):
                raise SaveAdapterError("save receipt belongs to a different approved final")
            readback = adapter.read_back(target)
            self._verify_readback(approved, target, readback)
        self.run_store.advance(run_id, "saved")
        return {"approved_final": approved, "save_receipt": receipt, "resumed": False}
