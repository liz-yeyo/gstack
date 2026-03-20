# gstack

你好，我是 [Garry Tan](https://x.com/garrytan)。我是 [Y Combinator](https://www.ycombinator.com/) 的 President & CEO。在 YC，我曾与数千家创业公司合作过，包括 Coinbase、Instacart 和 Rippling，那时他们的创始人还只是车库里的一两个人，如今这些公司已值数百亿美元。在加入 YC 之前，我设计过 Palantir 的 logo，也是 Palantir 最早的一批工程经理 / PM / 设计师之一。我还是 Posterous 的联合创始人，这个博客平台后来卖给了 Twitter。2013 年，我做了 Bookface，也就是 YC 的内部社交网络。作为设计师、PM 和工程经理，我做产品已经很久了。

而现在，我正处在一个完全像新时代开端的阶段。

在过去 60 天里，我写了 **超过 60 万行生产代码**，其中 35% 是测试；在继续履行 YC CEO 日常职责的同时，我每天还能产出 **1 万到 2 万行可用代码**。这不是笔误。我最近一次 `/retro`（过去 7 天的开发统计）横跨 3 个项目：**新增 140,751 行、362 个 commit、净增约 11.5 万 LOC**。模型每周都在显著变强。我们正站在一个真正的拐点上：一个人就能以过去需要二十人团队才能达到的规模持续交付。

**2026 年 - 目前已有 1,237 次贡献，还在继续：**

![GitHub contributions 2026 — 1,237 contributions, massive acceleration in Jan-Mar](docs/images/github-2026.png)

**2013 年 - 我在 YC 做 Bookface 时（772 次贡献）：**

![GitHub contributions 2013 — 772 contributions building Bookface at YC](docs/images/github-2013.png)

还是同一个人。时代不同了。差别在于工具。

**gstack 就是我做这件事的方法。** 它是我的开源软件工厂。它把 Claude Code 变成一个你真的能管理的虚拟工程团队：一个会重新定义产品的 CEO，一个锁定架构的工程经理，一个能识别 AI slop 的设计师，一个能找出生产 bug 的偏执审查员，一个会打开真实浏览器帮你点完整个应用的 QA 负责人，以及一个负责发 PR 的发布工程师。十五个专家角色，加上六个强力工具，全部以 slash command 的形式提供，全部是 Markdown，**全部免费，MIT 协议，现在就能用。**

截至 2026 年 3 月，我正在探索 agentic systems 能做到什么的边界，而这就是我的实时实验。我把它分享出来，是因为我希望全世界都能一起走上这条路。

Fork 它。改进它。把它变成你的。别酸，欣赏就好。

**这适合谁：**
- **Founders 和 CEOs**，尤其是仍然想亲自 ship 的技术型创始人。这是你像二十人团队一样建产品的方法。
- **第一次使用 Claude Code 的人**。gstack 是最好的起点，因为你拿到的是结构化角色，而不是一块空白提示框。
- **Tech leads 和 staff engineers**。你可以把严格的 review、QA 和发布自动化带进每一个 PR。

## 快速开始：前 10 分钟

1. 安装 gstack（30 秒，见下文）
2. 运行 `/office-hours`，描述你要构建的东西。它会在你写第一行代码之前重构这个问题。
3. 对任意功能想法运行 `/plan-ceo-review`
4. 对任何有改动的分支运行 `/review`
5. 对你的 staging URL 运行 `/qa`
6. 到这里先停。你会知道它是不是你要的东西。

在任何已经配好测试的仓库里，通常 5 分钟内就能得到第一次真正有用的结果。

**如果你只打算再读一个部分，就读这一段。**

## 安装 - 30 秒搞定

**要求：** [Claude Code](https://docs.anthropic.com/en/docs/claude-code)、[Git](https://git-scm.com/)、[Bun](https://bun.sh/) v1.0+

### 第 1 步：安装到你的机器上

打开 Claude Code，把下面这段贴进去，剩下的 Claude 会帮你做完。

> 安装 gstack：运行 **`git clone https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup`**，然后在 `CLAUDE.md` 里加一个 `gstack` 小节，内容包括：所有网页浏览都使用 gstack 的 `/browse`；永远不要使用 `mcp__claude-in-chrome__*` 工具；列出可用技能 `/office-hours`、`/plan-ceo-review`、`/plan-eng-review`、`/plan-design-review`、`/design-consultation`、`/review`、`/ship`、`/browse`、`/qa`、`/qa-only`、`/design-review`、`/setup-browser-cookies`、`/retro`、`/investigate`、`/document-release`、`/codex`、`/careful`、`/freeze`、`/guard`、`/unfreeze`、`/gstack-upgrade`。然后询问用户是否也想把 gstack 加进当前项目，以便团队成员也能用。

### 第 2 步：把它加进你的仓库，让团队成员也能获得它（可选）

> 把 gstack 加进这个项目：运行 **`cp -Rf ~/.claude/skills/gstack .claude/skills/gstack && rm -rf .claude/skills/gstack/.git && cd .claude/skills/gstack && ./setup`**，然后在这个项目的 `CLAUDE.md` 里增加一个 `gstack` 小节，说明：所有网页浏览都使用 gstack 的 `/browse`；永远不要使用 `mcp__claude-in-chrome__*` 工具；列出可用技能 `/office-hours`、`/plan-ceo-review`、`/plan-eng-review`、`/plan-design-review`、`/design-consultation`、`/review`、`/ship`、`/browse`、`/qa`、`/qa-only`、`/design-review`、`/setup-browser-cookies`、`/retro`、`/investigate`、`/document-release`、`/codex`、`/careful`、`/freeze`、`/guard`、`/unfreeze`、`/gstack-upgrade`，并告诉 Claude：如果 gstack 技能不可用，就运行 `cd .claude/skills/gstack && ./setup` 来构建二进制并注册技能。

这里提交进仓库的都是真实文件，不是 submodule，所以 `git clone` 之后就能直接工作。所有内容都在 `.claude/` 里。它不会污染你的 PATH，也不会在后台常驻什么服务。

### Codex、Gemini CLI 或 Cursor

gstack 可以运行在任何支持 [SKILL.md standard](https://github.com/anthropics/claude-code) 的 agent 上。技能放在 `.agents/skills/` 中，会被自动发现。

```bash
git clone https://github.com/garrytan/gstack.git ~/.codex/skills/gstack
cd ~/.codex/skills/gstack && ./setup --host codex
```

或者让 setup 自动检测你已经安装了哪些 agent：

```bash
git clone https://github.com/garrytan/gstack.git ~/gstack
cd ~/gstack && ./setup --host auto
```

它会根据环境安装到 `~/.claude/skills/gstack` 和 / 或 `~/.codex/skills/gstack`。21 个技能都能在所有支持的 agent 上运行。基于 hook 的安全技能（careful、freeze、guard）在非 Claude 宿主上会退化成内联安全提醒文本。

## 看它怎么工作

```
You:    I want to build a daily briefing app for my calendar.
You:    /office-hours
Claude: [asks about the pain — specific examples, not hypotheticals]

You:    Multiple Google calendars, events with stale info, wrong locations.
        Prep takes forever and the results aren't good enough...

Claude: I'm going to push back on the framing. You said "daily briefing
        app." But what you actually described is a personal chief of
        staff AI.
        [extracts 5 capabilities you didn't realize you were describing]
        [challenges 4 premises — you agree, disagree, or adjust]
        [generates 3 implementation approaches with effort estimates]
        RECOMMENDATION: Ship the narrowest wedge tomorrow, learn from
        real usage. The full vision is a 3-month project — start with
        the daily briefing that actually works.
        [writes design doc → feeds into downstream skills automatically]

You:    /plan-ceo-review
        [reads the design doc, challenges scope, runs 10-section review]

You:    /plan-eng-review
        [ASCII diagrams for data flow, state machines, error paths]
        [test matrix, failure modes, security concerns]

You:    Approve plan. Exit plan mode.
        [writes 2,400 lines across 11 files. ~8 minutes.]

You:    /review
        [AUTO-FIXED] 2 issues. [ASK] Race condition → you approve fix.

You:    /qa https://staging.myapp.com
        [opens real browser, clicks through flows, finds and fixes a bug]

You:    /ship
        Tests: 42 → 51 (+9 new). PR: github.com/you/app/pull/42
```

你说“daily briefing app”。代理听完后却说“你在做的是 personal chief of staff AI”，因为它听的是你的真实痛点，而不是你的功能请求。接着它挑战你的前提，生成三种实现路径，推荐最窄的 wedge，再写出一个设计文档，供所有下游 skill 继续使用。八条命令。这不是 copilot。这是一个团队。

## 这条 sprint

gstack 不是一组工具的堆砌，而是一条流程。技能的排列顺序就是一个 sprint 的运行顺序：

**Think → Plan → Build → Review → Test → Ship → Reflect**

每个 skill 都会把结果传给下一个。`/office-hours` 写设计文档，`/plan-ceo-review` 读取它；`/plan-eng-review` 写测试计划，`/qa` 接着使用；`/review` 抓出 bug，`/ship` 验证这些 bug 已经被修复。不会有事情从环节之间漏掉，因为每一步都知道前面发生了什么。

一个 sprint、一个人、一个功能，用 gstack 大约 30 分钟。但真正改变一切的是：你可以同时并行运行 10 到 15 个这样的 sprint。不同功能、不同分支、不同代理，同时推进。这就是我在做本职工作的同时，还能每天 ship 一万多行生产代码的原因。

| Skill | 你的专家 | 他们做什么 |
|-------|----------|-----------|
| `/office-hours` | **YC Office Hours** | 从这里开始。六个高压问题，在你写代码前重新定义你的产品。它会反驳你当前的 framing，挑战前提，生成不同实现路径。设计文档会流向所有下游 skill。 |
| `/plan-ceo-review` | **CEO / Founder** | 重新思考问题。找到需求里隐藏的 10 星产品。四种模式：扩张、选择性扩张、保持范围、范围收缩。 |
| `/plan-eng-review` | **Eng Manager** | 锁定架构、数据流、图、边界情况和测试。把隐藏假设逼出来。 |
| `/plan-design-review` | **Senior Designer** | 给每个设计维度打 0 到 10 分，解释 10 分长什么样，再把计划修改到那个水平。带 AI Slop 检测。交互式，每个设计决策对应一个 AskUserQuestion。 |
| `/design-consultation` | **Design Partner** | 从零构建设计系统。理解设计语境，提出创意风险，生成真实感产品 mockup。设计是所有阶段的中心。 |
| `/review` | **Staff Engineer** | 找出那些 CI 能过、线上却会炸的 bug。自动修掉明显问题，并标记完整性缺口。 |
| `/investigate` | **Debugger** | 系统化根因调试。铁律：没有调查就不允许修。追踪数据流、验证假设，连续失败 3 次就停。 |
| `/design-review` | **Designer Who Codes** | 做和 `/plan-design-review` 一样的审计，但会直接修。原子提交，前后截图对比。 |
| `/qa` | **QA Lead** | 测你的 app、找 bug、原子修复并重新验证。每个修复都会自动生成回归测试。 |
| `/qa-only` | **QA Reporter** | 和 `/qa` 同样的方法论，但只出报告。适合你只想看 bug 报告而不希望改代码。 |
| `/ship` | **Release Engineer** | 同步 main、跑测试、审覆盖率、推送并开 PR。即使你没测试框架，它也能帮你 bootstrapping。一个命令。 |
| `/document-release` | **Technical Writer** | 更新项目文档，让它们与你刚 ship 的内容保持一致。能自动发现 README 过期。 |
| `/retro` | **Eng Manager** | 团队感知的每周复盘。按人拆分、追踪 ship streak、测试健康趋势和成长机会。 |
| `/browse` | **QA Engineer** | 给代理装上眼睛。真实 Chromium、真实点击、真实截图。每个命令约 100ms。 |
| `/setup-browser-cookies` | **Session Manager** | 把你真实浏览器里的 cookie 导入 headless session。用来测试登录态页面。 |

### 强力工具

| Skill | 它做什么 |
|-------|----------|
| `/codex` | **Second Opinion** - 来自 OpenAI Codex CLI 的独立代码审查。三种模式：review（带 pass/fail gate）、对抗式 challenge、开放式咨询。当 `/review` 和 `/codex` 都跑过时，还能做跨模型分析。 |
| `/careful` | **Safety Guardrails** - 在 destructive command 前发出警告（`rm -rf`、`DROP TABLE`、强推）。你说“be careful”即可启用，也可以覆盖任何警告。 |
| `/freeze` | **Edit Lock** - 把编辑限制在一个目录里，避免调试时误改范围外代码。 |
| `/guard` | **Full Safety** - 一个命令同时启用 `/careful` + `/freeze`。生产环境工作时的最强安全模式。 |
| `/unfreeze` | **Unlock** - 移除 `/freeze` 边界。 |
| `/gstack-upgrade` | **Self-Updater** - 把 gstack 升到最新版本。能检测全局安装和 vendored 安装、同步两边，并告诉你发生了什么变化。 |

**[每个 skill 的深度讲解、示例和设计哲学 →](docs/skills.md)**

## 有什么新东西，以及为什么重要

**`/office-hours` 会在你写代码前重新定义产品。** 你说“daily briefing app”。它听的是你真实痛点，反驳当前 framing，告诉你你其实在做的是 personal chief of staff AI，挑战你的前提，并给出三种实现路径和工作量预估。它产出的设计文档会直接流入 `/plan-ceo-review` 和 `/plan-eng-review`，这样后续所有 skill 都是从清晰问题出发，而不是从一个模糊功能请求出发。

**设计是系统中心。** `/design-consultation` 不只是挑字体。它会研究你所在领域已有的东西，提出稳妥选择和更有野心的创意风险，生成贴近真实产品的 mockup，并写出 `DESIGN.md`。随后 `/design-review` 和 `/plan-eng-review` 会继续读取这些设计决策。设计决策会贯穿整个系统。

**`/qa` 是巨大飞跃。** 它让我从同时运行 6 个 worker 提升到 12 个。Claude Code 说出 *"I SEE THE ISSUE"*，然后真的把问题修掉、补回归测试、重新验证，这彻底改变了我的工作方式。代理现在真的有眼睛了。

**智能 review 路由。** 就像一家运转良好的创业公司：CEO 不需要看基础设施 bug，纯后端改动也不一定要走 design review。gstack 会跟踪哪些 review 跑过，自动判断什么最合适，并做出聪明决策。Review Readiness Dashboard 会告诉你 ship 前处于什么状态。

**把所有东西都测起来。** 如果你的项目还没有测试框架，`/ship` 会从零帮你搭。每次 `/ship` 都会产出覆盖率审计。每次 `/qa` 修 bug 都会生成回归测试。目标是 100% 覆盖率 - 这样 vibe coding 才会安全，而不是 yolo coding。

**`/document-release` 就像你一直没有的那位工程师。** 它会读取项目里的每一份文档，对照代码 diff，把漂移的部分全部更新回来。README、ARCHITECTURE、CONTRIBUTING、CLAUDE.md、TODOS 都会自动保持最新。而且现在 `/ship` 还会自动调用它 - 你不需要额外执行命令，文档也能保持同步。

**当 AI 卡住时的浏览器接力。** 遇到 CAPTCHA、鉴权墙或者 MFA？`$B handoff` 会打开一个可见的 Chrome，停在完全相同的页面上，并保留 cookie 和 tab。你解决完问题，告诉 Claude 一声，再运行 `$B resume`，它就会从刚才停下的地方继续。连续失败 3 次后，代理甚至会自动建议这么做。

**多 AI 第二视角。** `/codex` 会从 OpenAI Codex CLI 获得一份独立审查 - 完全不同的 AI，看的是同一份 diff。三种模式：带 pass/fail gate 的代码审查、主动找漏洞的 adversarial challenge、以及带会话连续性的开放式咨询。当 `/review`（Claude）和 `/codex`（OpenAI）都审过同一分支时，你还能得到跨模型分析，看到哪些问题是共识，哪些是各自独有。

**按需启用的安全护栏。** 你说“be careful”，`/careful` 就会在任何 destructive command 前发警告 - `rm -rf`、`DROP TABLE`、强推、`git reset --hard`。`/freeze` 会把编辑锁在一个目录里，让 Claude 调试时不能顺手“修”掉不相干的代码。`/guard` 同时打开两者。`/investigate` 在调查时会自动 freeze 到对应模块。

**主动 skill 建议。** gstack 能感知你现在处在哪个阶段 - brainstorming、review、debug、testing - 然后建议最合适的 skill。不喜欢？说“stop suggesting”，它会跨会话记住。

## 10 到 15 个并行 sprint

只有一个 sprint 时，gstack 已经很强；十个同时跑时，它就变成质变。

[Conductor](https://conductor.build) 能同时运行多个 Claude Code session，每个 session 在隔离工作区里独立运行。一个 session 用 `/office-hours` 讨论新想法，另一个在做 `/review`，第三个在实现功能，第四个在 staging 上跑 `/qa`，还有六个在其他分支上干活。全部同时进行。我经常并行跑 10 到 15 个 sprint - 这已经是目前的实际极限。

之所以能并行，是因为 sprint 本身有结构。没有流程时，十个 agent 只是十个制造混乱的来源；有了 think、plan、build、review、test、ship 这条链路后，每个 agent 都知道自己该做什么、何时停下。你管理它们的方式，就像 CEO 管团队一样：只在真正重要的决策点介入，其余让系统自己运转。

---

## 一起冲浪吧

这是 **免费、MIT 协议、开源、现在就能用** 的。没有 premium 档。没有 waitlist。没有任何附加条件。

我把自己的开发方式开源了，而且我也在这里持续升级这座软件工厂。你可以 fork，改造，变成你自己的系统。这本来就是目的。我希望所有人都能一起上路。

同样的工具，不同的结果，因为 gstack 提供的是结构化角色和 review gate，而不是泛化的 agent 混乱。这个治理层，就是“高速 ship”和“鲁莽 ship”之间的差别。

模型正在飞快变强。现在就弄清楚如何真正和它们协作的人 - 不是浅尝辄止，而是真的把它们用起来的人 - 会获得巨大的优势。现在就是那个窗口。冲吧。

十五个专家角色，六个强力工具。全部是 slash command。全部是 Markdown。全部免费。**[github.com/garrytan/gstack](https://github.com/garrytan/gstack)** - MIT License

> **我们在招人。** 想每天 ship 1 万行以上代码、一起打磨 gstack 吗？
> 来 YC 吧 - [ycombinator.com/software](https://ycombinator.com/software)
> 极具竞争力的薪酬和股权。地点：旧金山 Dogpatch District。

## 文档

| 文档 | 内容 |
|-----|------|
| [Skill Deep Dives](docs/skills.md) | 每个 skill 的理念、示例与工作流（包含 Greptile 集成） |
| [Architecture](ARCHITECTURE.md) | 设计决策与系统内部实现 |
| [Browser Reference](BROWSER.md) | `/browse` 的完整命令参考 |
| [Contributing](CONTRIBUTING.md) | 开发环境、测试、contributor mode 和 dev mode |
| [Changelog](CHANGELOG.md) | 每个版本的新内容 |

## 隐私与遥测

gstack 包含 **自愿开启（opt-in）** 的使用遥测，用来帮助改进项目。具体行为如下：

- **默认关闭。** 除非你明确同意，否则不会向任何地方发送数据。
- **首次运行时，** gstack 会问你是否愿意分享匿名使用数据。你可以拒绝。
- **如果你开启，会发送什么：** skill 名称、耗时、成功 / 失败、gstack 版本、操作系统。就这些。
- **永远不会发送什么：** 代码、文件路径、仓库名、分支名、prompt 或任何用户生成内容。
- **随时关闭：** `gstack-config set telemetry off` 会立刻关闭全部遥测。

数据存储在 [Supabase](https://supabase.com) 上（开源版 Firebase 替代品）。数据表结构在 [`supabase/migrations/001_telemetry.sql`](supabase/migrations/001_telemetry.sql) 里，你可以自己核对到底收集了什么。仓库里提交的 Supabase publishable key 是公开 key（就像 Firebase API key 一样）；真正的访问能力受到 row-level security 策略限制，只允许 insert。

**本地分析始终可用。** 运行 `gstack-analytics` 就能从本地 JSONL 文件里看到你自己的使用仪表盘，不需要任何远端数据。

## 故障排查

**Skill 没显示出来？** `cd ~/.claude/skills/gstack && ./setup`

**`/browse` 失败？** `cd ~/.claude/skills/gstack && bun install && bun run build`

**安装过期？** 运行 `/gstack-upgrade` - 或者在 `~/.gstack/config.yaml` 里设置 `auto_upgrade: true`

**Claude 说它看不到这些 skills？** 确保你的项目 `CLAUDE.md` 里有一段 gstack 配置。可以加上：

```
## gstack
Use /browse from gstack for all web browsing. Never use mcp__claude-in-chrome__* tools.
Available skills: /office-hours, /plan-ceo-review, /plan-eng-review, /plan-design-review,
/design-consultation, /review, /ship, /browse, /qa, /qa-only, /design-review,
/setup-browser-cookies, /retro, /investigate, /document-release, /codex, /careful,
/freeze, /guard, /unfreeze, /gstack-upgrade.
```

## 许可证

MIT。永久免费。去做点东西吧。
