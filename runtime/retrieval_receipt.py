"""Build the P2 operational receipt without becoming a Writer context pack."""

from __future__ import annotations

from typing import Any


def build_retrieval_receipt(
    run: dict[str, Any],
    retrieval: dict[str, Any],
    snapshots: dict[str, Any],
    direction: dict[str, Any],
) -> dict[str, Any]:
    proposed = {"business_refs": set(), "peer_refs": set(), "method_refs": set(), "reference_refs": set()}
    for option in direction["options"]:
        for key in proposed:
            proposed[key].update(option["selected_sources"][key])

    entries: list[dict[str, Any]] = []
    ip_anchor = retrieval["ip_anchor"]
    entries.append(
        {
            "role": "05",
            "source_ref": ip_anchor["ref"] if ip_anchor else None,
            "candidate_status": "available" if ip_anchor else retrieval["ip_status"],
            "gate_a_status": "proposed" if ip_anchor else "not_proposed",
            "final_selection_status": "pending_gate_a",
            "selected_use": "speaker identity and core anchors" if ip_anchor else None,
            "not_selected_reason": None if ip_anchor else "none or unavailable IP",
            "snippet_count": ip_anchor["snippet_count"] if ip_anchor else 0,
            "character_count": ip_anchor["character_count"] if ip_anchor else 0,
            "in_context_pack": False,
        }
    )

    mappings = (
        ("business_candidates", "03", "business_refs"),
        ("peer_candidates", "04", "peer_refs"),
        ("method_candidates", "04", "method_refs"),
    )
    for candidate_key, role, proposed_key in mappings:
        for item in retrieval[candidate_key]:
            is_proposed = item["ref"] in proposed[proposed_key]
            entries.append(
                {
                    "role": role,
                    "source_ref": item["ref"],
                    "candidate_status": "candidate",
                    "gate_a_status": "proposed" if is_proposed else "not_proposed",
                    "final_selection_status": "pending_gate_a",
                    "selected_use": item["asset_type"] if is_proposed else None,
                    "not_selected_reason": None if is_proposed else "not used by current Gate A proposal",
                    "snippet_count": item["snippet_count"],
                    "character_count": item["character_count"],
                    "in_context_pack": False,
                }
            )

    for snapshot in snapshots["references"]:
        is_proposed = snapshot["reference_ref"] in proposed["reference_refs"]
        entries.append(
            {
                "role": "reference",
                "source_ref": snapshot["reference_ref"],
                "candidate_status": "complete_snapshot",
                "gate_a_status": "proposed" if is_proposed else "not_proposed",
                "final_selection_status": "pending_gate_a",
                "selected_use": "benchmark mechanism" if is_proposed else None,
                "not_selected_reason": None if is_proposed else "not used by current Gate A proposal",
                "snippet_count": 1,
                "character_count": snapshot["character_count"],
                "in_context_pack": False,
            }
        )

    return {
        "schema_version": 1,
        "run_id": run["run_id"],
        "knowledge_base_identity": run["knowledge_base_identity"],
        "ip_identity": run["ip_identity"],
        "access_log": retrieval["access_log"],
        "entries": entries,
        "totals": {
            "05_profiles_read": 1 if ip_anchor else 0,
            "03_candidates": len(retrieval["business_candidates"]),
            "04_peer_candidates": len(retrieval["peer_candidates"]),
            "04_method_candidates": len(retrieval["method_candidates"]),
            "references_prepared": len(snapshots["references"]),
            "characters_read": sum(item["character_count"] for item in entries),
            "context_packs": 0,
        },
    }
