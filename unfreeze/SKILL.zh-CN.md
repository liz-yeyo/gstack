# /unfreeze 中文阅读版

> 说明：这是中文阅读辅助文件，不参与 gstack 的实际执行。
> 角色定位：解除编辑范围锁
> 对应英文源文件：`unfreeze/SKILL.md`
> 源文件摘要：`7bb33d28bd2b`
> 生成日期：2026-03-20

## 作用
清除由 `/freeze` 或 `/guard` 设置的编辑边界，让代理重新可以在整个仓库范围内工作。

## 什么时候用
- 你已经完成局部调试，准备恢复全局编辑能力。
- 你说“unfreeze”“unlock edits”“allow all edits”。

## 核心流程
1. 读取当前 freeze 边界状态。
1. 移除目录级限制，恢复默认编辑范围。
1. 继续后续更大范围的实现或重构工作。

## 关键约束
- 它只负责解除冻结，不会自动关闭 `/careful` 的风险提醒。

## 关联 skill
- `/freeze`
- `/guard`

## 延伸阅读
- [中文技能详解](../docs/skills.zh-CN.md#unfreeze)
