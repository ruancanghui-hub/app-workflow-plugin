---
name: create-flutter-app
description: >-
  用标准 Flutter SDK 或用户提供的团队模板创建新 App 工程。
  Use when the user wants a new Flutter project or the workflow reaches the scaffold phase.
---

# 创建 Flutter App

## 输入

- 项目工作区与一个尚不存在的输出目录。默认 `apps/<product_slug>/`。
- Dart 包名与产品 slug 一致，使用 ASCII 小写 snake_case。
- 目标平台来自 handoff。组织域与展示名称按用户提供的值配置，发版用组织域须确认。
- 若用户指定现有团队模板，按其文档创建实例。使用兼容的 GetX 团队模板时参考 [团队模板](team-template.md)。

## 标准脚手架

在项目工作区运行，将示例包名、组织域和平台列表换成实际值：

```bash
flutter create --project-name sample_app --org com.example --platforms=ios,android apps/sample_app
cd apps/sample_app
flutter analyze
flutter test
flutter run
```

按目标选择 `ios`、`android` 或 `ios,android`。使用平台原生配置设置展示名称，接入已审批的图标和启动图。标准工程的运行与发布采用默认配置。选用团队模板时，按模板实际配置选用 Dev / Prod flavor。

## 验收与交接

- 确认目标 Flutter 文件存在，分析和测试通过。
- 记录 `phases.flutter` 的输出目录、包名、组织域和展示名称。
- 向用户提供从生成工程目录运行的命令。后续功能实现沿用工程的导航、状态管理和依赖注入方式。
