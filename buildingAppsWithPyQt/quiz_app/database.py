import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(quiz_scores.db)
        self.cursor = self.conn.cursor()
        self.create_table()
        
    def create_table(self):
        # Creates the scores table if it doesn't exist
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS scores(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT,
                    score INTEGER,
                    total_questions INTEGER,
                    date_time TEXT DEFAULT CURRENT_TIMESTAMP
                )
""")
        self.conn.commit()
        
    def save_score(self, player_name, score, total_questions):
        # inserts the player's score into the database
        self.cursor.execute("""
            INSERT INTO scores (player_name, score, total_questions) 
            VALUES (?, ?, ?)
        """, (player_name, score, total_questions))
        self.conn.commit()

    def get_top_scores(self, limit=10):
        # retrieves the top scores from the database
        self.cursor.execute("""
            SELECT player_name, score, total_questions, date_time 
            FROM scores 
            ORDER BY score DESC, date_time DESC 
            LIMIT ?
        """, (limit,))
        return self.cursor.fetchall()

    def close(self):
        # closes the database connection
        self.conn.close()