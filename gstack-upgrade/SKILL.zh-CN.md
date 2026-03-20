# /gstack-upgrade 中文阅读版

> 说明：这是中文阅读辅助文件，不参与 gstack 的实际执行。
> 角色定位：gstack 自升级器
> 对应英文源文件：`gstack-upgrade/SKILL.md`
> 源文件摘要：`af686a45c682`
> 生成日期：2026-03-20

## 作用
负责把 gstack 升到最新版本，并区分全局安装与 vendored 安装，避免只更新一半。它不仅执行升级，还会告诉你发生了什么变化。

## 什么时候用
- 你想更新 gstack 本身，而不是项目业务代码。
- 你说“upgrade gstack”“update gstack”“get latest version”。

## 核心流程
1. 检测当前是全局安装、仓库 vendored 安装，还是两者并存。
1. 执行合适的升级路径，并同步相关安装位置。
1. 输出版本变化和后续需要注意的事项。

## 关键约束
- 这是针对 gstack 本身的维护操作，不是一般的项目依赖升级器。

## 延伸阅读
- [中文技能详解](../docs/skills.zh-CN.md#gstack-upgrade)
