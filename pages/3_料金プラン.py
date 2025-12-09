import streamlit as st

# ページ設定
st.set_page_config(
    page_title="料金プラン",
    page_icon="💰",
    layout="wide"
)

# タイトル
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

