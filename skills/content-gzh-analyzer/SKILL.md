---
name: content-gzh-analyzer
description: Deeply analyze 0–5 complete benchmark articles and combine bounded 05/03/04 candidates into a content-gzh-slim Gate A direction. Internal only; does not create Runs, search a knowledge base, write articles or titles, save, or publish.
---

# Content GZH Analyzer

Use only when `content-gzh-slim` supplies one frozen Run, bounded 05/03/04 candidates, and independently prepared reference snapshots.

Before analyzing, read [references/analysis-contract.md](references/analysis-contract.md). Return only:

1. one analysis object satisfying that contract; and
2. one direction template containing one complete option, or exactly three complete options when both topic and user thoughts are insufficient.

If a requested reference is not a complete snapshot, stop and report which source is incomplete. Do not infer the missing body from a title, abstract, or summary.

Do not create or mutate a Run, search any knowledge base, read paths outside the supplied bundle, create an Article Context Pack, write article prose or titles, save, distribute, or publish.
