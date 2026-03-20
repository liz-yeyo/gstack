# Project Memory

## 中文文档同步规则

- 这个仓库的英文 skill 文件仍然是 source of truth；中文文件只做阅读辅助，**不要为了翻译去改动英文原文件**。
- 当前中文阅读版采用“同目录新增 `SKILL.zh-CN.md`”的方式维护，根目录入口也有对应的 `SKILL.zh-CN.md`。
- 批量生成命令：`python3 scripts/gen-zh-skill-docs.py`。
- 技能中文总览文件：
  - `docs/skills.zh-CN.md`
  - `docs/translation-index.zh-CN.md`
- 项目级中文对照文档：
  - `README.zh-CN.md`
  - `AGENTS.zh-CN.md`
  - `ARCHITECTURE.zh-CN.md`

## 什么时候必须同步中文版本

- 任何 `SKILL.md.tmpl` 变化后。
- 任何生成后的 `SKILL.md` 变化后。
- 新增或删除 skill 目录后。
- `README.md`、`AGENTS.md`、`ARCHITECTURE.md`、`CLAUDE.md`、`docs/skills.md`、`scripts/gen-skill-docs.ts` 有显著变化，导致中文说明失真后。

## 同步时的工作约定

- 先更新英文 source，再刷新中文阅读版，不要反过来。
- 翻译工作不能覆盖英文原文件。
- 刷新完 `SKILL.zh-CN.md` 后，顺手检查：
  - `docs/skills.zh-CN.md`
  - `docs/project-overview.zh-CN.md`
  - `docs/translation-index.zh-CN.md`
- 如果 `README.md`、`AGENTS.md`、`ARCHITECTURE.md` 更新了，要同步刷新：
  - `README.zh-CN.md`
  - `AGENTS.zh-CN.md`
  - `ARCHITECTURE.zh-CN.md`
- 如果项目级说明发生变化，要重新导出：
  - `output/doc/gstack-project-overview.zh-CN.docx`
  - `output/pdf/gstack-project-overview.zh-CN.pdf`

## 本仓库当前约定

- 中文文件的目标是帮助中文读者快速理解 skill 的职责、使用时机、工作流和约束。
- 中文文件不是运行时输入；代理实际执行时读取的仍然是英文 `SKILL.md`。
- 当前工作区快照中，源码层有 `codex/` skill，但 `.agents/skills/` 目录里暂未看到对应的 `gstack-codex` 输出；阅读项目时要区分“源码层”和“宿主分发层”。
