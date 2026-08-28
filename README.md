# Content GZH Slim

`content-gzh-slim` 是一套面向多知识库、多项目和多 IP 的微信公众号内容生产系统。

当前仓库已形成 **P7 开发候选**：P1—P6 主链、两次真人 Gate、唯一 Context Pack、正文与 Top 3 标题、Obsidian/飞书注入式保存、可选分发包均已实现；P7 正在执行自包含构建、项目级安装和两次真实 Host 验收。

## 当前真相源

1. `CONTENT-GZH-SLIM-SPEC.md`：Master SPEC，产品与开发的最高真相源。
2. `SLIM-COMPASS.md`：每次执行前的轻量入口，不得新增 Master SPEC 中不存在的要求。
3. `project-state.json`：当前阶段和授权状态。
4. `PHASE-P7.md`：当前阶段实施卡；记录授权、安装、真实 Run 和 Review 边界。

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
- Implementation：P7 development candidate; 63 tests passed
- Current phase：P7 build and project-level installed-host validation
- Next action：等待真实 Run 1 的 Gate B 确认，随后保存到 `/tmp` 隔离 Obsidian 并回读
- Installed：Yes，项目级测试 Host；未写入全局 Skill
- Published：No
