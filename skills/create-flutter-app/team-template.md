
# 从 App 模板创建新应用

## 模板路径

使用用户提供的模板目录。以下命令以 `flutter-app-template/` 为例。

`flutter-app-template/`

- **模板源**：`flutter-app-template/template/`
- **创建脚本**：`flutter-app-template/scripts/create_from_template.sh`
- **布局校验**：`flutter-app-template/scripts/verify_template_layout.sh`

## 输入（缺则向用户确认）

| 参数 | CLI | 规则 |
|------|-----|------|
| 输出目录 | `<output_dir>` | 目录**不得已存在**；monorepo 默认 `apps/<project_name>/` |
| Dart 包名 | `--project-name` | snake_case，如 `sample_app` |
| 组织域 | `--org` | 如 `com.example` |
| 应用实例 ID | `--app-id` | 运营侧唯一 id，如 `sample_app_v1` |
| 展示名 | `--app-name` | 如 `睡眠助手` |

未给 `--app-id` / `--app-name` 时脚本用 `project_name` 与 `project_name_local` 填充。

## 执行序列

**完成标准**：新目录存在、`dart analyze` 通过、已向用户说明如何 `flutter run`。

1. **Preflight**

```bash
cd flutter-app-template
./scripts/verify_template_layout.sh --strict
```

失败则先修模板源，不要强行创建实例。

2. **Create**

```bash
./scripts/create_from_template.sh <output_dir> \
  --project-name <project_name> \
  --org <org> \
  --app-id <app_id> \
  --app-name "<app_name>"
```

脚本会 rsync 模板源、`flutter create` 修复双端、写入 `dart_defines.dev.json`、`dart analyze lib test`。

3. **Smoke（推荐）**

```bash
cd <output_dir>
flutter test
flutter run --flavor dev --dart-define-from-file=dart_defines.dev.json
```

Android 可直接 `--flavor dev`。iOS 需先按 `ios/FLAVORS.md` 在 Xcode 复制 `dev`/`prod` scheme（模板未自动改 pbxproj）。

4. **Monorepo 收尾（在团队 monorepo 内时）**

- 将 `apps/<name>/` 纳入 git（勿提交 `build/`、`.dart_tool/`）
- 业务 spec / tickets 放 `.scratch/<app-name>/`，术语对齐根 `CONTEXT.md`

## 创建后可选配置

| 需求 | 做法 |
|------|------|
| Firebase 真适配器 | 见 [team-template-reference.md](team-template-reference.md#firebase) |
| 应用运营台心跳 | `OPS_CONSOLE_BASE_URL` dart-define |
| prod 变体 | `--flavor prod --dart-define=APP_VARIANT=prod` |

不配 Firebase / 运营台时，假实现默认可跑。

## 业务开发约定

新实例沿用模板结构，勿改模板源 `flutter-app-template/template/`：

- `lib/features/<feature>/` → `binding` → `controller` → `pages`
- 运维能力走端口（Analytics / RemoteConfig / CrashReporter），经 GetX Binding 注入
- 构建变体：`APP_VARIANT` 必须与 `--flavor` 一致（`dev` 或 `prod`）

详细配置与 gotcha 见 [team-template-reference.md](team-template-reference.md)。

## 示例（睡眠助手 MVP）

```bash
cd flutter-app-template
./scripts/create_from_template.sh ../apps/sample_app \
  --project-name sample_app \
  --org com.example \
  --app-id sample_app_v1 \
  --app-name "睡眠助手"
```

运行：

```bash
cd ../apps/sample_app
flutter run --flavor dev --dart-define-from-file=dart_defines.dev.json
```
