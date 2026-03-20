# gstack / 主入口 中文阅读版

> 说明：这是中文阅读辅助文件，不参与 gstack 的实际执行。
> 角色定位：持久化浏览器入口 + 技能路由器
> 对应英文源文件：`SKILL.md`
> 源文件摘要：`40afb3b99ef9`
> 生成日期：2026-03-20

## 作用
这是整个 gstack 的总入口。它一方面把 `/browse` 的持久化无头浏览器能力暴露给代理，另一方面在用户处于 brainstorming、planning、review、QA、ship 等不同阶段时，主动建议切换到更合适的专用 skill。

## 什么时候用
- 需要真实浏览器去访问页面、点击、截图、做 QA 或验收。
- 需要通过 `$B <command>` 直接控制持久化 Chromium。
- 想知道当前阶段更适合切换到哪一个 gstack 专用 skill。

## 核心流程
1. 先运行统一 preamble，检查版本、会话状态、遥测设置与 AskUserQuestion 规范。
1. 定位 `browse` 二进制并连接到持久化浏览器守护进程，避免每条命令都冷启动浏览器。
1. 使用 `snapshot` 生成 `@e1` / `@c1` 引用，再配合 `click`、`fill`、`console`、`screenshot` 等命令完成交互。
1. 根据用户当前所处阶段，建议使用 `/office-hours`、`/review`、`/qa`、`/ship` 等更专业的技能。

## 关键约束
- 这份中文文件只用于阅读，不会被当成真正可执行的 skill。
- 英文 `SKILL.md` 仍然是运行时的 source of truth。
- 浏览器相关操作优先走 `$B`，不要回退到 `mcp__claude-in-chrome__*`。

## 关联 skill
- `/browse`
- `/office-hours`
- `/review`
- `/qa`
- `/ship`

## 延伸阅读
- [中文技能详解](docs/skills.zh-CN.md#gstack-root)
