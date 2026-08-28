# PHASE P5：飞书 / Obsidian 安全保存

## 状态

- 当前：唯一修复轮已完成；PM Recheck pending
- 授权：`EXECUTE_PHASE: P5`
- 上游 Gate：P4 completed，用户以精确决定 `确认正文和标题` 批准 Gate B

## 唯一目标

把同一 Run 已批准的当前正文与最终标题锁定为 `approved_final.json`，通过注入式后端 create-only 保存并回读，只有完全一致才生成 `save_receipt.json` 和状态 `saved`。

## 本阶段允许

1. 创建 Obsidian 与 Feishu 两个确定性 Runtime Adapter，不创建新 Skill。
2. 创建 Gate B、版本、digest、标题与目标绑定合同。
3. 创建且只创建 `approved_final.json`、`save_receipt.json` 两个 P5 Run Artifact。
4. 使用虚构 fixture、临时目录和 fake Feishu client 测试。
5. 将已批准 WorkBuddy 样本只保存到 `/tmp` 新建隔离 Obsidian 映射并回读。

## 本阶段禁止

- 不访问真实 Obsidian Vault、飞书、网络或真实凭据。
- 不写 01—05，不接受绝对、父级、越界或未映射目标。
- 不覆盖同名不同内容，不把回读失败冒充 `saved`。
- 不创建 Review、QC、Source Pack、Writing Packet 或分发产物。
- 不进入 P6，不安装、不合并 main、不发布。

## Gate P5

- 同一 Run 必须有唯一精确 Gate B 批准收据并处于 `final_approved`。
- 锁定当前匹配的 `draft_vN.md`、`headline_vN.json`、正文 digest、Context digest 与最终标题。
- `确认正文和标题` 锁定 Gate B 展示的推荐标题；只有 `使用标题：...` 才能改选另一候选或用户新标题。
- backend 与冻结知识库、保存预览和注入 Adapter 完全一致。
- create-only 写入后回读标题、正文、目标、版本和 digest；一致后才进入 `saved`。
- `saved` 明确不等于草稿箱、发布或分发。

## 开发候选回执

- 候选日期：2026-08-28
- 分支：`feature/content-gzh-slim`
- 候选收据：`phase-receipts/P5-candidate.json`
- 开发测试：49 项通过（P1—P4 39 项回归，P5 10 项）
- 后端验证：Obsidian 注入隔离根与 Feishu fake client 均通过 create-only / 回读
- 临时真实验证：WorkBuddy 成稿只保存到 `/tmp` 隔离 Obsidian 映射，回读一致，Run 为 `saved`
- PM Review：总控已执行唯一 1 次，结论 CHANGES REQUESTED；待唯一 Recheck，不得写为 PASS
- P5 修复轮：1 次，已用完修复预算；只修推荐标题授权与 01—05 分隔目录保护
- P6：未授权、未执行
