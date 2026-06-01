#!/usr/bin/env python3
"""
倪海厦医案关键词检索脚本
==========================

用法:
    python3 case-search.py [--formula "方名"] [--disease "疾病"] [--date "YYYY"] "关键词1" "关键词2" ...

示例:
    # 检索包含"四逆汤"和"手脚冰冷"的医案
    python3 case-search.py "四逆汤" "手脚冰冷"

    # 检索 2005 年的所有癌症医案
    python3 case-search.py --date "2005" --disease "癌症"

数据源:
    本仓库 references/cases-classified.md
    外部 jangviktor-web/nihaixia 仓 cases/ 目录 (245 医案)
    外部 jangviktor-web/nihaixia 仓 modules/03_yian.md (849 医案)

设计灵感:
    来自 [JuneYaooo/nihaixia](https://github.com/JuneYaooo/nihaixia) scripts/search_screenshots.py
    的加权评分算法
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# 关键词权重（参考 JuneYaooo/nihaixia 的 search_screenshots.py）
WEIGHTS = {
    "exact_match": 20,        # 全部关键词都命中
    "desc": 10,                # 描述命中
    "category": 4,             # 分类命中
    "lesson": 3,               # 课次命中
    "formula": 8,              # 方剂名命中（加权）
    "disease": 8,              # 疾病名命中（加权）
    "text": 1,                 # 全文命中
}

# 高风险方剂清单（命中时给出警告）
HIGH_RISK_FORMULAS = {
    "四逆汤", "通脉四逆汤", "白通汤", "白通加猪胆汁汤",
    "真武汤", "附子汤", "麻黄附子细辛汤", "麻黄附子甘草汤",
    "大承气汤", "小承气汤", "调胃承气汤",
    "抵当汤", "抵当丸", "大陷胸汤", "大陷胸丸", "桃核承气汤",
    "十枣汤", "甘遂半夏汤", "大黄甘遂汤", "己椒苈黄丸",
    "生附子", "炮附子", "生硫磺", "生半夏", "商陆", "巴豆",
    "乌梅丸", "附子泻心汤",
}

# 白话→中医术语 / 方剂名 映射（参考 colloquial-questions.md + symptom-index.md）
# 用户说"手脚冰凉"能映射到"四逆汤""当归四逆汤""少阴"等核心术语
COLLOQUIAL_TO_TERMS = {
    # 寒热类
    "手脚冰凉": ["四逆", "当归四逆", "少阴", "厥阴", "四逆汤", "脉微"],
    "手脚冰冷": ["四逆", "少阴", "脉微", "四逆汤"],
    "怕冷": ["少阴", "阳虚", "四逆", "麻黄附子细辛汤", "当归四逆"],
    "畏寒": ["少阴", "阳虚", "附子"],
    "发热": ["太阳", "阳明", "少阳", "桂枝汤", "白虎", "小柴胡"],
    "发烧": ["太阳", "阳明", "桂枝汤", "麻黄汤", "白虎"],
    # 疼痛类
    "头痛": ["太阳", "川芎", "葛根", "吴茱萸"],
    "偏头痛": ["少阳", "小柴胡", "川芎"],
    "胃痛": ["建中", "理中", "吴茱萸", "黄连"],
    "肚子痛": ["建中", "理中", "承气", "芍药甘草"],
    "腰痛": ["肾着", "真武", "附子", "肾气丸"],
    "关节痛": ["桂枝芍药知母", "乌头汤", "当归四逆", "白术附子"],
    "经痛": ["温经", "当归四逆", "芍药甘草", "吴茱萸"],
    # 呼吸类
    "咳嗽": ["小青龙", "麻黄", "麦门冬", "桔梗", "射干麻黄"],
    "气喘": ["小青龙", "麻黄附子细辛", "肾气丸"],
    "哮喘": ["小青龙", "射干麻黄", "肾气丸"],
    "鼻塞": ["葛根汤", "小青龙", "麻黄附子细辛"],
    # 消化类
    "拉肚子": ["理中", "四逆", "五苓散", "葛根芩连", "下利"],
    "腹泻": ["理中", "四逆", "下利", "太阴"],
    "便秘": ["承气", "麻子仁丸", "脾约", "大黄"],
    "胃酸": ["建中", "黄连", "吴茱萸"],
    # 心血管
    "心悸": ["炙甘草", "桂枝甘草", "真武", "苓桂术甘"],
    "胸闷": ["枳实薤白", "瓜蒌薤白", "四逆"],
    "高血压": ["建瓴", "镇肝", "大柴胡", "柴胡加龙牡"],
    "心脏病": ["炙甘草", "真武", "四逆", "苓桂术甘"],
    # 慢性病
    "糖尿病": ["白虎", "肾气丸", "真武", "瓜蒌瞿麦"],
    "肾衰竭": ["真武", "四逆", "肾气丸", "猪苓汤"],
    "肝硬化": ["四逆", "小柴胡", "鳖甲煎丸", "十枣"],
    "腹水": ["十枣", "真武", "甘遂半夏", "己椒苈黄"],
    "癌症": ["小柴胡", "四逆", "大承气", "抵当", "桂枝茯苓"],
    "肿瘤": ["桂枝茯苓", "抵当", "大黄蟅虫", "小柴胡"],
    # 皮肤
    "湿疹": ["麻黄连翘赤小豆", "消风散", "当归拈痛"],
    "痒": ["麻黄", "消风", "荆芥连翘"],
    # 妇科
    "月经不调": ["温经", "当归芍药", "四物", "小柴胡"],
    "不孕": ["温经", "肾气丸", "艾附暖宫", "当归芍药"],
    # 神志
    "失眠": ["黄连阿胶", "酸枣仁", "柴胡加龙牡", "栀子豉"],
    "焦虑": ["柴胡加龙牡", "半夏厚朴", "甘麦大枣", "百合"],
    "抑郁": ["柴胡加龙牡", "半夏厚朴", "甘麦大枣", "百合地黄"],
    "癫痫": ["柴胡加龙牡", "风引汤", "桂枝加葛根", "大承气"],
}


def load_cases() -> List[Dict]:
    """
    加载 cases-classified.md 的所有医案
    """
    cases = []
    cases_file = Path(__file__).parent.parent / "references" / "cases-classified.md"

    if not cases_file.exists():
        print(f"⚠️ 找不到 {cases_file}", file=sys.stderr)
        return []

    with open(cases_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. 解析表格行（支持两种表头：3列 医案号/日期/疾病 和 6列 医案号/日期/疾病/六经/方剂/摘要）
    case_pattern = re.compile(
        r"^\|\s*(?P<id>[\d-]+|\.{3})\s*\|\s*(?P<date>\d{4}-\d{2}-\d{2}|—|\.{3})\s*\|"
        r"\s*(?P<disease>[^|]+?)\s*\|"
        r"(?:\s*(?P<six_channel>[^|]*?)\s*\|"
        r"\s*(?P<formula>[^|]*?)\s*\|"
        r"\s*(?P<summary>[^|]*?)\s*\|)?",
        re.MULTILINE
    )

    for match in case_pattern.finditer(content):
        # 跳过表头行 / 分隔行 / 统计行
        id_val = match.group("id").strip()
        if id_val in ("医案号", "...", "—") or "..." in id_val:
            continue
        # 跳过 "共 X 个" 这样的统计行
        disease_val = match.group("disease").strip()
        if "共" in disease_val and "个" in disease_val:
            continue
        case = {
            "id": id_val,
            "date": match.group("date").strip(),
            "disease": disease_val,
            "six_channel": (match.group("six_channel") or "").strip() if match.group("six_channel") else "",
            "formula": (match.group("formula") or "").strip() if match.group("formula") else "",
            "summary": (match.group("summary") or "").strip() if match.group("summary") else "",
        }
        cases.append(case)

    # 2. 从全文中抽取"六经"和"方剂"信息（基于章节小计表）
    # 例如 "| 肝癌 | ~25 | 四逆汤、十枣汤、小柴胡汤 |"
    section_pattern = re.compile(
        r"^\|\s*(?P<disease_type>[^|]+?)\s*\|\s*~?(?P<count>\d+)\s*\|\s*(?P<formula>[^|]+?)\s*\|",
        re.MULTILINE
    )

    # 3. 按章节切分：每条 case 只在自己所属分类的全文里搜
    # （避免 26 条 case 都共享同一份 8000 字全文导致误命中）
    section_chunks = []
    current_section = ""
    current_title = ""
    for line in content.split("\n"):
        if line.startswith("## "):
            current_title = line.strip("# ").strip()
            current_section = line + "\n"
        elif line.startswith("# "):
            current_title = line.strip("# ").strip()
            current_section = line + "\n"
        else:
            current_section += line + "\n"
        section_chunks.append((current_title, current_section))

    for case in cases:
        # 用"癌症/心血管/代谢/自身免疫/神经/其他"做粗匹配
        disease = case.get("disease", "")
        section_text = current_section  # 默认用最后一个章节（其他/补充）
        for title, chunk in section_chunks:
            # 标题包含疾病关键分类
            if any(kw in title for kw in [
                "癌症", "心血管", "代谢", "自身免疫", "神经", "其他", "医案"
            ]):
                # 判断本 case 属于哪个章节
                if title.startswith("一、癌症") and any(k in disease for k in [
                    "癌", "瘤", "白血病", "血癌", "淋巴", "舌", "骨", "脑"
                ]):
                    section_text = chunk
                    break
                elif title.startswith("二、心血管") and any(k in disease for k in [
                    "心脏", "高血压", "中风", "动脉", "心脏肥大", "心瓣"
                ]):
                    section_text = chunk
                    break
                elif title.startswith("三、代谢") and any(k in disease for k in [
                    "糖尿病", "肾衰", "腹水", "肝硬化", "肾", "肝"
                ]):
                    section_text = chunk
                    break
                elif title.startswith("四、自身免疫") and any(k in disease for k in [
                    "类风湿", "红斑狼疮", "风湿", "免疫"
                ]):
                    section_text = chunk
                    break
                elif title.startswith("五、神经") and any(k in disease for k in [
                    "癫痫", "脑瘤", "帕金森", "神经", "精神", "智障"
                ]):
                    section_text = chunk
                    break
        case["full_text"] = section_text

    return cases


def expand_colloquial(keywords: List[str]) -> List[Tuple[str, int]]:
    """
    把白话关键词展开为（展开后词, 权重衰减）的列表
    返回 [("原词", 1.0), ("展开词1", 0.5), ("展开词2", 0.3), ...]
    """
    expanded = []
    for kw in keywords:
        expanded.append((kw, 1.0))  # 原词全权重
        if kw in COLLOQUIAL_TO_TERMS:
            # 每个展开词按位置衰减
            for i, term in enumerate(COLLOQUIAL_TO_TERMS[kw]):
                decay = 0.5 if i == 0 else (0.3 if i == 1 else 0.15)
                expanded.append((term, decay))
    return expanded


def score_case(case: Dict, keywords: List[str]) -> Tuple[int, List[str]]:
    """
    计算单条医案的评分
    返回 (score, matched_keywords)
    """
    matched = []
    score = 0

    # 合并所有可搜索字段
    searchable_text = " ".join([
        case.get("id", ""),
        case.get("date", ""),
        case.get("disease", ""),
        case.get("six_channel", ""),
        case.get("formula", ""),
        case.get("summary", ""),
        case.get("full_text", ""),  # 全文搜索
    ]).lower()

    # 展开白话关键词
    expanded_kws = expand_colloquial(keywords)

    for kw, weight in expanded_kws:
        kw_lower = kw.lower()
        if kw_lower in searchable_text:
            if weight == 1.0:  # 原词匹配，记录到 matched
                matched.append(kw)
            # 按匹配位置给权重（再乘以白话展开的衰减）
            if case.get("disease", "").lower() == kw_lower:
                score += int(WEIGHTS["disease"] * weight)
            elif case.get("formula", "").lower() == kw_lower:
                score += int(WEIGHTS["formula"] * weight)
            elif case.get("summary", "").lower().find(kw_lower) >= 0:
                score += int(WEIGHTS["desc"] * weight)
            else:
                score += max(1, int(WEIGHTS["text"] * weight))

    # 全部原词都命中，加分
    if len(matched) == len(keywords):
        score += WEIGHTS["exact_match"]

    return score, matched


def check_high_risk(case: Dict) -> List[str]:
    """
    检查医案是否涉及高风险方剂
    """
    formula = case.get("formula", "")
    return [hr for hr in HIGH_RISK_FORMULAS if hr in formula]


def main():
    parser = argparse.ArgumentParser(
        description="倪海厦医案关键词检索脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 case-search.py "四逆汤" "手脚冰冷"
  python3 case-search.py --date "2005" --disease "乳癌"
  python3 case-search.py --top 5 "血癌"
        """
    )

    parser.add_argument(
        "keywords",
        nargs="*",
        help="搜索关键词（多个用空格分隔）"
    )

    parser.add_argument(
        "--formula",
        type=str,
        help="按方剂名过滤"
    )

    parser.add_argument(
        "--disease",
        type=str,
        help="按疾病名过滤"
    )

    parser.add_argument(
        "--date",
        type=str,
        help="按日期过滤（YYYY 或 YYYY-MM）"
    )

    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="返回前 N 条结果（默认 10）"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="JSON 格式输出"
    )

    args = parser.parse_args()

    # 合并关键词
    keywords = list(args.keywords)
    if args.formula:
        keywords.append(args.formula)
    if args.disease:
        keywords.append(args.disease)
    if args.date:
        keywords.append(args.date)

    if not keywords:
        parser.print_help()
        sys.exit(1)

    # 加载医案
    cases = load_cases()

    if not cases:
        print("❌ 没有加载到任何医案。请确认 references/cases-classified.md 存在。")
        sys.exit(1)

    # 评分
    scored_cases = []
    for case in cases:
        score, matched = score_case(case, keywords)
        if score > 0:
            scored_cases.append((score, matched, case))

    # 排序
    scored_cases.sort(key=lambda x: -x[0])

    # 取 top N
    top_cases = scored_cases[:args.top]

    # 输出
    if args.json:
        output = []
        for score, matched, case in top_cases:
            high_risk = check_high_risk(case)
            output.append({
                "score": score,
                "matched_keywords": matched,
                "case": case,
                "high_risk": high_risk,
            })
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(f"🔍 倪海厦医案检索：{keywords}")
        print(f"📊 总命中：{len(scored_cases)} 条，返回 Top {len(top_cases)} 条\n")

        for i, (score, matched, case) in enumerate(top_cases, 1):
            high_risk = check_high_risk(case)

            print(f"--- 医案 {i}（评分 {score}） ---")
            print(f"  ID：{case['id']}")
            print(f"  日期：{case['date']}")
            print(f"  疾病：{case['disease']}")
            if case.get("six_channel"):
                print(f"  六经：{case['six_channel']}")
            if case.get("formula"):
                print(f"  方剂：{case['formula']}")
            print(f"  命中关键词：{', '.join(matched)}")
            if high_risk:
                print(f"  ⚠️  高风险方剂：{', '.join(high_risk)}")
            print()

        if scored_cases and not top_cases:
            print("⚠️ 没有任何医案命中。试试其他关键词。")
        elif not scored_cases:
            # 数据局限提示
            print("💡 提示：本检索基于 cases-classified.md（245 个倪师大症医案）。")
            print("   • 失眠/心悸等慢病调理，请参考 references/formula-patterns.md")
            print("   • 经方方证速查：references/formula-patterns.md")
            print("   • 辨证分水岭：references/symptom-index.md")
            print("   • 白话症状→术语映射：references/colloquial-questions.md")


if __name__ == "__main__":
    main()
