"""Create-only, versioned optional distribution artifacts after saved state."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .approved_direction import canonical_digest
from .artifact_store import ArtifactStore
from .distribution_contract import (
    DistributionContractError,
    frozen_distribution_constraints,
    validate_distribution_candidate,
    validate_saved_receipt,
)
from .run_store import RunStore, RunStoreError


class DistributionService:
    def __init__(self, store_root: str | Path) -> None:
        self.run_store = RunStore(store_root)
        self.artifacts = ArtifactStore(store_root)

    def _versions(self, run_id: str) -> list[int]:
        run_dir = self.artifacts.boundary.child("runs", run_id)
        return sorted(
            int(match.group(1))
            for path in run_dir.glob("distribution_v*.json")
            if (match := re.fullmatch(r"distribution_v(\d+)\.json", path.name))
        )

    @staticmethod
    def _content(artifact: dict[str, Any]) -> dict[str, Any]:
        return {
            key: artifact[key]
            for key in (
                "wechat_final_title",
                "xiaohongshu",
                "wechat_channels",
                "douyin",
                "moments",
            )
        }

    def generate(
        self, run_id: str, *, explicit_request: str, candidate: dict[str, Any]
    ) -> dict[str, Any]:
        if explicit_request != "生成分发包":
            raise DistributionContractError("distribution requires the exact explicit request")
        run = self.run_store.load(run_id)
        if run["status"] not in {"saved", "distribution_optional"}:
            raise RunStoreError("distribution requires saved and is never a third Gate")
        approved = self.artifacts.read_json(run_id, "approved_final.json")
        receipt = self.artifacts.read_json(run_id, "save_receipt.json")
        context = self.artifacts.read_json(run_id, "article_context_v1.json")
        approved_digest = canonical_digest(approved)
        validate_saved_receipt(run, approved, receipt)
        if approved.get("context_digest") != canonical_digest(context):
            raise DistributionContractError("distribution Context digest mismatch")
        constraints = frozen_distribution_constraints(context)
        normalized = validate_distribution_candidate(
            candidate, approved, constraints["must_avoid"]
        )
        versions = self._versions(run_id)
        if versions:
            latest = self.artifacts.read_json(run_id, f"distribution_v{versions[-1]}.json")
            if (
                latest.get("approved_final_digest") != approved_digest
                or latest.get("save_receipt_digest") != canonical_digest(receipt)
                or latest.get("body_digest") != approved["draft"]["digest"]
                or latest.get("wechat_final_title")
                != approved["headline"]["final_title"]
            ):
                raise DistributionContractError("stored distribution binding is stale or mismatched")
            if self._content(latest) == normalized:
                return {"distribution": latest, "resumed": True}
        version = versions[-1] + 1 if versions else 1
        artifact = {
            "schema_version": 1,
            "run_id": run_id,
            "distribution_version": version,
            "approved_final_digest": approved_digest,
            "save_receipt_digest": canonical_digest(receipt),
            "body_digest": approved["draft"]["digest"],
            "frozen_distribution_constraints": constraints,
            **normalized,
            "semantics": {
                "article_body_modified": False,
                "wechat_title_modified": False,
                "saved_to_knowledge_base": False,
                "draftbox": False,
                "published": False,
            },
        }
        self.artifacts.write_json_once_or_verify(
            run_id, f"distribution_v{version}.json", artifact
        )
        if run["status"] == "saved":
            self.run_store.advance(run_id, "distribution_optional")
        return {"distribution": artifact, "resumed": False}
