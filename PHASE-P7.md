# PHASE P7：构建、项目级安装与真实 Host 验收

## 状态

- 当前：项目级安装 PASS；真实 Run 1 等待用户 Gate B 确认
- 授权：`EXECUTE_PHASE: P7`
- 用户边界：允许构建、项目级安装、一个真实飞书测试文档和两次真实 Run；每次 Gate 逐次人工确认；Review 后停止，不合并、不发布
- 上游 Gate：P6 PM Recheck PASS，3 个授权样本派生 5 个隔离 Run 全部通过

## 唯一目标

把 P1—P6 的 6 个 Skill、Runtime、Schema 和统一启动器打成不含客户数据与凭据的自包含候选包，安装到当前仓库的 `.agents/skills` 测试 Host；完成两次连续真实 Run、一次真实 Obsidian 保存回读、一次真实飞书保存回读，然后执行唯一 PM Review。

## 本阶段允许

1. 更新公开入口，使其描述完整 Slim 主链而非历史 P3 候选。
2. 给 5 个内部 Skill 设置 explicit-only，保持唯一公开入口。
3. 新增统一 Runtime CLI、真实 `lark-cli` 注入客户端和确定性候选构建器。
4. 构建到 Git 忽略的 `.p7-test-host`，把仓库级 `.agents/skills` 软链接到候选包。
5. 两次真实 Run 使用 `/tmp` 私有 bundle 与 RunStore；每次 Gate A、Gate B 都向用户逐次确认。
6. 创建一个飞书测试文档并通过真实回读验证；不复制或保存 lark-cli 凭据。

## 本阶段禁止

- 不写入全局 `~/.codex/skills`，不复制登录凭据。
- 不修改、调用或替换 `shu-gongzhonghao-v1`。
- 不把真实知识库、IP 语料、正文、链接 token 或 Run Artifact 提交到 Git。
- 不创建 Reviewer、第三 Gate、第二 Context Pack、视觉、口播、草稿箱或发布能力。
- 不合并 main、不打 Tag、不发布版本。
- PM Review 后最多一轮最小修复和一次复核；禁止第二轮自动修复。

## Gate P7

- 候选包隐私扫描通过，含 6 个 Skill、Runtime、Schema、单一 launcher，不含测试 fixture、客户数据或凭据。
- 项目级安装后 `content-gzh-slim` 可发现，5 个内部 Skill 不参与隐式路由。
- 两次连续真实 Run 均为 1 Run、1 Context Pack、2 Gate、Writer 0 次知识库搜索、Reviewer 0。
- Obsidian 与飞书各有一条真实 create-only 保存和回读一致证据。
- 保存仍不等于草稿箱或发布，V1 未变化，GitHub 继续 Private。

## 开发候选回执

- 候选日期：2026-08-28
- 基线：`fef2205f175ff9492d3600aefb5487e6e99cceed`
- 分支：`feature/content-gzh-slim`
- 候选收据：`phase-receipts/P7-candidate.json`
- 自动测试：63 项通过（P1—P6 59 项回归，P7 4 项）
- Skill 校验：6 个 Skill 全部通过
- 候选包黑盒：完整 fixture 链经 bundled launcher 保存到隔离 Obsidian 并回读通过
- 真实飞书：CLI 1.0.91、user 身份和文档读写权限已只读核验；尚未创建测试文档
- 项目级安装：候选 `b188329` 已安装到仓库级 `.agents/skills`，隐私扫描与 manifest probe 通过
- 真实 Run 1：Gate A 已由用户确认；已生成 1 Context、5452 字符正文和 Top 3，停在 `waiting_final`；0 Reviewer、0 保存，等待用户 Gate B
- 真实 Run 2、PM Review：尚未执行
