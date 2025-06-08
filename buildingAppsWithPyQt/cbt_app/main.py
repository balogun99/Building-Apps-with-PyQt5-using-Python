import sys
import sqlite3
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QRadioButton,
    QGroupBox, QHBoxLayout, QProgressBar, QLineEdit, QMessageBox
)
from PyQt5.QtCore import QTimer

# Load Questions from JSON
def load_questions():
    with open("cbt_app/questions.json", "r") as file:
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

setup_database()  # Ensure DB is set up

class QuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quiz Application")
        self.setGeometry(300, 150, 500, 400)

        # Layout
        self.layout = QVBoxLayout()
        
        # Username Input
        self.username_label = QLabel("Enter your username:")
        self.username_input = QLineEdit()
        self.start_button = QPushButton("Start Quiz")
        self.start_button.clicked.connect(self.start_quiz)

        # Add widgets
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)

        # Quiz Variables
        self.questions = load_questions()
        self.current_question_index = 0
        self.score = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.time_left = 15  # 15 seconds per question

    def start_quiz(self):
        self.username = self.username_input.text().strip()
        if not self.username:
            QMessageBox.warning(self, "Warning", "Please enter a username!")
            return

        # Remove username input and start the quiz
        self.username_label.deleteLater()
        self.username_input.deleteLater()
        self.start_button.deleteLater()

        self.show_question()

    def show_question(self):
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Get Current Question
        question_data = self.questions[self.current_question_index]

        # Question Label
        self.question_label = QLabel(question_data["question"])
        self.layout.addWidget(self.question_label)

        # Answer Choices (Radio Buttons)
        self.options_group = QGroupBox("Options")
        self.options_layout = QVBoxLayout()
        self.options = []
        for option in question_data["options"]:
            btn = QRadioButton(option)
            self.options.append(btn)
            self.options_layout.addWidget(btn)

        self.options_group.setLayout(self.options_layout)
        self.layout.addWidget(self.options_group)

        # Next Button
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_question)
        self.layout.addWidget(self.next_button)

        # Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(15)
        self.progress_bar.setValue(self.time_left)
        self.layout.addWidget(self.progress_bar)

        # Start Timer
        self.time_left = 15
        self.timer.start(1000)

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.progress_bar.setValue(self.time_left)
        else:
            self.timer.stop()
            QMessageBox.warning(self, "Time Up!", "You ran out of time!")
            self.next_question()

    def next_question(self):
        self.timer.stop()

        # Get Selected Answer
        selected_answer = None
        for option in self.options:
            if option.isChecked():
                selected_answer = option.text()
                break

        # Check Answer
        correct_answer = self.questions[self.current_question_index]["correct"]
        if selected_answer == correct_answer:
            self.score += 1

        # Remove old widgets
        self.question_label.deleteLater()
        self.options_group.deleteLater()
        self.next_button.deleteLater()
        self.progress_bar.deleteLater()

        # Move to Next Question
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.show_question()
        else:
            self.show_results()

    def show_results(self):
        # Display Score
        QMessageBox.information(self, "Quiz Completed", f"Your score: {self.score}/{len(self.questions)}")
        
        # Save Score to Database
        conn = sqlite3.connect("quiz_leaderboard.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO leaderboard (username, score) VALUES (?, ?)", (self.username, self.score))
        conn.commit()
        conn.close()

        # Show Leaderboard
        self.show_leaderboard()

    def show_leaderboard(self):
        # Remove Old Widgets
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        self.setWindowTitle("Leaderboard")

        # Fetch Top 5 Scores
        conn = sqlite3.connect("quiz_leaderboard.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username, score FROM leaderboard ORDER BY score DESC LIMIT 5")
        leaderboard_data = cursor.fetchall()
        conn.close()

        # Display Leaderboard
        self.layout.addWidget(QLabel("🏆 Leaderboard 🏆"))
        for i, (user, score) in enumerate(leaderboard_data, start=1):
            self.layout.addWidget(QLabel(f"{i}. {user} - {score} points"))

        # Exit Button
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)
        self.layout.addWidget(exit_button)

# Run the App
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuizApp()
    window.show()
    sys.exit(app.exec_())
