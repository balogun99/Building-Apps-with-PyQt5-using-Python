import sys
import json
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QRadioButton, QButtonGroup, QLineEdit, QMessageBox, QProgressBar, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer

# Database setup
DB_FILE = "quiz_leaderboard.db"

def initialize_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

initialize_db()

# Load questions from JSON file
def load_questions():
    with open("cbt_app_6/questions.json", "r") as file:
        return json.load(file)

class UsernameScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter Username")
        self.setGeometry(200, 200, 300, 150)
        
        self.layout = QVBoxLayout()
        self.label = QLabel("Enter your username:")
        self.username_input = QLineEdit()
        self.start_button = QPushButton("Start Quiz")
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.start_button)
        self.setLayout(self.layout)
        
        self.start_button.clicked.connect(self.start_quiz)

    def start_quiz(self):
        username = self.username_input.text().strip()
        if not username:
            QMessageBox.warning(self, "Input Error", "Please enter a username.")
        else:
            self.quiz_screen = QuizScreen(username)
            self.quiz_screen.show()
            self.close()

class QuizScreen(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Quiz Application")
        self.setGeometry(200, 200, 500, 300)
        
        self.username = username
        self.questions = load_questions()
        self.current_question = 0
        self.score = 0
        self.time_left = 15  # 15 seconds per question

        self.layout = QVBoxLayout()
        self.question_label = QLabel()
        self.layout.addWidget(self.question_label)

        self.radio_group = QButtonGroup()
        self.radio_buttons = []

        for i in range(4):
            btn = QRadioButton()
            self.radio_group.addButton(btn)
            self.radio_buttons.append(btn)
            self.layout.addWidget(btn)

        self.submit_button = QPushButton("Submit Answer")
        self.layout.addWidget(self.submit_button)
        self.submit_button.clicked.connect(self.check_answer)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.layout.addWidget(self.progress_bar)

        self.timer_label = QLabel("Time left: 15s")
        self.layout.addWidget(self.timer_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.setLayout(self.layout)
        self.load_question()

    def load_question(self):
        if self.current_question < len(self.questions):
            self.timer.start(1000)  # Start 1-second interval timer
            self.time_left = 15
            self.update_timer()

            q = self.questions[self.current_question]
            self.question_label.setText(q["question"])

            for i, option in enumerate(q["options"]):
                self.radio_buttons[i].setText(option)
                self.radio_buttons[i].setChecked(False)

            self.progress_bar.setValue(int((self.current_question / len(self.questions)) * 100))
        else:
            self.finish_quiz()

    def update_timer(self):
        self.timer_label.setText(f"Time left: {self.time_left}s")
        if self.time_left == 0:
            self.timer.stop()
            QMessageBox.warning(self, "Time Up", "Time is up for this question!")
            self.current_question += 1
            self.load_question()
        self.time_left -= 1

    def check_answer(self):
        self.timer.stop()  # Stop timer when answer is submitted

        selected_button = self.radio_group.checkedButton()
        if selected_button:
            answer = selected_button.text()
            correct_answer = self.questions[self.current_question]["correct"]

            if answer == correct_answer:
                self.score += 1

        self.current_question += 1
        self.load_question()

    def finish_quiz(self):
        QMessageBox.information(self, "Quiz Completed", f"Your score: {self.score}/{len(self.questions)}")
        save_score(self.username, self.score)
        self.leaderboard_screen = LeaderboardScreen()
        self.leaderboard_screen.show()
        self.close()

class LeaderboardScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Leaderboard")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QVBoxLayout()
        self.title_label = QLabel("🏆 Leaderboard")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.leaderboard_list = QLabel()
        self.layout.addWidget(self.leaderboard_list)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)
        self.layout.addWidget(self.exit_button)

        self.setLayout(self.layout)
        self.load_leaderboard()

    def load_leaderboard(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT username, score FROM leaderboard ORDER BY score DESC LIMIT 5")
        rows = cursor.fetchall()
        conn.close()

        leaderboard_text = "\n".join([f"{i+1}. {row[0]} - {row[1]} points" for i, row in enumerate(rows)])
        self.leaderboard_list.setText(leaderboard_text)

def save_score(username, score):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO leaderboard (username, score) VALUES (?, ?)", (username, score))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    username_screen = UsernameScreen()
    username_screen.show()
    sys.exit(app.exec_())
