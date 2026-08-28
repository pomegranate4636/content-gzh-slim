# PHASE P6：可选分发包与全链反膨胀验收

## 状态

- 当前：PM Recheck PASS；最终真实矩阵 Gate 待用户授权
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
- 开发测试：59 项通过（P1—P5 49 项回归，P6 10 项）
- Skill 校验：6 个 Skill 全部通过，未超预算
- 分发验证：仅受控 fixture 在精确请求后生成；真实 WorkBuddy Run 未生成分发文件
- P3-D01：已通过可复现三选一 fixture 最小闭环关闭
- P1-D01 / P1-D02：无主链真实失败，未安装依赖、未做审美修复，原样保留
- PM Review：总控已执行唯一 1 次，结论 CHANGES REQUESTED
- P6 修复轮：1 次，已用完修复预算；只修 must_avoid 执行与 save receipt 全字段绑定
- PM Recheck：唯一 1 次，代码结论 PASS；59 项回归与 6 个 Skill 校验通过
- 授权隔离矩阵：3 个真实选题、5 个隔离 Run；覆盖 full IP、有/无对标、none、limited、同库多 IP，全部保存到 `/tmp` 并回读一致
- 反膨胀结果：每个 Run 仅 1 个 Context、2 个测试 Gate、Writer 0 次搜索、Reviewer 0、分发 0
- 飞书边界：按用户授权范围继续使用 fake client；真实飞书保存回读仍是 P7 最终 Definition of Done 前置条件
- 非阻断差异：5000 字偏好的两稿实际约 3868 / 3366 字；P6 不进行第二轮修复，交 P7 真实 Host 验收决定
- P7：等待用户关键授权；未安装、未合并、未发布
