"""Independently prepare complete fixture reference snapshots for P2 analysis."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ReferencePrepError(ValueError):
    """Raised when a requested reference is missing, ambiguous, or incomplete."""


class FixtureReferencePreparer:
    def __init__(self, catalog_path: str | Path) -> None:
        with Path(catalog_path).open("r", encoding="utf-8") as handle:
            catalog = json.load(handle)
        references = catalog.get("references") if isinstance(catalog, dict) else None
        if not isinstance(references, list):
            raise ReferencePrepError("fixture catalog must contain references")
        self._references = references

    def prepare(self, requested_refs: list[str]) -> dict[str, Any]:
        if len(requested_refs) > 5:
            raise ReferencePrepError("at most five references may be prepared")
        snapshots = []
        for requested_ref in requested_refs:
            matches = [item for item in self._references if item.get("ref") == requested_ref]
            if len(matches) != 1:
                raise ReferencePrepError(f"reference must resolve uniquely: {requested_ref}")
            source = matches[0]
            if source.get("completeness") != "full":
                raise ReferencePrepError(
                    f"reference is not a complete body and cannot be deeply analyzed: {requested_ref}"
                )
            content = source.get("content")
            if not isinstance(content, str) or not content.strip():
                raise ReferencePrepError(f"complete reference body is empty: {requested_ref}")
            snapshots.append(
                {
                    "reference_ref": requested_ref,
                    "title": str(source.get("title", "")),
                    "source_type": source.get("source_type", "fixture_text"),
                    "source_completeness": "full",
                    "content": content.strip(),
                    "character_count": len(content.strip()),
                }
            )
        return {"schema_version": 1, "references": snapshots}
