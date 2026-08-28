---
name: content-gzh-slim
description: Start or resume a content-gzh-slim公众号 Run from an explicit knowledge-base reference, IP name or none, and article task input. P1 foundation only; do not use it yet for real knowledge-base retrieval, analysis, writing, titles, saving, distribution, or publishing.
---

# Content GZH Slim

Use this entry only to create or resume the deterministic Run that owns one article task.

## Required input

- `knowledge_base`: one explicit knowledge-base name, link, or path reference.
- `ip`: one explicit IP name, `none`, or `无IP`. Never guess it.
- Optional task fields follow `schemas/task_input.schema.json`.

## P1 workflow

1. Validate and normalize the input with `runtime.contracts.validate_task_input`.
2. Resolve only the synthetic fixture metadata with `runtime.fixture_adapter.FixtureAdapter`.
3. Call `runtime.run_store.RunStore.create_or_resume`.
4. Report whether the Run was created or resumed, its current state, and the next valid state.
5. Stop. P1 has no content-producing downstream capability.

The Run freezes one knowledge base and one primary IP or `none`. Changing the knowledge base, IP, original task input, or reference set creates a different Run. A mechanical retry of identical normalized input resumes the existing Run.

## Gate boundary

The state machine contains exactly two human waiting states: `waiting_direction` and `waiting_final`. Never bypass either state. P1 does not generate Gate content or accept real approvals; it only enforces legal state transitions for fixture tests.

## Hard boundaries

- Use fixture metadata only. Do not open real Obsidian, Feishu, customer, 03, 04, or 05 content.
- Do not analyze references, retrieve content, create a Context Pack, write an article, create titles, save, distribute, or publish.
- Do not call legacy V1, Content V2, or ZSK.
- Do not install this Skill from the repository.

