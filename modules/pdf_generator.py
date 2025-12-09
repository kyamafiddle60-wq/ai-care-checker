"""
PDF生成機能モジュール
ReportLabを使用して診断結果をPDF化
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # GUI不要のバックエンド
import io
from PIL import Image as PILImage
import os
import subprocess
import urllib.request
import zipfile
import shutil
from modules.scoring import INDUSTRY_AVERAGES
from modules.questions import CATEGORIES

# 日本語フォント設定（japanize-matplotlibの代替）
def setup_japanese_font():
    """matplotlibで日本語フォントを設定"""
    try:
        # macOSの場合
        if os.name == 'posix':
            # macOSのシステムフォントを使用
            font_paths = [
                '/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc',
                '/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc',
                '/Library/Fonts/ヒラギノ角ゴシック W3.ttc',
            ]
            for font_path in font_paths:
                if os.path.exists(font_path):
                    plt.rcParams['font.family'] = 'Hiragino Sans'
                    break
            else:
                # フォントが見つからない場合はデフォルトを使用
                plt.rcParams['font.family'] = 'DejaVu Sans'
        else:
            # Windows/Linuxの場合
            plt.rcParams['font.family'] = 'DejaVu Sans'
    except Exception as e:
        print(f"フォント設定エラー: {e}")
        plt.rcParams['font.family'] = 'DejaVu Sans'

# フォント設定を実行
setup_japanese_font()

class DiagnosticPDFGenerator:
    """診断結果PDF生成クラス"""
    
    def __init__(self):
        """初期化"""
        self.setup_fonts()
        self.styles = self.create_styles()
        
    def setup_fonts(self):
        """日本語フォントの設定"""
        self.font_name = None  # 初期値はNone（エラー検出用）
        
        try:
            # プロジェクト内のフォントファイルを優先的に探す（正しいTTFファイルの場合のみ）
            font_paths = [
                os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets/fonts/NotoSansJP-Regular.ttf"),
                os.path.join(os.getcwd(), "assets/fonts/NotoSansJP-Regular.ttf"),
                "assets/fonts/NotoSansJP-Regular.ttf",
            ]
            
            for font_path in font_paths:
                if os.path.exists(font_path):
                    # ファイルが実際にTTFファイルか確認
                    try:
                        # fileコマンドでファイルタイプを確認
                        result = subprocess.run(['file', font_path], capture_output=True, text=True)
                        file_type = result.stdout.lower()
                        # HTMLファイルやテキストファイルは削除してスキップ
                        if 'html' in file_type or ('text' in file_type and 'truetype' not in file_type and 'opentype' not in file_type):
                            print(f"警告: '{font_path}' はHTML/テキストファイルです。削除します。")
                            os.remove(font_path)
                            continue
                        if 'truetype' in file_type or ('opentype' in file_type and 'postscript' not in file_type) or font_path.endswith('.ttf'):
                            font_name = 'notosansjp'
                            try:
                                pdfmetrics.registerFont(TTFont(font_name, font_path))
                                pdfmetrics.registerFontFamily(
                                    font_name,
                                    normal=font_name,
                                    bold=font_name,
                                    italic=font_name,
                                    boldItalic=font_name
                                )
                                if pdfmetrics.getFont(font_name):
                                    self.font_name = font_name
                                    print(f"✅ フォント '{font_name}' を正常に登録しました: {font_path}")
                                    return
                            except Exception as font_error:
                                # PostScriptアウトラインの場合はスキップ
                                if 'postscript' in str(font_error).lower():
                                    print(f"警告: '{font_path}' はPostScriptアウトラインのため使用できません。スキップします。")
                                    os.remove(font_path)
                                    continue
                                raise font_error
                    except Exception as e:
                        print(f"フォント '{font_path}' の登録に失敗: {e}")
                        # 不正なファイルの可能性があるので削除
                        try:
                            if os.path.exists(font_path):
                                os.remove(font_path)
                        except:
                            pass
                        continue
            
            # macOSのシステムフォントを試す（TTCファイルはPostScriptアウトラインのためReportLabでは使用不可）
            # 代わりに、ユーザーのホームディレクトリやその他の場所を探す
            if os.name == 'posix':
                # ユーザーのフォントディレクトリを探す
                user_font_dirs = [
                    os.path.expanduser('~/Library/Fonts'),
                    '/Library/Fonts',
                ]
                
                for font_dir in user_font_dirs:
                    if os.path.exists(font_dir):
                        # Noto Sans JPフォントを探す
                        for font_file in os.listdir(font_dir):
                            if 'noto' in font_file.lower() and 'jp' in font_file.lower() and (font_file.endswith('.ttf') or font_file.endswith('.otf')):
                                font_path = os.path.join(font_dir, font_file)
                                try:
                                    font_name = 'notosansjp'
                                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                                    pdfmetrics.registerFontFamily(
                                        font_name,
                                        normal=font_name,
                                        bold=font_name,
                                        italic=font_name,
                                        boldItalic=font_name
                                    )
                                    if pdfmetrics.getFont(font_name):
                                        self.font_name = font_name
                                        print(f"システムフォント '{font_name}' を正常に登録しました: {font_path}")
                                        return
                                except Exception as e:
                                    print(f"フォント '{font_path}' の登録に失敗: {e}")
                                    continue
            
            
            # フォントが登録されなかった場合、自動ダウンロードを試みる
            if self.font_name is None:
                print("日本語フォントが見つかりません。自動ダウンロードを試みます...")
                font_downloaded = self._download_font()
                if font_downloaded:
                    # ダウンロード後に再度フォントを探す
                    font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets/fonts/NotoSansJP-Regular.ttf")
                    if os.path.exists(font_path):
                        try:
                            result = subprocess.run(['file', font_path], capture_output=True, text=True)
                            file_type = result.stdout.lower()
                            if 'truetype' in file_type or 'opentype' in file_type:
                                font_name = 'notosansjp'
                                pdfmetrics.registerFont(TTFont(font_name, font_path))
                                pdfmetrics.registerFontFamily(
                                    font_name,
                                    normal=font_name,
                                    bold=font_name,
                                    italic=font_name,
                                    boldItalic=font_name
                                )
                                if pdfmetrics.getFont(font_name):
                                    self.font_name = font_name
                                    print(f"✅ フォント '{font_name}' を正常に登録しました: {font_path}")
                                    return
                        except Exception as e:
                            print(f"ダウンロードしたフォントの登録に失敗: {e}")
                
                # フォントが登録されなかった場合の処理
                print("=" * 80)
                print("警告: 日本語フォントが見つかりませんでした。")
                print("PDFの日本語表示が正しく行われない可能性があります。")
                print("")
                print("解決方法（手動ダウンロード）:")
                print("1. 以下のURLからNoto Sans JPフォントをダウンロードしてください:")
                print("   https://fonts.google.com/noto/specimen/Noto+Sans+JP")
                print("2. ダウンロードしたZIPファイルを解凍し、")
                print("   'NotoSansJP-Regular.ttf' ファイルを以下の場所に配置してください:")
                print(f"   {os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets/fonts/NotoSansJP-Regular.ttf')}")
                print("3. アプリケーションを再起動してください")
                print("")
                print("注意: ファイル名は 'NotoSansJP-Regular.ttf' である必要があります")
                print("=" * 80)
                # デフォルトフォントを使用（日本語は文字化けする）
                self.font_name = 'Helvetica'
        except Exception as e:
            print(f"フォント設定エラー: {e}")
            import traceback
            traceback.print_exc()
            # エラーが発生した場合もデフォルトフォントで続行
            if self.font_name is None:
                print("警告: フォント設定に失敗しました。デフォルトフォント（Helvetica）を使用します。")
                print("日本語は文字化けする可能性があります。")
                self.font_name = 'Helvetica'
    
    def _download_font(self):
        """Noto Sans JPフォントを自動ダウンロード"""
        try:
            # assets/fontsディレクトリのパスを取得
            base_dir = os.path.dirname(os.path.dirname(__file__))
            fonts_dir = os.path.join(base_dir, "assets", "fonts")
            os.makedirs(fonts_dir, exist_ok=True)
            
            font_path = os.path.join(fonts_dir, "NotoSansJP-Regular.ttf")
            
            # 既に正しいフォントファイルが存在する場合はスキップ
            if os.path.exists(font_path):
                try:
                    result = subprocess.run(['file', font_path], capture_output=True, text=True)
                    file_type = result.stdout.lower()
                    if 'truetype' in file_type or 'opentype' in file_type:
                        return True  # 既に正しいフォントファイルが存在
                    else:
                        # HTMLファイルや不正なファイルの場合は削除
                        print(f"警告: 不正なフォントファイルを検出しました。削除して再ダウンロードします。")
                        os.remove(font_path)
                except:
                    pass
            
            # 信頼できるソースからTTFフォントを直接ダウンロード
            # Google FontsのGitHubリポジトリからTTFファイルを取得
            font_urls = [
                # Google FontsのGitHubリポジトリ（正しいパス）
                "https://raw.githubusercontent.com/googlefonts/noto-fonts/main/hinted/ttf/NotoSansJP/NotoSansJP-Regular.ttf",
                # 別のGitHubリポジトリ（バックアップ）
                "https://raw.githubusercontent.com/googlefonts/noto-cjk/main/Sans/Variable/TTF/Subset/NotoSansCJK-Regular.ttf",
            ]
            
            font_url = None
            for url in font_urls:
                try:
                    # URLが有効か確認（HEADリクエスト）
                    req = urllib.request.Request(url, method='HEAD')
                    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
                    with urllib.request.urlopen(req, timeout=10) as response:
                        if response.status == 200:
                            font_url = url
                            print(f"有効なURLを見つけました: {url}")
                            break
                except Exception as e:
                    print(f"URL確認失敗 ({url}): {e}")
                    continue
            
            # 有効なURLが見つからない場合、最初のURLを試す
            if font_url is None:
                font_url = font_urls[0]
                print(f"デフォルトURLを使用: {font_url}")
            
            print(f"フォントをダウンロード中: {font_url}")
            print(f"保存先: {font_path}")
            
            # フォントファイルをダウンロード（タイムアウト設定とUser-Agentヘッダー）
            req = urllib.request.Request(font_url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
            
            try:
                with urllib.request.urlopen(req, timeout=30) as response:
                    with open(font_path, 'wb') as out_file:
                        shutil.copyfileobj(response, out_file)
            except urllib.error.HTTPError as e:
                # 404エラーの場合、別のURLを試す
                if e.code == 404:
                    print(f"URLが見つかりませんでした: {font_url}")
                    # 代替URLを順番に試す
                    for alt_url in font_urls[1:]:
                        print(f"代替URLを試します: {alt_url}")
                        try:
                            alt_req = urllib.request.Request(alt_url)
                            alt_req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
                            with urllib.request.urlopen(alt_req, timeout=30) as alt_response:
                                with open(font_path, 'wb') as out_file:
                                    shutil.copyfileobj(alt_response, out_file)
                            font_url = alt_url
                            break
                        except Exception as alt_e:
                            print(f"代替URLも失敗: {alt_e}")
                            continue
                    else:
                        raise e
                else:
                    raise e
            
            # ダウンロードしたファイルが正しいか確認
            if os.path.exists(font_path) and os.path.getsize(font_path) > 1000:  # 1KB以上
                result = subprocess.run(['file', font_path], capture_output=True, text=True)
                file_type = result.stdout.lower()
                # HTMLファイルやテキストファイルの場合は削除
                if 'html' in file_type or ('text' in file_type and 'truetype' not in file_type and 'opentype' not in file_type):
                    print(f"警告: ダウンロードしたファイルがHTML/テキストファイルです: {file_type}")
                    os.remove(font_path)
                    return False
                if 'truetype' in file_type or ('opentype' in file_type and 'postscript' not in file_type):
                    # ReportLabでフォントを登録して確認（PostScriptアウトラインでないことを確認）
                    try:
                        test_font_name = 'test_notosansjp_temp'
                        test_font = TTFont(test_font_name, font_path)
                        # フォントが正常に読み込めた場合は成功
                        del test_font  # テスト用フォントを削除
                        print("✅ フォントのダウンロードが完了しました（TrueTypeアウトライン確認済み）")
                        return True
                    except Exception as font_test_error:
                        if 'postscript' in str(font_test_error).lower():
                            print(f"警告: ダウンロードしたフォントはPostScriptアウトラインのため使用できません")
                            os.remove(font_path)
                            return False
                        print(f"警告: フォントの読み込みに失敗しました: {font_test_error}")
                        os.remove(font_path)
                        return False
                else:
                    print(f"警告: ダウンロードしたファイルが正しいフォントファイルではありません: {file_type}")
                    os.remove(font_path)
                    return False
            else:
                print("警告: フォントのダウンロードに失敗しました")
                if os.path.exists(font_path):
                    os.remove(font_path)
                return False
                
        except Exception as e:
            print(f"フォントのダウンロード中にエラーが発生しました: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def create_styles(self):
        """PDFスタイルの作成"""
        styles = getSampleStyleSheet()
        
        # 登録されたフォント名を使用（Noneの場合はデフォルト）
        if self.font_name is None:
            self.font_name = 'Helvetica'
        
        font_name = self.font_name
        
        # タイトルスタイル（親スタイルから継承せず、完全に独立）
        styles.add(ParagraphStyle(
            name='CustomTitle',
            fontName=font_name,
            fontSize=24,
            textColor=colors.HexColor('#1E3A8A'),
            alignment=TA_CENTER,
            spaceAfter=30,
            leading=28
        ))
        
        # 見出しスタイル1（親スタイルから継承せず、完全に独立）
        styles.add(ParagraphStyle(
            name='CustomHeading1',
            fontName=font_name,
            fontSize=18,
            textColor=colors.HexColor('#1E3A8A'),
            spaceAfter=12,
            spaceBefore=12,
            leading=22
        ))
        
        # 見出しスタイル2（親スタイルから継承せず、完全に独立）
        styles.add(ParagraphStyle(
            name='CustomHeading2',
            fontName=font_name,
            fontSize=14,
            textColor=colors.HexColor('#2563EB'),
            spaceAfter=10,
            spaceBefore=10,
            leading=18
        ))
        
        # 本文スタイル（親スタイルから継承せず、完全に独立）
        styles.add(ParagraphStyle(
            name='CustomBody',
            fontName=font_name,
            fontSize=10,
            leading=16,
            textColor=colors.HexColor('#1F2937')
        ))
        
        return styles
    
    def create_radar_chart_image(self, scores_dict):
        """レーダーチャートを画像として生成"""
        # カテゴリー名のリストとスコアのリストを取得
        categories = list(scores_dict.keys())
        values = list(scores_dict.values())
        
        # カテゴリー数と値の数を確認
        if len(categories) != len(values):
            raise ValueError(f"カテゴリー数({len(categories)})と値の数({len(values)})が一致しません")
        
        # 業界平均をカテゴリー順に取得
        # scores_dictのキーはカテゴリー名（日本語）なので、CATEGORIESの逆引きでキーを取得
        category_keys = []
        for cat_name in categories:
            # カテゴリー名からキーを逆引き
            for key, name in CATEGORIES.items():
                if name == cat_name:
                    category_keys.append(key)
                    break
        
        # 業界平均値をカテゴリー順に取得
        industry_avg = [INDUSTRY_AVERAGES.get(key, 50) for key in category_keys]
        
        # データの整合性チェック
        if len(industry_avg) != len(values):
            # フォールバック: デフォルト値を生成
            industry_avg = [50] * len(values)
        
        # レーダーチャート作成
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, polar=True)
        
        # 日本語フォント設定を確実に適用
        setup_japanese_font()
        
        # 角度を計算（カテゴリー数に応じて）
        num_categories = len(categories)
        angles = [n / float(num_categories) * 2 * 3.14159 for n in range(num_categories)]
        
        # レーダーチャートを閉じるために最初の値を最後に追加
        values_closed = values + [values[0]]
        industry_avg_closed = industry_avg + [industry_avg[0]]
        angles_closed = angles + [angles[0]]
        
        # プロット
        ax.plot(angles_closed, values_closed, 'o-', linewidth=2, label='あなたの施設', color='#3B82F6')
        ax.fill(angles_closed, values_closed, alpha=0.25, color='#3B82F6')
        ax.plot(angles_closed, industry_avg_closed, 'o-', linewidth=2, label='業界平均', color='#EF4444')
        ax.fill(angles_closed, industry_avg_closed, alpha=0.15, color='#EF4444')
        
        # ラベル設定（日本語フォントを明示的に指定）
        ax.set_xticks(angles)
        ax.set_xticklabels(categories, fontsize=12, fontfamily=plt.rcParams['font.family'])
        ax.set_ylim(0, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), prop={'family': plt.rcParams['font.family']})
        ax.grid(True)
        
        # 画像として保存
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=150)
        buffer.seek(0)
        plt.close()
        
        return buffer
    
    def create_score_bar_table(self, categories_data):
        """カテゴリー別スコアバーをテーブルで作成"""
        data = [['カテゴリー', 'スコア', '達成率', '業界平均との差']]
        
        for cat in categories_data:
            name = cat['name']
            score = f"{cat['score']}/100点"
            percentage = f"{cat['percentage']:.1f}%"
            diff = cat['diff']
            diff_text = f"業界平均より {abs(diff)}点{'高い' if diff > 0 else '低い'}"
            
            data.append([name, score, percentage, diff_text])
        
        table = Table(data, colWidths=[100*mm, 40*mm, 30*mm, 60*mm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), self.font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTNAME', (0, 1), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        return table
    
    def generate_pdf(self, diagnosis_data, filename="診断結果レポート.pdf"):
        """
        診断結果PDFを生成
        
        Args:
            diagnosis_data (dict): 診断データ
                {
                    'facility_name': str,
                    'diagnosis_date': datetime,
                    'total_score': int,
                    'max_score': int,
                    'percentage': float,
                    'rank': str,
                    'categories': list,
                    'top3_improvements': list,
                    'answers': list
                }
            filename (str): 出力ファイル名
        
        Returns:
            str: 生成されたPDFファイルのパス
        """
        # PDFドキュメント作成
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        # ==================== 1ページ目: 表紙 ====================
        story.append(Spacer(1, 80*mm))
        
        title = Paragraph("AI導入準備度診断結果レポート", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 20*mm))
        
        if diagnosis_data.get('facility_name'):
            facility = Paragraph(f"施設名: {diagnosis_data['facility_name']}", self.styles['CustomBody'])
            story.append(facility)
            story.append(Spacer(1, 10*mm))
        
        date_str = diagnosis_data['diagnosis_date'].strftime('%Y年%m月%d日')
        date_para = Paragraph(f"診断日: {date_str}", self.styles['CustomBody'])
        story.append(date_para)
        story.append(Spacer(1, 20*mm))
        
        # 総合スコア（大きく表示）
        score_text = f"総合スコア: {diagnosis_data['total_score']}/{diagnosis_data['max_score']}点"
        score_para = Paragraph(score_text, self.styles['CustomTitle'])
        story.append(score_para)
        
        rank_text = f"準備度ランク: {diagnosis_data['rank']}"
        rank_para = Paragraph(rank_text, self.styles['CustomTitle'])
        story.append(rank_para)
        
        story.append(PageBreak())
        
        # ==================== 2ページ目: サマリー ====================
        summary_title = Paragraph("診断結果サマリー", self.styles['CustomHeading1'])
        story.append(summary_title)
        story.append(Spacer(1, 5*mm))
        
        summary_text = f"""
        この診断は、貴施設のAI導入準備度を総合的に評価したものです。<br/>
        総合スコアは<b>{diagnosis_data['total_score']}点（{diagnosis_data['percentage']:.1f}%）</b>で、
        準備度ランクは<b>{diagnosis_data['rank']}</b>と評価されました。
        """
        story.append(Paragraph(summary_text, self.styles['CustomBody']))
        story.append(Spacer(1, 10*mm))
        
        # レーダーチャート挿入
        scores_dict = {cat['name']: cat['score'] for cat in diagnosis_data['categories']}
        radar_image_buffer = self.create_radar_chart_image(scores_dict)
        radar_img = Image(radar_image_buffer, width=140*mm, height=140*mm)
        story.append(radar_img)
        
        story.append(PageBreak())
        
        # ==================== 3ページ目: カテゴリー別詳細 ====================
        category_title = Paragraph("カテゴリー別詳細分析", self.styles['CustomHeading1'])
        story.append(category_title)
        story.append(Spacer(1, 5*mm))
        
        # カテゴリーテーブル
        category_table = self.create_score_bar_table(diagnosis_data['categories'])
        story.append(category_table)
        story.append(Spacer(1, 10*mm))
        
        # 各カテゴリーの評価コメント
        for cat in diagnosis_data['categories']:
            cat_heading = Paragraph(f"【{cat['name']}】", self.styles['CustomHeading2'])
            story.append(cat_heading)
            
            comment = f"スコア: {cat['score']}/100点（{cat['percentage']:.1f}%）<br/>"
            comment += cat.get('comment', 'このカテゴリーの改善が推奨されます。')
            story.append(Paragraph(comment, self.styles['CustomBody']))
            story.append(Spacer(1, 5*mm))
        
        story.append(PageBreak())
        
        # ==================== 4ページ目: 改善優先度TOP3 ====================
        improvement_title = Paragraph("改善優先度 TOP3", self.styles['CustomHeading1'])
        story.append(improvement_title)
        story.append(Spacer(1, 5*mm))
        
        for i, improvement in enumerate(diagnosis_data['top3_improvements'], 1):
            priority_heading = Paragraph(f"{i}. {improvement['category']}", self.styles['CustomHeading2'])
            story.append(priority_heading)
            
            priority_text = f"""
            <b>現在のスコア:</b> {improvement['score']}/100点（{improvement['percentage']:.1f}%）<br/>
            <b>業界平均との差:</b> 業界平均より {abs(improvement['diff'])}点低い<br/>
            <br/>
            <b>💡 改善提案:</b><br/>
            {improvement['suggestion']}
            """
            story.append(Paragraph(priority_text, self.styles['CustomBody']))
            story.append(Spacer(1, 8*mm))
        
        story.append(PageBreak())
        
        # ==================== 5ページ目: 質問回答詳細 ====================
        answers_title = Paragraph("質問回答の詳細", self.styles['CustomHeading1'])
        story.append(answers_title)
        story.append(Spacer(1, 5*mm))
        
        # カテゴリーごとに質問を整理
        current_category = None
        for answer in diagnosis_data['answers']:
            category_key = answer['category']
            category_name = answer.get('category_name', category_key)
            if category_key != current_category:
                current_category = category_key
                cat_heading = Paragraph(f"【{category_name}】", self.styles['CustomHeading2'])
                story.append(cat_heading)
                story.append(Spacer(1, 3*mm))
            
            q_text = f"Q{answer['number']}. {answer['question']}<br/><b>回答:</b> {answer['answer']}"
            story.append(Paragraph(q_text, self.styles['CustomBody']))
            story.append(Spacer(1, 3*mm))
        
        story.append(PageBreak())
        
        # ==================== 6ページ目: 次のステップ ====================
        next_step_title = Paragraph("次のステップ", self.styles['CustomHeading1'])
        story.append(next_step_title)
        story.append(Spacer(1, 5*mm))
        
        next_step_text = """
        <b>🎯 推奨アクション</b><br/>
        1. 改善優先度TOP3のカテゴリーから着手してください<br/>
        2. 詳細レポートやROI試算が必要な場合は、有料プランをご検討ください<br/>
        3. 補助金の活用も可能です。最新の補助金情報をチェックしましょう<br/>
        <br/>
        <b>📞 お問い合わせ</b><br/>
        ご不明な点やご相談は、お気軽にお問い合わせください。<br/>
        Email: support@ai-care-checker.com<br/>
        TEL: 03-XXXX-XXXX
        """
        story.append(Paragraph(next_step_text, self.styles['CustomBody']))
        
        # PDF生成
        doc.build(story)
        
        return filename
