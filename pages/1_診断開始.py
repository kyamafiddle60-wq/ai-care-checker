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

st.markdown("""
<style>
    /* ラジオボタンを確実に表示 */
    [data-baseweb="radio"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
</style>
<script>
(function() {
    const GREEN = '#10b981';
    const RED = '#ef4444';
    
    function applyRadioColors() {
        // すべてのラジオボタンを取得
        const radios = document.querySelectorAll('[data-baseweb="radio"]');
        
        if (radios.length === 0) {
            return;
        }
        
        // ラジオボタンをグループごとに処理（同じ質問のラジオボタンは同じ親要素の下に存在）
        const radioGroups = new Map();
        
        radios.forEach(radio => {
            // 親要素を探す（ラジオボタンのグループ）
            let parent = radio.closest('div[data-testid], div[class*="radio"], div[class*="stRadio"]');
            if (!parent) {
                parent = radio.parentElement;
            }
            
            const groupId = parent ? parent.getAttribute('data-testid') || parent.className || 'default' : 'default';
            
            if (!radioGroups.has(groupId)) {
                radioGroups.set(groupId, []);
            }
            radioGroups.get(groupId).push(radio);
        });
        
        // 各グループごとに、選択されたラジオボタンを1つだけ特定
        radioGroups.forEach((groupRadios, groupId) => {
            // グループ内で実際に選択されているラジオボタンを探す
            let checkedRadio = null;
            
            groupRadios.forEach(radio => {
                const isChecked = radio.getAttribute('aria-checked') === 'true';
                const computedStyle = window.getComputedStyle(radio);
                
                // より正確な選択状態の判定
                if (isChecked && computedStyle.display !== 'none') {
                    // 既にチェック済みのラジオボタンが見つかった場合
                    if (checkedRadio) {
                        // 後から見つかった方を優先（Streamlitが更新した方）
                        checkedRadio = radio;
                    } else {
                        checkedRadio = radio;
                    }
                }
            });
            
            // グループ内のすべてのラジオボタンに色を適用
            groupRadios.forEach(radio => {
                radio.style.display = 'flex';
                radio.style.visibility = 'visible';
                radio.style.opacity = '1';
                
                // 選択されているかどうか
                const isThisChecked = (radio === checkedRadio);
                
                // 色を適用
                if (isThisChecked) {
                    // 選択済み: 緑色
                    radio.style.setProperty('border-color', GREEN, 'important');
                    radio.style.setProperty('background-color', GREEN, 'important');
                    
                    // 子要素にも緑色を適用
                    radio.querySelectorAll('*').forEach(child => {
                        if (child.tagName === 'DIV' || child.tagName === 'SVG' || child.tagName === 'circle') {
                            const computed = window.getComputedStyle(child);
                            const borderRadius = computed.borderRadius;
                            const width = parseFloat(computed.width) || 0;
                            
                            if (borderRadius === '50%' || borderRadius === '9999px' || (width > 0 && width < 30)) {
                                child.style.setProperty('border-color', GREEN, 'important');
                                if (width >= 10) {
                                    child.style.setProperty('background-color', GREEN, 'important');
                                } else if (width < 10) {
                                    child.style.setProperty('background-color', 'white', 'important');
                                }
                            }
                        }
                        if (child.tagName === 'svg' || child.tagName === 'circle') {
                            child.style.setProperty('stroke', GREEN, 'important');
                            child.style.setProperty('fill', isThisChecked ? GREEN : 'transparent', 'important');
                        }
                    });
                } else {
                    // 未選択: 赤色
                    radio.style.setProperty('border-color', RED, 'important');
                    radio.style.setProperty('background-color', 'transparent', 'important');
                    
                    // 子要素にも赤色を適用
                    radio.querySelectorAll('*').forEach(child => {
                        if (child.tagName === 'DIV' || child.tagName === 'SVG' || child.tagName === 'circle') {
                            const computed = window.getComputedStyle(child);
                            const borderRadius = computed.borderRadius;
                            
                            if (borderRadius === '50%' || borderRadius === '9999px') {
                                child.style.setProperty('border-color', RED, 'important');
                                child.style.setProperty('background-color', 'transparent', 'important');
                            }
                        }
                        if (child.tagName === 'svg' || child.tagName === 'circle') {
                            child.style.setProperty('stroke', RED, 'important');
                            child.style.setProperty('fill', 'transparent', 'important');
                        }
                    });
                }
            });
        });
    }
    
    // 即座に実行
    applyRadioColors();
    
    // 複数のタイミングで実行
    setTimeout(applyRadioColors, 100);
    setTimeout(applyRadioColors, 300);
    setTimeout(applyRadioColors, 500);
    setTimeout(applyRadioColors, 1000);
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(applyRadioColors, 100);
            setTimeout(applyRadioColors, 500);
        });
    }
    
    // MutationObserverで監視（aria-checked属性の変更を検出）
    const observer = new MutationObserver(function(mutations) {
        let needsUpdate = false;
        mutations.forEach(function(mutation) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'aria-checked') {
                needsUpdate = true;
            }
            if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                needsUpdate = true;
            }
        });
        if (needsUpdate) {
            setTimeout(applyRadioColors, 50);
            setTimeout(applyRadioColors, 150);
            setTimeout(applyRadioColors, 300);
        }
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['aria-checked', 'class']
    });
    
    // クリックイベントでも更新
    document.addEventListener('click', function(e) {
        if (e.target.closest('[data-baseweb="radio"]')) {
            setTimeout(applyRadioColors, 10);
            setTimeout(applyRadioColors, 100);
            setTimeout(applyRadioColors, 300);
        }
    }, true);
    
    // 定期的にチェック
    setInterval(applyRadioColors, 500);
})();
</script>
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
        
        selected_index_with_placeholder = st.radio(
            question_text,
            options=option_values,  # use int values
            format_func=lambda i: display_options[i],
            index=saved_index,
            key=radio_key,
            on_change=save_answer_callback
        )

        
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

