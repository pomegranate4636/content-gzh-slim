# PHASE P9：干货文章人设融合与素材检索修复

## 状态

- 当前：源码实现与本地回归完成；未构建、未安装、未发布
- 授权：`EXECUTE_PHASE: P9`
- RED 检查点：`ef73308`
- GREEN 检查点：`6a99d7a`

## 用户结果

`ganhuo` 继续交付方法、解释、清单和避坑价值，同时使用已批准 IP 的表达方式与专业判断连接读者。Gate A 在进入正文前冻结读者处境、专业判断和用户可执行的核验动作，Writer 不再因“有人设、有观点”而切换为 `huati`。

## 范围

1. `writer_mode` 与 `voice_and_viewpoint` 解耦。
2. Gate A 强制包含 `voice_mode`、`professional_judgments`、`reader_situations`、`verification_actions`。
3. Profile 按章节语义装配身份事实、表达方式、专业判断、读者理解、真实经历和业务边界；每类最多四条，总计最多二十条。
4. `ganhuo` 的主要问题单元使用“读者真实处境→IP 明确判断→专业解释或证据→用户可执行核验动作”，不要求每个自然段机械重复。
5. 飞书04只在 Manifest 指定根下递归两层；03保持直接子级；读取数量预算不变。

## 非目标

- 不修改 `must_keep` / `must_avoid` 合同。
- 不增加 Reviewer、Skill、Gate 或第二份 Context Pack。
- 不读取或修改客户01—05资料。
- 不构建候选、不安装、不打 Tag、不建 Release、不保存或发布内容。

## 验证

- 目标 RED：8项预期失败，分别覆盖 Context 缺字段、Gate A 未拦截缺字段、Profile 未分类、04不递归和 Writer 规则缺失。
- 目标 GREEN：5个测试方法全部通过。
- 全量回归：79个测试全部通过。
- 覆盖率：当前 Python 环境未安装可选 `coverage` 模块，未生成百分比，不擅自安装依赖。
- 发布校验：`tools/verify.py` 因 `release-manifest.json` 尚未重建而拒绝 `runtime/content_source.py`；这是未获授权的构建边界，不代表已生成发布候选。

## 闭环决定

- 决定：`writeback`
- 写回：Master SPEC、Analyzer/Context/Writer 契约、Runtime、Schema、fixtures 和回归测试。
- 下一轮复用键：`ganhuo_persona_viewpoint_and_bounded_feishu04_depth`
