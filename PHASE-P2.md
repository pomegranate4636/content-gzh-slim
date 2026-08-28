# PHASE P2：05→03→04 受控检索与深度 Analyzer

## 状态

- 当前：Development candidate ready; PM Review pending
- 授权：`EXECUTE_PHASE: P2`
- 上游 Gate：P1 PASS

## 唯一目标

使用纯虚构 fixture 实现 05→03→04 受控候选检索、显式对标逐篇保真准备和深度拆解、读取收据，以及停在 `waiting_direction` 的可读 Gate A 方向卡。

## 本阶段允许

1. 创建 `content-gzh-analyzer` 内部 Skill。
2. 创建候选检索、reference prep、读取收据和 Gate A Runtime。
3. 为 `reference_snapshot_vN.json`、`analysis_vN.json`、`direction_vN.json` 和 `retrieval_receipt.json` 建立 P2 合同。
4. 用纯虚构 fixture 测试 IP full/limited/unused、读取预算、完整对标和 Gate A。
5. 准备后续真实 Gate A 测试入口说明，但本阶段不选择、不读取真实知识库。

## 本阶段禁止

- 不读取或写入真实飞书、Obsidian、客户 03/04/05。
- 不创建 Article Context Pack。
- 不创建 Context Retriever、Writer、标题、保存或分发 Skill。
- 不批准 Gate A，不进入 P3。
- 不安装 Skill，不修改 P1 的 `P1-D01`、`P1-D02`。
- 不合并 main，不发布版本。

## Gate P2

- 05 第一段先读，且只读本次 IP；limited/unused 提醒后继续。
- 03 候选不超过 5；04 同行候选不超过 3、方法候选不超过 2。
- 候选、Gate A 拟采用项和最终选中状态分层；P2 不宣称已最终选中或进入 Context Pack。
- 0—5 篇显式对标逐篇准备；全文不完整时停止深拆，不把摘要冒充全文。
- 每篇深拆覆盖标题、首屏、读者承诺、结构职责、冲突、论证证据、案例数字、转场、节奏、结尾 CTA、可迁移和禁止迁移项。
- Gate A 可读，模糊回复不算批准，Run 停在 `waiting_direction`。
- 没有 `article_context_v1.json`，没有真实知识库访问。

## 后续真实 Gate A 测试入口

由总控或用户明确提供一个获准测试的知识库、一个 IP 名称或 `无IP`、选题和 0—5 篇对标后，再单独授权真实 Gate A 测试。授权前只使用 `runtime.p2_fixture_entry`；当前代码没有真实后端参数，也不会把 fixture 参数解释成真实路径或飞书 token。

## 开发候选回执

- 候选日期：2026-08-28
- 分支：`feature/content-gzh-slim`
- 候选收据：`phase-receipts/P2-candidate.json`
- 开发测试：21 项通过（含 10 项 P1 回归）
- Skill 校验：`content-gzh-slim`、`content-gzh-analyzer` 均通过
- PM Review：待总控执行，当前开发自检不计入 PM Review
- Gate A：仅生成 fixture 预览，未批准
- P3：未授权、未执行
