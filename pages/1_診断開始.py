import streamlit as st
from modules.questions import QUESTIONS, CATEGORIES

# ページ設定
st.set_page_config(
    page_title="AI導入診断",
    page_icon="🏥",
    layout="wide"
)

# タイトル
st.title("🏥 AI導入準備度診断（30問）")
st.markdown("### 各質問に最も当てはまる選択肢を選んでください")
st.markdown("---")

# セッション状態の初期化
if "answers" not in st.session_state:
    st.session_state.answers = {}

# 進捗バー
total_questions = sum(len(questions) for questions in QUESTIONS.values())
answered = len(st.session_state.answers)
progress = answered / total_questions if total_questions > 0 else 0.0

# 進捗表示
col1, col2 = st.columns([3, 1])
with col1:
    st.progress(progress)
with col2:
    st.markdown(f"**回答済み: {answered}/{total_questions}問**")

st.markdown("---")

# 各カテゴリーの質問を表示
for category, category_name in CATEGORIES.items():
    st.subheader(f"📊 {category_name}")
    
    questions = QUESTIONS[category]
    
    for question in questions:
        question_id = question["id"]
        question_text = question["text"]
        choices = question["choices"]
        
        # 選択肢のテキストを取得
        choices_text = [choice["text"] for choice in choices]
        
        # 現在の回答を取得（なければNone）
        current_answer = st.session_state.answers.get(question_id, None)
        
        # ラジオボタンで選択肢を表示
        selected_index = st.radio(
            question_text,
            options=range(len(choices_text)),
            format_func=lambda x: choices_text[x],
            key=question_id,
            index=current_answer if current_answer is not None else None
        )
        
        # 回答をセッション状態に保存
        if selected_index is not None:
            st.session_state.answers[question_id] = selected_index
        
        # 質問間のスペース
        st.markdown("")
    
    st.markdown("---")

# 回答状況の確認
answered = len(st.session_state.answers)

# 全問回答済みの場合、結果ページへのボタンを表示
if answered == total_questions:
    st.success("✅ 全ての質問に回答しました！")
    st.markdown("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📊 診断結果を見る", type="primary", use_container_width=True):
            st.switch_page("pages/2_診断結果.py")
else:
    remaining = total_questions - answered
    st.info(f"💡 残り **{remaining}問** です。全ての質問に回答してください。")

