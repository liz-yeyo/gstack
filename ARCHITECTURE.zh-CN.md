# 架构

这份文档解释的是 gstack **为什么** 要这样构建。关于安装和命令，请看 `CLAUDE.md`。关于参与贡献，请看 `CONTRIBUTING.md`。

## 核心想法

gstack 给 Claude Code 提供了一个持久化浏览器，以及一组带明确立场的工作流技能。浏览器这一层才是难点，其它大部分东西本质上都是 Markdown。

关键洞察是：AI agent 与浏览器交互时，需要 **亚秒级延迟** 和 **持久化状态**。如果每条命令都会冷启动一次浏览器，你每次工具调用都要等 3 到 5 秒；如果浏览器在命令之间死掉，你会丢失 cookie、tab 和登录会话。所以 gstack 运行的是一个长生命周期的 Chromium daemon，由 CLI 通过 localhost HTTP 与它通信。

```
Claude Code                     gstack
─────────                      ──────
                               ┌──────────────────────┐
  Tool call: $B snapshot -i    │  CLI（编译后的二进制）│
  ─────────────────────────→   │  • 读取状态文件       │
                               │  • 向 /command POST   │
                               │    到 localhost:PORT  │
                               └──────────┬───────────┘
                                          │ HTTP
                               ┌──────────▼───────────┐
                               │  Server（Bun.serve） │
                               │  • 分发命令           │
                               │  • 与 Chromium 通信   │
                               │  • 返回纯文本结果     │
                               └──────────┬───────────┘
                                          │ CDP
                               ┌──────────▼───────────┐
                               │  Chromium（headless） │
                               │  • 持久化 tab         │
                               │  • cookie 可延续      │
                               │  • 30 分钟空闲超时    │
                               └───────────────────────┘
```

第一次调用会启动整套系统（约 3 秒）。之后每次调用通常只要 100 到 200ms。

## 为什么选 Bun

Node.js 当然也能做。但在这里，Bun 更合适，主要有四个原因：

1. **可编译二进制。** `bun build --compile` 可以产出一个约 58MB 的单文件可执行程序。运行时不需要 `node_modules`，不需要 `npx`，也不需要配置 PATH。二进制直接可运行。这一点很重要，因为 gstack 是安装到 `~/.claude/skills/` 里的，用户并不会期待自己在这里维护一个 Node.js 项目。

2. **原生 SQLite。** cookie 解密需要直接读取 Chromium 的 SQLite cookie 数据库。Bun 内置了 `new Database()`，不需要 `better-sqlite3`、不需要 native addon 编译，也不需要 gyp。不同机器上少一个坏掉的点。

3. **原生 TypeScript。** 开发时，server 直接以 `bun run server.ts` 启动。不需要额外编译步骤，不需要 `ts-node`，也不需要靠 source map 来调试。编译后的二进制是给部署用的，源文件是给开发用的。

4. **内置 HTTP server。** `Bun.serve()` 足够快、足够简单，不需要 Express 或 Fastify。服务端总共也就十来个路由，引入框架只会增加负担。

真正的瓶颈始终是 Chromium，而不是 CLI 或 server。Bun 的启动速度优势（编译后二进制约 1ms，而 Node 大约 100ms）当然不错，但这不是我们选择它的核心原因。真正关键的是可编译二进制和原生 SQLite。

## 守护进程模型

### 为什么不每条命令都启动一次浏览器？

Playwright 启动 Chromium 大约需要 2 到 3 秒。对于单次截图来说，这还能接受；但如果你要做一场包含 20 多条命令的 QA 会话，光浏览器启动开销就要 40 多秒。更糟的是：命令之间所有状态都会丢掉。cookie、localStorage、登录会话、打开的 tab，统统清空。

守护进程模型带来的结果是：

- **持久化状态。** 登录一次，就能一直保持登录。打开一个 tab，它会一直在那里。localStorage 也会跨命令保留。
- **亚秒级命令。** 第一次调用之后，每条命令都只是一个 HTTP POST。包括 Chromium 真正执行的时间在内，通常往返也只有 100 到 200ms。
- **自动生命周期管理。** 首次使用时自动启动 server，空闲 30 分钟后自动关闭。不需要手动管进程。

### 状态文件

server 会写出 `.gstack/browse.json`（通过临时文件 + rename 原子写入，权限模式 `0o600`）：

```json
{ "pid": 12345, "port": 34567, "token": "uuid-v4", "startedAt": "...", "binaryVersion": "abc123" }
```

CLI 通过这个文件找到 server。如果文件丢失、过期，或者里面记录的 PID 已经死掉了，CLI 就会启动一个新的 server。

### 端口选择

随机选择 10000 到 60000 之间的端口（碰撞时最多重试 5 次）。这意味着 10 个 Conductor 工作区可以零配置、零冲突地各自运行自己的 browse daemon。以前那种扫描 9400 到 9409 的做法，在多工作区场景下经常出问题。

### 版本自动重启

构建时会把 `git rev-parse HEAD` 写进 `browse/dist/.version`。每次 CLI 调用时，如果发现当前二进制版本与正在运行的 server 的 `binaryVersion` 不一致，CLI 就会杀掉旧 server 并启动新 server。这样可以彻底避免“二进制已经更新，但后台跑的还是旧 server”这一类 stale binary 问题 - 只要重新构建，下一条命令就会自动切到新版本。

## 安全模型

### 只绑定 localhost

HTTP server 绑定的是 `localhost`，不是 `0.0.0.0`。外部网络无法访问。

### Bearer token 鉴权

每个 server session 都会生成一个随机 UUID token，并以 `0o600` 权限写入状态文件（只有 owner 可读）。每个 HTTP 请求都必须带上 `Authorization: Bearer <token>`。token 不匹配时，server 会返回 401。

这样可以阻止同一台机器上的其它进程随意访问你的 browse server。cookie picker UI（`/cookie-picker`）和健康检查（`/health`）是例外，它们只在 localhost 上暴露，而且不执行实际命令。

### Cookie 安全

cookie 是 gstack 处理过的最敏感数据。这里的设计是：

1. **访问 Keychain 必须经过用户批准。** 每个浏览器第一次导入 cookie 时，都会触发 macOS Keychain 对话框。用户必须点击 “Allow” 或 “Always Allow”。gstack 不会静默访问凭证。

2. **解密在进程内完成。** cookie 值会在内存中解密（PBKDF2 + AES-128-CBC），加载进 Playwright context，并且不会以明文写回磁盘。cookie picker UI 也不会显示 cookie 值，只显示域名和数量。

3. **数据库只读。** gstack 会先把 Chromium 的 cookie 数据库复制到一个临时文件（避免和正在运行的浏览器争抢 SQLite 锁），然后只读打开。它不会修改你真实浏览器的 cookie 数据库。

4. **密钥缓存按 session 生命周期生存。** Keychain 密码和派生出来的 AES key 只会缓存在 server 存活期间的内存中。server 一旦关闭（空闲超时或显式停止），缓存也随之消失。

5. **日志里不包含 cookie 值。** console、network 和 dialog 日志中都不会记录 cookie 值。`cookies` 命令会输出 cookie 元信息（域名、名称、过期时间），但值会被截断。

### 防止 shell 注入

浏览器注册表（Comet、Chrome、Arc、Brave、Edge）是硬编码的。数据库路径由已知常量拼出来，绝不来自用户输入。Keychain 访问使用的是带显式参数数组的 `Bun.spawn()`，而不是 shell 字符串拼接。

## 引用系统（ref system）

引用（`@e1`、`@e2`、`@c1`）让 agent 可以在不写 CSS selector 或 XPath 的情况下定位页面元素。

### 它是怎么工作的

```
1. Agent 运行：$B snapshot -i
2. Server 调用 Playwright 的 page.accessibility.snapshot()
3. 解析器遍历 ARIA tree，顺序分配引用：@e1、@e2、@e3...
4. 对每个引用，构建一个 Playwright Locator：getByRole(role, { name }).nth(index)
5. 在 BrowserManager 实例上保存 Map<string, RefEntry>（role + name + Locator）
6. 把带注释的树以纯文本形式返回

之后：
7. Agent 运行：$B click @e3
8. Server 将 @e3 解析为 Locator，然后执行 locator.click()
```

### 为什么用 Locator，而不是修改 DOM？

最直觉的做法，是往 DOM 里注入 `data-ref="@e1"` 这类属性。但它会在这些场景下出问题：

- **CSP（Content Security Policy）**。很多生产站点会阻止脚本修改 DOM。
- **React / Vue / Svelte hydration**。框架重渲染时可能把注入属性清掉。
- **Shadow DOM**。外部无法直接伸进去。

Playwright Locator 是独立于 DOM 存在的。它利用的是可访问性树（Chromium 内部维护）和 `getByRole()` 查询。无需修改 DOM，不受 CSP 影响，也不和框架冲突。

### 引用的生命周期

在导航发生时（主 frame 上的 `framenavigated` 事件），所有 ref 都会被清空。这样是对的 - 导航之后，旧 locator 全部过期。agent 必须重新执行 `snapshot` 拿到新的 ref。这是故意的：stale ref 应该明确失败，而不是误点到别的元素。

### stale ref 检测

SPA 可以在不触发 `framenavigated` 的情况下修改 DOM（例如 React Router 跳转、tab 切换、modal 打开）。这会让 ref 失效，即便 URL 没变。为了解决这个问题，`resolveRef()` 在使用任何 ref 之前，都会异步调用一次 `count()`：

```
resolveRef(@e3) → entry = refMap.get("e3")
                → count = await entry.locator.count()
                → if count === 0: throw "Ref @e3 is stale — element no longer exists. Run 'snapshot' to get fresh refs."
                → if count > 0: return { locator }
```

这样只付出约 5ms 的额外开销，就能快速失败，而不用等 Playwright 的 30 秒 action timeout 在缺失元素上耗尽。`RefEntry` 还会同时保存 `role` 和 `name` 元信息，方便错误消息告诉 agent 这个元素原本是什么。

### Cursor-interactive refs（`@c`）

`-C` flag 会找出那些**可点击但不在 ARIA tree 里**的元素，例如设置了 `cursor: pointer` 的元素、带 `onclick` 的元素，或者自定义 `tabindex` 的组件。这些元素会被分配 `@c1`、`@c2` 这类单独命名空间的 ref。这样就能抓住那些框架渲染成 `<div>`、但本质上是按钮的自定义组件。

## 日志架构

有三个环形缓冲区（每个 50,000 条记录，`O(1)` push）：

```
Browser events → CircularBuffer（内存）→ 异步 flush 到 .gstack/*.log
```

console、network 和 dialog 各自拥有独立缓冲区。flush 每秒发生一次 - server 只把上次 flush 之后新增的记录 append 到磁盘。这意味着：

- HTTP 请求处理不会被磁盘 I/O 阻塞
- server 崩溃后日志仍然大多能保住（最多损失 1 秒数据）
- 内存是有上界的（50K × 3 个缓冲区）
- 磁盘文件是 append-only 的，可以被外部工具读取

`console`、`network` 和 `dialog` 命令读取的都是内存缓冲，而不是磁盘文件。磁盘文件主要用于事后分析。

## SKILL.md 模板系统

### 问题

`SKILL.md` 文件负责告诉 Claude 怎样使用 browse 命令。如果文档里列出了一个实际上不存在的 flag，或者漏掉了新增命令，agent 就会报错。手工维护的文档总会和代码漂移。

### 解决方案

```
SKILL.md.tmpl          （人工编写的正文 + 占位符）
       ↓
gen-skill-docs.ts      （从源码元信息中读取数据）
       ↓
SKILL.md               （提交进仓库的自动生成结果）
```

模板里放的是真正需要人来判断的东西：工作流、提示和示例。占位符则在构建时从源码中填充：

| 占位符 | 来源 | 会生成什么 |
|--------|------|-----------|
| `{{COMMAND_REFERENCE}}` | `commands.ts` | 分类后的命令表 |
| `{{SNAPSHOT_FLAGS}}` | `snapshot.ts` | flag 参考与示例 |
| `{{PREAMBLE}}` | `gen-skill-docs.ts` | 启动区块：更新检查、session tracking、contributor mode、AskUserQuestion 格式 |
| `{{BROWSE_SETUP}}` | `gen-skill-docs.ts` | 二进制发现和 setup 指引 |
| `{{BASE_BRANCH_DETECT}}` | `gen-skill-docs.ts` | PR 类技能（ship、review、qa、plan-ceo-review）的动态 base branch 检测 |
| `{{QA_METHODOLOGY}}` | `gen-skill-docs.ts` | `/qa` 与 `/qa-only` 共用 QA 方法论区块 |
| `{{DESIGN_METHODOLOGY}}` | `gen-skill-docs.ts` | `/plan-design-review` 与 `/design-review` 共用设计审计方法论 |
| `{{REVIEW_DASHBOARD}}` | `gen-skill-docs.ts` | `/ship` 预检时的 Review Readiness Dashboard |
| `{{TEST_BOOTSTRAP}}` | `gen-skill-docs.ts` | `/qa`、`/ship`、`/design-review` 的测试框架检测、初始化和 CI/CD 配置 |

这个结构有很强的约束力：只要命令真实存在于代码里，它就会出现在文档中；如果代码里不存在，它就不可能平白出现在文档里。

### preamble

每个 skill 在自身逻辑开始之前，都会先执行一个 `{{PREAMBLE}}` 区块。这个区块用一条 bash 命令处理四件事：

1. **更新检查** - 调用 `gstack-update-check`，如果有新版本就提示。
2. **Session tracking** - touch `~/.gstack/sessions/$PPID`，并统计活跃 session 数（过去两小时内被修改的文件）。当有 3 个以上 session 同时运行时，所有 skill 都会进入 “ELI16 mode” - 因为用户往往在多个窗口来回切换，所以每次提问都要重新把上下文讲清楚。
3. **Contributor mode** - 从配置里读取 `gstack_contributor`。如果为 true，当 gstack 自己行为异常时，agent 会把现场反馈写到 `~/.gstack/contributor-logs/`。
4. **AskUserQuestion 格式** - 统一格式：先交代上下文，再提问题，然后给出 `RECOMMENDATION: Choose X because ___`，最后给出字母选项。所有 skill 一致。

### 为什么把生成结果提交进仓库，而不是运行时动态生成？

有三个原因：

1. **Claude 会在加载 skill 时就读取 `SKILL.md`。** 当用户调用 `/browse` 时，没有额外 build step；文件必须已经存在，而且内容必须正确。
2. **CI 可以校验 freshness。** `gen:skill-docs --dry-run` 加上 `git diff --exit-code`，可以在合并前发现文档是否过期。
3. **Git blame 可追踪。** 你可以看到某条命令是在哪个 commit 里加进来的。

### 模板测试分层

| 层级 | 内容 | 成本 | 速度 |
|------|------|------|------|
| 1 - 静态校验 | 解析 `SKILL.md` 里的每个 `$B` 命令，并与命令注册表比对 | 免费 | <2s |
| 2 - 通过 `claude -p` 做 E2E | 启动真实 Claude session，逐个运行 skill，检查是否报错 | 约 `$3.85` | 约 20 分钟 |
| 3 - LLM 评审 | 让 Sonnet 对文档的清晰度 / 完整性 / 可操作性打分 | 约 `$0.15` | 约 30 秒 |

Tier 1 会在每次 `bun test` 时运行。Tier 2 和 3 只有在 `EVALS=1` 时才会触发。思路是：95% 的问题都先用免费静态检查抓住，只有真正需要判断的地方再用 LLM。

## 命令分发

命令会按副作用分类：

- **READ**（`text`、`html`、`links`、`console`、`cookies` 等）：不修改页面状态。可安全重试。返回页面状态。
- **WRITE**（`goto`、`click`、`fill`、`press` 等）：会修改页面状态。不是幂等操作。
- **META**（`snapshot`、`screenshot`、`tabs`、`chain` 等）：更偏 server 级操作，不太适合归入纯读 / 纯写。

这不只是分类而已，server 真正依赖它来做分发：

```typescript
if (READ_COMMANDS.has(cmd))  → handleReadCommand(cmd, args, bm)
if (WRITE_COMMANDS.has(cmd)) → handleWriteCommand(cmd, args, bm)
if (META_COMMANDS.has(cmd))  → handleMetaCommand(cmd, args, bm, shutdown)
```

`help` 命令会把这三类集合都返回出来，让 agent 可以自己发现系统支持哪些能力。

## 错误处理哲学

错误消息是写给 AI agent 看的，不是写给人类看的。所以每条错误都必须是可操作的：

- `"Element not found"` → `"Element not found or not interactable. Run \`snapshot -i\` to see available elements."`
- `"Selector matched multiple elements"` → `"Selector matched multiple elements. Use @refs from \`snapshot\` instead."`
- 超时 → `"Navigation timed out after 30s. The page may be slow or the URL may be wrong."`

Playwright 的原生错误会经过 `wrapError()` 改写，去掉内部 stack trace，并补上指导信息。agent 读到错误后，应该能在没有人类帮助的情况下知道下一步该做什么。

### 崩溃恢复

server 不会尝试自愈。如果 Chromium 崩了（`browser.on('disconnected')`），server 会立刻退出。CLI 会在下一条命令时发现 server 已死，然后自动重启。相比试图重新接管一个半死不活的浏览器进程，这种方式更简单，也更可靠。

## E2E 测试基础设施

### Session runner（`test/helpers/session-runner.ts`）

E2E 测试通过完全独立的子进程启动 `claude -p` - 而不是走 Agent SDK，因为 Agent SDK 不能嵌套在 Claude Code session 里。runner 的工作包括：

1. 把 prompt 写入临时文件（避免 shell escaping 问题）
2. 启动 `sh -c 'cat prompt | claude -p --output-format stream-json --verbose'`
3. 从 stdout 实时流式读取 NDJSON，展示进度
4. 与可配置超时做 race
5. 把完整 NDJSON transcript 解析成结构化结果

`parseNDJSON()` 是纯函数 - 没有 I/O、没有副作用，因此可以单独测试。

### 可观测性数据流

```
  skill-e2e.test.ts
        │
        │ 生成 runId，并把 testName + runId 传给每次调用
        │
  ┌─────┼──────────────────────────────┐
  │     │                              │
  │  runSkillTest()              evalCollector
  │  (session-runner.ts)         (eval-store.ts)
  │     │                              │
  │  每次工具调用：               每次 addTest()：
  │  ┌──┼──────────┐              savePartial()
  │  │  │          │                   │
  │  ▼  ▼          ▼                   ▼
  │ [HB] [PL]    [NJ]          _partial-e2e.json
  │  │    │        │             （原子覆盖）
  │  │    │        │
  │  ▼    ▼        ▼
  │ e2e-  prog-  {name}
  │ live  ress   .ndjson
  │ .json .log
  │
  │  失败时：
  │  {name}-failure.json
  │
  │  所有文件都在 ~/.gstack-dev/
  │  运行目录：e2e-runs/{runId}/
  │
  │         eval-watch.ts
  │              │
  │        ┌─────┴─────┐
  │     读 HB        读 partial
  │        └─────┬─────┘
  │              ▼
  │        渲染 dashboard
  │        （超过 10 分钟没更新就告警）
```

**职责拆分：** session-runner 负责 heartbeat（当前正在执行哪个测试），eval-store 负责 partial result（已完成测试的状态）。watcher 同时读取两者。两个组件彼此互不了解，只通过文件系统交换数据。

**一切都不致命：** 所有可观测性 I/O 都包在 `try/catch` 里。写入失败永远不会让测试本身失败。真正的 truth source 是测试结果本身；可观测性只是 best-effort。

**机器可读的诊断信息：** 每个测试结果都包含 `exit_reason`（`success`、`timeout`、`error_max_turns`、`error_api`、`exit_code_N`）、`timeout_at_turn` 和 `last_tool_call`。这样你就能直接写出类似下面的 `jq` 查询：

```bash
jq '.tests[] | select(.exit_reason == "timeout") | .last_tool_call' ~/.gstack-dev/evals/_partial-e2e.json
```

### Eval 持久化（`test/helpers/eval-store.ts`）

`EvalCollector` 会累积测试结果，并以两种方式写盘：

1. **增量写入：** `savePartial()` 在每个测试结束后写 `_partial-e2e.json`（原子写：先写 `.tmp`，再 `fs.renameSync`）。即便进程被杀，也能保住进度。
2. **最终写入：** `finalize()` 会写一个带时间戳的 eval 文件（例如 `e2e-20260314-143022.json`）。partial 文件不会被清理，而是和 final 文件一起保留，方便可观测性分析。

`eval:compare` 用来对比两次 eval 运行。`eval:summary` 用来统计 `~/.gstack-dev/evals/` 目录下所有运行结果。

### 测试分层

| 层级 | 内容 | 成本 | 速度 |
|------|------|------|------|
| 1 - 静态校验 | 解析 `$B` 命令、和 registry 比对、可观测性单测 | 免费 | <5s |
| 2 - 通过 `claude -p` 做 E2E | 启动真实 Claude session，运行各个 skill，并扫描错误 | 约 `$3.85` | 约 20 分钟 |
| 3 - LLM 评审 | 让 Sonnet 对文档清晰度 / 完整性 / 可操作性打分 | 约 `$0.15` | 约 30 秒 |

Tier 1 会在每次 `bun test` 时运行。Tier 2 和 Tier 3 只有在 `EVALS=1` 时才会执行。理念仍然一样：95% 的问题先用免费方式抓住，LLM 只用在 judgment call 和集成级测试上。

## 有意不做的事情

- **不做 WebSocket 流式通信。** HTTP 请求 / 响应更简单，可以直接用 curl 调试，也已经足够快。引入 streaming 只会为了边际收益增加复杂度。
- **不做 MCP 协议。** MCP 每次请求都有 JSON schema 开销，还要求持久连接。纯 HTTP + 纯文本输出对 token 更省，也更好调试。
- **不做多用户支持。** 一个工作区一个 server，一个用户。token 鉴权只是 defense-in-depth，不是为了做 multi-tenant。
- **不做 Windows / Linux 的 cookie 解密。** 目前只支持 macOS Keychain。Linux（GNOME Keyring / kwallet）和 Windows（DPAPI）在架构上可行，但尚未实现。
- **不支持 iframe。** Playwright 能处理 iframe，但当前 ref system 还不能跨 frame 工作。这是目前用户最常提的缺失功能。
