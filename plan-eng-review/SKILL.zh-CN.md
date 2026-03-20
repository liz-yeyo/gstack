# /plan-eng-review 中文阅读版

> 说明：这是中文阅读辅助文件，不参与 gstack 的实际执行。
> 角色定位：工程经理计划审查
> 对应英文源文件：`plan-eng-review/SKILL.md`
> 源文件摘要：`583f955257fd`
> 生成日期：2026-03-20

## 作用
这个 skill 把产品方向变成可实施的技术方案：架构、数据流、状态机、边界条件、测试覆盖、性能与失败路径。它负责把“想法”收敛成“能安全落地的计划”。

## 什么时候用
- 已经有设计文档或产品方向，准备开始编码。
- 你说“review the architecture”“engineering review”“lock in the plan”。
- 想在开工前提前暴露隐藏假设和测试空洞。

## 核心流程
1. 审视架构、依赖边界、数据流和关键状态转换。
1. 用图和表把抽象描述落成更可验证的执行方案。
1. 输出测试计划和 review readiness 信号，为后面的 `/qa` 做准备。

## 关键约束
- 它关注的是执行计划质量，不直接写功能代码。
- 这是 gstack 里最像“技术评审会”的一个 skill。

## 关联 skill
- `/plan-ceo-review`
- `/plan-design-review`
- `/qa`

## 延伸阅读
- [中文技能详解](../docs/skills.zh-CN.md#plan-eng-review)
