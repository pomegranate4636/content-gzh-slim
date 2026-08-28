"""Validate one optional P6 distribution output without changing saved content."""

from __future__ import annotations

from typing import Any

from .approved_direction import canonical_digest


class DistributionContractError(ValueError):
    """Raised when distribution output changes the article or misses platform fields."""


_ROOT_FIELDS = {"wechat_final_title", "xiaohongshu", "wechat_channels", "douyin", "moments"}
_PLATFORM_FIELDS = {"title", "intro", "tags"}


def frozen_distribution_constraints(context: dict[str, Any]) -> dict[str, Any]:
    profile = context.get("selected_05_profile_context", {})
    anchors = profile.get("core_anchors", {}) if isinstance(profile, dict) else {}
    return {
        "ip_status": context.get("ip_identity_and_status", {}).get("status"),
        "voice": anchors.get("voice", "") if isinstance(anchors, dict) else "",
        "content_boundary": (
            anchors.get("content_boundary", "") if isinstance(anchors, dict) else ""
        ),
        "must_avoid": list(context.get("must_avoid", [])),
    }


def validate_distribution_candidate(
    candidate: Any,
    approved_final: dict[str, Any],
    forbidden_phrases: list[str],
) -> dict[str, Any]:
    if not isinstance(candidate, dict) or set(candidate) != _ROOT_FIELDS:
        raise DistributionContractError("distribution output fields are invalid")
    final_title = approved_final["headline"]["final_title"]
    if candidate.get("wechat_final_title") != final_title:
        raise DistributionContractError("distribution may not change the WeChat final title")
    external_texts = []

    def collect_text(value: Any) -> None:
        if isinstance(value, str):
            external_texts.append(value)
        elif isinstance(value, dict):
            for nested in value.values():
                collect_text(nested)
        elif isinstance(value, list):
            for nested in value:
                collect_text(nested)

    collect_text(candidate)
    for phrase in forbidden_phrases:
        if isinstance(phrase, str) and phrase.strip() and any(
            phrase.strip().casefold() in text.casefold() for text in external_texts
        ):
            raise DistributionContractError(
                f"distribution text contains must_avoid phrase: {phrase.strip()}"
            )

    normalized: dict[str, Any] = {"wechat_final_title": final_title}
    for platform in ("xiaohongshu", "wechat_channels", "douyin"):
        value = candidate.get(platform)
        if not isinstance(value, dict) or set(value) != _PLATFORM_FIELDS:
            raise DistributionContractError(f"{platform} fields are invalid")
        title = value.get("title")
        intro = value.get("intro")
        tags = value.get("tags")
        if not isinstance(title, str) or not title.strip():
            raise DistributionContractError(f"{platform} title is empty")
        if not isinstance(intro, str) or not 50 <= len(intro.strip()) <= 100:
            raise DistributionContractError(f"{platform} intro must be 50-100 characters")
        if (
            not isinstance(tags, list)
            or not tags
            or any(not isinstance(tag, str) or not tag.strip() for tag in tags)
            or len(tags) != len(set(tags))
        ):
            raise DistributionContractError(f"{platform} tags are invalid")
        normalized[platform] = {
            "title": title.strip(),
            "intro": intro.strip(),
            "tags": [tag.strip() for tag in tags],
        }
    moments = candidate.get("moments")
    if not isinstance(moments, dict) or set(moments) != {"copy"}:
        raise DistributionContractError("moments output must contain one copy field")
    copy_value = moments.get("copy")
    if not isinstance(copy_value, str) or not copy_value.strip():
        raise DistributionContractError("moments copy is empty")
    normalized["moments"] = {"copy": copy_value.strip()}
    return normalized


def validate_saved_receipt(
    run: dict[str, Any], approved: dict[str, Any], receipt: dict[str, Any]
) -> None:
    semantics = receipt.get("semantics", {})
    expected_backend = approved.get("knowledge_base_identity", {}).get("backend")
    checks = (
        (approved.get("run_id") == run.get("run_id"), "approved_final run_id mismatch"),
        (
            expected_backend == run.get("knowledge_base_identity", {}).get("backend"),
            "approved_final backend mismatch",
        ),
        (
            approved.get("save_target", {}).get("backend") == expected_backend,
            "approved_final save target backend mismatch",
        ),
        (receipt.get("run_id") == run.get("run_id"), "save receipt run_id mismatch"),
        (
            receipt.get("approved_final_digest") == canonical_digest(approved),
            "save receipt approved_final digest mismatch",
        ),
        (receipt.get("backend") == expected_backend, "save receipt backend mismatch"),
        (
            receipt.get("version") == approved.get("draft", {}).get("version"),
            "save receipt draft version mismatch",
        ),
        (
            receipt.get("title") == approved.get("headline", {}).get("final_title"),
            "save receipt final title mismatch",
        ),
        (
            receipt.get("body_digest") == approved.get("draft", {}).get("digest"),
            "save receipt body digest mismatch",
        ),
        (
            receipt.get("context_digest") == approved.get("context_digest"),
            "save receipt Context digest mismatch",
        ),
        (receipt.get("readback_status") == "verified", "save receipt readback is not verified"),
        (semantics.get("saved") is True, "save receipt does not confirm saved"),
        (semantics.get("draftbox") is False, "save receipt incorrectly claims draftbox"),
        (semantics.get("published") is False, "save receipt incorrectly claims published"),
        (
            semantics.get("distribution_generated") is False,
            "save receipt already claims distribution generated",
        ),
    )
    for valid, message in checks:
        if not valid:
            raise DistributionContractError(message)
