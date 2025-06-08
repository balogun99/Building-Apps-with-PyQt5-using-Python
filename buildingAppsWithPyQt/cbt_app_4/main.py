import sys
import json
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QRadioButton, QButtonGroup, QProgressBar, QLineEdit
from PyQt5.QtCore import QTimer

# Database Setup
DB_NAME = "quiz_leaderboard.db"

def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            score INTEGER
        )
    """)
    conn.commit()
    conn.close()

# Load Questions
def load_questions():
    with open("cbt_app_4/questions.json", "r") as file:
        return json.load(file)

class UsernameScreen(QWidget):
    """Initial screen to enter username before starting the quiz."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quiz App - Enter Username")
        self.setGeometry(100, 100, 400, 200)
        
        self.layout = QVBoxLayout()
        
        self.label = QLabel("Enter your username:")
        self.layout.addWidget(self.label)
        
        self.username_input = QLineEdit(self)
        self.layout.addWidget(self.username_input)
        
        self.start_button = QPushButton("Start Quiz")
        self.start_button.clicked.connect(self.start_quiz)
        self.layout.addWidget(self.start_button)
        
        self.setLayout(self.layout)

    def start_quiz(self):
        username = self.username_input.text().strip()
        if username:
            self.quiz_screen = QuizScreen(username)
            self.quiz_screen.show()
            self.close()

class QuizScreen(QWidget):
    """Quiz screen where the user answers questions."""
    
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Quiz App - Quiz")
        self.setGeometry(100, 100, 600, 400)
        
        self.username = username
        self.questions = load_questions()
        self.current_question_index = 0
        self.score = 0
        self.time_left = 15  # Timer in seconds

        self.layout = QVBoxLayout()

        self.timer_label = QLabel(f"Time Left: {self.time_left} sec")
        self.layout.addWidget(self.timer_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(15)
        self.progress_bar.setValue(self.time_left)
        self.layout.addWidget(self.progress_bar)

        self.question_label = QLabel("")
        self.layout.addWidget(self.question_label)

        self.radio_group = QButtonGroup()
        self.radio_buttons = [QRadioButton() for _ in range(4)]
        for rb in self.radio_buttons:
            self.radio_group.addButton(rb)
            self.layout.addWidget(rb)

        self.submit_button = QPushButton("Submit Answer")
        self.submit_button.clicked.connect(self.check_answer)
        self.layout.addWidget(self.submit_button)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # 1 second interval

        self.setLayout(self.layout)
        self.load_question()

    def load_question(self):
        """Loads the next question into the UI."""
        if self.current_question_index < len(self.questions):
            self.time_left = 15  # Reset Timer
            self.timer_label.setText(f"Time Left: {self.time_left} sec")
            self.progress_bar.setValue(self.time_left)
            self.timer.start(1000)

            question_data = self.questions[self.current_question_index]
            self.question_label.setText(question_data["question"])
            for i, option in enumerate(question_data["options"]):
                self.radio_buttons[i].setText(option)
                self.radio_buttons[i].setChecked(False)
        else:
            self.end_quiz()

    def update_timer(self):
        """Updates the timer and progress bar."""
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.setText(f"Time Left: {self.time_left} sec")
            self.progress_bar.setValue(self.time_left)
        else:
            self.check_answer()

    def check_answer(self):
        """Checks the selected answer and updates the score."""
        self.timer.stop()
        selected_button = self.radio_group.checkedButton()
        if selected_button:
            selected_answer = selected_button.text()
            correct_answer = self.questions[self.current_question_index]["correct"]
            if selected_answer == correct_answer:
                self.score += 1

        self.current_question_index += 1
        self.load_question()

    def end_quiz(self):
        """Shows the result screen after quiz completion."""
        self.result_screen = ResultScreen(self.username, self.score)
        self.result_screen.show()
        self.close()

class ResultScreen(QWidget):
    """Result screen displaying the user's score and leaderboard."""

    def __init__(self, username, score):
        super().__init__()
        self.setWindowTitle("Quiz App - Results")
        self.setGeometry(100, 100, 400, 300)
        
        self.username = username
        self.score = score

        self.layout = QVBoxLayout()

        self.result_label = QLabel(f"Quiz Completed!\n{self.username}, your score: {self.score}")
        self.layout.addWidget(self.result_label)

        self.save_score()
        
        self.view_leaderboard_button = QPushButton("View Leaderboard")
        self.view_leaderboard_button.clicked.connect(self.show_leaderboard)
        self.layout.addWidget(self.view_leaderboard_button)

        self.quit_button = QPushButton("Exit")
        self.quit_button.clicked.connect(self.close)
        self.layout.addWidget(self.quit_button)

        self.setLayout(self.layout)

    def save_score(self):
        """Saves the user's score into the database."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO leaderboard (username, score) VALUES (?, ?)", (self.username, self.score))
        conn.commit()
        conn.close()

    def show_leaderboard(self):
        """Displays the leaderboard screen."""
        self.leaderboard_screen = LeaderboardScreen()
        self.leaderboard_screen.show()

class LeaderboardScreen(QWidget):
    """Leaderboard screen displaying top scores."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quiz App - Leaderboard")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()
        self.label = QLabel("🏆 Top 5 Leaderboard 🏆")
        self.layout.addWidget(self.label)

        self.load_leaderboard()

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        self.layout.addWidget(self.close_button)

        self.setLayout(self.layout)

    def load_leaderboard(self):
        """Fetches top scores from the database and displays them."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT username, score FROM leaderboard ORDER BY score DESC LIMIT 5")
        leaderboard_data = cursor.fetchall()
        conn.close()

        for i, (user, score) in enumerate(leaderboard_data, start=1):
            self.layout.addWidget(QLabel(f"{i}. {user} - {score} pts"))

if __name__ == "__main__":
    setup_database()
    app = QApplication(sys.argv)
    window = UsernameScreen()
    window.show()
    sys.exit(app.exec_())
