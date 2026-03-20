# /careful 中文阅读版

> 说明：这是中文阅读辅助文件，不参与 gstack 的实际执行。
> 角色定位：危险操作防护栏
> 对应英文源文件：`careful/SKILL.md`
> 源文件摘要：`8c77c3a95afd`
> 生成日期：2026-03-20

## 作用
在代理准备执行高风险命令时发出显式警告，例如 `rm -rf`、`DROP TABLE`、强推、`git reset --hard`、`kubectl delete` 等。核心目标是让代理在动手前先停下来，给用户一个明确的确认点。

## 什么时候用
- 在生产环境、共享环境或真实数据环境中工作。
- 你明确说“be careful”“careful mode”“prod mode”。
- 任务里可能涉及删除、重置、回滚或不可逆写操作。

## 核心流程
1. 识别潜在 destructive command。
1. 先说明风险、影响面以及为什么危险，再请求用户确认。
1. 只有在用户明确允许后才继续执行；否则保持只读或寻找更安全的替代方案。

## 关键约束
- `/careful` 是“警告 + 确认”，不是文件范围锁。
- 如果你还想限制编辑目录，需要搭配 `/freeze` 或直接用 `/guard`。

## 关联 skill
- `/freeze`
- `/guard`

## 延伸阅读
- [中文技能详解](../docs/skills.zh-CN.md#careful)
