import streamlit as st

# ページ設定
st.set_page_config(
    page_title="AI Ready Checker - 介護施設版",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# サイドバーメニュー
st.sidebar.title("🏥 AI Ready Checker")
st.sidebar.markdown("---")

# セッション状態の初期化
if 'menu' not in st.session_state:
    st.session_state['menu'] = "ホーム"

# メニュー選択
menu = st.sidebar.radio(
    "メニュー",
    ["ホーム", "無料診断", "診断結果", "料金プラン"],
    index=["ホーム", "無料診断", "診断結果", "料金プラン"].index(st.session_state['menu']),
    label_visibility="collapsed"
)

# メニューが変更されたらセッション状態を更新
if menu != st.session_state['menu']:
    st.session_state['menu'] = menu

st.sidebar.markdown("---")

# ホームページ
if st.session_state['menu'] == "ホーム":
    st.title("🏥 AI Ready Checker - 介護施設版")
    st.markdown("### 5分で分かる、あなたの施設のAI導入準備度")
    st.markdown("---")
    
    # ツールの説明
    st.header("📋 このツールについて")
    st.markdown("""
    AI Ready Checkerは、介護施設のAI導入準備度を診断する無料ツールです。
    簡単な質問に答えるだけで、あなたの施設がAIを導入する準備ができているかを
    5分で診断できます。
    """)
    
    st.markdown("---")
    
    # 主な特徴
    st.header("✨ 主な特徴")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        - **無料診断30問**
          - 施設の現状を把握するための30の質問
          - 5分で完了可能
        
        - **カスタマイズレポート**
          - 診断結果に基づいた詳細レポート
          - 改善点と推奨事項を提示
        """)
    
    with col2:
        st.markdown("""
        - **ROI試算**
          - AI導入による投資対効果を試算
          - 具体的な数値で効果を可視化
        
        - **補助金ガイド**
          - 利用可能な補助金・助成金情報
          - 申請方法のガイド
        """)
    
    st.markdown("---")
    
    # 開発者プロフィール
    st.header("👨‍💻 開発者プロフィール")
    st.info("""
    **山本喜一郎 (71歳)**
    - C言語・アセンブラ歴40年
    - AI学習1年
    """)
    
    st.markdown("---")
    
    # 無料診断を始めるボタン
    st.header("🚀 無料診断を始める")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("無料診断を始める", type="primary", use_container_width=True):
            st.session_state['menu'] = "無料診断"
            st.rerun()

# 無料診断ページ
elif st.session_state['menu'] == "無料診断":
    # 診断ページに自動遷移
    st.switch_page("pages/1_診断開始.py")

# 診断結果ページ
elif st.session_state['menu'] == "診断結果":
    # 診断結果ページに自動遷移
    if "answers" in st.session_state and len(st.session_state.answers) > 0:
        st.switch_page("pages/2_診断結果.py")
    else:
        st.title("📊 診断結果")
        st.markdown("---")
        st.warning("⚠️ 診断を完了していません。先に診断を受けてください。")
        if st.button("診断を開始する"):
            st.session_state['menu'] = "無料診断"
            st.switch_page("pages/1_診断開始.py")

# 料金プランページ
elif st.session_state['menu'] == "料金プラン":
    st.title("💰 料金プラン")
    st.markdown("---")
    
    # 3つのプランをカード形式で表示
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='border: 2px solid #e0e0e0; border-radius: 10px; padding: 20px; text-align: center; height: 100%;'>
            <h2>無料プラン</h2>
            <h1 style='color: #1f77b4;'>¥0</h1>
            <p>基本的な診断機能</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='border: 2px solid #ff9800; border-radius: 10px; padding: 20px; text-align: center; height: 100%;'>
            <h2>スタンダード</h2>
            <h1 style='color: #ff9800;'>¥9,800</h1>
            <p style='font-size: 0.9em;'>/月</p>
            <p>詳細レポート・ROI試算</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='border: 2px solid #f44336; border-radius: 10px; padding: 20px; text-align: center; height: 100%;'>
            <h2>プレミアム</h2>
            <h1 style='color: #f44336;'>¥29,800</h1>
            <p style='font-size: 0.9em;'>/月</p>
            <p>全機能 + サポート</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # プランの詳細説明
    st.markdown("### プラン詳細")
    
    st.markdown("""
    | 機能 | 無料プラン | スタンダード | プレミアム |
    |------|-----------|-------------|-----------|
    | 基本診断 | ✅ | ✅ | ✅ |
    | 詳細レポート | ❌ | ✅ | ✅ |
    | ROI試算 | ❌ | ✅ | ✅ |
    | 補助金ガイド | ❌ | ✅ | ✅ |
    | 専任サポート | ❌ | ❌ | ✅ |
    | カスタムコンサル | ❌ | ❌ | ✅ |
    """)

