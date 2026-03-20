# /ship 中文阅读版

> 说明：这是中文阅读辅助文件，不参与 gstack 的实际执行。
> 角色定位：发布工程师
> 对应英文源文件：`ship/SKILL.md`
> 源文件摘要：`ae8c6b67a727`
> 生成日期：2026-03-20

## 作用
把“准备上线”的那堆零散动作串成一个工作流：同步 base、跑测试、审 diff、更新版本与 changelog、提交、推送并创建 PR。

## 什么时候用
- 分支准备好了，想一次性完成发版前后动作。
- 你说“ship”“deploy”“create a PR”“merge and push”。

## 核心流程
1. 识别目标 base branch，并把当前分支同步到合理状态。
1. 执行测试与必要的质量检查，确认 review/QA 闸门状态。
1. 更新 `VERSION`、`CHANGELOG` 等发布相关元数据。
1. 提交、推送并创建 PR，把分散的发布步骤收口到一个流程。

## 关键约束
- 适合在代码与测试已经基本稳定时使用。
- 如果问题还很多，应先用 `/review` 或 `/qa` 处理，再来 `/ship`。

## 关联 skill
- `/review`
- `/qa`
- `/document-release`

## 延伸阅读
- [中文技能详解](../docs/skills.zh-CN.md#ship)
