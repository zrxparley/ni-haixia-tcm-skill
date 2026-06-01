# 致谢

本项目（zrxparley/ni-haixia-tcm-skill）凝聚了三个上游开源倪海厦中医项目的精华，特此致谢：

## 上游项目

### 1. [JuneYaooo/nihaixia](https://github.com/JuneYaooo/nihaixia)
**贡献**：完整的 Agent Skill 框架 + 12 个课程蒸馏 + 2986 张截图证据
**核心借鉴**：
- `colloquial-questions.md`（白话翻译层）
- `learner-entry.md`（按学习目的组织）
- `usage-scenarios.md`（用户场景路由）
- `Safety Requirements` 4 条硬性要求
- 多平台 `install_as_skill.sh` 设计思想
- 12 个课程模块的蒸馏方法论

**特别价值**：这是目前最成熟的倪海厦 Agent Skill 实现。

### 2. [9527qingfeng/hantang-nihaixia-follower](https://github.com/9527qingfeng/hantang-nihaixia-follower)
**贡献**：人纪 5 部经典完整 MD 化 + 妙方 17 方 + 102 个汉唐方剂 + 紫极先生补全
**核心借鉴**：
- `mifang-collection.md`（17 方短平快验方）
- `jingui-23p.md`（金匮要略 25 篇）
- `bencao-345.md`（神农本草经 365 味）
- `zhongjing-xinfa.md`（仲景心法）
- 紫极先生方剂讲解思路
- 维护者家庭真实医案（160 篇）

**特别价值**：维护者深度参与、有完整学习路径、第一手真实医案丰富的资源库。

### 3. [jangviktor-web/nihaixia](https://github.com/jangviktor-web/nihaixia)
**贡献**：结构化蒸馏（modules/ + cases/ + expression_style）+ 849 医案 + 闭门课精华
**核心借鉴**：
- `bimen-hantang.md`（闭门课 7 大重病专题）
- `expression-dna.md`（8 大表达模式）
- `cases-classified.md`（按疾病分类 245 例医案）
- `honesty-boundary.md`（诚实边界）
- `drug-properties.md`（药性总义 + 倪师独创）
- `bencao-345.md`（神农本草经 345 味）
- `zhenjiu.md`（针灸教程）
- `tianji.md`（天纪命理）
- 249 例医案 vs modules/03 全部 849 例

**特别价值**：v2.0.0 精简后仅 4MB，却覆盖 11 个课程 + 表达 DNA + 诚实边界 + 12 个 references/research 元数据。

## 致谢的"倪师"本人

**倪海厦**（1954-2012），台湾著名经方派中医师，汉唐中医诊所创始人。
- 1954 年生于台北
- 高中拜师周左宇、徐济民
- 1980 年移民美国，创立汉唐中医诊所
- 2009.12 与梁冬对话（7 期录音稿）
- 2010.9 斯坦福大学演讲
- 2012 年去世

**核心理念**：
- "中医很简单，就是阴阳气血。你搞懂了，一通百通。"
- "不懂伤寒，不算入门"
- "阳气是生命的根本"

## 引用规范

使用本 skill 时，若涉及具体方剂、剂量、辨证思路，请明确标注：
> "本内容引自倪海厦老师课程体系，整合自 [JuneYaooo/nihaixia](https://github.com/JuneYaooo/nihaixia) / [9527qingfeng/hantang-nihaixia-follower](https://github.com/9527qingfeng/hantang-nihaixia-follower) / [jangviktor-web/nihaixia](https://github.com/jangviktor-web/nihaixia) GitHub 项目，仅供学习。"

## 免责声明

本 skill 仅用于中医学习与理论整理，**不构成医疗建议**。所有内容遵循上游项目的医疗边界声明。涉及真实症状、诊断、处方、剂量、针灸操作、急症、孕产儿童、肿瘤或附子等高风险内容时，必须咨询合格医疗专业人员。

---

*愿倪师学问薪火相传。*
