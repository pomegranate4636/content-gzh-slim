from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


def _load(relative: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class UniversalPackageTests(unittest.TestCase):
    def test_installer_resolves_codex_and_workbuddy_homes(self) -> None:
        installer = _load("install.py", "content_gzh_installer_hosts")
        with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(
            installer.Path, "home", return_value=Path("/users/customer")
        ):
            self.assertEqual(installer._default_agent_home("codex"), Path("/users/customer/.codex"))
            self.assertEqual(
                installer._default_agent_home("workbuddy"), Path("/users/customer/.workbuddy")
            )

        with mock.patch.dict(
            os.environ,
            {"CODEX_HOME": "/agents/codex", "WORKBUDDY_HOME": "/agents/workbuddy"},
            clear=True,
        ):
            self.assertEqual(installer._default_agent_home("codex"), Path("/agents/codex"))
            self.assertEqual(
                installer._default_agent_home("workbuddy"), Path("/agents/workbuddy")
            )

    def test_workbuddy_skill_frontmatter_matches_release_version(self) -> None:
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        skill = (ROOT / "workbuddy" / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\n"))
        self.assertIn("name: content-gzh-slim", skill)
        self.assertIn(f"version: {version}", skill)
        self.assertIn("description:", skill)
        self.assertIn("scripts/content-gzh-slim", skill)
        self.assertIn("skills/content-gzh-analyzer/SKILL.md", skill)

    def test_universal_zip_contains_both_host_surfaces_and_verified_manifest(self) -> None:
        builder = ROOT / "tools" / "build_universal_package.py"
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            output = Path(temporary) / "content-gzh-slim.zip"
            completed = subprocess.run(
                [sys.executable, "-B", str(builder), "--output", str(output), "--allow-dirty"],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="strict",
            )
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            self.assertTrue(output.is_file())
            with zipfile.ZipFile(output) as archive:
                names = set(archive.namelist())
                self.assertIn("SKILL.md", names)
                self.assertIn("workbuddy.json", names)
                self.assertIn("install.py", names)
                self.assertIn("scripts/content-gzh-slim", names)
                self.assertIn("runtime/host_cli.py", names)
                for name in (
                    "content-gzh-slim",
                    "content-gzh-analyzer",
                    "content-gzh-context-retriever",
                    "content-gzh-writer",
                    "content-gzh-headline",
                    "content-gzh-distribution-pack",
                ):
                    self.assertIn(f"skills/{name}/SKILL.md", names)
                self.assertFalse(any(name.startswith(".git/") for name in names))
                self.assertFalse(any("phase-receipts/" in name for name in names))
                manifest = json.loads(archive.read("UNIVERSAL-PACKAGE-MANIFEST.json"))
                self.assertEqual(manifest["version"], (ROOT / "VERSION").read_text().strip())
                self.assertEqual(manifest["hosts"], ["codex", "workbuddy"])
                self.assertEqual(manifest["operating_systems"], ["macos", "windows"])
                self.assertEqual(manifest["source_revision"], subprocess.run(
                    ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
                    capture_output=True, text=True, encoding="utf-8"
                ).stdout.strip())
                for relative, expected in manifest["files"].items():
                    import hashlib

                    self.assertEqual(hashlib.sha256(archive.read(relative)).hexdigest(), expected)

    def test_ci_runs_universal_package_on_windows_and_macos(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "universal-package.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("windows-latest", workflow)
        self.assertIn("macos-latest", workflow)
        self.assertIn("test_universal_package", workflow)
        self.assertIn("build_universal_package.py", workflow)


if __name__ == "__main__":
    unittest.main()
