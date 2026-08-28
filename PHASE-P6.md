# PHASE P6：可选分发包与全链反膨胀验收

## 状态

- 当前：Development candidate ready; PM Review pending
- 授权：`EXECUTE_PHASE: P6`
- 上游 Gate：P5 PM Recheck PASS，临时 WorkBuddy Run 已隔离保存并回读

## 唯一目标

创建第 6 个且最后一个 Skill，为已保存文章按显式请求生成版本化分发文案；用受控 fixture 完成 SPEC 25 全链、负面与复杂度矩阵，并关闭 P3-D01 三选一绑定缺口。

## 本阶段允许

1. 创建 `content-gzh-distribution-pack`，Skill 总数固定为 6。
2. 创建显式触发、create-only、版本化的 `distribution_vN.json` Runtime。
3. 在 `waiting_direction` 受控记录用户选择的 `option_id`，随后仍以精确 `确认方向` 批准 Gate A。
4. 使用参数化 fixture 覆盖有/无 IP、有/无方向、有/无对标、limited、隔离、两个保存后端和负面矩阵。
5. 将既有 WorkBuddy 真实证据计为“有 IP + 对标 + Obsidian 隔离保存”，但不为它生成分发包。

## 本阶段禁止

- 没有精确 `生成分发包` 请求时不运行分发。
- 不读取知识库、Profile 原路径或其他未授权桌面样本。
- 不修改正文、公众号最终标题、保存收据或既有真实成稿。
- 不创建第三 Gate、Reviewer、额外 Pack、Manifest 链、配图、口播、草稿箱或发布能力。
- 不进入 P7，不安装、不合并 main、不发布。

## Gate P6

- 分发只接受 `saved` Run 的 `approved_final`、已验证 `save_receipt` 和同一 Context 的少量冻结 IP 禁区。
- 公众号最终标题与正文 digest 原样绑定；分发 Artifact create-only 且可版本化。
- 小红书、视频号、抖音均含标题、50—100 字导语与标签；朋友圈含一版利他转发文案。
- 三选一方向必须先绑定明确 `option_id`，不得默认第一项，也不增加真人 Gate。
- 正常 Run 仍为 1 Run、1 Context、2 Gate、0 Writer 搜索、0 Reviewer，来源与 Skill 总数不超预算。

## 开发候选回执

- 候选日期：2026-08-28
- 分支：`feature/content-gzh-slim`
- 候选收据：`phase-receipts/P6-candidate.json`
- 开发测试：58 项通过（P1—P5 49 项回归，P6 9 项）
- Skill 校验：6 个 Skill 全部通过，未超预算
- 分发验证：仅受控 fixture 在精确请求后生成；真实 WorkBuddy Run 未生成分发文件
- P3-D01：已通过可复现三选一 fixture 最小闭环关闭
- P1-D01 / P1-D02：无主链真实失败，未安装依赖、未做审美修复，原样保留
- PM Review：待总控执行，开发自检不计入 PM Review
- P6 修复轮：0 次
- 真实矩阵缺口：仅一条 WorkBuddy 样本获授权；无 IP、limited、多 IP、Feishu 等真实样本仍待用户授权，不冒充 fixture 为真实
- P7：未授权、未执行
