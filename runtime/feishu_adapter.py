"""Feishu save adapter over one injected, controlled client interface."""

from __future__ import annotations

from typing import Any, Protocol

from .obsidian_adapter import SaveAdapterError


class FeishuClient(Protocol):
    def create_document_once(
        self, parent_ref: str, title: str, body: str, metadata: dict[str, Any]
    ) -> str: ...

    def read_document(self, object_ref: str) -> dict[str, Any]: ...


class FeishuAdapter:
    backend = "feishu"

    def __init__(self, client: FeishuClient, target_map: dict[str, str]) -> None:
        self.client = client
        self.target_map = dict(target_map)

    def write_create_only(self, approved: dict[str, Any]) -> dict[str, Any]:
        target_ref = approved["save_target"]["target_ref"]
        parent_ref = self.target_map.get(target_ref)
        if not isinstance(parent_ref, str) or not parent_ref.strip():
            raise SaveAdapterError("Feishu target ref is not in the injected target map")
        if any(part in {"01", "02", "03", "04", "05"} for part in parent_ref.split("/")):
            raise SaveAdapterError("Feishu target map may not write 01-05")
        metadata = {
            "version": approved["draft"]["version"],
            "body_digest": approved["draft"]["digest"],
            "context_digest": approved["context_digest"],
        }
        object_ref = self.client.create_document_once(
            parent_ref,
            approved["headline"]["final_title"],
            approved["draft"]["body"],
            metadata,
        )
        if not isinstance(object_ref, str) or not object_ref:
            raise SaveAdapterError("Feishu client returned no object ref")
        return {"backend": self.backend, "object_ref": object_ref, "created": True}

    def read_back(self, target: dict[str, Any]) -> dict[str, Any]:
        value = self.client.read_document(target.get("object_ref", ""))
        if not isinstance(value, dict):
            raise SaveAdapterError("Feishu readback returned an invalid object")
        return {
            "backend": self.backend,
            "object_ref": target.get("object_ref"),
            "version": value.get("metadata", {}).get("version"),
            "body_digest": value.get("metadata", {}).get("body_digest"),
            "context_digest": value.get("metadata", {}).get("context_digest"),
            "title": value.get("title"),
            "body": value.get("body"),
        }
