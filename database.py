import sqlite3
from datetime import datetime

class ResponseDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('responses.db', check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Create responses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                response TEXT NOT NULL,
                sources TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create feedback table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                response_id INTEGER,
                feedback_type TEXT NOT NULL,
                feedback_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (response_id) REFERENCES responses (id)
            )
        ''')
        
        self.conn.commit()
    
    def save_response(self, question_id, question, answer, response, sources=None):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO responses (question_id, question, answer, response, sources)
            VALUES (?, ?, ?, ?, ?)
        ''', (question_id, question, answer, response, sources))
        self.conn.commit()
        return cursor.lastrowid
    
    def update_response(self, response_id, response):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE responses 
            SET response = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (response, response_id))
        self.conn.commit()
    
    def save_feedback(self, response_id, feedback_type, feedback_text=None):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO feedback (response_id, feedback_type, feedback_text)
            VALUES (?, ?, ?)
        ''', (response_id, feedback_type, feedback_text))
        self.conn.commit()
    
    def get_response_history(self, question_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM responses 
            WHERE question_id = ?
            ORDER BY created_at DESC
        ''', (question_id,))
        return cursor.fetchall() 