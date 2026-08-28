# Content GZH Slim

`content-gzh-slim` 是一套面向多知识库、多项目和多 IP 的微信公众号内容生产系统。

当前仓库已完成 **P1 Runtime 基座与唯一入口候选**：包含未安装的入口 Skill 骨架、输入合同、确定性 RunStore、状态机、路径边界和纯 fixture adapter。尚未读取真实知识库，也未实现内容生产或保存能力。

## 当前真相源

1. `CONTENT-GZH-SLIM-SPEC.md`：Master SPEC，产品与开发的最高真相源。
2. `SLIM-COMPASS.md`：每次执行前的轻量入口，不得新增 Master SPEC 中不存在的要求。
3. `project-state.json`：当前阶段和授权状态。
4. `PHASE-P1.md`：下一阶段实施卡；只有用户明确授权后才能执行。

## 核心结论

- 一套共享的 `content-gzh-slim`，每次任务由提示词注入知识库和 IP。
- 同一知识库可以有多个 IP；同一套流程可以服务多个知识库、项目和 IP。
- 单个 Run 冻结一个知识库和一个主 IP；没有 IP 时显式填写 `无IP`。
- 有 IP 时按 `05 IP → 03 业务知识 → 04 内容方法` 的顺序按需检索，不全量读取。
- 主链只有两次真人确认：方向、正文与标题。
- Writer 只读取一份唯一 Article Context Pack。
- 正文确认后保存回本次指定知识库；全平台分发包是可选支线。
- 现役 `shu-gongzhonghao-v1` 只作为冻结对照组，不在本仓库修改。

## 仓库状态

- Repository visibility：Private
- Implementation：P1 complete and reviewed
- Current phase：P1 Runtime foundation and entry Skill
- Next phase：P2（未授权、未执行）
- Installed：No
- Published：No
