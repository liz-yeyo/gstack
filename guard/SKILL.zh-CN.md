# /guard 中文阅读版

> 说明：这是中文阅读辅助文件，不参与 gstack 的实际执行。
> 角色定位：完全安全模式
> 对应英文源文件：`guard/SKILL.md`
> 源文件摘要：`6e6f38220c53`
> 生成日期：2026-03-20

## 作用
把 `/careful` 和 `/freeze` 组合到一起，既对危险命令发出警告，又限制编辑范围。适合生产环境、共享环境或任何你想把代理控制得更严格的场景。

## 什么时候用
- 要在高风险环境里工作，并且同时担心误删和误改范围。
- 你说“guard mode”“full safety”“maximum safety”。

## 核心流程
1. 先启用 destructive command 警告机制。
1. 再设置可编辑目录边界，避免范围扩散。
1. 在整个工作流中同时执行这两层保护。

## 关键约束
- 它本质上是 `/careful` + `/freeze` 的组合，适合最严格的控制模式。
- 如果只是想恢复正常编辑，需要 `/unfreeze`。

## 关联 skill
- `/careful`
- `/freeze`
- `/unfreeze`

## 延伸阅读
- [中文技能详解](../docs/skills.zh-CN.md#guard)
