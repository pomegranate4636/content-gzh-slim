"""Resolve synthetic knowledge-base and IP metadata without touching real systems."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class FixtureResolutionError(ValueError):
    """Raised when the synthetic fixture catalog is invalid or ambiguous."""


class FixtureAdapter:
    def __init__(self, catalog_path: str | Path) -> None:
        self.catalog_path = Path(catalog_path)
        with self.catalog_path.open("r", encoding="utf-8") as handle:
            catalog = json.load(handle)
        entries = catalog.get("knowledge_bases") if isinstance(catalog, dict) else None
        if not isinstance(entries, list) or not entries:
            raise FixtureResolutionError("fixture catalog must contain knowledge_bases")
        self._entries = entries

    def resolve(self, knowledge_base: str, ip_name: str) -> tuple[dict[str, str], dict[str, Any]]:
        matches = [
            entry
            for entry in self._entries
            if knowledge_base in {entry.get("alias"), entry.get("ref")}
        ]
        if len(matches) != 1:
            raise FixtureResolutionError("fixture knowledge base must resolve uniquely")
        entry = matches[0]
        backend = entry.get("backend")
        ref = entry.get("ref")
        revision = entry.get("manifest_revision")
        if backend not in {"obsidian", "feishu"}:
            raise FixtureResolutionError("fixture backend must simulate obsidian or feishu")
        if not isinstance(ref, str) or not ref.startswith("fixture://"):
            raise FixtureResolutionError("fixture ref must use fixture:// and never a real path or token")
        if not isinstance(revision, str) or not revision:
            raise FixtureResolutionError("fixture manifest_revision is required")

        knowledge_base_identity = {
            "backend": backend,
            "ref": ref,
            "manifest_revision": revision,
        }
        if ip_name == "none":
            return knowledge_base_identity, {
                "requested_name": "none",
                "resolved_ref": None,
                "status": "none",
            }

        ips = entry.get("ips", {})
        resolved_value = ips.get(ip_name) if isinstance(ips, dict) else None
        if isinstance(resolved_value, str):
            resolved_ref = resolved_value
            status = "full"
        elif isinstance(resolved_value, dict):
            resolved_ref = resolved_value.get("ref")
            status = resolved_value.get("status")
            if status not in {"full", "limited"}:
                raise FixtureResolutionError("fixture IP status must be full or limited")
        else:
            resolved_ref = None
            status = "unused"
        if resolved_ref is not None and (
            not isinstance(resolved_ref, str) or not resolved_ref.startswith("fixture://")
        ):
            raise FixtureResolutionError("fixture IP ref must use fixture://")
        return knowledge_base_identity, {
            "requested_name": ip_name,
            "resolved_ref": resolved_ref,
            "status": status,
        }

