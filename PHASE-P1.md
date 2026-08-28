# PHASE P1：Runtime 基座与唯一入口

## 状态

- 当前：Pending
- 授权：未授权
- 启动口令：`EXECUTE_PHASE: P1`

## 唯一目标

建立独立、可测试但尚不读取真实客户资料的 Runtime 基座和 `content-gzh-slim` 入口骨架。

## 本阶段允许

1. 创建 `skills/content-gzh-slim/` 的最小 Skill 结构。
2. 创建知识库引用、IP 名称、用户输入和 Run 的 Schema。
3. 创建确定性 RunStore、状态机、路径边界和 fixture adapter。
4. 实现两次 Gate 的合法状态，但不实现 Analyzer、检索、Writer、标题、保存和分发内容。
5. 使用纯 fixture 验证：同输入恢复同 Run，不同知识库或 IP 产生不同 Run。

## 本阶段禁止

- 不读取真实飞书、Obsidian 或客户 03/04/05。
- 不创建其他 5 个内部 AI Skill。
- 不生成公众号正文、标题或分发包。
- 不写客户知识库，不安装到 `~/.codex/skills`。
- 不修改现役 V1、Content V2 或 ZSK。
- 不进入 P2。

## Gate P1

只有同时满足以下条件才能申请 Review：

- 唯一入口能创建和恢复一个受控 Run。
- 知识库和 IP 都是本次任务参数，不存在永久客户死绑。
- 同一 Run 冻结一个知识库和一个主 IP 或 `无IP`。
- 两次 Gate 的状态存在，但不可跳过。
- fixture 不含真实客户资料和绝对客户路径。
- 没有越过 Skill 数量和 Runtime 模块预算。
