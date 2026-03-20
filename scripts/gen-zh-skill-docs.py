#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import os
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TODAY = date.today().isoformat()

ROOT_ITEM = {
    "source": "SKILL.md",
    "target": "SKILL.zh-CN.md",
    "anchor": "gstack-root",
    "command": "gstack / 主入口",
    "role": "持久化浏览器入口 + 技能路由器",
    "summary": (
        "这是整个 gstack 的总入口。它一方面把 `/browse` 的持久化无头浏览器能力暴露给代理，"
        "另一方面在用户处于 brainstorming、planning、review、QA、ship 等不同阶段时，"
        "主动建议切换到更合适的专用 skill。"
    ),
    "when": [
        "需要真实浏览器去访问页面、点击、截图、做 QA 或验收。",
        "需要通过 `$B <command>` 直接控制持久化 Chromium。",
        "想知道当前阶段更适合切换到哪一个 gstack 专用 skill。",
    ],
    "workflow": [
        "先运行统一 preamble，检查版本、会话状态、遥测设置与 AskUserQuestion 规范。",
        "定位 `browse` 二进制并连接到持久化浏览器守护进程，避免每条命令都冷启动浏览器。",
        "使用 `snapshot` 生成 `@e1` / `@c1` 引用，再配合 `click`、`fill`、`console`、`screenshot` 等命令完成交互。",
        "根据用户当前所处阶段，建议使用 `/office-hours`、`/review`、`/qa`、`/ship` 等更专业的技能。",
    ],
    "constraints": [
        "这份中文文件只用于阅读，不会被当成真正可执行的 skill。",
        "英文 `SKILL.md` 仍然是运行时的 source of truth。",
        "浏览器相关操作优先走 `$B`，不要回退到 `mcp__claude-in-chrome__*`。",
    ],
    "related": ["/browse", "/office-hours", "/review", "/qa", "/ship"],
}

SKILL_ITEMS = [
    {
        "source": "browse/SKILL.md",
        "target": "browse/SKILL.zh-CN.md",
        "anchor": "browse",
        "command": "/browse",
        "role": "QA 浏览器工程师",
        "summary": (
            "提供一个持久化的 Chromium 浏览器 CLI，适合做 QA、dogfooding、部署验收、截图、"
            "响应式检查、表单与上传测试。它的关键价值是浏览器状态常驻，首条命令负责启动，"
            "后续命令通常只需要 100 到 200ms。"
        ),
        "when": [
            "要验证某个页面是否真的能打开、点击、提交和展示正确结果。",
            "要做截图、响应式对比、控制台错误检查或网络请求排查。",
            "要为 bug 报告补充可视化证据。",
        ],
        "workflow": [
            "用 `$B goto <url>` 打开页面，再用 `$B snapshot -i` 看页面上哪些元素可交互。",
            "通过 `@eN` / `@cN` 引用去 `click`、`fill`、`hover`、`upload`、`press`，而不是手写脆弱选择器。",
            "配合 `console`、`network`、`dialog`、`snapshot -D` 观察交互前后变化。",
            "需要截图时用 `screenshot` 或 `responsive`，然后把图片读出来给用户确认。",
        ],
        "constraints": [
            "浏览器第一次调用会冷启动，之后复用同一个守护进程。",
            "页面导航后旧的 `@e` 引用会失效，需要重新 `snapshot`。",
            "如果测试的是登录态页面，通常先搭配 `/setup-browser-cookies`。",
        ],
        "related": ["/qa", "/qa-only", "/setup-browser-cookies"],
    },
    {
        "source": "careful/SKILL.md",
        "target": "careful/SKILL.zh-CN.md",
        "anchor": "careful",
        "command": "/careful",
        "role": "危险操作防护栏",
        "summary": (
            "在代理准备执行高风险命令时发出显式警告，例如 `rm -rf`、`DROP TABLE`、强推、"
            "`git reset --hard`、`kubectl delete` 等。核心目标是让代理在动手前先停下来，"
            "给用户一个明确的确认点。"
        ),
        "when": [
            "在生产环境、共享环境或真实数据环境中工作。",
            "你明确说“be careful”“careful mode”“prod mode”。",
            "任务里可能涉及删除、重置、回滚或不可逆写操作。",
        ],
        "workflow": [
            "识别潜在 destructive command。",
            "先说明风险、影响面以及为什么危险，再请求用户确认。",
            "只有在用户明确允许后才继续执行；否则保持只读或寻找更安全的替代方案。",
        ],
        "constraints": [
            "`/careful` 是“警告 + 确认”，不是文件范围锁。",
            "如果你还想限制编辑目录，需要搭配 `/freeze` 或直接用 `/guard`。",
        ],
        "related": ["/freeze", "/guard"],
    },
    {
        "source": "codex/SKILL.md",
        "target": "codex/SKILL.zh-CN.md",
        "anchor": "codex",
        "command": "/codex",
        "role": "第二模型意见",
        "summary": (
            "这是 OpenAI Codex CLI 的包装 skill，用来做独立代码审查、对抗式挑战或开放式咨询。"
            "它的价值不在于替代 `/review`，而在于让另一个模型从不同角度看同一段代码。"
        ),
        "when": [
            "你想要一个独立于当前主代理的第二意见。",
            "需要 pass/fail 风格的 diff 审查，或想主动找出代码的脆弱点。",
            "想持续追问一个复杂技术问题，并保留 Codex 会话上下文。",
        ],
        "workflow": [
            "根据目标选择 review、challenge 或 consult 模式。",
            "把当前分支 diff 或问题交给 Codex CLI，收集结构化结论。",
            "如果 `/review` 也跑过，再做一次交叉比对，看哪些问题是交集，哪些是模型特有发现。",
        ],
        "constraints": [
            "它依赖本机已经可用的 Codex CLI 与对应认证状态。",
            "更适合当“第二视角”，不应该取代你对代码和测试的直接验证。",
        ],
        "related": ["/review", "/ship"],
    },
    {
        "source": "design-consultation/SKILL.md",
        "target": "design-consultation/SKILL.zh-CN.md",
        "anchor": "design-consultation",
        "command": "/design-consultation",
        "role": "设计合伙人",
        "summary": (
            "为新产品或新界面建立完整设计系统，包括审美方向、字体、颜色、布局、间距、"
            "动效与视觉语气，并把结果写入 `DESIGN.md`。它关注的是“设计源头”，不是事后修补。"
        ),
        "when": [
            "项目还没有稳定的设计系统或品牌规范。",
            "你说“design system”“brand guidelines”“create DESIGN.md”。",
            "你要从 0 到 1 定义一个产品的视觉语言。",
        ],
        "workflow": [
            "理解产品、用户、品类与竞品背景。",
            "提出安全选项和更有野心的设计风险点，帮助你明确审美方向。",
            "产出字体/配色预览和设计规范，并落成 `DESIGN.md`。",
        ],
        "constraints": [
            "如果是已经上线的站点，优先用 `/plan-design-review` 逆推出现有设计系统。",
            "它更偏“定体系”，上线后的视觉 QA 更适合 `/design-review`。",
        ],
        "related": ["/plan-design-review", "/design-review"],
    },
    {
        "source": "design-review/SKILL.md",
        "target": "design-review/SKILL.zh-CN.md",
        "anchor": "design-review",
        "command": "/design-review",
        "role": "会改代码的设计审查员",
        "summary": (
            "对已经实现的界面做设计 QA，找出层级、间距、视觉一致性、AI slop、慢交互等问题，"
            "并进入“发现问题 -> 原子修复 -> 截图复验”的闭环。"
        ),
        "when": [
            "页面已经存在，你想做视觉审计和抛光。",
            "你说“audit the design”“visual QA”“check if it looks good”。",
            "需要 before/after 证据，而不是停留在口头审美建议上。",
        ],
        "workflow": [
            "用浏览器和源码一起检查现有 UI，定位最影响体验的问题。",
            "逐项修改代码，保持每个修复都是独立、可验证、可回滚的原子变更。",
            "重新截图或重测，确认视觉问题真的被修掉。",
        ],
        "constraints": [
            "它针对的是已实现界面；如果还在规划阶段，先用 `/plan-design-review`。",
            "保持原子提交和截图复验是它的重要纪律。",
        ],
        "related": ["/plan-design-review", "/design-consultation", "/qa"],
    },
    {
        "source": "document-release/SKILL.md",
        "target": "document-release/SKILL.zh-CN.md",
        "anchor": "document-release",
        "command": "/document-release",
        "role": "发版后文档维护者",
        "summary": (
            "在功能已经实现或准备发版时，回头统一更新项目文档。它会交叉对照代码 diff 与 README、"
            "ARCHITECTURE、CONTRIBUTING、CLAUDE、CHANGELOG、TODOS 等文档，减少“代码变了、"
            "文档没变”的漂移。"
        ),
        "when": [
            "代码已经合并，或者准备发布时要做文档收尾。",
            "你说“update the docs”“sync documentation”“post-ship docs”。",
            "担心 README 和实际实现已经不一致。",
        ],
        "workflow": [
            "先读代码 diff 和已有文档，判断哪些说明已经过期。",
            "把 README、ARCHITECTURE、CONTRIBUTING、CLAUDE、CHANGELOG、TODOS 按照最新行为同步。",
            "必要时顺带更新 `VERSION` 或整理残留 TODO。",
        ],
        "constraints": [
            "它应该建立在代码行为已经稳定的基础上，否则文档会被反复重写。",
            "更偏“发布收尾”而不是“设计或实现”。",
        ],
        "related": ["/ship"],
    },
    {
        "source": "freeze/SKILL.md",
        "target": "freeze/SKILL.zh-CN.md",
        "anchor": "freeze",
        "command": "/freeze",
        "role": "编辑范围锁",
        "summary": (
            "把本次会话的文件编辑权限锁到某个指定目录，阻止代理顺手去改其它模块。"
            "它不是提醒，而是硬性的编辑边界。"
        ),
        "when": [
            "你只想让代理碰某个目录或某个模块。",
            "在 debug 期间不希望代理“顺便修别处”。",
            "你说“freeze”“only edit this folder”“lock down edits”。",
        ],
        "workflow": [
            "指定允许编辑的目录边界。",
            "后续所有 Edit/Write 都必须落在该边界内。",
            "如果后续需要扩大范围，再显式解除或切换边界。",
        ],
        "constraints": [
            "它只限制编辑范围，不负责 destructive command 风险提示。",
            "用完后通常要搭配 `/unfreeze` 恢复全仓库可编辑状态。",
        ],
        "related": ["/guard", "/unfreeze"],
    },
    {
        "source": "gstack-upgrade/SKILL.md",
        "target": "gstack-upgrade/SKILL.zh-CN.md",
        "anchor": "gstack-upgrade",
        "command": "/gstack-upgrade",
        "role": "gstack 自升级器",
        "summary": (
            "负责把 gstack 升到最新版本，并区分全局安装与 vendored 安装，避免只更新一半。"
            "它不仅执行升级，还会告诉你发生了什么变化。"
        ),
        "when": [
            "你想更新 gstack 本身，而不是项目业务代码。",
            "你说“upgrade gstack”“update gstack”“get latest version”。",
        ],
        "workflow": [
            "检测当前是全局安装、仓库 vendored 安装，还是两者并存。",
            "执行合适的升级路径，并同步相关安装位置。",
            "输出版本变化和后续需要注意的事项。",
        ],
        "constraints": [
            "这是针对 gstack 本身的维护操作，不是一般的项目依赖升级器。",
        ],
        "related": [],
    },
    {
        "source": "guard/SKILL.md",
        "target": "guard/SKILL.zh-CN.md",
        "anchor": "guard",
        "command": "/guard",
        "role": "完全安全模式",
        "summary": (
            "把 `/careful` 和 `/freeze` 组合到一起，既对危险命令发出警告，又限制编辑范围。"
            "适合生产环境、共享环境或任何你想把代理控制得更严格的场景。"
        ),
        "when": [
            "要在高风险环境里工作，并且同时担心误删和误改范围。",
            "你说“guard mode”“full safety”“maximum safety”。",
        ],
        "workflow": [
            "先启用 destructive command 警告机制。",
            "再设置可编辑目录边界，避免范围扩散。",
            "在整个工作流中同时执行这两层保护。",
        ],
        "constraints": [
            "它本质上是 `/careful` + `/freeze` 的组合，适合最严格的控制模式。",
            "如果只是想恢复正常编辑，需要 `/unfreeze`。",
        ],
        "related": ["/careful", "/freeze", "/unfreeze"],
    },
    {
        "source": "investigate/SKILL.md",
        "target": "investigate/SKILL.zh-CN.md",
        "anchor": "investigate",
        "command": "/investigate",
        "role": "根因分析调试器",
        "summary": (
            "这是系统化 debug skill。它强调先调查和建模，再提出假设，最后才实施修复。"
            "其核心原则是：没有根因就不要修。"
        ),
        "when": [
            "你遇到 bug、异常行为、错误日志或“昨天还好好的，今天坏了”。",
            "你说“debug this”“why is this broken”“root cause analysis”。",
        ],
        "workflow": [
            "先收集复现条件、日志、数据流和相关代码区域。",
            "分析现象，提出有限数量的根因假设并逐步验证。",
            "只有在证据指向清晰根因时，才开始修改代码并验证修复。",
            "如果连续多次修不动，要停下来升级问题，而不是继续盲猜。",
        ],
        "constraints": [
            "禁止盲修和试错式乱改。",
            "它更强调证据链和因果关系，而不是“先改了再说”。",
        ],
        "related": ["/qa", "/review"],
    },
    {
        "source": "office-hours/SKILL.md",
        "target": "office-hours/SKILL.zh-CN.md",
        "anchor": "office-hours",
        "command": "/office-hours",
        "role": "YC Office Hours 合伙人",
        "summary": (
            "这是 gstack 的起点 skill，用来在写代码之前先重新定义问题。"
            "它分创业模式和 builder 模式两条路径，最终产出的是设计文档，而不是代码。"
        ),
        "when": [
            "你有一个新想法，想先想清楚问题、用户和切入点。",
            "你说“brainstorm this”“I have an idea”“office hours”“is this worth building”。",
            "准备进入 `/plan-ceo-review` 或 `/plan-eng-review` 之前。",
        ],
        "workflow": [
            "先读仓库上下文、已有设计文档和最近变更，理解项目背景。",
            "询问你的目标是创业、内部项目、hackathon、开源、学习还是玩一玩，从而切换不同提问方式。",
            "在创业模式下用 6 个高压问题逼出需求真相；在 builder 模式下帮助你找到最酷、最值得做的版本。",
            "把结论写成设计文档，供后续 plan skills 继续使用。",
        ],
        "constraints": [
            "硬性门禁：只产出设计文档，不做实现，不写业务代码。",
            "它的价值是澄清问题，而不是直接跳进开发。",
        ],
        "related": ["/plan-ceo-review", "/plan-eng-review"],
    },
    {
        "source": "plan-ceo-review/SKILL.md",
        "target": "plan-ceo-review/SKILL.zh-CN.md",
        "anchor": "plan-ceo-review",
        "command": "/plan-ceo-review",
        "role": "CEO / Founder 计划审查",
        "summary": (
            "这个 skill 负责重新审视产品方向，找出需求里隐藏的“10 星产品”，并挑战需求背后的前提。"
            "它不是执行层，而是高层产品与范围决策层。"
        ),
        "when": [
            "你觉得当前方案太保守，想“think bigger”。",
            "你说“expand scope”“strategy review”“is this ambitious enough”。",
            "已经有设计文档或初步方案，准备做产品层复盘。",
        ],
        "workflow": [
            "读取设计文档或现有方案，判断真正的产品目标是什么。",
            "根据你选择的模式执行范围扩张、选择性扩张、保持范围或范围收缩。",
            "把每个大改动拆成可以逐一同意或拒绝的决策点，而不是一口气改写整个项目。",
        ],
        "constraints": [
            "它关注“做什么”和“为什么做”，不负责落实现细节。",
            "做完后通常交给 `/plan-eng-review` 继续把想法变成可实施方案。",
        ],
        "related": ["/office-hours", "/plan-eng-review", "/plan-design-review"],
    },
    {
        "source": "plan-design-review/SKILL.md",
        "target": "plan-design-review/SKILL.zh-CN.md",
        "anchor": "plan-design-review",
        "command": "/plan-design-review",
        "role": "规划阶段的设计审稿人",
        "summary": (
            "在还没写代码之前，用设计师视角去挑计划里的空白：信息层级、交互状态、移动端、"
            "可访问性、AI slop 风险等，并把这些缺口补回计划里。"
        ),
        "when": [
            "你已经有方案，但担心 UI/UX 描述太模糊。",
            "你说“review the design plan”“design critique”。",
            "准备编码前，想先把设计决策讲清楚。",
        ],
        "workflow": [
            "按多个设计维度给计划打分，说明“10 分长什么样”。",
            "对明显缺失的部分直接补齐，对存在真实取舍的问题用交互式提问让你拍板。",
            "把修改后的设计结论重新写回计划，供工程实现使用。",
        ],
        "constraints": [
            "它只适用于 plan mode，不适合已经上线的实际页面。",
            "真实页面的视觉 QA 要交给 `/design-review`。",
        ],
        "related": ["/design-consultation", "/design-review", "/plan-eng-review"],
    },
    {
        "source": "plan-eng-review/SKILL.md",
        "target": "plan-eng-review/SKILL.zh-CN.md",
        "anchor": "plan-eng-review",
        "command": "/plan-eng-review",
        "role": "工程经理计划审查",
        "summary": (
            "这个 skill 把产品方向变成可实施的技术方案：架构、数据流、状态机、边界条件、"
            "测试覆盖、性能与失败路径。它负责把“想法”收敛成“能安全落地的计划”。"
        ),
        "when": [
            "已经有设计文档或产品方向，准备开始编码。",
            "你说“review the architecture”“engineering review”“lock in the plan”。",
            "想在开工前提前暴露隐藏假设和测试空洞。",
        ],
        "workflow": [
            "审视架构、依赖边界、数据流和关键状态转换。",
            "用图和表把抽象描述落成更可验证的执行方案。",
            "输出测试计划和 review readiness 信号，为后面的 `/qa` 做准备。",
        ],
        "constraints": [
            "它关注的是执行计划质量，不直接写功能代码。",
            "这是 gstack 里最像“技术评审会”的一个 skill。",
        ],
        "related": ["/plan-ceo-review", "/plan-design-review", "/qa"],
    },
    {
        "source": "qa/SKILL.md",
        "target": "qa/SKILL.zh-CN.md",
        "anchor": "qa",
        "command": "/qa",
        "role": "可修复问题的 QA 负责人",
        "summary": (
            "系统化测试 Web 应用，找到 bug 以后直接进入修复与复验闭环，并为每个修复补回归测试。"
            "它不是只出报告，而是把问题尽量解决掉。"
        ),
        "when": [
            "功能已经做完，想知道到底能不能用。",
            "你说“qa”“test this site”“find bugs”“test and fix”。",
            "需要基于实际 URL 或 feature branch 做完整验证。",
        ],
        "workflow": [
            "先根据 URL 或分支 diff 确定要测的页面、流程和改动范围。",
            "用 `/browse` 去访问真实页面、检查控制台、点击交互、截图留证。",
            "把问题分级后逐个修复，保持原子提交，并在修完后重新验证。",
            "尽可能为修掉的问题补上自动化回归测试。",
        ],
        "constraints": [
            "如果你只想拿 bug 报告、不希望改代码，应改用 `/qa-only`。",
            "它假设项目允许你在发现问题后直接动手修。",
        ],
        "related": ["/qa-only", "/browse", "/ship"],
    },
    {
        "source": "qa-only/SKILL.md",
        "target": "qa-only/SKILL.zh-CN.md",
        "anchor": "qa-only",
        "command": "/qa-only",
        "role": "只报告不修复的 QA 记录员",
        "summary": (
            "使用与 `/qa` 相同的方法去测试站点，但只产出结构化报告、复现步骤、截图和健康分数，"
            "不会改任何代码。"
        ),
        "when": [
            "你想先看 bug 清单，再决定是否修。",
            "你说“qa report only”“test but don't fix”“just report bugs”。",
            "当前会话只允许读，不允许写。",
        ],
        "workflow": [
            "按和 `/qa` 相同的方式探索页面、流程和控制台状态。",
            "记录问题、截图、复现步骤与严重程度。",
            "输出结构化 QA 报告，但到此为止，不进入修复环节。",
        ],
        "constraints": [
            "它绝不会帮你改代码。",
            "如果需要从报告切回修复闭环，再转用 `/qa`。",
        ],
        "related": ["/qa", "/browse"],
    },
    {
        "source": "retro/SKILL.md",
        "target": "retro/SKILL.zh-CN.md",
        "anchor": "retro",
        "command": "/retro",
        "role": "工程周回顾主持人",
        "summary": (
            "分析提交历史、工作模式、代码质量和趋势，形成一份面向个人或团队的工程复盘。"
            "它强调节奏、产出、质量与成长，而不只是简单罗列 commit。"
        ),
        "when": [
            "一周结束、冲刺结束，或者想复盘最近做了什么。",
            "你说“weekly retro”“what did we ship”“engineering retrospective”。",
        ],
        "workflow": [
            "读取最近的提交、作者、测试与代码变化统计。",
            "总结每个人做了什么、哪些模式值得保留、哪里有风险或改进空间。",
            "形成带趋势感的回顾，而不是单次流水账。",
        ],
        "constraints": [
            "它更适合阶段性复盘，不是即时 bug 排查或发布工具。",
        ],
        "related": ["/ship", "/review"],
    },
    {
        "source": "review/SKILL.md",
        "target": "review/SKILL.zh-CN.md",
        "anchor": "review",
        "command": "/review",
        "role": "预合并 PR 审查员",
        "summary": (
            "对当前分支相对 base branch 的 diff 做结构化代码审查，重点找那些 CI 可能过了、"
            "但线上会出问题的风险，例如 SQL/data safety、并发、LLM 信任边界、条件副作用、"
            "遗漏测试、范围漂移等。"
        ),
        "when": [
            "代码基本写完，准备合并前做最后质量闸门。",
            "你说“review this PR”“code review”“check my diff”。",
            "想把“发现问题”升级成“自动修掉一部分问题”。",
        ],
        "workflow": [
            "先检测 base branch 和当前 diff，判断是否存在范围漂移或遗漏需求。",
            "读取 review checklist，对关键风险类别进行两轮审查。",
            "把发现的问题分类成 AUTO-FIX 或 ASK，先自动修机械问题，再把需要拍板的项打包问用户。",
            "如启用了 Greptile，还会把外部评论纳入同一套修复闭环。",
        ],
        "constraints": [
            "这是 fix-first review，不是只提意见不落地。",
            "它重点看 bug、风险、回归和缺失，不以“总结得好不好看”为目标。",
        ],
        "related": ["/codex", "/ship"],
    },
    {
        "source": "setup-browser-cookies/SKILL.md",
        "target": "setup-browser-cookies/SKILL.zh-CN.md",
        "anchor": "setup-browser-cookies",
        "command": "/setup-browser-cookies",
        "role": "登录态会话搬运工",
        "summary": (
            "把你真实浏览器里的 cookie 导入到 gstack 的无头浏览器会话里，"
            "让代理能测试登录后的页面，而不必重新走复杂登录流程。"
        ),
        "when": [
            "要测试登录后页面，且不想在 headless 浏览器里重新手输账号密码。",
            "你说“import cookies”“authenticate the browser”“login to the site”。",
        ],
        "workflow": [
            "打开交互式 cookie 选择器，或直接按域名导入。",
            "将解密后的 cookie 注入当前 headless 浏览器上下文。",
            "随后切回 `/browse`、`/qa` 或 `/qa-only` 继续测试真实登录态页面。",
        ],
        "constraints": [
            "第一次读取浏览器 cookie 可能触发系统钥匙串授权。",
            "它的职责是搬运登录态，不负责后续测试逻辑。",
        ],
        "related": ["/browse", "/qa", "/qa-only"],
    },
    {
        "source": "ship/SKILL.md",
        "target": "ship/SKILL.zh-CN.md",
        "anchor": "ship",
        "command": "/ship",
        "role": "发布工程师",
        "summary": (
            "把“准备上线”的那堆零散动作串成一个工作流：同步 base、跑测试、审 diff、"
            "更新版本与 changelog、提交、推送并创建 PR。"
        ),
        "when": [
            "分支准备好了，想一次性完成发版前后动作。",
            "你说“ship”“deploy”“create a PR”“merge and push”。",
        ],
        "workflow": [
            "识别目标 base branch，并把当前分支同步到合理状态。",
            "执行测试与必要的质量检查，确认 review/QA 闸门状态。",
            "更新 `VERSION`、`CHANGELOG` 等发布相关元数据。",
            "提交、推送并创建 PR，把分散的发布步骤收口到一个流程。",
        ],
        "constraints": [
            "适合在代码与测试已经基本稳定时使用。",
            "如果问题还很多，应先用 `/review` 或 `/qa` 处理，再来 `/ship`。",
        ],
        "related": ["/review", "/qa", "/document-release"],
    },
    {
        "source": "unfreeze/SKILL.md",
        "target": "unfreeze/SKILL.zh-CN.md",
        "anchor": "unfreeze",
        "command": "/unfreeze",
        "role": "解除编辑范围锁",
        "summary": (
            "清除由 `/freeze` 或 `/guard` 设置的编辑边界，让代理重新可以在整个仓库范围内工作。"
        ),
        "when": [
            "你已经完成局部调试，准备恢复全局编辑能力。",
            "你说“unfreeze”“unlock edits”“allow all edits”。",
        ],
        "workflow": [
            "读取当前 freeze 边界状态。",
            "移除目录级限制，恢复默认编辑范围。",
            "继续后续更大范围的实现或重构工作。",
        ],
        "constraints": [
            "它只负责解除冻结，不会自动关闭 `/careful` 的风险提醒。",
        ],
        "related": ["/freeze", "/guard"],
    },
]


def file_hash(relative_path: str) -> str:
    data = (ROOT / relative_path).read_bytes()
    return hashlib.sha256(data).hexdigest()[:12]


def detail_link(target_path: str, anchor: str) -> str:
    parent = (ROOT / target_path).parent
    relative = os.path.relpath(ROOT / "docs/skills.zh-CN.md", parent).replace(os.sep, "/")
    return f"[中文技能详解]({relative}#{anchor})"


def write_text(relative_path: str, content: str) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def render_skill_file(item: dict[str, object]) -> str:
    source = str(item["source"])
    link = detail_link(str(item["target"]), str(item["anchor"]))
    lines = [
        f"# {item['command']} 中文阅读版",
        "",
        "> 说明：这是中文阅读辅助文件，不参与 gstack 的实际执行。",
        f"> 角色定位：{item['role']}",
        f"> 对应英文源文件：`{source}`",
        f"> 源文件摘要：`{file_hash(source)}`",
        f"> 生成日期：{TODAY}",
        "",
        "## 作用",
        str(item["summary"]),
        "",
        "## 什么时候用",
    ]
    lines.extend(f"- {value}" for value in item["when"])
    lines.extend(
        [
            "",
            "## 核心流程",
        ]
    )
    lines.extend(f"1. {value}" for value in item["workflow"])
    lines.extend(
        [
            "",
            "## 关键约束",
        ]
    )
    lines.extend(f"- {value}" for value in item["constraints"])
    related = item["related"]
    if related:
        lines.extend(
            [
                "",
                "## 关联 skill",
            ]
        )
        lines.extend(f"- `{value}`" for value in related)
    lines.extend(
        [
            "",
            "## 延伸阅读",
            f"- {link}",
        ]
    )
    return "\n".join(lines)


def render_skills_doc(items: list[dict[str, object]]) -> str:
    lines = [
        "# gstack 技能深度导读（中文）",
        "",
        "> 说明：这是给中文读者准备的阅读辅助文档，对应英文版 `docs/skills.md` 和各个 `SKILL.md`。",
        "> 它帮助你理解每个 skill 的定位、适用场景和工作方式，但不会参与真正的 skill 执行。",
        f"> 生成日期：{TODAY}",
        "",
        "## 怎么读这份文档",
        "- 如果你想先搞懂整个仓库，而不是逐个看 skill，先看 `docs/project-overview.zh-CN.md`。",
        "- 如果你正在看某个具体 skill，可直接打开同目录下的 `SKILL.zh-CN.md`，再回到这里看更完整的中文说明。",
        "- 英文原文仍然是运行时的 source of truth；中文文档的目标是帮助阅读，不取代源文件。",
        "",
        "## 总览",
        "",
        "| Skill | 角色定位 | 核心作用 |",
        "|------|----------|----------|",
    ]
    for item in items:
        lines.append(f"| `{item['command']}` | {item['role']} | {item['summary']} |")
    for item in items:
        lines.extend(
            [
                "",
                f'<a id="{item["anchor"]}"></a>',
                "",
                f"## `{item['command']}`",
                "",
                f"**角色定位：** {item['role']}",
                "",
                f"**核心作用：** {item['summary']}",
                "",
                "**适用场景：**",
            ]
        )
        lines.extend(f"- {value}" for value in item["when"])
        lines.extend(
            [
                "",
                "**核心流程：**",
            ]
        )
        lines.extend(f"1. {value}" for value in item["workflow"])
        lines.extend(
            [
                "",
                "**关键约束：**",
            ]
        )
        lines.extend(f"- {value}" for value in item["constraints"])
        related = item["related"]
        if related:
            lines.extend(
                [
                    "",
                    "**关联 skill：**",
                ]
            )
            lines.extend(f"- `{value}`" for value in related)
    return "\n".join(lines)


def render_index_doc(items: list[dict[str, object]]) -> str:
    lines = [
        "# 中文技能文档索引",
        "",
        "> 说明：这个索引用于追踪英文 skill 文件和中文阅读版之间的对应关系。",
        f"> 生成日期：{TODAY}",
        "",
        "| 英文源文件 | 中文文件 | 源文件摘要 |",
        "|-----------|----------|------------|",
    ]
    for item in items:
        lines.append(
            f"| `{item['source']}` | `{item['target']}` | `{file_hash(str(item['source']))}` |"
        )
    lines.extend(
        [
            "",
            "## 使用约定",
            "- 英文文件仍然是 source of truth，中文文件只做阅读辅助。",
            "- 当 `SKILL.md.tmpl`、`SKILL.md`、相关架构文档或技能说明变化时，要同步刷新对应中文文件。",
            "- 推荐命令：`python3 scripts/gen-zh-skill-docs.py`。",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    items = [ROOT_ITEM] + SKILL_ITEMS
    for item in items:
        write_text(str(item["target"]), render_skill_file(item))
    write_text("docs/skills.zh-CN.md", render_skills_doc(items))
    write_text("docs/translation-index.zh-CN.md", render_index_doc(items))
    print(f"Generated {len(items)} Chinese skill companion files and 2 docs.")


if __name__ == "__main__":
    main()
