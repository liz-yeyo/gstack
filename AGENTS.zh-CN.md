# gstack - AI 工程工作流

gstack 是一组 `SKILL.md` 文件的集合，用来给 AI agent 在软件开发中赋予结构化角色。每个 skill 都是一种专家：CEO 审查者、工程经理、设计师、QA 负责人、发布工程师、调试器等等。

## 可用技能

技能位于 `.agents/skills/`。通过名字调用它们（例如 `/office-hours`）。

| Skill | 它做什么 |
|-------|----------|
| `/office-hours` | 从这里开始。在你写代码之前重新定义产品想法。 |
| `/plan-ceo-review` | CEO 级计划审查：从需求里找到 10 星产品。 |
| `/plan-eng-review` | 锁定架构、数据流、边界情况和测试。 |
| `/plan-design-review` | 给每个设计维度打 0 到 10 分，并解释 10 分长什么样。 |
| `/design-consultation` | 从零构建完整设计系统。 |
| `/review` | 合并前 PR 审查。找出那些 CI 能过、线上却会出问题的 bug。 |
| `/debug` | 系统化根因调试。没有调查，就不允许修。 |
| `/design-review` | 设计审计 + 原子修复循环。 |
| `/qa` | 打开真实浏览器，找 bug、修 bug，再重新验证。 |
| `/qa-only` | 与 `/qa` 相同，但只出报告，不做代码改动。 |
| `/ship` | 跑测试、做 review、推送并打开 PR。一个命令。 |
| `/document-release` | 让所有文档与你刚 ship 的内容保持一致。 |
| `/retro` | 每周复盘，带按人拆分和连续 ship 记录。 |
| `/browse` | 无头浏览器 - 真实 Chromium、真实点击、每条命令约 100ms。 |
| `/setup-browser-cookies` | 从你的真实浏览器导入 cookie，用于登录态测试。 |
| `/careful` | 在 destructive command 前发出警告（`rm -rf`、`DROP TABLE`、强推）。 |
| `/freeze` | 把编辑锁定在一个目录里。不是提醒，而是硬限制。 |
| `/guard` | 同时开启 careful 与 freeze。 |
| `/unfreeze` | 移除目录编辑限制。 |
| `/gstack-upgrade` | 把 gstack 升级到最新版本。 |

## 构建命令

```bash
bun install              # 安装依赖
bun test                 # 运行测试（免费，<5s）
bun run build            # 生成文档并编译二进制
bun run gen:skill-docs   # 从模板重新生成 SKILL.md 文件
bun run skill:check      # 查看所有技能的健康面板
```

## 关键约定

- `SKILL.md` 文件是从 `.tmpl` 模板**生成**出来的。改模板，不要直接改生成物。
- 运行 `bun run gen:skill-docs --host codex` 来重新生成适配 Codex 的输出。
- `browse` 二进制提供无头浏览器能力。在 skill 中使用 `$B <command>`。
- 安全技能（careful、freeze、guard）使用内联提示文本；执行 destructive operation 前始终要再次确认。
