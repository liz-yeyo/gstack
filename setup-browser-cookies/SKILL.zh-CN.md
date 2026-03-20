# /setup-browser-cookies 中文阅读版

> 说明：这是中文阅读辅助文件，不参与 gstack 的实际执行。
> 角色定位：登录态会话搬运工
> 对应英文源文件：`setup-browser-cookies/SKILL.md`
> 源文件摘要：`d71b2382ea92`
> 生成日期：2026-03-20

## 作用
把你真实浏览器里的 cookie 导入到 gstack 的无头浏览器会话里，让代理能测试登录后的页面，而不必重新走复杂登录流程。

## 什么时候用
- 要测试登录后页面，且不想在 headless 浏览器里重新手输账号密码。
- 你说“import cookies”“authenticate the browser”“login to the site”。

## 核心流程
1. 打开交互式 cookie 选择器，或直接按域名导入。
1. 将解密后的 cookie 注入当前 headless 浏览器上下文。
1. 随后切回 `/browse`、`/qa` 或 `/qa-only` 继续测试真实登录态页面。

## 关键约束
- 第一次读取浏览器 cookie 可能触发系统钥匙串授权。
- 它的职责是搬运登录态，不负责后续测试逻辑。

## 关联 skill
- `/browse`
- `/qa`
- `/qa-only`

## 延伸阅读
- [中文技能详解](../docs/skills.zh-CN.md#setup-browser-cookies)
