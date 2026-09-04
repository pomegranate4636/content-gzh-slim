# Universal Codex and WorkBuddy package TDD evidence

## Source and user journeys

Journeys were derived from the user request on 2026-09-04.

1. A customer can use one release ZIP with either Codex or WorkBuddy.
2. The same source supports Windows and macOS without embedding a customer path.
3. A WorkBuddy upload sees a root `SKILL.md`, while Codex retains the six-Skill installed package.
4. Every ZIP file is hash-bound to one Git source revision and contains no credentials or customer data.

## RED evidence

Command:

```text
py -X utf8 -B -m unittest tests.test_universal_package -v
```

Initial result: 4 errors. The repository had no WorkBuddy root Skill, host-home resolver, universal ZIP builder, or Windows/macOS CI workflow.

The first WorkBuddy activation integration run then exposed `WinError 206` on a long Windows path. The privacy regression also exposed a JSON-key quoting gap in the first scanner expression. Both failures were preserved as regression tests before the final GREEN run.

The first final-ZIP installation attempt found a third release-only failure: the upload root contained `SKILL.md`, but the archive omitted the committed `workbuddy/SKILL.md` source path required by `release-manifest.json`. The build now retains both the WorkBuddy upload surface and its Git-tracked source mirror.

## GREEN evidence

Command:

```text
py -X utf8 -B tools\verify.py
```

Windows result: PASS, version 1.1.0, 6 Skills, 74 release-manifest files, 86 tests.

The WorkBuddy integration test builds an isolated package, activates it in copy mode, runs the active root launcher, and requires `probe` to return `ready`. The universal ZIP test verifies the WorkBuddy root surface, Codex six-Skill tree, file hashes, source revision, privacy flags, extraction, and probe.

## Test specification

| Guarantee | Evidence | Type | Result |
|---|---|---|---|
| Codex and WorkBuddy resolve separate default homes | `test_installer_resolves_codex_and_workbuddy_homes` | unit | PASS |
| WorkBuddy root frontmatter matches `VERSION` | `test_workbuddy_skill_frontmatter_matches_release_version` | contract | PASS |
| ZIP contains both host surfaces and hash-valid files | `test_universal_zip_contains_both_host_surfaces_and_verified_manifest` | integration | PASS |
| Extracted WorkBuddy package probes without Git | `test_workbuddy_activation_is_self_contained_and_probes_without_git` | integration | PASS |
| Embedded credential assignments fail the build | `test_universal_builder_rejects_embedded_credentials` | security | PASS |
| GitHub CI names Windows and macOS native runners | `test_ci_runs_universal_package_on_windows_and_macos` | structure | PASS |

## Coverage and remaining evidence

`coverage.py` is not installed. Python standard-library `trace` ran all 85 tests from the earlier full pass and showed most runtime modules above 80%, but subprocess-driven CLI modules are undercounted; it is not claimed as an 80% aggregate coverage result. The authoritative local evidence is the 86-test Windows release verification.

Actual macOS runtime evidence is pending the GitHub Actions `macos-latest` job. WorkBuddy UI upload recognition is also pending and must not be inferred from isolated filesystem activation.

## Loop decision

- Decision: `proposal` until GitHub Windows/macOS CI completes, then `writeback` if both pass.
- Writeback targets: installer host contract, WorkBuddy root Skill, deterministic package builder, release manifest, CI matrix, and this regression record.
- Next reuse key: `universal_codex_workbuddy_windows_macos_release_zip`.
