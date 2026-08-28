"""Validate deep Analyzer output without performing semantic analysis in Runtime."""

from __future__ import annotations

from typing import Any


class AnalysisContractError(ValueError):
    """Raised when Analyzer output is shallow, incomplete, or source-mismatched."""


_REQUIRED_FIELDS = {
    "title_mechanism",
    "opening_hook",
    "target_reader_and_promise",
    "sections",
    "conflict",
    "argument_and_evidence",
    "cases_numbers_details",
    "transitions",
    "emotion_and_pacing",
    "ending_and_cta",
    "transferable_mechanisms",
    "forbidden_transfers",
}


def _meaningful(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return False


def validate_analysis(payload: Any, reference_snapshot: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        raise AnalysisContractError("analysis must be a schema_version 1 object")
    analyses = payload.get("reference_analyses")
    if not isinstance(analyses, list):
        raise AnalysisContractError("reference_analyses must be a list")

    expected_refs = [item["reference_ref"] for item in reference_snapshot["references"]]
    actual_refs = [item.get("reference_ref") for item in analyses if isinstance(item, dict)]
    if sorted(actual_refs) != sorted(expected_refs) or len(actual_refs) != len(set(actual_refs)):
        raise AnalysisContractError("analysis must contain exactly one object per prepared reference")

    for item in analyses:
        if item.get("source_completeness") != "full":
            raise AnalysisContractError("only complete reference snapshots may be analyzed")
        missing = sorted(field for field in _REQUIRED_FIELDS if not _meaningful(item.get(field)))
        if missing:
            raise AnalysisContractError(
                f"reference analysis is missing deep fields: {', '.join(missing)}"
            )
        sections = item["sections"]
        if not all(
            isinstance(section, dict)
            and _meaningful(section.get("section"))
            and _meaningful(section.get("function"))
            for section in sections
        ):
            raise AnalysisContractError("every reference section must state its function")

    synthesis = payload.get("multi_reference_synthesis")
    if len(expected_refs) == 0 and synthesis is not None:
        raise AnalysisContractError("zero-reference analysis must not invent a synthesis")
    if len(expected_refs) >= 2:
        if not isinstance(synthesis, dict) or any(
            not _meaningful(synthesis.get(field))
            for field in ("common_mechanisms", "differences", "conflict_resolution")
        ):
            raise AnalysisContractError("multi-reference analysis requires a complete synthesis")
    return payload
