# /document-release 中文阅读版

> 说明：这是中文阅读辅助文件，不参与 gstack 的实际执行。
> 角色定位：发版后文档维护者
> 对应英文源文件：`document-release/SKILL.md`
> 源文件摘要：`7885bf1e5d35`
> 生成日期：2026-03-20

## 作用
在功能已经实现或准备发版时，回头统一更新项目文档。它会交叉对照代码 diff 与 README、ARCHITECTURE、CONTRIBUTING、CLAUDE、CHANGELOG、TODOS 等文档，减少“代码变了、文档没变”的漂移。

## 什么时候用
- 代码已经合并，或者准备发布时要做文档收尾。
- 你说“update the docs”“sync documentation”“post-ship docs”。
- 担心 README 和实际实现已经不一致。

## 核心流程
1. 先读代码 diff 和已有文档，判断哪些说明已经过期。
1. 把 README、ARCHITECTURE、CONTRIBUTING、CLAUDE、CHANGELOG、TODOS 按照最新行为同步。
1. 必要时顺带更新 `VERSION` 或整理残留 TODO。

## 关键约束
- 它应该建立在代码行为已经稳定的基础上，否则文档会被反复重写。
- 更偏“发布收尾”而不是“设计或实现”。

## 关联 skill
- `/ship`

## 延伸阅读
- [中文技能详解](../docs/skills.zh-CN.md#document-release)
