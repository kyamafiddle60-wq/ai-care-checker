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
# 表示文言修正：慎重に→もっとも当てはまる
st.markdown("### 各質問について、もっとも当てはまる選択肢を選んでください。")

# CSSスタイルを追加（未回答のラジオボタンを視覚的に区別）
st.markdown("""
<style>
    /* 未回答のラジオボタンコンテナに特別なスタイルを適用 */
    div[data-question-id] {
        opacity: 0.5 !important;
        filter: grayscale(40%) !important;
        transition: opacity 0.3s ease, filter 0.3s ease;
    }
    
    /* 未回答のラジオボタン内のすべての要素を半透明に */
    div[data-question-id] div[data-testid="stRadio"] {
        opacity: 0.5 !important;
    }
    
    /* 未回答のラジオボタンのラベルテキスト */
    div[data-question-id] label {
        color: rgba(250, 250, 250, 0.6) !important;
        opacity: 0.6 !important;
    }
    
    /* 未回答のラジオボタンの円形部分 */
    div[data-question-id] input[type="radio"] {
        opacity: 0.5 !important;
    }
    
    /* ホバー時に少し明るくする */
    div[data-question-id]:hover {
        opacity: 0.75 !important;
        filter: grayscale(25%) !important;
    }
    
    div[data-question-id]:hover div[data-testid="stRadio"] {
        opacity: 0.75 !important;
    }
</style>
""", unsafe_allow_html=True)

# 診断をやり直すボタン（既に回答がある場合のみ表示）
if "answers" in st.session_state and len(st.session_state.answers) > 0:
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🔄 診断をやり直す", use_container_width=True, key="reset_diagnosis"):
            # セッション状態をクリア
            st.session_state.answers = {}
            # ラジオボタンのセッション状態もクリア
            keys_to_delete = [key for key in st.session_state.keys() if key.startswith("radio_")]
            for key in keys_to_delete:
                del st.session_state[key]
            # 前回の値もクリア
            st.session_state.radio_previous_values = {}
            st.rerun()

# セッション状態の初期化（診断をやり直すボタンが押されていない場合）
if "answers" not in st.session_state:
    st.session_state.answers = {}

# 初回表示時、ラジオボタンのセッション状態をクリア
if "diagnosis_initialized" not in st.session_state:
    st.session_state.diagnosis_initialized = True
    # ラジオボタンのセッション状態をクリア
    keys_to_delete = [key for key in st.session_state.keys() if key.startswith("radio_")]
    for key in keys_to_delete:
        del st.session_state[key]

st.markdown("---")

# 全質問数を計算
total_questions = sum(len(questions) for questions in QUESTIONS.values())

# 進捗（sticky表示用）
answered_top = len(st.session_state.answers)
progress_top = answered_top / total_questions if total_questions > 0 else 0.0

# Sticky Progress Bar用のCSS
st.markdown(
    """
    <style>
    .progress-sticky-wrapper {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999;
        background-color: #0e1117;
        padding: 12px 20px 16px 20px;
        border-bottom: 1px solid rgba(250, 250, 250, 0.1);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Streamlitのメインコンテナに上部パディングを追加して、固定バーの下にコンテンツが隠れないようにする */
    .main .block-container {
        padding-top: 80px !important;
    }
    
    /* サイドバーがある場合の調整 */
    [data-testid="stSidebar"] ~ .main .block-container {
        padding-top: 80px !important;
    }
    
    /* サイドバーの幅を考慮して進捗バーの位置を調整 */
    @media (min-width: 768px) {
        [data-testid="stSidebar"][aria-expanded="true"] ~ .main .progress-sticky-wrapper {
            margin-left: 21rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sticky Progress Bar
st.markdown('<div class="progress-sticky-wrapper">', unsafe_allow_html=True)
c1, c2 = st.columns([3, 1])
with c1:
    st.progress(progress_top)
with c2:
    st.markdown(f"**回答済み: {answered_top}/{total_questions}問**")
st.markdown("</div>", unsafe_allow_html=True)

# 各カテゴリーの質問を表示
for category, category_name in CATEGORIES.items():
    st.subheader(f"📊 {category_name}")
    
    questions = QUESTIONS[category]
    
    for question in questions:
        question_id = question["id"]
        question_text = question["text"]
        choices = question["choices"]
        
        # プレースホルダー付きの選択肢（index 0 を「選択してください」とする）
        choices_text = [choice["text"] for choice in choices]
        placeholder = "選択してください"
        display_options = [placeholder] + choices_text
        option_values = list(range(len(display_options)))  # 0..len-1
        
        # ラジオボタンのセッション状態キー
        radio_key = f"radio_{question_id}"
        # 既に選択したインデックス（プレースホルダーを含めたindex）
        saved_index_raw = st.session_state.get(radio_key, 0)
        saved_index = saved_index_raw if isinstance(saved_index_raw, int) and saved_index_raw >= 0 else 0
        
        # 回答を保存するコールバック関数
        def make_save_answer_callback(q_id, r_key):
            def save_answer():
                # on_changeコールバック内では、st.session_stateから現在の値を取得する
                current_value = st.session_state.get(r_key, 0)
                if isinstance(current_value, int) and current_value > 0:
                    # プレースホルダー(0)以外を回答として保存
                    answer_index = current_value - 1  # プレースホルダー分を補正
                    st.session_state.answers[q_id] = answer_index
                else:
                    # プレースホルダーの場合は未回答扱いにする
                    if q_id in st.session_state.answers:
                        del st.session_state.answers[q_id]
            return save_answer
        
        save_answer_callback = make_save_answer_callback(question_id, radio_key)
        
        # 未回答の場合は、ラジオボタンを半透明表示
        if saved_index == 0:
            st.markdown(f'<div data-question-id="{question_id}">', unsafe_allow_html=True)
        
        selected_index_with_placeholder = st.radio(
            question_text,
            options=option_values,  # use int values
            format_func=lambda i: display_options[i],
            index=saved_index,
            key=radio_key,
            on_change=save_answer_callback
        )
        
        if saved_index == 0:
            st.markdown("</div>", unsafe_allow_html=True)
        
        # 保存ロジック：プレースホルダー(0)以外を回答として保存
        if selected_index_with_placeholder > 0:
            answer_index = selected_index_with_placeholder - 1  # プレースホルダー分を補正
            st.session_state.answers[question_id] = answer_index
        else:
            # プレースホルダーの場合は未回答扱いにする
            if question_id in st.session_state.answers:
                del st.session_state.answers[question_id]
        
        # 質問間のスペース
        st.markdown("")
    
    st.markdown("---")

# 回答状況の再計算（入力処理後に計算して遅延を防ぐ）
answered = len(st.session_state.answers)
progress = answered / total_questions if total_questions > 0 else 0.0

# 全問回答済みの場合、結果ページへのボタンを表示
if answered == total_questions:
    st.success("✅ 全ての質問に回答しました！")
    st.markdown("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # ボタンクリック時に直接ページ遷移
        if st.button("📊 診断結果を見る", type="primary", use_container_width=True, key="view_results"):
            # セッション状態を確認してから遷移
            if len(st.session_state.answers) == total_questions:
                # ページ遷移前に少し待機してDOM操作を完了させる
                st.switch_page("pages/2_診断結果.py")
else:
    remaining = total_questions - answered
    st.info(f"💡 残り **{remaining}問** です。全ての質問に回答してください。")

