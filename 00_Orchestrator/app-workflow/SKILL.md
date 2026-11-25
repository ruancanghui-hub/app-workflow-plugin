---
name: app-workflow
description: >-
  一句话启动完整 App 工作流：PRD → 品牌 IP → UI/UX 原型 → Flutter 脚手架 → 功能实现 → QA 打磨 → App Store 提审；
  并通过规则之三将重复步骤沉淀为 Playbook，持续进化流水线。
  Use when the user wants to build an app end-to-end, run the full pipeline, 一句话建 App,
  app-workflow, or orchestrate all workflow phases through App Store submission.
---

# App Workflow Orchestrator

将用户的一句话产品意图，编排为**七个可验证阶段 + 持续进化环**。每阶段只向下游传递**文件契约**，不靠聊天记忆串联。任一质量门未 PASS，不得进入下一阶段。每个 Gate 通过后执行 `evolve-workflow` 阶段回顾。

## 插件目录与项目工作区

以当前加载的本插件 `00_Orchestrator/app-workflow/SKILL.md` 所在目录向上两级确定 `APP_WORKFLOW_ROOT`，也就是包含 `.codex-plugin/plugin.json` 和 `00_Orchestrator/` 的目录。直接使用同一插件里的子技能、模板和脚本。

保持命令工作目录为产品工作区。各阶段路径从插件根目录解析。脚本通过 `python3 "$APP_WORKFLOW_ROOT/<阶段目录>/<技能>/scripts/<脚本>.py"` 调用，项目输入和输出路径从工作区解析。将 `docs/`、`output/`、`apps/` 和 `.app-workflow/` 写入产品工作区。

## Child skills (do not reimplement)

| Phase | Skill directory | Skill name |
|-------|-----------------|------------|
| 1 PRD | `01_PRD/creating-app-product-docs/` | `creating-app-product-docs` |
| 2 IP | `02_IP/generate-app-brand-ip/` | `generate-app-brand-ip` |
| 2b Assets | `02_IP/regenerating-ui-redbox-assets/` | `regenerating-ui-redbox-assets` |
| 2c Asset UI | `03_UI_UX/composing-asset-ui-prototype/` | `composing-asset-ui-prototype` |
| 2d HTML / Figma (optional) | `02_IP/converting-sliced-ui-to-html-figma/` | `converting-sliced-ui-to-html-figma` |
| 3 UI/UX | `03_UI_UX/creating-app-prototypes/` | `creating-app-prototypes` |
| 4 Scaffold | `04_Dev/create-flutter-app/` | `create-flutter-app` |
| 5 Features | `05_Feature/implement-flutter-features/` | `implement-flutter-features` |
| 5b Asset page (optional) | `05_Feature/regenerating-ui-assets-to-flutter-page/` | `regenerating-ui-assets-to-flutter-page` |
| 6 QA | `06_QA/polish-app-quality/` | `polish-app-quality` |
| 7 App Store | `07_AppStore/release-to-app-store/` | `release-to-app-store` |
| ∞ Evolution | `08_Learn/evolve-workflow/` | `evolve-workflow` |

Read each child `SKILL.md` in full before executing that phase. This orchestrator defines **order, gates, handoff, failure policy, and evolution hooks**.

## Core principle

Research and define before generating visuals or code. Preserve verified competitor baseline. One MVP loop. Every stage leaves auditable artifacts. Smooth UX is specified in prototype interaction docs, not invented during Flutter coding.

## Start

1. Inspect the workspace; preserve existing files.
2. Parse the user brief: competitor links/names, one-sentence differentiation, platform preference, and mode.
3. If mode is absent, ask once:

   - **A. 智能模式（快速产出，子技能最多三个关键问题）**
   - **C. 深度访谈模式（逐项确认后产出）**

   Never silently choose a mode. When switching from 智能模式 to 深度访谈模式, preserve confirmed facts in `assumptions.md` and the handoff manifest.

4. Create or update the workflow root:

   ```
   docs/workflow/<product_slug>/
   ├── handoff-manifest.json
   ├── glossary.md
   └── adr/
   ```

5. Copy `assets/handoff-manifest.template.json` to `docs/workflow/<product_slug>/handoff-manifest.json` and fill `intake` before Phase 1.

## Intake contract (one-sentence entry)

Minimum user input:

```text
/app-workflow 智能模式
参考：<竞品链接或名称>
我想做：<一句话差异化>
平台：<iOS 优先 | 双端 | Android 优先>
```

Infer conservatively; record every inference in the product `assumptions.md` and `handoff-manifest.json` → `intake.inferences`.

Select a filesystem-safe `product_slug` (snake_case, ASCII). Use the same slug for Flutter `--project-name` unless the user overrides.

## State machine

```
INTAKE
  → PHASE_1_PRD → GATE_PRD
  → PHASE_2_IP ─────────────┐
  → GATE_IP                 │
  → PHASE_3_PROTOTYPE       │  Phase 3 build waits for IP direction
  → GATE_PROTOTYPE          │
  → PHASE_4_FLUTTER_SCAFFOLD┘
  → GATE_FLUTTER_SCAFFOLD
  → PHASE_5_FEATURES
  → GATE_FEATURES
  → PHASE_6_QA
  → GATE_QA
  → PHASE_7_APP_STORE
  → GATE_APP_STORE
  → COMPLETE

EVOLUTION (continuous): after every GATE_* → evolve-workflow 阶段回顾
```

Update `handoff-manifest.json` → `workflow.phase` after every transition. Use `schema_version: 2` for new projects.

## Phase 1 — PRD (`creating-app-product-docs`)

**Goal:** Five validated product documents plus a testable MVP loop.

**Execute:** Follow `01_PRD/creating-app-product-docs/SKILL.md` exactly.

**Outputs (required):**

```
docs/product/YYYY-MM-DD-<产品名>/
├── 01-功能清单.md
├── 02-PRD.md
├── 03-MVP范围.md
├── sources.md
└── assumptions.md
```

**Gate:**

```bash
python3 "$APP_WORKFLOW_ROOT/01_PRD/creating-app-product-docs/scripts/validate_product_docs.py" \
  docs/product/YYYY-MM-DD-<产品名>/
```

Must print `PASS`. On failure: fix documents, rerun, do not proceed.

**Handoff updates:** Set `phases.prd` paths, metadata (产品名、模式、平台、目标用户、商业策略), `mvp_loop`, and `gates.prd = "PASS"`.

**Domain docs:** Seed `glossary.md` with product name, user roles, core entities, and MVP states. Add `adr/001-mvp-loop.md` summarizing the chosen hypothesis and veto conditions from `03-MVP范围.md`.

## Phase 2 — Brand IP (`generate-app-brand-ip`)

**Goal:** One coherent mascot-led brand system aligned to the PRD promise.

**Prerequisites:** `gates.prd == "PASS"`.

**Inputs:** `02-PRD.md`, `03-MVP范围.md` (authoritative).

**Execute:** Follow `02_IP/generate-app-brand-ip/SKILL.md`. Required companions: `imagegen`, and `creative-production:produce` when available.

**Outputs:** Delivery tree with canonical character anchor, App Icon, launch screen, 15-action sheet, three core-Tab UI directions, ZIP + manifest + QA report. If the user selects a direction before Phase 3, also apply the Brand IP `core_tab_ui` supplement and deliver every PRD root Tab under `04-core-tab-ui/core_tab_ui/`.

**Gate:** Visual inspection of every asset; `pack_delivery.py` ZIP test succeeds. For an approved Tab direction, verify the untouched source hash, canvas size, exact root labels/order, PRD mapping, and shared-component requirement. Generated raster drift may be recorded as `PASS_WITH_RASTER_LIMITATION`, but wrong IA or an unacknowledged drift is a failure. Set `gates.ip = "PASS"` only after this contract is recorded.

**Handoff updates:** Record `phases.brand.direction_id`, `tab_ui_direction`, and absolute paths to icon and launch screen. Set `core_tab_ui_requested = true` only when post-selection root expansion was requested; then also record the selected Tab UI reference, `core_tab_ui_dir`, `core_tab_ui_contract`, `core_tab_ui_status`, and any `deferred_root_tabs`.

**Failure policy:** If Tab UI directions conflict with PRD IA, or root pages do not preserve the selected Tab-shell contract, stop and reconcile before Phase 3 build. Phase 3 may accept `PASS_WITH_RASTER_LIMITATION` only by implementing one shared editable Tab component and testing active-only variation.

### Phase 2b — UI asset packaging (`regenerating-ui-redbox-assets`)

**Goal:** Turn annotated Tab UI screenshots into code-ready PNG asset packages (icons, feature art, backgrounds) for prototype and Flutter implementation.

**When to run:** After core Tab UI images exist from Phase 2 and the user requests 切图 / 打包 / 红框标注 / code-ready assets — or before Phase 3 when the prototype needs decomposed assets.

**Prerequisites:** Approved or candidate Tab UI image from `output/brand-ip/<slug>/04-core-tab-ui/` (skeleton, direction, or `core_tab_ui/` page).

**Execute:** Follow `02_IP/regenerating-ui-redbox-assets/SKILL.md` and [references/workflow-integration.md](../../02_IP/regenerating-ui-redbox-assets/references/workflow-integration.md). Required companion: `imagegen`.

**Inputs:** User-annotated screenshot with red rectangles marking each asset (or agent-assisted detection via `detect_red_boxes.py`).

**Outputs:**

```
output/brand-ip/<slug>/05-ui-assets/
├── backgrounds/
├── feature_art/
├── nav_icons/
├── status/
├── ui_controls/
├── manifest.json
└── <slug>-ui-assets.zip
```

**Gate:** Every requested marked asset exists as a separate PNG; `manifest.json` complete; ZIP validates. Set `phases.brand.ui_assets_status = "PASS"` and record `ui_assets_dir` / `ui_assets_zip` in handoff. This supplement does not block Phase 3 if not requested (`ui_assets_status` stays `NOT_REQUESTED`).

**Handoff updates:** Record `phases.brand.ui_assets_dir`, `ui_assets_zip`, `ui_assets_status`. Phase 4 scaffold copies `nav_icons/` and `ui_controls/` into Flutter `assets/images/` when present.

### Phase 2c — Asset UI prototype (`composing-asset-ui-prototype`)

**Goal:** Verify `05-ui-assets` reconstructs the locked `04-core-tab-ui` visual contract as a clickable HTML composite with overlay QA — a 2b→3 bridge, not a full Phase 3 package.

**When to run:** After Phase 2b `ui_assets_status = "PASS"` (or per-Tab manifests exist) and the user requests 资产合成原型 / `06_asset_ui` / 1:1 叠对照验收 — optionally before Phase 3 to catch asset gaps early.

**Prerequisites:** `04-core-tab-ui/` reference PNGs with QA PASS; `05-ui-assets/<tab>/manifest.json` for every core Tab.

**Execute:** Follow `03_UI_UX/composing-asset-ui-prototype/SKILL.md` and [references/workflow-integration.md](../../03_UI_UX/composing-asset-ui-prototype/references/workflow-integration.md).

**Locked decisions:**

- Fidelity: overlay QA at ~40% opacity — backgrounds/icons/text align; CSS glass is approximate.
- Text: HTML only for labels; PNG for icons and backgrounds.
- Scope: asset verification + `layout-spec.json` coordinates; interaction specs remain Phase 3.

**Outputs:**

```
output/brand-ip/<slug>/06_asset_ui/
├── index.html
├── styles.css
├── app.js
├── layout-spec.json
├── README.md
└── visual-analysis.md

# Overlay QA references ../04-core-tab-ui/ directly (no PNG copies)
```

**Gate:** Run `python3 "$APP_WORKFLOW_ROOT/03_UI_UX/composing-asset-ui-prototype/scripts/validate_asset_ui_prototype.py" output/brand-ip/<slug>`. Set `phases.brand.asset_ui_prototype_status = "PASS"` and record `asset_ui_prototype_dir` / `layout_spec`. Does **not** block Phase 3 if `NOT_REQUESTED`.

## Phase 3 — UI/UX prototype (`creating-app-prototypes`)

**Goal:** Reviewable prototype package with full interaction states — this is where “丝滑” is defined.

**Prerequisites:** `gates.prd == "PASS"`. Phase 3 **build** requires `gates.ip == "PASS"` and a selected `tab_ui_direction`.

**Inputs:**

- `01-功能清单.md`, `02-PRD.md`, `03-MVP范围.md`
- Brand assets from Phase 2 (icon palette, character, selected Tab direction)
- Competitor screenshots captured per child skill rules

**Execute:** Follow `03_UI_UX/creating-app-prototypes/SKILL.md`. For static or clickable HTML and Figma import from available sliced UI assets, use `02_IP/converting-sliced-ui-to-html-figma/SKILL.md`.

**Outputs:**

```
docs/prototype/
├── 00-需求追溯矩阵.md
├── 01-低保真原型说明.md
├── 02-交互说明文档.md
├── 03-页面跳转逻辑图.md
├── 04-原型评审清单.md
└── cdb/   # optional CDB export when requested
```

**Gate:**

```bash
python3 "$APP_WORKFLOW_ROOT/03_UI_UX/creating-app-prototypes/scripts/validate_prototype_package.py" <project-root>
```

Check every declared navigation transition. Run CDB preflight when CDB export is in scope. Set `gates.prototype = "PASS"`.

**Handoff updates:** Record `phases.prototype.dir`, traceability row count, and NFR targets copied from PRD (launch time, animation, offline behavior).

**Interaction minimum for “丝滑”:** Every MVP page documents loading, empty, error, permission-denied, and interruption recovery in `02-交互说明文档.md`.

## Phase 4 — Flutter scaffold (`create-flutter-app`)

**Goal:** Runnable Flutter project with brand assets wired; ready for feature implementation.

**Prerequisites:** `gates.prototype == "PASS"`.

**Inputs from handoff:**

| Parameter | Source |
|-----------|--------|
| `output_dir` | Default `apps/<product_slug>/` — must not already exist |
| `--project-name` | `product_slug` |
| `--org` | User or team domain; confirm the release identifier |
| `--app-id` | `<product_slug>_v1` unless specified, for team templates that use it |
| `--app-name` | PRD 产品名 |
| Icon / launch | Phase 2 delivery paths |

**Execute:** Follow `04_Dev/create-flutter-app/SKILL.md`. Use the standard Flutter scaffold by default, or the team template supplied by the user. Record the scaffold and the actual run command in the handoff.

**Post-scaffold (orchestrator responsibilities):**

1. Copy App Icon and launch image from Phase 2 into `ios/Runner/Assets.xcassets` and Android `mipmap`/`drawable` per platform conventions.
2. Create `.scratch/<app-name>/` with a feature checklist derived from `00-需求追溯矩阵.md` (one row per `lib/features/<feature>/`).
3. When using a team template, keep edits in the generated project.

**Gate:** New directory exists; `dart analyze` clean; `flutter test` passes. Set `gates.flutter_scaffold = "PASS"`.

**Evolution hook:** Ask if scaffold setup had repeatable friction; `log_repetition.py` if yes.

## Phase 5 — Feature implementation (`implement-flutter-features`)

**Goal:** MVP P0 traceability rows implemented in Flutter with tests.

**Prerequisites:** `gates.flutter_scaffold == "PASS"`.

**Execute:** Follow `05_Feature/implement-flutter-features/SKILL.md`.

**Outputs:** `docs/workflow/<product_slug>/implementation-trace.md`, `lib/features/*`, updated `.scratch/<app-name>/feature-checklist.md`.

**Gate:**

```bash
python3 "$APP_WORKFLOW_ROOT/05_Feature/implement-flutter-features/scripts/validate_feature_implementation.py" \
  <flutter_app_dir> \
  docs/workflow/<product_slug>/implementation-trace.md
```

Set `gates.features = "PASS"`; update `phases.features.*` in handoff.

**Evolution hook:** Log any step you repeated for the third time (e.g. route wiring, permission flow).

### Phase 5b — Asset-driven Flutter page (`regenerating-ui-assets-to-flutter-page`)

**Goal:** Reconstruct one requested Flutter page from an annotated visual reference and its regenerated code-ready asset package.

**When to run:** The Flutter app exists and the user asks to generate red-box assets, package them, and use them to make a specific page high fidelity.

**Execute:** Follow `05_Feature/regenerating-ui-assets-to-flutter-page/SKILL.md`. It invokes Phase 2b asset packaging only when that page has no valid package yet.

**Prerequisites:** `gates.flutter_scaffold == "PASS"`, a target page/route, and either a valid `05-ui-assets/<page>/manifest.json` or an annotated source reference.

**Outputs:** The page-specific asset package and ZIP, copied Flutter assets registered in `pubspec.yaml`, and the updated page implementation.

**Handoff updates:** Record `phases.features.asset_page_dir`, `asset_page_assets`, and `asset_page_status`. This is optional and contributes evidence to Phase 5; it does not add a separate gate.

## Phase 6 — QA polish (`polish-app-quality`)

**Goal:** Measurable smooth UX on real device; all P0 interaction states verified.

**Prerequisites:** `gates.features == "PASS"`.

**Execute:** Follow `06_QA/polish-app-quality/SKILL.md`.

**Outputs:** `docs/workflow/<product_slug>/qa-report.md`.

**Gate:**

```bash
python3 "$APP_WORKFLOW_ROOT/06_QA/polish-app-quality/scripts/validate_qa_report.py" \
  docs/workflow/<product_slug>/qa-report.md
```

Set `gates.qa = "PASS"`; update `phases.qa.*` in handoff.

**Evolution hook:** Promote recurring QA setup (simulator profiles, network conditioning) to playbooks.

## Phase 7 — App Store release (`release-to-app-store`)

**Goal:** Complete submission package uploaded and submitted for review.

**Prerequisites:** `gates.qa == "PASS"`.

**Execute:** Follow `07_AppStore/release-to-app-store/SKILL.md`.

**Outputs:**

```
docs/workflow/<product_slug>/
├── app-store-submission.md
├── privacy-questionnaire.md
└── screenshots/
```

**Gate:**

```bash
python3 "$APP_WORKFLOW_ROOT/07_AppStore/release-to-app-store/scripts/validate_app_store_package.py" \
  docs/workflow/<product_slug>/app-store-submission.md
```

Set `gates.app_store = "PASS"` when submission is testflight/submitted/approved. Update `phases.app_store.*`.

**Note:** PASS means submission package complete and sent — not Apple approval.

**Evolution hook:** Promote repeated cert/screenshot/privacy steps.

## Phase ∞ — Workflow evolution (`evolve-workflow`)

Runs **after every gate** and whenever the user says a step feels repetitive.

**Registry:** `.app-workflow/repetition-log.json` in the product workspace

**Playbooks:** Bundled [playbook index](playbooks/INDEX.md) and the product workspace’s `.app-workflow/playbooks/INDEX.md`

**Rule of three:** Same pattern logged 3 times → mandatory `promote_to_playbook.py` → complete the workspace playbook. To distribute the improvement, merge it into an editable checkout of the plugin.

```bash
python3 "$APP_WORKFLOW_ROOT/08_Learn/evolve-workflow/scripts/log_repetition.py" \
  --phase features --pattern "..." --context "..." --product-slug <slug>

python3 "$APP_WORKFLOW_ROOT/08_Learn/evolve-workflow/scripts/promote_to_playbook.py" \
  --pattern-id <id> --title "..."
```

Before starting any phase, check the bundled and workspace indexes for applicable playbooks and apply them first.

## Handoff manifest

Single source of truth: `docs/workflow/<product_slug>/handoff-manifest.json`.

Template: `00_Orchestrator/app-workflow/assets/handoff-manifest.template.json`.

After each gate, run:

```bash
python3 "$APP_WORKFLOW_ROOT/00_Orchestrator/app-workflow/scripts/validate_handoff.py" \
  docs/workflow/<product_slug>/handoff-manifest.json
```

Fix all reported issues before claiming phase completion.

## Failure policy

| Failure | Action |
|---------|--------|
| PRD validator FAIL | Stay in Phase 1 |
| IP assets incomplete | Progress update only; no Phase 3 build |
| Prototype missing interaction states | Extend `02-交互说明文档.md`; no Flutter |
| `verify_template_layout.sh` FAIL | Resolve the selected team template validation failure before using it |
| `output_dir` already exists | New slug or explicit user consent to use another path |
| PRD ↔ prototype traceability gap | Add rows to `00-需求追溯矩阵.md` before scaffold |
| Feature trace incomplete | Stay in Phase 5 |
| QA blocker open | Stay in Phase 6 or return to Phase 5 |
| App Store rejection (bug) | Phase 5/6 per `ios-release-checklist.md` |
| Repetition count ≥ 3 | Run `promote_to_playbook.py` before next project |

Never overwrite `docs/product/*` or `docs/prototype/` silently; use numeric suffix directories per child skill rules.

## Final response (workflow complete through Phase 7)

Lead with completion scope. Provide:

1. Link `handoff-manifest.json`, `glossary.md`, and `playbooks/INDEX.md` if updated
2. Links to all phase output roots
3. MVP loop one-liner; TestFlight / submission status
4. Every gate status (`PASS` / pending)
5. Exact `flutter run` and `flutter build ipa` commands
6. New playbooks promoted this run

Do not claim Apple approval until `submission_status: approved`.

## Example

User:

```text
/app-workflow 智能模式
参考：Tide
我想做：睡前心率+呼吸辅助的轻冥想 App
平台：iOS 优先
```

1. Create `docs/workflow/sample_app/handoff-manifest.json`
2. Run Phase 1 → five product files → validator PASS
3. Run Phase 2 → brand ZIP → gate PASS
4. Run Phase 3 → prototype package → validator PASS
5. Run Phase 4 → `apps/sample_app` → analyze + test PASS
6. Run Phase 5 → implementation-trace → validator PASS
7. Run Phase 6 → qa-report → validator PASS
8. Run Phase 7 → TestFlight + submit → validator PASS
9. Report handoff, playbooks, and submission status

## Common mistakes

- Skipping validators and claiming the workflow is done.
- Starting IP or prototype before PRD PASS.
- Building Flutter UI without `00-需求追溯矩阵.md`.
- Copying competitor branding, UI, or assets.
- Treating scaffold creation as a shippable App Store build.
- Losing metadata consistency (产品名、模式、平台、目标用户、商业策略) across phases.
- Ignoring the rule of three — repetition stays in chat instead of playbooks.
