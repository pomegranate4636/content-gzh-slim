# Installed runtime commands

Resolve the candidate root as the directory three levels above this Skill folder, then use its single launcher:

```text
<candidate-root>/bin/content-gzh-slim
```

The Host owns all backend access and AI outputs. Runtime accepts only explicit files and frozen Run identifiers.

1. `start --input ... --catalog ... --store ...`
2. `prepare-gate-a --input ... --catalog ... --analysis ... --direction ... --store ...`
3. Stop and show Gate A. After an explicit option and exact approval, use `approve-gate-a`.
4. `build-context --run-id ... --catalog ... --selection ... --store ...`
5. Invoke Writer with only `article_context_v1.json`, then Headline with that Context and the current draft.
6. `prepare-gate-b --run-id ... --draft-output ... --headline-output ... --store ...`
7. Stop and show Gate B. Only after an exact approval, use `approve-gate-b`.
8. Use exactly one matching save command: `save-obsidian` or `save-feishu`.
9. `generate-distribution` is optional and requires the exact request `生成分发包` after save.
10. `status` reports the real Run state. Never call a draft box or publish command; none exists.

Run `probe` before the first task. It verifies the package manifest, six Skill files, checksums, and the absence of copied credentials or a V1 replacement claim.
