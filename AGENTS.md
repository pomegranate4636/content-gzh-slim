# Content GZH Slim 工作规则

## 1. 真相源与阶段授权

- `CONTENT-GZH-SLIM-SPEC.md` 是最高真相源。
- `SLIM-COMPASS.md` 只能压缩和导航，不得发明新要求。
- `project-state.json` 只记录真实状态；`next_phase` 不代表已经授权。
- 每次只执行用户明确授权的一个阶段。
- 没有明确的 `EXECUTE_PHASE: Pn`，只允许读取、评估和更新方案，不得实现下游阶段。

## 2. 仓库边界

- 本仓库独立于 `~/.codex/skills`、Content V2、现役公众号 V1 和任何客户知识库。
- 未到构建安装阶段，不得写入 `~/.codex/skills`。
- 不修改 `shu-gongzhonghao-v1`、`content-slim`、`zsk-router` 或客户 01—05 资产。
- 客户资料、IP 语料、真实正文和测试隐私数据不得提交到本仓库。
- 测试只使用脱敏 fixture 或独立私有临时知识库。

## 3. 反膨胀原则

- 总量预算：1 个公开入口、5 个内部 AI Skill、2 个真人 Gate、1 个正式 Context Pack、0 Reviewer。
- 保存、状态、检索、路径校验和后端读写属于确定性 Runtime，不额外创建 Skill。
- 不增加第二层 Packet、Source Pack、Writing Packet、P0—P9 后处理链或多 Agent 审核链。
- 理论风险先登记；没有真实失败证据，不增加状态、Schema、Artifact、Gate、Skill 或用户字段。
- 每阶段新增内容超过 Master SPEC 预算时立即停止，先请求用户决定。

## 4. 内容与来源边界

- 05 只支撑本次指定 IP；03 支撑业务事实；04 支撑内容方向和表达方法。
- 候选素材不得升级为确认事实。
- IP 资料不足不阻断：提醒并继续，只用已确认片段；必要时降级为无 IP 写法。
- 不得把虚构经历、客户案例、结果数字或第一人称事实写成真实内容。
- 对标只迁移钩子、结构、论证和节奏，不迁移同行身份、经历、案例、专属数据和识别性原句。

## 5. Git 与交付

- 每阶段独立提交，提交信息必须说明阶段和真实范围。
- Gate Review 只审核当前阶段 Diff，不顺手修未来阶段。
- 未经明确授权，不合并、打 Tag、构建、安装或发布。
- 报告必须区分：文件已创建、测试已通过、已推送、已安装、已保存、已发布。
