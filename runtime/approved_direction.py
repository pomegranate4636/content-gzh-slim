"""Bind one exact Gate A receipt to one frozen P2 direction artifact."""

from __future__ import annotations

import hashlib
import json
from typing import Any


class ApprovedDirectionError(ValueError):
    """Raised when Gate A approval cannot be bound to one exact direction."""


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def materialize_approved_direction(
    run: dict[str, Any],
    direction: dict[str, Any],
    retrieval_receipt: dict[str, Any],
) -> dict[str, Any]:
    if run.get("status") not in {"direction_approved", "context_ready"}:
        raise ApprovedDirectionError("Run must be direction_approved before P3")
    approvals = [item for item in run.get("gate_approvals", []) if item.get("gate") == "A"]
    if len(approvals) != 1 or approvals[0].get("decision") != "确认方向":
        raise ApprovedDirectionError("P3 requires one exact dedicated Gate A approval receipt")

    if direction.get("run_id") != run.get("run_id"):
        raise ApprovedDirectionError("direction run_id does not match Run")
    if direction.get("knowledge_base_identity") != run.get("knowledge_base_identity"):
        raise ApprovedDirectionError("direction knowledge base does not match Run")
    if direction.get("ip_identity") != run.get("ip_identity"):
        raise ApprovedDirectionError("direction IP does not match Run")
    if direction.get("task_input") != run.get("task_input"):
        raise ApprovedDirectionError("direction task input does not match Run")
    if direction.get("mode") != "single" or len(direction.get("options", [])) != 1:
        raise ApprovedDirectionError(
            "Gate receipt does not bind one option; refusing to guess among multiple directions"
        )

    if retrieval_receipt.get("run_id") != run.get("run_id"):
        raise ApprovedDirectionError("retrieval receipt run_id does not match Run")
    if retrieval_receipt.get("knowledge_base_identity") != run.get("knowledge_base_identity"):
        raise ApprovedDirectionError("retrieval receipt knowledge base does not match Run")
    if retrieval_receipt.get("ip_identity") != run.get("ip_identity"):
        raise ApprovedDirectionError("retrieval receipt IP does not match Run")

    entries = retrieval_receipt.get("entries", [])
    role_refs = {
        "business_refs": {
            item["source_ref"] for item in entries if item.get("role") == "03"
        },
        "peer_refs": {
            item["source_ref"]
            for item in entries
            if item.get("role") == "04" and item.get("selected_use") == "peer_content_asset"
        },
        "method_refs": {
            item["source_ref"]
            for item in entries
            if item.get("role") == "04" and item.get("selected_use") == "content_method_asset"
        },
        "reference_refs": {
            item["source_ref"] for item in entries if item.get("role") == "reference"
        },
    }
    approved_option = direction["options"][0]
    selected_sources = approved_option.get("selected_sources", {})
    for key, available in role_refs.items():
        selected = selected_sources.get(key)
        if not isinstance(selected, list) or not set(selected).issubset(available):
            raise ApprovedDirectionError(f"approved direction contains unfrozen {key}")

    return {
        "schema_version": 1,
        "run_id": run["run_id"],
        "input_digest": run["input_digest"],
        "knowledge_base_identity": run["knowledge_base_identity"],
        "ip_identity": run["ip_identity"],
        "task_input": run["task_input"],
        "gate_receipt": approvals[0],
        "direction_digest": canonical_digest(direction),
        "retrieval_receipt_digest": canonical_digest(retrieval_receipt),
        "approved_option": approved_option,
        "frozen_candidates": {
            "ip_ref": run["ip_identity"].get("resolved_ref"),
            "business_candidate_refs": sorted(role_refs["business_refs"]),
            "selected_peer_refs": list(selected_sources["peer_refs"]),
            "selected_method_refs": list(selected_sources["method_refs"]),
            "reference_refs": list(selected_sources["reference_refs"]),
        },
    }
