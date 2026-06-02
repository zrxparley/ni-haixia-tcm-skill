# 倪海厦中医传承 Skill

> 倪师传习录 — 以倪海厦老师学术体系为核心的中医学习顾问与诊断辅助

**版本**：V3.0 · 2026-05-31  
**知识规模**：25 references + 5 templates + 1 script = 31 文件 · 15,000+ 行

---

## 简介

本 Skill 整合三个上游开源倪海厦中医项目，覆盖完整人纪 5 部经典（针灸 / 内经 / 本草 / 伤寒 / 金匮）+ 闭门课 7 大重病 + 仲景心法 + 梁冬对话 + 斯坦福演讲 + 妙方 17 方 + 245 分类医案 + 112 方证 + 6 经辨证。

**双模式设计**：
- **学习模式**：学习计划 / 进度追踪 / 知识讲解 / 阶段测试
- **诊断模式**：迭代式十问 / 六经辨证辅助 / 方证匹配

**4 层安全防护**：医疗边界声明 · Safety Requirements 4 条 · 诚实边界 · 禁用话术清单

> 所有内容仅作倪海厦课程学习与中医理论整理，不作个人医疗建议。

---

## 前置条件

| 条件 | 说明 |
|---|---|
| **AI Agent 平台** | OpenCode CLI / Workbuddy / 或支持 SKILL.md 的任何 Agent |
| **操作系统** | macOS / Linux |
| **Python**（可选）| 3.8+，仅医案检索脚本需要 |

---

## 安装

### 方法一：一键安装（推荐）

```bash
# 使用官方安装脚本（自动检测 OpenCode / Workbuddy 路径）
curl -fsSL https://raw.githubusercontent.com/zrxparley/ni-haixia-tcm-skill/main/install.sh | bash
```

### 方法二：手动安装

```bash
# 1. 克隆仓库
git clone https://github.com/zrxparley/ni-haixia-tcm-skill.git

# 2. 复制到对应平台的 skill 目录
# OpenCode:
cp -r ni-haixia-tcm-skill ~/.config/opencode/skills/ni-haixia-tcm/
# Workbuddy:
cp -r ni-haixia-tcm-skill ~/.workbuddy/skills/ni-haixia-tcm/
```

---

## 使用方法

### 触发激活（直接对话即可）

| 触发词 | 行为 |
|---|---|
| "倪师" / "倪海厦" | 致敬，进入学习模式 |
| "我要学中医" / "学中医" | 评估基础，制定学习计划 |
| "中医诊断" | 启动六经辨证辅助（诊断模式） |
| "中医研究" | 启动研究模式（查文献、分析案例） |
| "倪海厦会怎么看" | 进入倪师视角模式 |

### 显式切换命令

| 命令 | 说明 |
|---|---|
| `/学习模式` | 锁定学习模式 |
| `/诊断模式` | 锁定诊断模式 |
| `/状态` | 显示当前模式 + 学习进度 + 当前阶段 |
| `/重置学习` | 重置学习进度（需确认） |

### 学习模式示例

```
你：今天学什么？
AI：根据学习进度，当前是第 3 周（针灸大成阶段）...

你：学完了第 3 周
AI：启动阶段测试（5 题简答）...
```

### 诊断模式示例

```
你：头痛怕冷怎么办
AI：先说明：这是按倪海厦课程做学习拆解，不是诊断...
    你这个问题先看几个分水岭：有没有出汗？小便深黄还是清白？
```

---

## 知识库结构

```
ni-haixia-tcm-skill/
├── SKILL.md                          # Skill 主文件
├── README.md                         # 本文件
├── install.sh                        # 安装脚本
├── skill.json                        # Skill 元数据
├── CHANGELOG.md                      # 更新日志
├── ACKNOWLEDGEMENTS.md               # 致谢
├── references/ (25 文件)
│   ├── 核心路由（4 个）
│   │   ├── colloquial-questions.md   # 白话翻译层（18 个白话场景）
│   │   ├── learner-entry.md          # 5 大学习目的入口
│   │   ├── honesty-boundary.md       # 诚实边界（硬性约束）
│   │   └── expression-dna.md         # 8 大表达模式
│   ├── 临床核心（4 个）
│   │   ├── tcm-diagnosis.md          # 六经辨证框架
│   │   ├── symptom-index.md          # 症状入口索引
│   │   ├── formula-patterns.md       # 112 方方证速查
│   │   └── shanghan-lun.md           # 伤寒论 112 方速查
│   ├── 课程体系（6 个）
│   │   ├── zhenjiu.md                # 针灸大成
│   │   ├── huangdi-neijing.md        # 黄帝内经 71 篇
│   │   ├── bencao-345.md             # 神农本草经 345 味
│   │   ├── jingui-23p.md             # 金匮要略 23 篇
│   │   ├── bimen-hantang.md          # 闭门课 7 大重病
│   │   └── yijinjing.md              # 易筋经
│   ├── 临床应用（3 个）
│   │   ├── cases-classified.md       # 245 分类医案
│   │   ├── case-studies.md           # 6 类精选医案
│   │   └── mifang-collection.md      # 妙方 17 方
│   ├── 药性药理（2 个）
│   │   ├── drug-properties.md        # 药性总义+五味临床
│   │   └── hantang.md                # 汉唐文章精选
│   ├── 配套讲座（5 个）
│   │   ├── zhongjing-xinfa.md        # 仲景心法
│   │   ├── liangdong-dialogue.md     # 梁冬对话 7 期
│   │   ├── stanford-speech.md        # 斯坦福演讲
│   │   ├── fuyang-forum.md           # 扶阳论坛
│   │   └── tianji.md                 # 天纪命理
│   └── 学习辅助（2 个）
│       ├── lesson-map.md             # 15 课学习地图
│       └── ni-books-research.md      # 著作体系调研
├── templates/ (5 文件)
│   ├── daily-study-plan.md           # 零基础 12 个月学习计划
│   ├── diagnosis-template.md         # 标准化诊断模板
│   ├── case-replay.md                # 医案复盘 6 步骤
│   ├── weekly-plan-v3.md             # 周学习计划 V3
│   └── prescription-analysis.md      # 方剂解析模板
└── scripts/ (1 文件)
    └── case-search.py                # 医案关键词检索
```

### 文件加载优先级

| 优先级 | 文件 |
|---|---|
| P0（必读） | honesty-boundary.md · tcm-diagnosis.md · symptom-index.md · formula-patterns.md · colloquial-questions.md |
| P1（重要） | lesson-map.md · bimen-hantang.md · drug-properties.md · expression-dna.md · cases-classified.md |
| P2（拓展） | learner-entry.md · bencao-345.md · zhenjiu.md · jingui-23p.md · huangdi-neijing.md · mifang-collection.md · zhongjing-xinfa.md |
| P3（按需） | 其余 references（天纪 / 梁冬 / 斯坦福 / 扶阳 / 易筋经） |

---

## 上游项目致谢

本项目 V3.0 整合三个上游开源倪海厦中医项目的精华：

| 上游项目 | 核心贡献 |
|---|---|
| [JuneYaooo/nihaixia](https://github.com/JuneYaooo/nihaixia) | Agent Skill 框架 · 白话翻译层 · Safety Requirements 4 条 |
| [9527qingfeng/hantang-nihaixia-follower](https://github.com/9527qingfeng/hantang-nihaixia-follower) | 完整人纪 5 部 MD · 妙方 17 方 · 紫极先生方剂 |
| [jangviktor-web/nihaixia](https://github.com/jangviktor-web/nihaixia) | 结构化蒸馏 · 诚实边界 · 8 大表达 DNA · 245 分类医案 |

详见 [ACKNOWLEDGEMENTS.md](./ACKNOWLEDGEMENTS.md)。

---

## 免责声明

本 Skill 仅用于中医学习与理论整理，**不构成医疗建议**。涉及真实症状、诊断、处方、剂量、针灸操作、急症、孕产儿童、肿瘤或附子等高风险内容时，**必须**咨询合格医疗专业人员。

---

## 更新日志

- **V3.0** (2026-05-31) — 全面同步 3 个上游项目，新增 17 references + 3 templates + 1 script
- **V2.1** (2026-05-30) — 学习入口 7 大场景 · 逐课学习地图 · 倪师表达 DNA
- **V2.0** (2026-05-28) — 六经辨证框架 · 112 方方证速查
- **V1.0** (2026-05-20) — 初始版本

详见 [CHANGELOG.md](./CHANGELOG.md)。

---

## License

[MIT License](https://opensource.org/licenses/MIT)
