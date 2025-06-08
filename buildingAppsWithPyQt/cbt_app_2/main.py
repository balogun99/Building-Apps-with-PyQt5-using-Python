import sys
import json
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QRadioButton, QGroupBox, QHBoxLayout, QLineEdit, QProgressBar, QMessageBox
from PyQt5.QtCore import QTimer

# Database Setup (Leaderboard)
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

# Load Questions from JSON File
def load_questions():
    with open("cbt_app_2/questions.json", "r") as file:
        return json.load(file)

# Main Quiz Application
class QuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quiz Application")
        self.setGeometry(200, 200, 500, 400)

        # Initialize Variables
        self.questions = load_questions()
        self.current_question = 0
        self.score = 0
        self.time_limit = 15  # Timer for each question (seconds)
        self.username = ""

        # UI Elements
        self.layout = QVBoxLayout()
        self.username_label = QLabel("Enter your username:")
        self.username_input = QLineEdit()
        self.start_button = QPushButton("Start Quiz")
        self.start_button.clicked.connect(self.start_quiz)

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.start_button)

        # Question Section
        self.question_label = QLabel("")
        self.options_group = QGroupBox("Options")
        self.options_layout = QVBoxLayout()
        self.radio_buttons = [QRadioButton() for _ in range(4)]

        for btn in self.radio_buttons:
            self.options_layout.addWidget(btn)
        self.options_group.setLayout(self.options_layout)

        self.next_button = QPushButton("Next Question")
        self.next_button.clicked.connect(self.next_question)
        self.next_button.setEnabled(False)

        self.progress_bar = QProgressBar()
        self.timer_label = QLabel(f"Time Left: {self.time_limit}s")

        self.layout.addWidget(self.question_label)
        self.layout.addWidget(self.options_group)
        self.layout.addWidget(self.timer_label)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.next_button)

        self.setLayout(self.layout)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.remaining_time = self.time_limit

    def start_quiz(self):
        self.username = self.username_input.text().strip()
        if not self.username:
            QMessageBox.warning(self, "Warning", "Please enter a username before starting the quiz!")
            return

        self.username_label.hide()
        self.username_input.hide()
        self.start_button.hide()

        self.current_question = 0
        self.score = 0
        self.show_question()

    def show_question(self):
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            self.question_label.setText(question_data["question"])

            for i, option in enumerate(question_data["options"]):
                self.radio_buttons[i].setText(option)
                self.radio_buttons[i].setChecked(False)

            self.remaining_time = self.time_limit
            self.timer_label.setText(f"Time Left: {self.remaining_time}s")
            self.progress_bar.setValue(100)

            self.timer.start(1000)  # 1-second interval
            self.next_button.setEnabled(True)
        else:
            self.finish_quiz()

    def update_timer(self):
        self.remaining_time -= 1
        self.progress_bar.setValue(int((self.remaining_time / self.time_limit) * 100))
        self.timer_label.setText(f"Time Left: {self.remaining_time}s")

        if self.remaining_time <= 0:
            self.timer.stop()
            self.next_question()

    def next_question(self):
        self.timer.stop()
        selected_option = None

        for btn in self.radio_buttons:
            if btn.isChecked():
                selected_option = btn.text()
                break

        if selected_option and selected_option == self.questions[self.current_question]["correct"]:
            self.score += 1

        self.current_question += 1
        self.show_question()

    def finish_quiz(self):
        QMessageBox.information(self, "Quiz Completed", f"Your score: {self.score}/{len(self.questions)}")

        # Save score to leaderboard
        conn = sqlite3.connect("quiz_leaderboard.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO leaderboard (username, score) VALUES (?, ?)", (self.username, self.score))
        conn.commit()
        conn.close()

        self.show_leaderboard()

    def show_leaderboard(self):
        conn = sqlite3.connect("quiz_leaderboard.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username, score FROM leaderboard ORDER BY score DESC LIMIT 5")
        leaderboard_data = cursor.fetchall()
        conn.close()

        leaderboard_text = "🏆 Leaderboard:\n"
        for rank, (user, score) in enumerate(leaderboard_data, start=1):
            leaderboard_text += f"{rank}. {user} - {score} points\n"

        QMessageBox.information(self, "Leaderboard", leaderboard_text)
        self.close()

if __name__ == "__main__":
    setup_database()  # Ensure leaderboard DB is set up
    app = QApplication(sys.argv)
    window = QuizApp()
    window.show()
    sys.exit(app.exec_())
