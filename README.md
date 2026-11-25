# App Workflow

在 Codex 里从一句产品设想启动 App 工作流。插件包含 13 个技能及其模板、校验脚本和可复用 Playbook，覆盖 PRD、品牌 IP、原型、Flutter 脚手架、功能实现、QA 和 App Store 提审。可单独调用某个技能，也可用 handoff 接续已有项目。

## 工作流目录

| 阶段 | 内容 |
| --- | --- |
| [00_Orchestrator](00_Orchestrator/) | 流程入口、阶段编排、交接模板和质量门 |
| [01_PRD](01_PRD/) | 功能清单、PRD、MVP 范围和调研 |
| [02_IP](02_IP/) | 品牌 IP、UI 切图、HTML 与 Figma 导入辅助 |
| [03_UI_UX](03_UI_UX/) | 资产合成原型、交互说明和需求追溯 |
| [04_Dev](04_Dev/) | Flutter 脚手架和可选团队模板 |
| [05_Feature](05_Feature/) | MVP 功能开发与按页接入 UI 资产 |
| [06_QA](06_QA/) | 体验打磨、真机验收和 QA 报告 |
| [07_AppStore](07_AppStore/) | 发布构建、TestFlight 和 App Store 提审 |
| [08_Learn](08_Learn/) | 重复步骤登记与 Playbook 晋升 |

## 安装到 Codex

```bash
codex plugin marketplace add https://github.com/ruancanghui-hub/app-workflow-plugin.git
codex plugin add app-workflow@app-workflow-plugins
```

在目标产品工作区打开新的 Codex 对话，从技能列表选择 **App 全流程编排**，或者使用：

```text
$app-workflow:app-workflow 智能模式
参考：<竞品链接或名称>
我想做：<一句话说明产品和差异化>
平台：<iOS 优先 | 双端 | Android 优先>
```

需要逐项确认需求时使用「深度访谈模式」。已有项目可以直接指定 `docs/workflow/<product_slug>/handoff-manifest.json`，从已经通过的质量门继续。

## 工作区与依赖

- 插件包内的技能、模板和脚本可随插件安装使用。PRD、原型、品牌图、生成的 App 和 handoff 都写到当前产品工作区。新记录的 Playbook 与重复日志位于该工作区的 `.app-workflow/`。
- Python 3 运行各阶段校验，自动检测红框需额外安装 Pillow 与 NumPy。生成品牌图和切图需可用的图像生成工具。原型可使用本地 HTML，有相应工具时可按技能流程输出 Figma 导入文件。
- 默认使用 Flutter SDK 创建新工程。也可以指定自己的团队模板。iOS 构建和上架阶段需要 Xcode、相应签名和 Apple Developer 账号。

入口、阶段顺序、质量门和交付路径见 [编排技能](00_Orchestrator/app-workflow/SKILL.md)。规则之三与本地状态见 [工作流进化技能](08_Learn/evolve-workflow/SKILL.md)。

## 本地开发安装

在仓库根目录运行 `codex plugin marketplace add .`，再运行 `codex plugin add app-workflow@app-workflow-plugins`。修改后重新加载 marketplace 和插件进行验证。
