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

# URLパラメータからmenuを取得（料金プランページへの遷移用）
query_params = st.query_params
if 'menu' in query_params:
    menu_param = query_params['menu']
    if isinstance(menu_param, list):
        menu_param = menu_param[0]
    st.session_state['menu'] = menu_param

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
    # 料金プランページに自動遷移
    st.switch_page("pages/3_料金プラン.py")
    st.title("💰 料金プラン")
    st.markdown("### あなたの施設に最適なプランをお選びください")
    st.markdown("---")
    
    # 3つのプランをカード形式で表示
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='border: 2px solid #1f77b4; border-radius: 15px; padding: 30px 20px; text-align: center; height: 100%; background-color: rgba(31, 119, 180, 0.05);'>
            <h2 style='color: #1f77b4; margin-bottom: 20px;'>無料プラン</h2>
            <h1 style='color: #1f77b4; font-size: 2.5em; margin: 20px 0;'>¥0</h1>
            <p style='font-size: 1.1em; color: #666; margin-bottom: 30px;'>基本的な診断機能</p>
            <ul style='text-align: left; list-style: none; padding: 0;'>
                <li style='padding: 8px 0;'>✅ 基本診断（30問）</li>
                <li style='padding: 8px 0;'>✅ 診断結果表示</li>
                <li style='padding: 8px 0;'>✅ レーダーチャート</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='border: 2px solid #ff9800; border-radius: 15px; padding: 30px 20px; text-align: center; height: 100%; background-color: rgba(255, 152, 0, 0.05);'>
            <h2 style='color: #ff9800; margin-bottom: 20px;'>スタンダード</h2>
            <h1 style='color: #ff9800; font-size: 2.5em; margin: 20px 0;'>¥9,800</h1>
            <p style='font-size: 0.9em; color: #666; margin-bottom: 30px;'>/月</p>
            <p style='font-size: 1.1em; color: #666; margin-bottom: 30px;'>詳細レポート・ROI試算</p>
            <ul style='text-align: left; list-style: none; padding: 0;'>
                <li style='padding: 8px 0;'>✅ 基本診断（30問）</li>
                <li style='padding: 8px 0;'>✅ 詳細レポート</li>
                <li style='padding: 8px 0;'>✅ ROI試算</li>
                <li style='padding: 8px 0;'>✅ 補助金ガイド</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='border: 2px solid #f44336; border-radius: 15px; padding: 30px 20px; text-align: center; height: 100%; background-color: rgba(244, 67, 54, 0.05);'>
            <h2 style='color: #f44336; margin-bottom: 20px;'>プレミアム</h2>
            <h1 style='color: #f44336; font-size: 2.5em; margin: 20px 0;'>¥29,800</h1>
            <p style='font-size: 0.9em; color: #666; margin-bottom: 30px;'>/月</p>
            <p style='font-size: 1.1em; color: #666; margin-bottom: 30px;'>全機能 + サポート</p>
            <ul style='text-align: left; list-style: none; padding: 0;'>
                <li style='padding: 8px 0;'>✅ 基本診断（30問）</li>
                <li style='padding: 8px 0;'>✅ 詳細レポート</li>
                <li style='padding: 8px 0;'>✅ ROI試算</li>
                <li style='padding: 8px 0;'>✅ 補助金ガイド</li>
                <li style='padding: 8px 0;'>✅ 専任サポート</li>
                <li style='padding: 8px 0;'>✅ カスタムコンサル</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # プランの詳細説明
    st.markdown("### 📊 プラン詳細比較")
    
    st.markdown("""
    | 機能 | 無料プラン | スタンダード | プレミアム |
    |------|-----------|-------------|-----------|
    | 基本診断（30問） | ✅ | ✅ | ✅ |
    | 診断結果表示 | ✅ | ✅ | ✅ |
    | レーダーチャート | ✅ | ✅ | ✅ |
    | 詳細レポート | ❌ | ✅ | ✅ |
    | ROI試算 | ❌ | ✅ | ✅ |
    | 補助金ガイド | ❌ | ✅ | ✅ |
    | 専任サポート | ❌ | ❌ | ✅ |
    | カスタムコンサル | ❌ | ❌ | ✅ |
    """)
    
    st.markdown("---")
    
    # お問い合わせセクション
    st.markdown("### 📧 お問い合わせ")
    st.info("""
    プランの詳細や導入に関するご質問は、お気軽にお問い合わせください。
    スタンダードプラン・プレミアムプランのお申し込みも承っております。
    """)
    
    if st.button("📧 お問い合わせフォーム", type="primary", use_container_width=True):
        st.info("お問い合わせフォームは準備中です。")

