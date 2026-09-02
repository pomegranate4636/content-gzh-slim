# Installed runtime commands

Resolve the candidate root as the directory three levels above this Skill folder, then use its single launcher:

```text
<candidate-root>/bin/content-gzh-slim
```

The Host owns all backend access and AI outputs. `--store` is optional and defaults to the current host's persistent Content 公众号 Slim Runs directory.

1. Optional first-time binding: run `configure --knowledge-base ...`; show the zero-write preview, then rerun with its exact `--confirmation`.
2. `start --input ... [--registry ...] [--store ...]`. `--catalog` is only for repository tests.
3. `prepare-gate-a --input ... --analysis ... --direction ... [--store ...]`
4. Stop and show Gate A. After an explicit option and exact approval, use `approve-gate-a`.
5. `build-context --run-id ... --selection ... [--store ...]`; Runtime uses the frozen source catalog and revalidates hashes.
6. Invoke Writer with only `article_context_v1.json`, then Headline with that Context and the current draft.
7. `prepare-gate-b --run-id ... --draft-output ... --headline-output ... [--store ...]`
8. Stop and show Gate B. Only after an exact approval, use `approve-gate-b`.
9. Real Runs use `save --run-id ...`; the adapter and target come only from the frozen Manifest. Legacy fixture save commands remain test compatibility paths.
10. `generate-distribution` is optional and requires the exact request `生成分发包` after save. `status` reports the real Run state. No draft-box or publish command exists.

Run `probe` before the first task. It verifies the package manifest, six Skill files, checksums, and the absence of copied credentials or a V1 replacement claim.
