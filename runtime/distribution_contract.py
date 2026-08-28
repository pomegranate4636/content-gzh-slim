"""Validate one optional P6 distribution output without changing saved content."""

from __future__ import annotations

from typing import Any


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
    candidate: Any, approved_final: dict[str, Any]
) -> dict[str, Any]:
    if not isinstance(candidate, dict) or set(candidate) != _ROOT_FIELDS:
        raise DistributionContractError("distribution output fields are invalid")
    final_title = approved_final["headline"]["final_title"]
    if candidate.get("wechat_final_title") != final_title:
        raise DistributionContractError("distribution may not change the WeChat final title")

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
