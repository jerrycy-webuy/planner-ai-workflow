---
type: note
status: active
created: 2026-07-17
updated: 2026-07-17
source: Claude
owner: [Jerry]
bu: [Group]
tags: [webuy-itinerary, skill, product-design, print, workflow]
confidence: high
last_reviewed: 2026-07-17
---

# webuy-itinerary Skill v3 重设计 — 定稿方案（2026-07-17 Jerry 14 问确认）

> 输入：[[Jerry]] 提供的 5 份设计成品 PDF（WBMKMG 云南明星团 / WBKMG8 昆大丽 / WBISF11 意瑞法 / WBNSF13 北欧极光 / WBJSH8 北海道），5 个并行 agent 逐页逆向分析。
> 本版为 Q&A 定稿版：14 个开放问题已由 Jerry 逐一拍板（见 §3 决策记录）。

---

## 1. 五份成品的设计语法（House Grammar）— 分析结论

### 1.1 版式骨架（4 页 canon）

| 页 | 内容 | 固定组件 |
|---|---|---|
| P1 封面 | 全出血大图 | 左上**缺角丝带 tour-code 章**（5/5）、白色标题堆叠、USP 徽章（金蜡封/金边菱形）、**底部信任条**（logo+吉祥物+Nasdaq+联系方式+QR+APP badge+TA 牌照） |
| P2 Highlights | 单页信息中枢 | 纯色横幅、城市分组圆点时间线、**粉彩路线图**（色块+红色夜数圆徽+航班实线/大巴虚线图例+指南针）、餐食计划、**集中式酒店矩阵**（(2N) 连住标注）、自费项目、服务费、Remarks 框 |
| P3–P4 Itinerary | 双栏报纸流 | **纯色 DAY 横条**（`DAY n ｜ CITY_EN 中文 > CITY_EN 中文`，✈/> 编码交通）、条下一行橙色餐食线（只列含餐）、✦ bullet + 主色加粗景点名、栏宽照片（右下半透明双语 caption）、末页红框 Note |

WBMKMG（明星团）为 6 页豪华变体（渐变 DAY 带 + 交替活动条 + 互动徽章）——**不进首期**（Q9）。

### 1.2 色彩 = 一主色 + 固定语义色

每团一个主色贯穿全组件（#4544F6/#0272C4/#0AB674/#1D9E9E…）；语义色跨团固定：餐食橙 #FF9300/#EA6F4D、条款红 #C01900、夜数红 #E50012、地图粉彩组。正文黑/深灰，EN 浅灰分层。

### 1.3 双语微规范（进模板常量）

`CITY_EN 中文` 粘连路线；`>` 大巴 / `✈` 航班；`（当地5星）或同级 / (Local 5star) or similar`；`(2N)`；只列含餐、缺餐 `-`。

### 1.4 成品的系统性缺陷（自动化的价值锚点）

1. **印前全不合格**：5/5 是 216.3×303mm（A4+3mm 出血烤死）但 TrimBox=MediaBox、无裁切标，印厂靠猜。
2. **macOS Pages 手排**：字体汤（HelveticaNeue+PingFang+ArialHebrew 数字回退+AppleColorEmoji）、封面压扁位图不可改字、39–93MB。
3. **手工事故**：SAPPPOR 拼错、云南团配西藏鲁朗照片、同城两译名、同文档 3+ 种红、照片密度失衡、Day 跨页无续标。

---

## 2. v3 流程定稿（每步 Input / Output / Goal）

**总原则：TourSpec JSON = 唯一事实源。** 一切修改改 spec，PDF 永远是 spec 的确定性渲染。入口 = Claude Code/Cowork 会话（Q1）。

### Step 0｜工作区初始化
- **Input**：团号（或从文件名/内容推断）
- **Output**：本地 staging `<workspace>/<团号>/`（spec.json / assets/ / proofs/ / out/）
- **Goal**：中间产物有固定归宿；改版只 v+1 不覆盖

### Step 1｜Ingest 抽取（格式无关，Q2）
- **Input**：任意格式行程文件（xlsx→openpyxl 摊平 / pdf→PyMuPDF 文本+页图 / docx→flatten / txt·粘贴直读）+ 可选照片
- **Output**：spec.json 草稿 + 缺口清单（「必须问」/「有默认」两级）
- **Goal**：LLM-primary 一次抽全；缺口当场对话问清，绝不静默编造（沿用 v2 校验契约）

### Step 2｜资产解析
- **Input**：spec.json + planner 供图
- **Output**：assets/ 全量就位 + spec.assets 清单（每张记 source / license 状态 / 署名需求）
- **Goal**：校样所见即所得；版权状态显式
- 规则：照片链 = **供图 > Shutterstock 预览 > 免费图源（自动记署名）**（Q5）；主色 = **hero 取色**（约束色域+白字对比度校验，可覆盖）（Q10）；路线图 = **程序化仿成品风**（粉彩色块+夜数徽+图例+地标 icon）（Q6）

### Step 3｜校样 Proof（Q3）
- **Input**：spec.json + assets + brand kit tokens
- **Output**：proof.html（与成品同模板同 CSS），在会话 Browser pane 打开
- **Goal**：成品级预览；**文字点击即改（contenteditable + data-path），照片一键换**；换色/结构调整走对话
- 回写机制：planner 页面上改完说「保存」→ Claude 经 javascript_tool 读回 DOM diff → 回写 spec；备用「导出修改」按钮下载 spec.patch.json

### Step 4｜迭代
- **Input**：页面编辑 + 对话指令
- **Output**：spec.json v+1
- **Goal**：所有修改沉淀为数据，重出永远可复现

### Step 5｜确认 & 出成品（Q4：Planner 自确认即定稿）
- **Input**：planner「确认」
- **Output**：`<团号>_v<N>_print.pdf`（216×303、TrimBox/BleedBox、裁切标、300dpi、RGB，Q7）+ `<团号>_v<N>_digital.pdf`（A4 净尺寸、<5MB，Q8）+ spec 定版 + 署名清单
- **Goal**：一次确认出两档；印厂不用猜裁切线
- 确认时自动触发：① **Shutterstock 批量 licensing 换高清正版**（确认=授权扣费，Q14）② QA gates（校验契约/照片查重/译名一致/token lint/空页守卫/印前盒校验）

### Step 6｜归档（Q13）
- **Input**：定版产物
- **Output**：**Lark 云盘团文件夹 = 权威存档**；本地 staging 保留
- **Goal**：团队可见、改版可回溯

---

## 3. 决策记录（2026-07-17 Jerry 逐问拍板）

| # | 问题 | 决定 |
|---|---|---|
| Q1 | 使用入口 | Claude Code/Cowork 会话 |
| Q2 | 输入现状 | 五花八门无模板 → 全 LLM 抽取 |
| Q3 | 校样编辑范围 | 文字就地改 + 换照片；其余走对话 |
| Q4 | 确认机制 | Planner 自确认即定稿，无审批门 |
| Q5 | 照片来源 | 供图 > Shutterstock 正版 > 免费源（记署名） |
| Q6 | 路线图 | 程序化仿成品风 |
| Q7 | 印刷规格 | RGB + 出血 + TrimBox + 裁切标 + 300dpi（CMYK 不做） |
| Q8 | 电子版形态 | 轻量 PDF；网页版 + UTM 追踪 **缓至 P2/P3**（Q12 合并） |
| Q9 | 版式范围 | WEBUY 标准 + ALTITUDE 两套 + **WETRIP（新建 kit）**；明星豪华版不进首期 |
| Q10 | 主色 | AI 从 hero 图取色 + 可覆盖 |
| Q11 | 酒店 | 集中式为默认（spec 保留逐日字段） |
| Q13 | 存储 | Lark 云盘为权威归档 |
| Q14 | 图片付费 | 确认即自动 license |

### 我方既定默认（未另行询问，可推翻）

- 字体：弃 mac 系字体，用已捆绑 OFL 字体（Lato + Noto Sans SC；ALTITUDE: Libre Baskerville + MiSans），视觉近似即可
- Emoji 全部换内嵌 SVG icon（消除 AppleColorEmoji 平台依赖）
- 成品命名：`<团号>_v<N>_print/digital.pdf`；spec 每次确认落版本
- QA gates 全自动、不可跳过

## 4. 依赖清单（落地前置）

1. **WETRIP brand kit 资产**：logo / 主色 / 联系条 / 牌照信息 — 设计侧提供（owner 待定：[[Catherine]] branding 线 or [[Luna]] 设计团队）
2. **Lark 云盘写入通路**：JClaw bot 或 Lark OpenAPI token（现有 webuy-data 只读）
3. **Shutterstock licensing API 打通**：现有付费账号，需接 licensing endpoint + 确认计费方式
4. **Planner 机器部署**：Claude Code + skill 安装/更新脚本（git + uv venv，一次性）
5. GEMINI_API_KEY（可选：仅 AI 手绘地图备用路线用）

## 5. 分期与状态（2026-07-18 更新）

| 期 | 内容 | 状态 |
|---|---|---|
| P0 | TourSpec schema 正式化；多格式 ingest；印刷版后处理（印前盒+裁切标+双档导出）；统一工作目录 | ✅ **完成**（2026-07-17，WBTESJ 全链路验证） |
| P1 | Proof 可编辑校样（contenteditable+回写）；hero 取色定主色；程序化仿成品风路线图；design tokens 化；模板组件对齐 house grammar | ✅ **完成**（2026-07-18，WBTESJ v2 青色系成品验证；skill 目录已 git 版本化，commit ac775ef） |
| P2 | ALTITUDE/WETRIP kit 接入；Shutterstock licensing 自动化；Lark 归档通路；网页版 + UTM 追踪 | ⏸ 等外部依赖（§4：WETRIP 资产 / Lark 写通路 / Shutterstock API / GEMINI key） |

P0+P1 交付细节：schema/tourspec.schema.json + 9 个新脚本（ingest / validate_tourspec / spec_to_metadata / make_stub_docx / export_profiles / accent_from_hero / build_proof / apply_patch + proof_editor.js/css）+ 模板 house-grammar 重构（token 化：--accent 系 + --meal-color/--terms-red）+ 地图 pill 标签/粉彩/region_label。试点成品：`~/WEBUY_Tours/WBTESJ/out/WBTESJ_v2_{print,digital}.pdf`。

## 相关内容

- [[webuy-data]] · [[JClaw]] · [[Commercial_Platform]] · [[Bernice]] · [[Jasmin]] · [[Dorothy]] · [[Jaccy]]
- 分析原始输出：workflow wf_12dd7ce6-b4d（5 份逐页分析 JSON）
