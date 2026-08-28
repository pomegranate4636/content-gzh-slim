# PHASE P3：唯一 Article Context Pack

## 状态

- 当前：Development candidate ready; PM Review pending
- 授权：`EXECUTE_PHASE: P3`
- 上游 Gate：P2 completed，真实 Gate A 已以精确决定 `确认方向` 批准

## 唯一目标

把同一 Run 已批准的方向、冻结候选和少量最终片段装成唯一 `article_context_v1.json`，供未来 Writer 单文件读取。

## 本阶段允许

1. 创建 `content-gzh-context-retriever` 内部 Skill。
2. 创建 approved direction 绑定、冻结片段直取、Context 合同、receipt 最终状态更新和 create-only Context Runtime。
3. 创建 `approved_direction.json` 和唯一 `article_context_v1.json`。
4. 用纯虚构 fixture 测试后，再在已经批准的临时 WorkBuddy Run 中生成真实内容 Context Pack。

## 本阶段禁止

- 不读取或写入真实飞书、Obsidian 后端。
- 不在 Gate A 后重新搜索、替换或追加 04。
- 不把对标全文、作者经历、截图或识别性原句放进 Context Pack。
- 不创建 Source Pack、Writing Packet、Markdown Context 副本或 Reviewer。
- 不创建 Writer、标题、保存、分发或质量检查能力。
- 不安装 Skill，不合并 main，不发布版本，不进入 P4。

## Gate P3

- 只接受专用接口产生的 Gate A 精确批准收据。
- Run、知识库、IP、原始输入、方向版本和冻结候选全部一致。
- 05 第二段最多取少量同一 IP 的已确认片段；`none/unused` 不补造个人内容。
- 03 最终片段只来自 P2 冻结且 Gate A 拟采用的候选，最多 5 个。
- 04 同行最多 3、方法最多 2，必须与已批准 Gate A 完全一致。
- 对标只进入机制和禁止迁移边界，不进入全文、作者事实或图片。
- 正常 Run 只有一份 `article_context_v1.json`；机械重试可核验恢复，不同内容不可覆盖。
- `retrieval_receipt.json` 更新最终选择和 `in_context_pack`，但不能作为 Writer 输入。
- Run 停在 `context_ready`，P4 未启动。

## 开发候选回执

- 候选日期：2026-08-28
- 分支：`feature/content-gzh-slim`
- 候选收据：`phase-receipts/P3-candidate.json`
- 开发测试：30 项通过（10 项 P1、11 项 P2、9 项 P3）
- Skill 校验：`content-gzh-context-retriever` 通过
- 临时真实内容验证：已在获批 WorkBuddy Run 生成唯一 Context Pack，并停在 `context_ready`
- PM Review：待总控执行，开发自检不计入 PM Review
- P3 修复轮：0 次
- P4：未授权、未执行
- deferred issue：P3-D01，多方向 Gate 收据未绑定具体 option 时安全拒绝，不猜选项
