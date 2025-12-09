"""
診断結果エクスポート機能
JSON、CSV形式でのエクスポートをサポート
"""

import json
import csv
from datetime import datetime
import io

class ReportExporter:
    """診断結果エクスポートクラス"""
    
    @staticmethod
    def export_to_json(diagnosis_data):
        """
        診断結果をJSON形式でエクスポート
        
        Args:
            diagnosis_data (dict): 診断データ
        
        Returns:
            str: JSON文字列
        """
        def convert_datetime(obj):
            """datetimeオブジェクトを再帰的にISO形式の文字列に変換"""
            if isinstance(obj, datetime):
                return obj.isoformat()
            elif isinstance(obj, dict):
                return {key: convert_datetime(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_datetime(item) for item in obj]
            else:
                return obj
        
        # datetimeをISO形式の文字列に変換（再帰的に）
        export_data = convert_datetime(diagnosis_data)
        
        return json.dumps(export_data, ensure_ascii=False, indent=2)
    
    @staticmethod
    def export_to_csv(diagnosis_data):
        """
        診断結果をCSV形式でエクスポート（カテゴリー別スコア）
        
        Args:
            diagnosis_data (dict): 診断データ
        
        Returns:
            str: CSV文字列
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        # ヘッダー
        writer.writerow(['診断日', '施設名', '総合スコア', '達成率', 'ランク'])
        
        # 基本情報
        date_str = diagnosis_data['diagnosis_date'].strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow([
            date_str,
            diagnosis_data.get('facility_name', ''),
            f"{diagnosis_data['total_score']}/{diagnosis_data['max_score']}",
            f"{diagnosis_data['percentage']:.1f}%",
            diagnosis_data['rank']
        ])
        
        # 空行
        writer.writerow([])
        
        # カテゴリー別スコア
        writer.writerow(['カテゴリー', 'スコア', '達成率', '業界平均との差'])
        for cat in diagnosis_data['categories']:
            writer.writerow([
                cat['name'],
                f"{cat['score']}/100",
                f"{cat['percentage']:.1f}%",
                f"{cat['diff']:+d}"
            ])
        
        return output.getvalue()
    
    @staticmethod
    def export_answers_to_csv(diagnosis_data):
        """
        質問回答をCSV形式でエクスポート
        
        Args:
            diagnosis_data (dict): 診断データ
        
        Returns:
            str: CSV文字列
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        # ヘッダー
        writer.writerow(['カテゴリー', '質問番号', '質問', '回答', '配点'])
        
        # 各質問の回答
        for answer in diagnosis_data['answers']:
            writer.writerow([
                answer['category'],
                answer['number'],
                answer['question'],
                answer['answer'],
                answer.get('score', '')
            ])
        
        return output.getvalue()
