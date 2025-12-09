"""
診断履歴データベース管理モジュール
SQLiteを使用して診断結果を保存・取得
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

class DiagnosisDatabase:
    """診断履歴データベースクラス"""
    
    def __init__(self, db_path="data/diagnoses.db"):
        """
        初期化
        
        Args:
            db_path (str): データベースファイルのパス
        """
        self.db_path = db_path
        self._ensure_data_directory()
        self._init_database()
    
    def _ensure_data_directory(self):
        """dataディレクトリが存在しない場合は作成"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
    
    def _init_database(self):
        """データベーステーブルの初期化"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 診断結果テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS diagnoses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                facility_name TEXT,
                diagnosis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_score INTEGER NOT NULL,
                max_score INTEGER NOT NULL,
                percentage REAL NOT NULL,
                rank TEXT NOT NULL,
                categories_json TEXT NOT NULL,
                answers_json TEXT NOT NULL,
                session_id TEXT,
                user_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # インデックス作成
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_diagnosis_date 
            ON diagnoses(diagnosis_date DESC)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_session_id 
            ON diagnoses(session_id)
        ''')
        
        conn.commit()
        conn.close()
    
    def save_diagnosis(self, diagnosis_data):
        """
        診断結果を保存
        
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
                    'answers': list,
                    'session_id': str (optional),
                    'user_id': str (optional)
                }
        
        Returns:
            int: 保存された診断のID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO diagnoses (
                facility_name, diagnosis_date, total_score, max_score,
                percentage, rank, categories_json, answers_json,
                session_id, user_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            diagnosis_data.get('facility_name', ''),
            diagnosis_data['diagnosis_date'].isoformat(),
            diagnosis_data['total_score'],
            diagnosis_data['max_score'],
            diagnosis_data['percentage'],
            diagnosis_data['rank'],
            json.dumps(diagnosis_data['categories'], ensure_ascii=False),
            json.dumps(diagnosis_data['answers'], ensure_ascii=False),
            diagnosis_data.get('session_id', ''),
            diagnosis_data.get('user_id', '')
        ))
        
        diagnosis_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return diagnosis_id
    
    def get_diagnosis_by_id(self, diagnosis_id):
        """
        IDで診断結果を取得
        
        Args:
            diagnosis_id (int): 診断ID
        
        Returns:
            dict: 診断データ、存在しない場合はNone
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM diagnoses WHERE id = ?
        ''', (diagnosis_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_dict(row)
        return None
    
    def get_recent_diagnoses(self, limit=10, session_id=None):
        """
        最近の診断結果を取得
        
        Args:
            limit (int): 取得件数
            session_id (str): セッションIDでフィルタ（オプション）
        
        Returns:
            list: 診断データのリスト
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if session_id:
            cursor.execute('''
                SELECT * FROM diagnoses 
                WHERE session_id = ?
                ORDER BY diagnosis_date DESC 
                LIMIT ?
            ''', (session_id, limit))
        else:
            cursor.execute('''
                SELECT * FROM diagnoses 
                ORDER BY diagnosis_date DESC 
                LIMIT ?
            ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row) for row in rows]
    
    def get_all_diagnoses(self):
        """
        全ての診断結果を取得
        
        Returns:
            list: 診断データのリスト
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM diagnoses 
            ORDER BY diagnosis_date DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row) for row in rows]
    
    def delete_diagnosis(self, diagnosis_id):
        """
        診断結果を削除
        
        Args:
            diagnosis_id (int): 診断ID
        
        Returns:
            bool: 削除成功したかどうか
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM diagnoses WHERE id = ?
        ''', (diagnosis_id,))
        
        deleted_rows = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_rows > 0
    
    def _row_to_dict(self, row):
        """
        SQLite Rowを辞書に変換
        
        Args:
            row (sqlite3.Row): データベース行
        
        Returns:
            dict: 診断データ
        """
        return {
            'id': row['id'],
            'facility_name': row['facility_name'],
            'diagnosis_date': datetime.fromisoformat(row['diagnosis_date']),
            'total_score': row['total_score'],
            'max_score': row['max_score'],
            'percentage': row['percentage'],
            'rank': row['rank'],
            'categories': json.loads(row['categories_json']),
            'answers': json.loads(row['answers_json']),
            'session_id': row['session_id'],
            'user_id': row['user_id'],
            'created_at': datetime.fromisoformat(row['created_at'])
        }
