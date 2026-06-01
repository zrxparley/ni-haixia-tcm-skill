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

    # 1. 解析表格行
    case_pattern = re.compile(
        r"^\|\s*(?P<id>[\d-]+)\s*\|\s*(?P<date>\d{4}-\d{2}-\d{2}|—)\s*\|\s*(?P<disease>[^|]+)\s*\|",
        re.MULTILINE
    )

    for match in case_pattern.finditer(content):
        case = {
            "id": match.group("id").strip(),
            "date": match.group("date").strip(),
            "disease": match.group("disease").strip(),
            "six_channel": "",
            "formula": "",
            "summary": "",
        }
        cases.append(case)

    # 2. 从全文中抽取"六经"和"方剂"信息（基于章节小计表）
    # 例如 "| 肝癌 | ~25 | 四逆汤、十枣汤、小柴胡汤 |"
    section_pattern = re.compile(
        r"^\|\s*(?P<disease_type>[^|]+?)\s*\|\s*~?(?P<count>\d+)\s*\|\s*(?P<formula>[^|]+?)\s*\|",
        re.MULTILINE
    )

    # 3. 也直接存储整篇文档供全文搜索用
    for case in cases:
        case["full_text"] = content

    return cases


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

    for kw in keywords:
        kw_lower = kw.lower()
        if kw_lower in searchable_text:
            matched.append(kw)
            # 按匹配位置给权重
            if case.get("disease", "").lower() == kw_lower:
                score += WEIGHTS["disease"]
            elif case.get("formula", "").lower() == kw_lower:
                score += WEIGHTS["formula"]
            elif case.get("summary", "").lower().find(kw_lower) >= 0:
                score += WEIGHTS["desc"]
            else:
                score += WEIGHTS["text"]

    # 全部关键词都命中，加分
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


if __name__ == "__main__":
    main()
