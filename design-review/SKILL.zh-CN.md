# /design-review 中文阅读版

> 说明：这是中文阅读辅助文件，不参与 gstack 的实际执行。
> 角色定位：会改代码的设计审查员
> 对应英文源文件：`design-review/SKILL.md`
> 源文件摘要：`65dc35a69c46`
> 生成日期：2026-03-20

## 作用
对已经实现的界面做设计 QA，找出层级、间距、视觉一致性、AI slop、慢交互等问题，并进入“发现问题 -> 原子修复 -> 截图复验”的闭环。

## 什么时候用
- 页面已经存在，你想做视觉审计和抛光。
- 你说“audit the design”“visual QA”“check if it looks good”。
- 需要 before/after 证据，而不是停留在口头审美建议上。

## 核心流程
1. 用浏览器和源码一起检查现有 UI，定位最影响体验的问题。
1. 逐项修改代码，保持每个修复都是独立、可验证、可回滚的原子变更。
1. 重新截图或重测，确认视觉问题真的被修掉。

## 关键约束
- 它针对的是已实现界面；如果还在规划阶段，先用 `/plan-design-review`。
- 保持原子提交和截图复验是它的重要纪律。

## 关联 skill
- `/plan-design-review`
- `/design-consultation`
- `/qa`

## 延伸阅读
- [中文技能详解](../docs/skills.zh-CN.md#design-review)
