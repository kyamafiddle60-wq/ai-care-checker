"""
介護施設向けAI導入診断の質問データ
6カテゴリー × 5問 = 計30問
"""

QUESTIONS = {
    "business": [
        {
            "id": "b1",
            "text": "経営陣のAI導入に対する理解度は？",
            "choices": [
                {"text": "AIについて全く理解していない", "score": 0},
                {"text": "AIについて少し理解している", "score": 5},
                {"text": "AIの可能性を理解している", "score": 10},
                {"text": "AI導入の必要性を認識している", "score": 15},
                {"text": "AI導入を積極的に検討している", "score": 20}
            ]
        },
        {
            "id": "b2",
            "text": "AI導入の予算確保状況は？",
            "choices": [
                {"text": "予算は確保されていない", "score": 0},
                {"text": "予算確保を検討中", "score": 5},
                {"text": "一部予算を確保済み", "score": 10},
                {"text": "十分な予算を確保済み", "score": 15},
                {"text": "予算に余裕があり追加投資も可能", "score": 20}
            ]
        },
        {
            "id": "b3",
            "text": "AI導入によるROI（投資対効果）への期待は？",
            "choices": [
                {"text": "ROIを期待していない", "score": 0},
                {"text": "ROIについて検討していない", "score": 5},
                {"text": "ROIを期待しているが具体的ではない", "score": 10},
                {"text": "ROIの目標を設定している", "score": 15},
                {"text": "ROIを定量的に測定する体制がある", "score": 20}
            ]
        },
        {
            "id": "b4",
            "text": "AI導入の優先度は？",
            "choices": [
                {"text": "優先度は低い", "score": 0},
                {"text": "将来的に検討したい", "score": 5},
                {"text": "検討を開始している", "score": 10},
                {"text": "導入を計画している", "score": 15},
                {"text": "早期導入を目指している", "score": 20}
            ]
        },
        {
            "id": "b5",
            "text": "AI導入の目的・目標の明確さは？",
            "choices": [
                {"text": "目的・目標が不明確", "score": 0},
                {"text": "目的はあるが目標が不明確", "score": 5},
                {"text": "目的・目標を検討中", "score": 10},
                {"text": "目的・目標が明確", "score": 15},
                {"text": "目的・目標が明確で全員が共有している", "score": 20}
            ]
        }
    ],
    "data": [
        {
            "id": "d1",
            "text": "記録業務の現状は？",
            "choices": [
                {"text": "全て紙ベース", "score": 0},
                {"text": "一部デジタル化", "score": 10},
                {"text": "ほぼデジタル化", "score": 20}
            ]
        },
        {
            "id": "d2",
            "text": "利用者情報のデータ管理状況は？",
            "choices": [
                {"text": "データ管理システムがない", "score": 0},
                {"text": "基本的なデータ管理システムがある", "score": 5},
                {"text": "統合的なデータ管理システムがある", "score": 10},
                {"text": "データが構造化されて管理されている", "score": 15},
                {"text": "データが標準化され、AI活用可能な形式", "score": 20}
            ]
        },
        {
            "id": "d3",
            "text": "データの品質・正確性は？",
            "choices": [
                {"text": "データの品質が低い", "score": 0},
                {"text": "データの品質に課題がある", "score": 5},
                {"text": "データの品質は概ね良好", "score": 10},
                {"text": "データの品質管理が行われている", "score": 15},
                {"text": "データの品質が高く、継続的に改善している", "score": 20}
            ]
        },
        {
            "id": "d4",
            "text": "データの蓄積量は？",
            "choices": [
                {"text": "データの蓄積が少ない", "score": 0},
                {"text": "一部のデータが蓄積されている", "score": 5},
                {"text": "一定量のデータが蓄積されている", "score": 10},
                {"text": "十分なデータが蓄積されている", "score": 15},
                {"text": "大量のデータが体系的に蓄積されている", "score": 20}
            ]
        },
        {
            "id": "d5",
            "text": "データの共有・連携状況は？",
            "choices": [
                {"text": "データの共有・連携ができていない", "score": 0},
                {"text": "一部のデータのみ共有", "score": 5},
                {"text": "基本的なデータ共有ができている", "score": 10},
                {"text": "部門間でデータ連携ができている", "score": 15},
                {"text": "外部システムともデータ連携ができている", "score": 20}
            ]
        }
    ],
    "organization": [
        {
            "id": "o1",
            "text": "職員のITリテラシーは？",
            "choices": [
                {"text": "ITリテラシーが低い", "score": 0},
                {"text": "基本的なITスキルがある", "score": 5},
                {"text": "中程度のITスキルがある", "score": 10},
                {"text": "高いITスキルを持つ職員がいる", "score": 15},
                {"text": "ITスキルが高く、継続的に向上している", "score": 20}
            ]
        },
        {
            "id": "o2",
            "text": "AI・デジタル技術に関する研修体制は？",
            "choices": [
                {"text": "研修体制がない", "score": 0},
                {"text": "研修を検討中", "score": 5},
                {"text": "不定期に研修を実施", "score": 10},
                {"text": "定期的に研修を実施", "score": 15},
                {"text": "体系的な研修プログラムがある", "score": 20}
            ]
        },
        {
            "id": "o3",
            "text": "AI導入を推進する体制は？",
            "choices": [
                {"text": "推進体制がない", "score": 0},
                {"text": "推進体制を検討中", "score": 5},
                {"text": "一部の職員が担当", "score": 10},
                {"text": "専任の担当者がいる", "score": 15},
                {"text": "組織横断的な推進体制がある", "score": 20}
            ]
        },
        {
            "id": "o4",
            "text": "職員の変化への対応力は？",
            "choices": [
                {"text": "変化への抵抗が強い", "score": 0},
                {"text": "変化に消極的", "score": 5},
                {"text": "変化を受け入れる傾向", "score": 10},
                {"text": "変化に積極的", "score": 15},
                {"text": "変化を自ら推進する文化がある", "score": 20}
            ]
        },
        {
            "id": "o5",
            "text": "部門間の連携・協力体制は？",
            "choices": [
                {"text": "部門間の連携が弱い", "score": 0},
                {"text": "一部の部門のみ連携", "score": 5},
                {"text": "基本的な連携ができている", "score": 10},
                {"text": "積極的に連携している", "score": 15},
                {"text": "組織全体で協力する文化がある", "score": 20}
            ]
        }
    ],
    "technology": [
        {
            "id": "t1",
            "text": "IT環境・インフラの整備状況は？",
            "choices": [
                {"text": "IT環境が整備されていない", "score": 0},
                {"text": "基本的なIT環境のみ", "score": 5},
                {"text": "中程度のIT環境が整備", "score": 10},
                {"text": "充実したIT環境が整備", "score": 15},
                {"text": "最新のIT環境が整備され、継続的に更新", "score": 20}
            ]
        },
        {
            "id": "t2",
            "text": "ネットワーク環境の状況は？",
            "choices": [
                {"text": "ネットワーク環境が不安定", "score": 0},
                {"text": "基本的なネットワークのみ", "score": 5},
                {"text": "安定したネットワーク環境", "score": 10},
                {"text": "高速で安定したネットワーク", "score": 15},
                {"text": "クラウド対応の高品質ネットワーク", "score": 20}
            ]
        },
        {
            "id": "t3",
            "text": "セキュリティ対策の状況は？",
            "choices": [
                {"text": "セキュリティ対策が不十分", "score": 0},
                {"text": "基本的なセキュリティ対策のみ", "score": 5},
                {"text": "標準的なセキュリティ対策", "score": 10},
                {"text": "充実したセキュリティ対策", "score": 15},
                {"text": "高度なセキュリティ対策と監視体制", "score": 20}
            ]
        },
        {
            "id": "t4",
            "text": "クラウドサービスの利用状況は？",
            "choices": [
                {"text": "クラウドサービスを利用していない", "score": 0},
                {"text": "一部のクラウドサービスを利用", "score": 5},
                {"text": "複数のクラウドサービスを利用", "score": 10},
                {"text": "積極的にクラウドサービスを利用", "score": 15},
                {"text": "クラウドファーストの戦略で運用", "score": 20}
            ]
        },
        {
            "id": "t5",
            "text": "システム統合・連携の状況は？",
            "choices": [
                {"text": "システムが統合されていない", "score": 0},
                {"text": "一部のシステムが連携", "score": 5},
                {"text": "基本的なシステム連携ができている", "score": 10},
                {"text": "多くのシステムが統合されている", "score": 15},
                {"text": "全システムが統合され、API連携も可能", "score": 20}
            ]
        }
    ],
    "process": [
        {
            "id": "p1",
            "text": "業務プロセスの標準化状況は？",
            "choices": [
                {"text": "業務プロセスが標準化されていない", "score": 0},
                {"text": "一部の業務が標準化", "score": 5},
                {"text": "主要業務が標準化", "score": 10},
                {"text": "多くの業務が標準化", "score": 15},
                {"text": "全業務が標準化され、継続的に改善", "score": 20}
            ]
        },
        {
            "id": "p2",
            "text": "業務効率化への取り組みは？",
            "choices": [
                {"text": "業務効率化への取り組みがない", "score": 0},
                {"text": "業務効率化を検討中", "score": 5},
                {"text": "一部の業務を効率化", "score": 10},
                {"text": "積極的に業務効率化を推進", "score": 15},
                {"text": "継続的に業務効率化を改善している", "score": 20}
            ]
        },
        {
            "id": "p3",
            "text": "業務の可視化・分析状況は？",
            "choices": [
                {"text": "業務の可視化・分析をしていない", "score": 0},
                {"text": "一部の業務を可視化", "score": 5},
                {"text": "主要業務を可視化・分析", "score": 10},
                {"text": "多くの業務を可視化・分析", "score": 15},
                {"text": "全業務を可視化し、データドリブンで改善", "score": 20}
            ]
        },
        {
            "id": "p4",
            "text": "意思決定プロセスの状況は？",
            "choices": [
                {"text": "データに基づかない意思決定", "score": 0},
                {"text": "一部の意思決定にデータを活用", "score": 5},
                {"text": "データを参考に意思決定", "score": 10},
                {"text": "データに基づいて意思決定", "score": 15},
                {"text": "データドリブンな意思決定文化がある", "score": 20}
            ]
        },
        {
            "id": "p5",
            "text": "継続的改善（PDCA）の実施状況は？",
            "choices": [
                {"text": "継続的改善を実施していない", "score": 0},
                {"text": "継続的改善を検討中", "score": 5},
                {"text": "不定期に改善を実施", "score": 10},
                {"text": "定期的に改善を実施", "score": 15},
                {"text": "継続的改善が組織文化として定着", "score": 20}
            ]
        }
    ],
    "compliance": [
        {
            "id": "c1",
            "text": "個人情報保護の取り組みは？",
            "choices": [
                {"text": "個人情報保護の取り組みが不十分", "score": 0},
                {"text": "基本的な個人情報保護対策", "score": 5},
                {"text": "標準的な個人情報保護対策", "score": 10},
                {"text": "充実した個人情報保護対策", "score": 15},
                {"text": "高度な個人情報保護体制と監視", "score": 20}
            ]
        },
        {
            "id": "c2",
            "text": "法令遵守（コンプライアンス）体制は？",
            "choices": [
                {"text": "コンプライアンス体制が不十分", "score": 0},
                {"text": "基本的なコンプライアンス体制", "score": 5},
                {"text": "標準的なコンプライアンス体制", "score": 10},
                {"text": "充実したコンプライアンス体制", "score": 15},
                {"text": "高度なコンプライアンス体制と監査", "score": 20}
            ]
        },
        {
            "id": "c3",
            "text": "データ管理に関する規程・ポリシーは？",
            "choices": [
                {"text": "データ管理規程がない", "score": 0},
                {"text": "基本的な規程がある", "score": 5},
                {"text": "標準的な規程がある", "score": 10},
                {"text": "充実した規程がある", "score": 15},
                {"text": "詳細な規程があり、定期的に見直し", "score": 20}
            ]
        },
        {
            "id": "c4",
            "text": "インシデント対応体制は？",
            "choices": [
                {"text": "インシデント対応体制がない", "score": 0},
                {"text": "基本的な対応体制", "score": 5},
                {"text": "標準的な対応体制", "score": 10},
                {"text": "充実した対応体制", "score": 15},
                {"text": "高度な対応体制と定期的な訓練", "score": 20}
            ]
        },
        {
            "id": "c5",
            "text": "外部監査・認証の取得状況は？",
            "choices": [
                {"text": "外部監査・認証を取得していない", "score": 0},
                {"text": "取得を検討中", "score": 5},
                {"text": "一部の認証を取得", "score": 10},
                {"text": "主要な認証を取得", "score": 15},
                {"text": "複数の認証を取得し、継続的に更新", "score": 20}
            ]
        }
    ]
}

CATEGORIES = {
    "business": "ビジネス準備度",
    "data": "データ準備度",
    "organization": "組織準備度",
    "technology": "技術準備度",
    "process": "プロセス準備度",
    "compliance": "コンプライアンス準備度"
}

# カテゴリーの説明
CATEGORY_DESCRIPTIONS = {
    "business": "経営陣の理解、予算確保、ROI期待など、AI導入の経営的な準備度を評価します。",
    "data": "記録のデジタル化、データ品質、データ蓄積など、AI活用に必要なデータ準備度を評価します。",
    "organization": "職員のITリテラシー、研修体制、組織の変化対応力など、組織的な準備度を評価します。",
    "technology": "IT環境、セキュリティ、ネットワーク、クラウド活用など、技術的な準備度を評価します。",
    "process": "業務標準化、効率化意識、データドリブンな意思決定など、プロセス面の準備度を評価します。",
    "compliance": "個人情報保護、法令遵守、データ管理規程など、コンプライアンス面の準備度を評価します。"
}

# 全質問数を取得する関数
def get_total_questions():
    """全質問数を返す"""
    return sum(len(questions) for questions in QUESTIONS.values())

# カテゴリーごとの質問数を取得する関数
def get_questions_by_category(category):
    """指定されたカテゴリーの質問リストを返す"""
    return QUESTIONS.get(category, [])

# 質問IDから質問を取得する関数
def get_question_by_id(question_id):
    """質問IDから質問データを取得する"""
    for category_questions in QUESTIONS.values():
        for question in category_questions:
            if question["id"] == question_id:
                return question
    return None

