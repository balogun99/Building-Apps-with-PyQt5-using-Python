import sys
import sqlite3
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QRadioButton, QProgressBar, QLineEdit, QMessageBox
from PyQt5.QtCore import QTimer

# Load questions from JSON file
def load_questions():
    with open("cbt_app_5/questions.json", "r") as file:
        return json.load(file)

# Initialize Database
def setup_database():
    conn = sqlite3.connect("quiz_leaderboard.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Store user score
def save_score(username, score):
    conn = sqlite3.connect("quiz_leaderboard.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO leaderboard (username, score) VALUES (?, ?)", (username, score))
    conn.commit()
    conn.close()

# Fetch leaderboard
def get_leaderboard():
    conn = sqlite3.connect("quiz_leaderboard.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, score FROM leaderboard ORDER BY score DESC LIMIT 5")
    data = cursor.fetchall()
    conn.close()
    return data

# Main Quiz Application
class QuizApp(QWidget):
    def __init__(self):
        super().__init__()

        self.username = ""
        self.questions = load_questions()
        self.current_question = 0
        self.score = 0
        self.time_remaining = 30  # 30 seconds per question

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Quiz Application")
        self.setGeometry(400, 200, 600, 400)

        self.layout = QVBoxLayout()

        # Username Input
        self.username_label = QLabel("Enter your username:")
        self.username_input = QLineEdit()
        self.start_button = QPushButton("Start Quiz")
        self.start_button.clicked.connect(self.start_quiz)

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)

    def start_quiz(self):
        self.username = self.username_input.text().strip()
        if not self.username:
            QMessageBox.warning(self, "Error", "Please enter a username.")
            return

        # Remove username input UI
        self.layout.removeWidget(self.username_label)
        self.layout.removeWidget(self.username_input)
        self.layout.removeWidget(self.start_button)
        self.username_label.deleteLater()
        self.username_input.deleteLater()
        self.start_button.deleteLater()

        # Initialize Quiz UI
        self.question_label = QLabel("")
        self.layout.addWidget(self.question_label)

        # Answer Buttons
        self.option1 = QRadioButton("")
        self.option2 = QRadioButton("")
        self.option3 = QRadioButton("")
        self.option4 = QRadioButton("")
        self.layout.addWidget(self.option1)
        self.layout.addWidget(self.option2)
        self.layout.addWidget(self.option3)
        self.layout.addWidget(self.option4)

        self.submit_button = QPushButton("Submit Answer")
        self.submit_button.clicked.connect(self.check_answer)
        self.layout.addWidget(self.submit_button)

        # Progress Bar & Timer
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(self.time_remaining)
        self.layout.addWidget(self.progress_bar)

        self.timer_label = QLabel("Time left: 30s")
        self.layout.addWidget(self.timer_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Update every second

        self.load_question()

    def load_question(self):
        if self.current_question >= len(self.questions):
            self.finish_quiz()
            return

        question_data = self.questions[self.current_question]
        self.question_label.setText(question_data["question"])
        self.option1.setText(question_data["options"][0])
        self.option2.setText(question_data["options"][1])
        self.option3.setText(question_data["options"][2])
        self.option4.setText(question_data["options"][3])

        self.option1.setChecked(False)
        self.option2.setChecked(False)
        self.option3.setChecked(False)
        self.option4.setChecked(False)

        self.time_remaining = 30
        self.progress_bar.setValue(self.time_remaining)
        self.timer_label.setText(f"Time left: {self.time_remaining}s")

    def update_timer(self):
        self.time_remaining -= 1
        self.progress_bar.setValue(self.time_remaining)
        self.timer_label.setText(f"Time left: {self.time_remaining}s")

        if self.time_remaining == 0:
            self.timer.stop()
            QMessageBox.warning(self, "Time Up!", "You ran out of time for this question!")
            self.next_question()

    def check_answer(self):
        question_data = self.questions[self.current_question]
        selected_answer = ""

        if self.option1.isChecked():
            selected_answer = self.option1.text()
        elif self.option2.isChecked():
            selected_answer = self.option2.text()
        elif self.option3.isChecked():
            selected_answer = self.option3.text()
        elif self.option4.isChecked():
            selected_answer = self.option4.text()

        if selected_answer == question_data["correct"]:
            self.score += 1

        self.next_question()

    def next_question(self):
        self.current_question += 1
        self.load_question()

    def finish_quiz(self):
        self.timer.stop()
        save_score(self.username, self.score)

        QMessageBox.information(self, "Quiz Completed", f"Congratulations {self.username}! Your score: {self.score}")

        self.show_leaderboard()

    def show_leaderboard(self):
        leaderboard_data = get_leaderboard()
        leaderboard_text = "🏆 Leaderboard 🏆\n\n"
        for i, (user, score) in enumerate(leaderboard_data, start=1):
            leaderboard_text += f"{i}. {user} - {score} points\n"

        QMessageBox.information(self, "Leaderboard", leaderboard_text)
        self.close()

# Run Application
if __name__ == "__main__":
    setup_database()
    app = QApplication(sys.argv)
    window = QuizApp()
    window.show()
    sys.exit(app.exec_())
