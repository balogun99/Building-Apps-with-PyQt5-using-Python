from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from database import Database

class LeaderboardScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.database = Database()
        
    # UI Components
        self.title_label = QLabel("🏆 Leaderboard 🏆")
        self.scores_label = QLabel(self.get_top_scores()) # this fetch the scores
        self.back_button = QPushButton("Back to Menu")
        
        # layouts
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.scores_label)
        layout.addWidget(self.back_button)
        self.setLayout(layout)
        
        self.back_button.connect.clicked(self.parent.show_results)
        
    def get_top_scores(self):
        # Fetch top 10 scores from the database and format them
        scores = self.db.get_top_scores()
        if not scores:
            return "No Scores yet!. Be the first to play 🎮"
        
        leaderboard_text = "🥇Top Scores🥇\n\n"
        
        for i, (name, score, total, date) in enumerate (scores, 1):
            leaderboard_text += f"{i}. {name} - {score}/{total * 10} ({date})\n"
        return leaderboard_text