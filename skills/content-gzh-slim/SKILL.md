---
name: content-gzh-slim
description: Start, resume, or inspect one content-gzh-slim微信公众号 Run from an explicit Obsidian or Feishu knowledge base, one IP name or none, and article inputs; coordinate deep benchmark analysis, bounded 05→03→04 retrieval, two human Gates, article and title generation, verified save, and an optional distribution pack. Never draft, save, or publish outside this Run.
---

# Content GZH Slim

Use this as the only public entry. It orchestrates one deterministic Run and delegates analysis, Context selection, body writing, headline generation, and optional distribution to the five internal Skills.

## Required input

- `knowledge_base`: one explicit knowledge-base name, link, or path reference.
- `ip`: one explicit IP name, `none`, or `无IP`. Never guess it.
- Optional fields follow the bundled `schemas/task_input.schema.json`.

## Installed workflow

1. Run the bundled `probe` described in [references/runtime-commands.md](references/runtime-commands.md).
2. Resolve exactly the knowledge base and IP named by the user. Do not scan another customer, another knowledge base, or every file.
3. In a private temporary Run workspace outside this repository, prepare a fixture-compatible catalog from authorized source fragments. The internal `fixture://` refs are isolation handles, not claims that the source is synthetic.
4. With an IP, read bounded 05 first, then up to 5 relevant 03 candidates, then up to 3 peer and 2 method candidates from 04. Without an IP, skip 05. Record counts and characters.
5. Prepare full snapshots for 0–5 explicit benchmarks. Never call an abstract or snippet a full article.
6. Invoke `content-gzh-analyzer`, validate its deep analysis, prepare Gate A, show it, and stop.
7. After the user selects an option when needed and replies exactly `确认方向`, record the approval and invoke `content-gzh-context-retriever` once. Runtime creates exactly one `article_context_v1.json`.
8. Invoke `content-gzh-writer` with only that Context, then `content-gzh-headline` with the same Context and current draft. Show Gate B and stop.
9. Only after `确认正文和标题` or an exact `使用标题：...` approval, save through the matching Obsidian or Feishu adapter and verify readback.
10. End the main chain at `saved`. Only an exact later request `生成分发包` may invoke `content-gzh-distribution-pack`; it still does not publish.

The Run freezes one knowledge base, one primary IP or `none`, the task input, and the reference set. Changing any of them creates a different Run. Identical input resumes without repeating completed retrieval or writes.

## Gate boundary

The state machine contains exactly two human waiting states: `waiting_direction` and `waiting_final`. Never bypass either. Ambiguous replies do not approve, generate downstream work, or save. Gate A accepts exact `确认方向`; Gate B accepts exact `确认正文和标题` or `使用标题：<明确标题>`.

## Hard boundaries

- Keep temporary catalogs, source snapshots, Run artifacts, and client idempotency state outside this Git repository.
- The Writer reads one Context Pack and performs zero knowledge-base searches. Do not call a Reviewer, quality checker, old Writer, or title arbitration chain.
- Limited or unavailable IP material never blocks the Run, but must be disclosed; do not invent personal facts, cases, outcomes, or numbers.
- Save is create-only and must pass remote or local readback. Saved never means draft box or published.
- Do not call legacy V1, Content V2, or ZSK.
- Do not copy credentials into the candidate, replace `shu-gongzhonghao-v1`, enter a draft box, or publish.
