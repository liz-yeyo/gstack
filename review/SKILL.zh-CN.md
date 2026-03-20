# /review 中文阅读版

> 说明：这是中文阅读辅助文件，不参与 gstack 的实际执行。
> 角色定位：预合并 PR 审查员
> 对应英文源文件：`review/SKILL.md`
> 源文件摘要：`e95b3a5b5ad5`
> 生成日期：2026-03-20

## 作用
对当前分支相对 base branch 的 diff 做结构化代码审查，重点找那些 CI 可能过了、但线上会出问题的风险，例如 SQL/data safety、并发、LLM 信任边界、条件副作用、遗漏测试、范围漂移等。

## 什么时候用
- 代码基本写完，准备合并前做最后质量闸门。
- 你说“review this PR”“code review”“check my diff”。
- 想把“发现问题”升级成“自动修掉一部分问题”。

## 核心流程
1. 先检测 base branch 和当前 diff，判断是否存在范围漂移或遗漏需求。
1. 读取 review checklist，对关键风险类别进行两轮审查。
1. 把发现的问题分类成 AUTO-FIX 或 ASK，先自动修机械问题，再把需要拍板的项打包问用户。
1. 如启用了 Greptile，还会把外部评论纳入同一套修复闭环。

## 关键约束
- 这是 fix-first review，不是只提意见不落地。
- 它重点看 bug、风险、回归和缺失，不以“总结得好不好看”为目标。

## 关联 skill
- `/codex`
- `/ship`

## 延伸阅读
- [中文技能详解](../docs/skills.zh-CN.md#review)
