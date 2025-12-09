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
from modules.questions import CATEGORIES

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
        st.switch_page("app.py")
with col3:
    if st.button("📧 お問い合わせ", use_container_width=True):
        st.info("お問い合わせフォームは準備中です。")

