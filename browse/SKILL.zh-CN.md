# /browse 中文阅读版

> 说明：这是中文阅读辅助文件，不参与 gstack 的实际执行。
> 角色定位：QA 浏览器工程师
> 对应英文源文件：`browse/SKILL.md`
> 源文件摘要：`a36691011fdd`
> 生成日期：2026-03-20

## 作用
提供一个持久化的 Chromium 浏览器 CLI，适合做 QA、dogfooding、部署验收、截图、响应式检查、表单与上传测试。它的关键价值是浏览器状态常驻，首条命令负责启动，后续命令通常只需要 100 到 200ms。

## 什么时候用
- 要验证某个页面是否真的能打开、点击、提交和展示正确结果。
- 要做截图、响应式对比、控制台错误检查或网络请求排查。
- 要为 bug 报告补充可视化证据。

## 核心流程
1. 用 `$B goto <url>` 打开页面，再用 `$B snapshot -i` 看页面上哪些元素可交互。
1. 通过 `@eN` / `@cN` 引用去 `click`、`fill`、`hover`、`upload`、`press`，而不是手写脆弱选择器。
1. 配合 `console`、`network`、`dialog`、`snapshot -D` 观察交互前后变化。
1. 需要截图时用 `screenshot` 或 `responsive`，然后把图片读出来给用户确认。

## 关键约束
- 浏览器第一次调用会冷启动，之后复用同一个守护进程。
- 页面导航后旧的 `@e` 引用会失效，需要重新 `snapshot`。
- 如果测试的是登录态页面，通常先搭配 `/setup-browser-cookies`。

## 关联 skill
- `/qa`
- `/qa-only`
- `/setup-browser-cookies`

## 延伸阅读
- [中文技能详解](../docs/skills.zh-CN.md#browse)
