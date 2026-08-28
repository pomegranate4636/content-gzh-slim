---
name: content-gzh-slim
description: Start or resume a content-gzh-slim公众号 Run from an explicit knowledge-base reference, IP name or none, and article task input, then coordinate its human Gates. P2 supports fixture-only Gate A preparation; do not use it yet for real knowledge bases, writing, titles, saving, distribution, or publishing.
---

# Content GZH Slim

Use this entry only to create or resume the deterministic Run that owns one article task.

## Required input

- `knowledge_base`: one explicit knowledge-base name, link, or path reference.
- `ip`: one explicit IP name, `none`, or `无IP`. Never guess it.
- Optional task fields follow `schemas/task_input.schema.json`.

## Current fixture workflow

1. Validate and normalize the input with `runtime.contracts.validate_task_input`.
2. Resolve only synthetic fixture metadata with `runtime.fixture_adapter.FixtureAdapter`.
3. Call `runtime.run_store.RunStore.create_or_resume`.
4. For P2 Gate A preparation, dispatch `content-gzh-analyzer` only after Runtime has prepared bounded 05/03/04 candidates and complete reference snapshots.
5. Display the returned Gate A card and stop at `waiting_direction` for a real user decision.

The Run freezes one knowledge base and one primary IP or `none`. Changing the knowledge base, IP, original task input, or reference set creates a different Run. A mechanical retry of identical normalized input resumes the existing Run without redoing retrieval after the Gate A card exists.

## Gate boundary

The state machine contains exactly two human waiting states: `waiting_direction` and `waiting_final`. Never bypass either state. For Gate A, only the exact reply `确认方向` approves; `需要修改：<具体意见>` requests revision, `不采用` rejects, and all other replies remain unapproved. P2 only prepares the Gate A card and does not approve it.

## Hard boundaries

- Use fixture data only. Do not open real Obsidian, Feishu, customer, 03, 04, or 05 content without a later explicit real-test authorization.
- Do not create a Context Pack, write an article, create titles, save, distribute, or publish.
- Do not call legacy V1, Content V2, or ZSK.
- Do not install this Skill from the repository.
