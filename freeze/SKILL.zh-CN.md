# /freeze 中文阅读版

> 说明：这是中文阅读辅助文件，不参与 gstack 的实际执行。
> 角色定位：编辑范围锁
> 对应英文源文件：`freeze/SKILL.md`
> 源文件摘要：`828f9a9f7e55`
> 生成日期：2026-03-20

## 作用
把本次会话的文件编辑权限锁到某个指定目录，阻止代理顺手去改其它模块。它不是提醒，而是硬性的编辑边界。

## 什么时候用
- 你只想让代理碰某个目录或某个模块。
- 在 debug 期间不希望代理“顺便修别处”。
- 你说“freeze”“only edit this folder”“lock down edits”。

## 核心流程
1. 指定允许编辑的目录边界。
1. 后续所有 Edit/Write 都必须落在该边界内。
1. 如果后续需要扩大范围，再显式解除或切换边界。

## 关键约束
- 它只限制编辑范围，不负责 destructive command 风险提示。
- 用完后通常要搭配 `/unfreeze` 恢复全仓库可编辑状态。

## 关联 skill
- `/guard`
- `/unfreeze`

## 延伸阅读
- [中文技能详解](../docs/skills.zh-CN.md#freeze)
