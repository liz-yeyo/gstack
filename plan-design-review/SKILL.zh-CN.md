# /plan-design-review 中文阅读版

> 说明：这是中文阅读辅助文件，不参与 gstack 的实际执行。
> 角色定位：规划阶段的设计审稿人
> 对应英文源文件：`plan-design-review/SKILL.md`
> 源文件摘要：`650662c68b68`
> 生成日期：2026-03-20

## 作用
在还没写代码之前，用设计师视角去挑计划里的空白：信息层级、交互状态、移动端、可访问性、AI slop 风险等，并把这些缺口补回计划里。

## 什么时候用
- 你已经有方案，但担心 UI/UX 描述太模糊。
- 你说“review the design plan”“design critique”。
- 准备编码前，想先把设计决策讲清楚。

## 核心流程
1. 按多个设计维度给计划打分，说明“10 分长什么样”。
1. 对明显缺失的部分直接补齐，对存在真实取舍的问题用交互式提问让你拍板。
1. 把修改后的设计结论重新写回计划，供工程实现使用。

## 关键约束
- 它只适用于 plan mode，不适合已经上线的实际页面。
- 真实页面的视觉 QA 要交给 `/design-review`。

## 关联 skill
- `/design-consultation`
- `/design-review`
- `/plan-eng-review`

## 延伸阅读
- [中文技能详解](../docs/skills.zh-CN.md#plan-design-review)
