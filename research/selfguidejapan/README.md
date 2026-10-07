# Self-Guided Japan（selfguidejapan.com）线路与景点整理

> 抓取日期：2026-10-07（两轮） · 来源：https://selfguidejapan.com（BluePlanet「Self-Guided Japan」自助游套餐：酒店 + 新干线 + 行李托运 + 机场接站 + 24/7 支援，不含国际机票；每人、两人一房；SOLO 系列单人价）
> 用途：A1 市场雷达 / 日本线产品立项参考。**私有仓库内部资料。** 两站合并结果见 `../japan_merged/`，生成脚本见 `../build/`。

## 文件

| 文件 | 内容 |
|---|---|
| `tours_catalog.md` / `.csv` | 线路目录：89 条（代码 / 名称 EN+CN / 天数 / 住宿骨架 / 价格 / 主题 / 可信度 / URL），按系列分组 |
| `package_tours.md` / `.json` | **标准行程（Package Tour 格式）**：每条线路一节，house grammar（`CITY_EN 中文 (2N)`、`>` 陆路 / `✈` 航班）；18 条完整逐日 + 8 条部分逐日 |
| `attractions.md` / `.csv` | 景点列表：357 个景点/体验（EN / 中文 / 城市 / 区域 / 类别 / 出现线路） |
| `raw/` | 子任务原始抓取 JSON（第一轮按系列、第二轮 `pass2_*.json`、主会话 `main_session.json`、目的地页 `destinations.json`） |

## 覆盖情况

| 项 | 数量 |
|---|---|
| 站点自称线路数 | 111（/tours 页）～113（博客） |
| 本次确认存在的线路 | **89** |
| 其中拿到住宿骨架（城市 + 夜数） | 76 |
| 其中完整逐日行程 | **18**（BF001, BF002, FG002, FG003, FG004, FG005, GR002, GR007, KA003, KY003, LX001, LX002, LX003, SE003, SK006, SL003, SL007, TP004） |
| 其中部分逐日行程 | 8（GR010, HD001, HD002, KM004, KR003, KY001, SL004, SL005） |
| 来源可信度 | high 14 / low 27 / medium 48 |
| 景点 / 体验 | 357，覆盖 106 个城市/地点 |

系列分布：BF 5 · FG 5 · GR 18 · HD 2 · HK 8 · HS 3 · KA 3 · KM 4 · KR 1 · KY 5 · LX 3 · NT 9 · SE 5 · SK 6 · SL 6 · TP 6

- 探测过、判定不存在：HS004, HS005, HS006, HS101, HS102, HS103, LX004, LX005, SE006, SE101, SE102, SE103, SL002, SL006, SL008, SL009, SL010
- 探测过一次未命中、未二次确认（倾向不存在）：BF006, BF007, BF008, BF101, BF102, BF103, BF104, BF105, BF106, FG006, FG007, FG008, FG101, FG102, FG103, FG104, FG105, FG106, GR011, GR012, GR109, GR110, GR111, GR112, HD003, HD004, HD005, HD006, HK009, HK010, KA004, KA005, KA006, KA101, KA102, KA103, KA104, KY006, KY101, KY102, KY103, KY104, NT001, NT003, NT010, SL101, SL102, SL104, SL105, SL106, SL107, SL108, SL109, SL110, TP005, TP006, TP103, TP104, TP105, TP106

已知冲突（详见各条 `notes`）：SL003 页面真实标题为「SOLO Koyasan」（第一轮索引把「SOLO/Timeless Traditions: Shirakawago & Hida」挂在 SL003 上，该标题属 SL103）；GR005/GR006、SE003/SE004、KM001/KM002、HS001/HS002、KY004/KY005 的名称/价格在不同摘要间互换；NT009 标题两说（Sacred Trails & Coastal Traditions / Gourmet Rail Journey）。

## 方法与限制（必读）

1. **两个域名都被本云端环境的出站网络策略拦截**（代理对 CONNECT 返回 403，WebFetch 报 EGRESS_BLOCKED），所以**没有直接读取任何网页**。
2. 全部数据来自 WebSearch 的**搜索索引摘要**（限定域名），由并行子任务逐线路搜索；只记录明确归属到该线路页面的信息，交叉来源（博客、主题页）在 `raw/*.json` 的 `sources` / `notes` 里标明。
3. 搜索额度每轮 200 次（子任务共用）。两轮共约 390 次：第一轮做存在性 + 名称/天数/价格/住宿骨架，第二轮补逐日行程。**没有被搜索引擎索引的产品页无法再通过搜索补齐**，剩余逐日空缺只能靠放行域名后直接抓取。
4. 搜索摘要由小模型生成，存在**代码↔名称串标**；冲突均写入 `notes` 并标 `low`。
5. 中文名为本仓库整理时的译名（线路名意译；景点用通用中文名），非站点官方译名。

## 补全路径

在云端环境设置 → Network access 里放行 `selfguidejapan.com`，之后可直接抓取 111 条线路的完整逐日行程、酒店、含项，并用 `../build/` 脚本重新生成全部文件。
