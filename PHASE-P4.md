# PHASE P4：公众号正文、Top 3 标题与 Gate B

## 状态

- 当前：唯一修复轮已完成；PM Recheck pending
- 授权：`EXECUTE_PHASE: P4`
- 上游 Gate：P3 completed，唯一 Article Context Pack 已通过 PM Review

## 唯一目标

只从同一 Run 的唯一 `article_context_v1.json` 生成正文、Top 3 标题和一次 Gate B 展示，并停在 `waiting_final`。

## 本阶段允许

1. 创建 `content-gzh-writer` 与 `content-gzh-headline` 两个内部 Skill。
2. 创建正文、标题、版本化和 Gate B 的确定性 Runtime 与合同。
3. 创建 `draft_vN.md`、`headline_vN.json`，但不创建第二套 Pack 或质量 Review Artifact。
4. 先用纯虚构 fixture 测试，再在已批准的临时 WorkBuddy Run 生成真实内容候选。

## 本阶段禁止

- Writer 不读取知识库、检索器、原路径、第二份 Context 或旧写作链。
- 不重选知识库、IP、方向或 Writer 模式。
- 不调用 AI 味检查、Reviewer、自动润色或旧双标题引擎。
- Gate B 前不批准、不保存、不写飞书或 Obsidian、不生成分发包。
- 不安装 Skill，不合并 main，不发布版本，不进入 P5。

## Gate P4

- Run 必须处于 `context_ready`，且 Context 的 Run、知识库、IP、输入与 Gate A digest 全部一致。
- 首稿 Writer 正式输入文件只有 `article_context_v1.json`；修改稿只额外读取当前正文和一条用户意见。
- `ganhuo/huati` 只执行冻结的一种模式；正文不含标题、分析、状态、来源或保存说明。
- 正文遵守 `must_keep`、`must_avoid` 和事实缺口，不把候选或缺失证据写成完成事实。
- 标题在正文后生成，正好 Top 3；推荐标题必须来自 Top 3。
- Gate B 一次展示完整正文、Top 3、推荐标题、保存预览和事实缺口。
- 只有 SPEC 13.3 的四类精确决定可分类；`不采用`可明确拒绝，泛化修改和空意见 fail-closed。本候选不批准 Gate B，Run 停在 `waiting_final`。

## 开发候选回执

- 候选日期：2026-08-28
- 分支：`feature/content-gzh-slim`
- 候选收据：`phase-receipts/P4-candidate.json`
- 开发测试：39 项通过（10 项 P1、11 项 P2、9 项 P3、9 项 P4）
- Skill 校验：`content-gzh-writer`、`content-gzh-headline` 均通过
- 临时真实内容验证：已从唯一 WorkBuddy Context Pack 生成正文、Top 3 和 Gate B，Run 停在 `waiting_final`
- PM Review：总控已执行唯一 1 次，结论 CHANGES REQUESTED；待唯一 Recheck，不得写为 PASS
- P4 修复轮：1 次，已用完修复预算；只修复 Gate B 决策合同与 SPEC 13.3 不一致
- Gate B：未批准；未保存、未写回知识库、未生成分发包
- P5：未授权、未执行
