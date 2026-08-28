"""Keep all P1 RunStore artifacts under one explicit local root."""

from __future__ import annotations

from pathlib import Path


class PathBoundaryError(ValueError):
    """Raised when an artifact path would leave the configured RunStore root."""


class PathBoundary:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root).expanduser().resolve()

    def child(self, *parts: str) -> Path:
        if not parts or any(not part or Path(part).is_absolute() for part in parts):
            raise PathBoundaryError("artifact path must be relative to the RunStore root")
        candidate = self.root.joinpath(*parts).resolve()
        if candidate != self.root and self.root not in candidate.parents:
            raise PathBoundaryError("artifact path escapes the RunStore root")
        return candidate

