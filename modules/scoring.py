"""
スコアリング機能
診断結果からスコアを計算し、準備度ランクや改善優先度を判定
"""

from modules.questions import QUESTIONS, CATEGORIES

# 業界平均値
INDUSTRY_AVERAGES = {
    "business": 65,
    "data": 55,
    "organization": 60,
    "technology": 50,
    "process": 58,
    "compliance": 70
}

# 準備度ランクの定義
READINESS_RANKS = {
    "A": {"min": 541, "max": 600, "label": "優秀"},
    "B": {"min": 481, "max": 540, "label": "良好"},
    "C": {"min": 421, "max": 480, "label": "要改善"},
    "D": {"min": 360, "max": 420, "label": "大幅改善必要"},
    "E": {"min": 0, "max": 359, "label": "導入困難"}
}


def calculate_scores(answers: dict) -> dict:
    """
    診断結果からスコアを計算
    
    Args:
        answers: 質問IDをキー、選択肢インデックスを値とする辞書
                例: {"b1": 2, "b2": 1, ...}
    
    Returns:
        スコア情報を含む辞書:
        {
            "category_scores": {
                "business": 85,
                "data": 70,
                ...
            },
            "total_score": 450,
            "max_score": 600,
            "percentage": 75.0
        }
    """
    category_scores = {}
    
    # カテゴリーごとにスコアを計算
    for category, questions in QUESTIONS.items():
        category_score = 0
        for question in questions:
            question_id = question["id"]
            if question_id in answers:
                choice_index = answers[question_id]
                # 選択肢インデックスが有効範囲内かチェック
                if 0 <= choice_index < len(question["choices"]):
                    choice = question["choices"][choice_index]
                    category_score += choice["score"]
        category_scores[category] = category_score
    
    # 総合スコアを計算
    total_score = sum(category_scores.values())
    
    # 最大スコアを計算（全問で最高点を取った場合）
    max_score = 0
    for questions in QUESTIONS.values():
        for question in questions:
            max_choice_score = max(choice["score"] for choice in question["choices"])
            max_score += max_choice_score
    
    # パーセンテージを計算
    percentage = (total_score / max_score * 100) if max_score > 0 else 0.0
    
    return {
        "category_scores": category_scores,
        "total_score": total_score,
        "max_score": max_score,
        "percentage": round(percentage, 1)
    }


def get_readiness_rank(total_score: int) -> str:
    """
    準備度ランクを判定
    
    Args:
        total_score: 総合スコア
    
    Returns:
        ランク文字列 (A, B, C, D, E)
    """
    for rank, criteria in READINESS_RANKS.items():
        if criteria["min"] <= total_score <= criteria["max"]:
            return rank
    
    # 範囲外の場合はEを返す
    return "E"


def get_readiness_rank_label(rank: str) -> str:
    """
    ランクのラベルを取得
    
    Args:
        rank: ランク文字列 (A, B, C, D, E)
    
    Returns:
        ランクのラベル
    """
    return READINESS_RANKS.get(rank, {}).get("label", "不明")


def compare_with_average(category_scores: dict) -> dict:
    """
    業界平均値との比較
    
    Args:
        category_scores: カテゴリー別スコア
                        例: {"business": 85, "data": 70, ...}
    
    Returns:
        業界平均との差分
        例: {"business": +20, "data": +15, ...}
    """
    comparison = {}
    for category, score in category_scores.items():
        if category in INDUSTRY_AVERAGES:
            diff = score - INDUSTRY_AVERAGES[category]
            comparison[category] = diff
    
    return comparison


def get_improvement_priorities(category_scores: dict) -> list:
    """
    スコアが低い順に改善優先度を返す
    
    Args:
        category_scores: カテゴリー別スコア
                        例: {"business": 85, "data": 70, ...}
    
    Returns:
        改善優先度のリスト（スコアが低い順）
        例: [("data", 55), ("technology", 50), ...]
    """
    # スコアが低い順にソート
    sorted_categories = sorted(
        category_scores.items(),
        key=lambda x: x[1]
    )
    
    return sorted_categories


def get_category_max_score(category: str) -> int:
    """
    カテゴリーの最大スコアを取得
    
    Args:
        category: カテゴリー名
    
    Returns:
        最大スコア
    """
    if category not in QUESTIONS:
        return 0
    
    max_score = 0
    for question in QUESTIONS[category]:
        max_choice_score = max(choice["score"] for choice in question["choices"])
        max_score += max_choice_score
    
    return max_score


def get_category_percentage(category_score: int, category: str) -> float:
    """
    カテゴリーのスコアをパーセンテージで取得
    
    Args:
        category_score: カテゴリースコア
        category: カテゴリー名
    
    Returns:
        パーセンテージ
    """
    max_score = get_category_max_score(category)
    if max_score == 0:
        return 0.0
    
    return round((category_score / max_score * 100), 1)


def get_score_summary(answers: dict) -> dict:
    """
    スコアのサマリー情報を取得
    
    Args:
        answers: 診断結果の回答
    
    Returns:
        スコアサマリー情報
    """
    scores = calculate_scores(answers)
    rank = get_readiness_rank(scores["total_score"])
    comparison = compare_with_average(scores["category_scores"])
    priorities = get_improvement_priorities(scores["category_scores"])
    
    # カテゴリー別のパーセンテージを計算
    category_percentages = {}
    for category, score in scores["category_scores"].items():
        category_percentages[category] = get_category_percentage(score, category)
    
    return {
        "scores": scores,
        "rank": rank,
        "rank_label": get_readiness_rank_label(rank),
        "comparison": comparison,
        "priorities": priorities,
        "category_percentages": category_percentages
    }

