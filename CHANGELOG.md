# 更新日志

## V3.0 — 2026-05-31（当前）

> **主题**：倪师传习录 — 全面同步三个上游开源项目
> **整合来源**：
> - [JuneYaooo/nihaixia](https://github.com/JuneYaooo/nihaixia) — 完整 Agent Skill 框架
> - [9527qingfeng/hantang-nihaixia-follower](https://github.com/9527qingfeng/hantang-nihaixia-follower) — 课程资源库（人纪 5 部经典 + 妙方 + 医案）
> - [jangviktor-web/nihaixia](https://github.com/jangviktor-web/nihaixia) — 结构化蒸馏（modules/ + cases/ + 表达 DNA）

### 主要变更

**新增顶层文件**
- `CHANGELOG.md`（本文件）
- `ACKNOWLEDGEMENTS.md`（致谢上游）

**新增 references/**（17 个）
- `colloquial-questions.md` ★ — 白话翻译层（JuneYaooo 独有）
- `learner-entry.md` ★ — 7 大学习目的入口（JuneYaooo 独有）
- `expression-dna.md` ★ — 8 大表达模式（升级自 V2.1 expression-style.md）
- `honesty-boundary.md` ★ — 诚实边界（jangviktor 独有）
- `drug-properties.md` ★ — 药性总义+五味临床+倪师独创心法
- `bencao-345.md` — 神农本草经 345 味
- `bimen-hantang.md` ★ — 闭门课 7 大重病专题（血癌/乳癌/肝癌/肺癌/糖尿病/肾衰竭/中风）
- `cases-classified.md` ★ — 按疾病分类 245 例医案
- `mifang-collection.md` — 17 方短平快验方
- `jingui-23p.md` — 金匮要略 23 篇
- `zhenjiu.md` — 针灸教程（十二经+穴位）
- `tianji.md` — 天纪命理（紫微/易经/风水）
- `huangdi-neijing.md` — 黄帝内经 71 篇（重写）
- `zhongjing-xinfa.md` — 仲景心法 7 讲
- `liangdong-dialogue.md` — 梁冬对话 7 期精华
- `fuyang-forum.md` — 扶阳论坛演讲
- `stanford-speech.md` — 斯坦福演讲
- `yijinjing.md` — 易筋经

**新增 templates/**（3 个）
- `case-replay.md` — 医案复盘 6 步骤模板
- `weekly-plan-v3.md` — 周学习计划 V3
- `prescription-analysis.md` — 方剂解析模板

**新增 scripts/**（1 个）
- `case-search.py` — 医案关键词检索脚本

**SKILL.md 升级**：V2.1 → V3.0
- 加入 Safety Requirements 4 条硬性要求
- 加入诚实边界
- 升级文件结构图
- 升级加载优先级
- 升级学习入口

### 数据规模

| 指标 | V2.1 | V3.0 | 增量 |
|---|---:|---:|---:|
| SKILL.md | 23K | ~30K | +7K |
| references/ 文件数 | 11 | 26+ | +15 |
| templates/ 文件数 | 2 | 5 | +3 |
| scripts/ 文件数 | 0 | 1 | +1 |
| 知识库行数 | ~3,000 | ~15,000+ | +400% |
| 医案覆盖 | 6 类精选 | 849 例 + 245 分类 | +20× |
| 课程覆盖 | 5 经典 | 5 经典 + 闭门课 + 仲景心法 + 梁冬 + 斯坦福 + 扶阳 + 易筋经 + 妙方 | +8 |
| 表达 DNA | 6 模式 | 8 模式（合并 jangviktor 完整版） | +2 |

### 安全性提升

V3.0 新增 4 层防护：
1. **Skill 头部声明** — 医疗边界（沿用 V2.1）
2. **Safety Requirements 4 条** — 来自 JuneYaooo 框架
3. **诚实边界** — 来自 jangviktor（明列"扮演时倪师会说'错'的话"）
4. **禁用话术清单** — 防止 LLM 过度模仿（来自 jangviktor）

### 不在 V3.0 中

下列内容因体积或性质原因，**仅在 references/ 给出索引**：
- 78M 截图证据（来自 JuneYaooo，未 git 入仓）
- 631M hanthang 资源（git 体积限制）
- 110M jangviktor 原始讲义（v2.0.0 已精简）
- 1452 个 .doc 文档（格式问题，未 MD 化）
- 2986 张 WebP（链接到 JuneYaooo 原仓）

---

## V2.1 — 2026-05-30

- 学习入口 7 大场景
- 逐课学习地图（15 讲详表）
- 倪师表达 DNA（6 模式）
- 症状索引（170 行）

## V2.0 — 2026-05-28

- 六经辨证框架
- 112 方方证速查
- 9 个核心 references

## V1.0 — 2026-05-20

- 初始版本
- 基础六经框架 + 诊断模板
