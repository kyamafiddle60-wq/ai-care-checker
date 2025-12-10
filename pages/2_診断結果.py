import streamlit as st
import plotly.graph_objects as go
from modules.scoring import (
    calculate_scores,
    get_readiness_rank,
    get_readiness_rank_label,
    compare_with_average,
    get_improvement_priorities,
    get_score_summary,
    get_category_max_score,
    INDUSTRY_AVERAGES
)
from modules.questions import CATEGORIES, QUESTIONS

# ページ設定
st.set_page_config(
    page_title="診断結果",
    page_icon="📊",
    layout="wide"
)

# セッションチェック
if "answers" not in st.session_state or len(st.session_state.answers) == 0:
    st.warning("⚠️ 診断を完了していません。先に診断を受けてください。")
    if st.button("診断を開始する"):
        st.switch_page("pages/1_診断開始.py")
    st.stop()

# スコア計算
try:
    # デバッグ: 回答データを確認
    if "answers" in st.session_state:
        # 回答データの型を確認
        answers = st.session_state.answers
        # すべての回答が整数（インデックス）であることを確認
        for q_id, answer in answers.items():
            if not isinstance(answer, int):
                st.warning(f"質問 {q_id} の回答が整数ではありません: {type(answer)} = {answer}")
    
    summary = get_score_summary(st.session_state.answers)
except Exception as e:
    st.error(f"スコア計算中にエラーが発生しました: {str(e)}")
    import traceback
    st.code(traceback.format_exc())
    st.stop()

st.title("📊 AI導入準備度診断結果")

# 総合スコア表示
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        "総合スコア",
        f"{summary['scores']['total_score']}/{summary['scores']['max_score']}点"
    )
with col2:
    st.metric(
        "達成率",
        f"{summary['scores']['percentage']}%"
    )
with col3:
    rank = summary['rank']
    rank_label = summary['rank_label']
    # ランクに応じた色分け
    if rank == "A":
        st.success(f"**準備度ランク: {rank}**")
    elif rank == "B":
        st.info(f"**準備度ランク: {rank}**")
    elif rank == "C":
        st.warning(f"**準備度ランク: {rank}**")
    else:
        st.error(f"**準備度ランク: {rank}**")
    st.caption(rank_label)

st.markdown("---")

# レーダーチャート
st.subheader("📈 カテゴリー別分析")

categories = list(CATEGORIES.values())
category_keys = list(CATEGORIES.keys())
category_scores_list = [summary['scores']['category_scores'][cat] for cat in category_keys]

# 業界平均値を取得
average_scores = [INDUSTRY_AVERAGES[cat] for cat in category_keys]

fig = go.Figure()

# あなたの施設のスコア
fig.add_trace(go.Scatterpolar(
    r=category_scores_list,
    theta=categories,
    fill='toself',
    name='あなたの施設',
    line=dict(color='#1f77b4', width=3)
))

# 業界平均
fig.add_trace(go.Scatterpolar(
    r=average_scores,
    theta=categories,
    fill='toself',
    name='業界平均',
    line=dict(color='#ff7f0e', dash='dash', width=2),
    opacity=0.5
))

# 最大スコアを取得（各カテゴリーの最大スコアを計算）
max_scores = {}
for cat in category_keys:
    max_scores[cat] = get_category_max_score(cat)

# レーダーチャートの設定
max_max_score = max(max_scores.values()) if max_scores else 100
fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, max_max_score],
            tickmode='linear',
            tick0=0,
            dtick=max_max_score // 5
        )
    ),
    showlegend=True,
    height=500,
    title="カテゴリー別スコア比較"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# カテゴリー別詳細
st.subheader("📋 カテゴリー別詳細スコア")

comparison = summary['comparison']
category_percentages = summary['category_percentages']

for category, category_name in CATEGORIES.items():
    score = summary['scores']['category_scores'][category]
    diff = comparison[category]
    percentage = category_percentages[category]
    max_score = max_scores.get(category, 100)
    
    # カード形式で表示
    with st.container():
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        with col1:
            st.write(f"**{category_name}**")
        with col2:
            st.write(f"{score}/{max_score}点")
        with col3:
            st.write(f"({percentage}%)")
        with col4:
            if diff > 0:
                st.success(f"業界平均より +{diff}")
            elif diff < 0:
                st.error(f"業界平均より {diff}")
            else:
                st.info("業界平均と同等")
        
        # プログレスバー
        progress_value = score / max_score if max_score > 0 else 0
        st.progress(progress_value)
        
        st.markdown("")

st.markdown("---")

# 改善優先度
st.subheader("🎯 改善優先度 TOP3")

priorities = summary['priorities']

if len(priorities) >= 3:
    top3 = priorities[:3]
else:
    top3 = priorities

for i, (category, score) in enumerate(top3, 1):
    category_name = CATEGORIES[category]
    max_score = max_scores.get(category, 100)
    percentage = category_percentages[category]
    
    with st.container():
        st.markdown(f"### {i}. {category_name}")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write(f"**現在スコア: {score}/{max_score}点 ({percentage}%)**")
        with col2:
            diff = comparison[category]
            if diff < 0:
                st.error(f"業界平均より {abs(diff)}点低い")
        
        # 改善提案
        suggestions = {
            "data": "記録業務のデジタル化を進め、データ品質管理体制を整備しましょう。定期的なデータクレンジングと標準化を実施することで、AI活用の基盤が整います。",
            "technology": "IT環境の整備とセキュリティ対策を優先的に実施しましょう。クラウドサービスの導入やネットワーク環境の改善を検討してください。",
            "organization": "職員向けのIT研修を実施し、サポート体制を構築しましょう。AI導入を推進する専任チームの設置も検討してください。",
            "business": "経営陣とAI導入の効果について認識を共有しましょう。ROI目標を設定し、予算確保の計画を立ててください。",
            "process": "業務の標準化と効率化の取り組みを開始しましょう。データドリブンな意思決定プロセスを構築し、継続的改善の文化を定着させてください。",
            "compliance": "個人情報保護とコンプライアンス体制を強化しましょう。データ管理規程の整備と定期的な監査を実施してください。"
        }
        st.info(f"💡 **改善提案**: {suggestions.get(category, '専門家に相談することをお勧めします。')}")
        st.markdown("")

st.markdown("---")

# 次のアクション
st.subheader("🚀 次のステップ")

col1, col2 = st.columns(2)
with col1:
    st.info("""
    **📊 無料プラン**
    - 基本的な診断結果の閲覧
    - カテゴリー別スコア分析
    - 改善優先度の表示
    """)
with col2:
    st.success("""
    **⭐ 有料プラン**
    - 詳細なROI試算
    - 補助金・助成金ガイド
    - 個別コンサルティング
    - カスタマイズレポート
    """)

st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔄 診断をやり直す", use_container_width=True):
        # セッション状態をクリア
        st.session_state.answers = {}
        # ラジオボタンのセッション状態もクリア
        keys_to_delete = [key for key in st.session_state.keys() if key.startswith("radio_")]
        for key in keys_to_delete:
            del st.session_state[key]
        st.switch_page("pages/1_診断開始.py")
with col2:
    if st.button("💰 料金プランを見る", use_container_width=True):
        # 料金プランページに直接遷移
        st.switch_page("pages/3_料金プラン.py")
with col3:
    if st.button("📧 お問い合わせ", use_container_width=True):
        st.info("お問い合わせフォームは準備中です。")

# 既存のコードの最後に追加

# ======================================
# データベース保存とエクスポート機能
# ======================================
from modules.database import DiagnosisDatabase
from modules.pdf_generator import DiagnosticPDFGenerator
from modules.report_exporter import ReportExporter
from datetime import datetime

st.markdown("---")
st.header("📤 結果の保存とエクスポート")

# データベース初期化
db = DiagnosisDatabase()

# 必要な変数をsummaryから取得
total_score = summary['scores']['total_score']
max_score = summary['scores']['max_score']
percentage = summary['scores']['percentage']
category_scores = summary['scores']['category_scores']

# 質問データを取得（全カテゴリーの質問をフラットなリストに）
all_questions = []
for category_key, category_name in CATEGORIES.items():
    category_questions = QUESTIONS.get(category_key, [])
    for q in category_questions:
        all_questions.append({
            'category': category_key,
            'category_name': category_name,
            'id': q['id'],
            'text': q['text']
        })

# 診断データの準備
diagnosis_data = {
    'facility_name': st.session_state.get('facility_name', ''),
    'diagnosis_date': datetime.now(),
    'total_score': total_score,
    'max_score': max_score,
    'percentage': percentage,
    'rank': rank,
    'categories': [
        {
            'name': category,
            'score': score,
            'percentage': (score / max_scores.get(category, 100)) * 100 if max_scores.get(category, 100) > 0 else 0,
            'diff': score - comparison.get(category, 0),
            'comment': f'{CATEGORIES.get(category, category)}のスコアは{score}点です。'
        }
        for category, score in category_scores.items()
    ],
    'answers': [
        {
            'category': q['category'],
            'category_name': q['category_name'],
            'number': idx + 1,
            'question_id': q['id'],
            'question': q['text'],
            'answer': st.session_state.answers.get(q['id'], '選択されていません')
        }
        for idx, q in enumerate(all_questions)
    ],
    'session_id': st.session_state.get('session_id', ''),
    'user_id': st.session_state.get('user_id', '')
}

# 改善提案TOP3を生成
sorted_categories = sorted(
    diagnosis_data['categories'],
    key=lambda x: x['score']
)[:3]

top3_improvements = [
    {
        'category': CATEGORIES.get(cat['name'], cat['name']),
        'score': cat['score'],
        'percentage': cat['percentage'],
        'diff': cat['diff'],
        'suggestion': f"{CATEGORIES.get(cat['name'], cat['name'])}の改善を優先的に進めることを推奨します。経営陣とAI導入の効果について認識を共有し、ROI目標を設定し、予算確保の計画を立ててください。"
    }
    for cat in sorted_categories
]

diagnosis_data['top3_improvements'] = top3_improvements

# エクスポートボタン
col1, col2, col3, col4 = st.columns(4)

exporter = ReportExporter()
pdf_gen = DiagnosticPDFGenerator()

with col1:
    if st.button("💾 履歴に保存", type="primary", use_container_width=True):
        try:
            diagnosis_id = db.save_diagnosis(diagnosis_data)
            st.success(f"✅ 診断結果を保存しました（ID: {diagnosis_id}）")
        except Exception as e:
            st.error(f"❌ 保存エラー: {e}")

with col2:
    # JSON ダウンロード
    try:
        json_data = exporter.export_to_json(diagnosis_data)
        st.download_button(
            label="📄 JSON",
            data=json_data,
            file_name=f"診断結果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"JSON エラー: {e}")

with col3:
    # CSV ダウンロード
    try:
        csv_data = exporter.export_to_csv(diagnosis_data)
        st.download_button(
            label="📊 CSV",
            data=csv_data,
            file_name=f"診断結果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"CSV エラー: {e}")

with col4:
    # PDF 生成
    if st.button("📕 PDF生成", use_container_width=True):
        with st.spinner("PDF生成中... しばらくお待ちください"):
            try:
                pdf_filename = f"診断結果レポート_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                pdf_path = pdf_gen.generate_pdf(diagnosis_data, filename=pdf_filename)
                
                st.success("✅ PDF生成完了！")
                
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="📕 PDFをダウンロード",
                        data=pdf_file,
                        file_name=pdf_filename,
                        mime="application/pdf",
                        key="pdf_download",
                        use_container_width=True
                    )
            
            except Exception as e:
                st.error(f"❌ PDF生成エラー: {e}")
                st.exception(e)

# 履歴ページへのリンク
st.markdown("---")
st.info("💡 過去の診断結果を確認するには、診断履歴ページをご利用ください")

if st.button("📚 診断履歴を見る", use_container_width=True):
    st.switch_page("pages/3_📚_診断履歴.py")
    