"""
診断履歴管理ページ
過去の診断結果の閲覧・比較・削除機能
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from modules.database import DiagnosisDatabase
from modules.pdf_generator import DiagnosticPDFGenerator
from modules.report_exporter import ReportExporter

# ページ設定
st.set_page_config(
    page_title="診断履歴 | AI Ready Checker",
    page_icon="📚",
    layout="wide"
)

# データベース初期化
db = DiagnosisDatabase()

# タイトル
st.title("📚 診断履歴")
st.markdown("過去の診断結果を確認・比較できます")

# ======================================
# サイドバー: フィルター機能
# ======================================
st.sidebar.header("🔍 フィルター")

# セッションIDフィルター
filter_session = st.sidebar.checkbox("現在のセッションのみ表示", value=False)
session_id = st.session_state.get('session_id', None) if filter_session else None

# 診断履歴を取得
if filter_session and session_id:
    diagnoses = db.get_recent_diagnoses(limit=100, session_id=session_id)
else:
    diagnoses = db.get_all_diagnoses()

# ======================================
# メインコンテンツ
# ======================================

if not diagnoses:
    st.info("📭 診断履歴がありません。まずは診断を実施してください。")
    if st.button("🏥 診断を開始する"):
        st.switch_page("pages/1_🏥_診断開始.py")
    st.stop()

st.success(f"✅ {len(diagnoses)}件の診断履歴が見つかりました")

# ======================================
# 診断履歴一覧
# ======================================
st.header("📋 診断履歴一覧")

# データフレーム作成
df = pd.DataFrame([
    {
        'ID': d['id'],
        '診断日時': d['diagnosis_date'].strftime('%Y-%m-%d %H:%M'),
        '施設名': d['facility_name'] if d['facility_name'] else '（未入力）',
        '総合スコア': f"{d['total_score']}/{d['max_score']}",
        '達成率': f"{d['percentage']:.1f}%",
        'ランク': d['rank']
    }
    for d in diagnoses
])

# 表示
st.dataframe(df, use_container_width=True, hide_index=True)

# ======================================
# 詳細表示・エクスポート機能
# ======================================
st.header("🔍 診断結果の詳細")

selected_id = st.selectbox(
    "表示する診断を選択してください",
    options=[d['id'] for d in diagnoses],
    format_func=lambda x: f"ID: {x} - {next((d['diagnosis_date'].strftime('%Y-%m-%d %H:%M') for d in diagnoses if d['id'] == x), '')}"
)

if selected_id:
    selected_diagnosis = db.get_diagnosis_by_id(selected_id)
    
    if selected_diagnosis:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("総合スコア", f"{selected_diagnosis['total_score']}/{selected_diagnosis['max_score']}")
        with col2:
            st.metric("達成率", f"{selected_diagnosis['percentage']:.1f}%")
        with col3:
            st.metric("ランク", selected_diagnosis['rank'])
        
        # カテゴリー別スコア
        st.subheader("📊 カテゴリー別スコア")
        
        categories_df = pd.DataFrame(selected_diagnosis['categories'])
        st.dataframe(categories_df, use_container_width=True, hide_index=True)
        
        # エクスポートボタン
        st.subheader("📤 エクスポート")
        
        col1, col2, col3, col4 = st.columns(4)
        
        exporter = ReportExporter()
        pdf_gen = DiagnosticPDFGenerator()
        
        with col1:
            # JSON エクスポート
            json_data = exporter.export_to_json(selected_diagnosis)
            st.download_button(
                label="📄 JSON",
                data=json_data,
                file_name=f"診断結果_{selected_diagnosis['id']}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            # CSV エクスポート（サマリー）
            csv_data = exporter.export_to_csv(selected_diagnosis)
            st.download_button(
                label="📊 CSV",
                data=csv_data,
                file_name=f"診断結果_{selected_diagnosis['id']}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col3:
            # CSV エクスポート（回答詳細）
            answers_csv = exporter.export_answers_to_csv(selected_diagnosis)
            st.download_button(
                label="📋 回答詳細CSV",
                data=answers_csv,
                file_name=f"診断回答_{selected_diagnosis['id']}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col4:
            # PDF エクスポート
            if st.button("📕 PDF生成", key=f"pdf_{selected_id}"):
                with st.spinner("PDF生成中..."):
                    try:
                        pdf_filename = f"診断結果レポート_{selected_diagnosis['id']}.pdf"
                        pdf_path = pdf_gen.generate_pdf(selected_diagnosis, filename=pdf_filename)
                        
                        st.success(f"✅ PDF生成完了")
                        
                        with open(pdf_path, "rb") as pdf_file:
                            st.download_button(
                                label="📕 PDFダウンロード",
                                data=pdf_file,
                                file_name=pdf_filename,
                                mime="application/pdf",
                                use_container_width=True,
                                key=f"pdf_dl_{selected_id}"
                            )
                    
                    except Exception as e:
                        st.error(f"❌ PDF生成エラー: {e}")

# ======================================
# 診断履歴の比較機能
# ======================================
st.markdown("---")
st.header("📈 診断履歴の比較")

if len(diagnoses) >= 2:
    st.markdown("複数の診断結果を比較して、改善の進捗を確認できます")
    
    # 比較する診断を選択
    compare_ids = st.multiselect(
        "比較する診断を選択してください（2〜5件）",
        options=[d['id'] for d in diagnoses],
        format_func=lambda x: f"ID: {x} - {next((d['diagnosis_date'].strftime('%Y-%m-%d %H:%M') for d in diagnoses if d['id'] == x), '')}",
        max_selections=5
    )
    
    if len(compare_ids) >= 2:
        # 比較データ取得
        compare_data = [db.get_diagnosis_by_id(did) for did in compare_ids]
        
        # 総合スコアの推移グラフ
        fig = go.Figure()
        
        for data in compare_data:
            fig.add_trace(go.Scatter(
                x=[data['diagnosis_date']],
                y=[data['total_score']],
                mode='markers+text',
                name=f"ID: {data['id']}",
                text=[f"{data['total_score']}点"],
                textposition="top center",
                marker=dict(size=15)
            ))
        
        fig.update_layout(
            title="総合スコアの推移",
            xaxis_title="診断日時",
            yaxis_title="スコア（点）",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # カテゴリー別比較
        st.subheader("📊 カテゴリー別スコア比較")
        
        # レーダーチャート
        fig_radar = go.Figure()
        
        for data in compare_data:
            categories = [cat['name'] for cat in data['categories']]
            scores = [cat['score'] for cat in data['categories']]
            
            fig_radar.add_trace(go.Scatterpolar(
                r=scores,
                theta=categories,
                fill='toself',
                name=f"ID: {data['id']} ({data['diagnosis_date'].strftime('%Y-%m-%d')})"
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=True,
            height=500
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)

else:
    st.info("📊 診断が2件以上になると、比較機能が利用できます")

# ======================================
# 診断削除機能
# ======================================
st.markdown("---")
st.header("🗑️ 診断履歴の削除")

with st.expander("⚠️ 診断を削除する"):
    st.warning("削除した診断は復元できません。慎重に操作してください。")
    
    delete_id = st.selectbox(
        "削除する診断を選択",
        options=[d['id'] for d in diagnoses],
        format_func=lambda x: f"ID: {x} - {next((d['diagnosis_date'].strftime('%Y-%m-%d %H:%M') for d in diagnoses if d['id'] == x), '')}",
        key="delete_select"
    )
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("🗑️ 削除実行", type="secondary", use_container_width=True):
            if db.delete_diagnosis(delete_id):
                st.success(f"✅ ID: {delete_id} の診断を削除しました")
                st.rerun()
            else:
                st.error("❌ 削除に失敗しました")

# ======================================
# ナビゲーション
# ======================================
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    if st.button("🏠 ホームに戻る", use_container_width=True):
        st.switch_page("app.py")

with col2:
    if st.button("🏥 新しい診断を開始", use_container_width=True):
        st.switch_page("pages/1_🏥_診断開始.py")
