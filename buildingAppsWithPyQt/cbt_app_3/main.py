import sys
import json
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QRadioButton, QProgressBar, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt, QTimer

# Database setup for leaderboard
def initialize_database():
    conn = sqlite3.connect("quiz_leaderboard.db")
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

class QuizApp(QWidget):
    def __init__(self):
        super().__init__()

        self.username = None
        self.current_question = 0
        self.score = 0
        self.time_left = 15  # Timer for each question

        self.load_questions()
        self.init_ui()

    def load_questions(self):
        """Load questions from JSON file."""
        with open("cbt_app_3/questions.json", "r") as file:
            self.questions = json.load(file)

    def init_ui(self):
        """Initialize UI components."""
        self.setWindowTitle("Quiz Application")
        self.setGeometry(200, 200, 600, 400)

        self.layout = QVBoxLayout()

        # Username Input
        self.username_label = QLabel("Enter your username:")
        self.username_input = QLineEdit(self)
        self.username_submit = QPushButton("Start Quiz")
        self.username_submit.clicked.connect(self.start_quiz)

        # Question Section
        self.question_label = QLabel("")
        self.option1 = QRadioButton("")
        self.option2 = QRadioButton("")
        self.option3 = QRadioButton("")
        self.option4 = QRadioButton("")

        # Answer Submission
        self.submit_button = QPushButton("Submit Answer")
        self.submit_button.clicked.connect(self.check_answer)

        # Progress Bar & Timer
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        self.timer_label = QLabel("Time Left: 15s")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        # Layout Setup
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.username_submit)

        self.layout.addWidget(self.question_label)
        self.layout.addWidget(self.option1)
        self.layout.addWidget(self.option2)
        self.layout.addWidget(self.option3)
        self.layout.addWidget(self.option4)

        self.layout.addWidget(self.submit_button)
        self.layout.addWidget(self.timer_label)
        self.layout.addWidget(self.progress_bar)

        self.setLayout(self.layout)
        self.hide_quiz_elements()

    def start_quiz(self):
        """Start the quiz after username input."""
        self.username = self.username_input.text().strip()
        if not self.username:
            QMessageBox.warning(self, "Input Error", "Please enter a username to continue.")
            return

        self.username_label.hide()
        self.username_input.hide()
        self.username_submit.hide()

        self.show_quiz_elements()
        self.load_question()

    def load_question(self):
        """Load a new question and reset the timer."""
        if self.current_question >= len(self.questions):
            self.end_quiz()
            return

        question = self.questions[self.current_question]
        self.question_label.setText(question["question"])
        self.option1.setText(question["options"][0])
        self.option2.setText(question["options"][1])
        self.option3.setText(question["options"][2])
        self.option4.setText(question["options"][3])

        self.option1.setChecked(False)
        self.option2.setChecked(False)
        self.option3.setChecked(False)
        self.option4.setChecked(False)

        self.time_left = 15
        self.progress_bar.setValue(100)
        self.timer_label.setText(f"Time Left: {self.time_left}s")
        self.timer.start(1000)  # Update timer every second

    def update_timer(self):
        """Update timer and progress bar."""
        if self.time_left > 0:
            self.time_left -= 1
            self.progress_bar.setValue((self.time_left / 15) * 100)
            self.timer_label.setText(f"Time Left: {self.time_left}s")
        else:
            self.timer.stop()
            self.check_answer(auto_submit=True)

    def check_answer(self, auto_submit=False):
        """Check the selected answer."""
        selected_option = None
        if self.option1.isChecked():
            selected_option = self.option1.text()
        elif self.option2.isChecked():
            selected_option = self.option2.text()
        elif self.option3.isChecked():
            selected_option = self.option3.text()
        elif self.option4.isChecked():
            selected_option = self.option4.text()

        correct_answer = self.questions[self.current_question]["correct"]
        if not auto_submit and not selected_option:
            QMessageBox.warning(self, "Selection Error", "Please select an answer.")
            return

        if selected_option == correct_answer:
            self.score += 1

        self.current_question += 1
        self.load_question()

    def end_quiz(self):
        """End the quiz and store the score in the database."""
        self.timer.stop()
        QMessageBox.information(self, "Quiz Completed", f"Quiz Over! Your Score: {self.score}")

        self.save_score()
        self.show_leaderboard()

    def save_score(self):
        """Save the score to the SQLite leaderboard."""
        conn = sqlite3.connect("quiz_leaderboard.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO leaderboard (username, score) VALUES (?, ?)", (self.username, self.score))
        conn.commit()
        conn.close()

    def show_leaderboard(self):
        """Display the leaderboard after the quiz."""
        conn = sqlite3.connect("quiz_leaderboard.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username, score FROM leaderboard ORDER BY score DESC LIMIT 5")
        leaderboard_data = cursor.fetchall()
        conn.close()

        leaderboard_text = "🏆 Leaderboard 🏆\n"
        for i, (user, score) in enumerate(leaderboard_data, start=1):
            leaderboard_text += f"{i}. {user} - {score} points\n"

        QMessageBox.information(self, "Leaderboard", leaderboard_text)

    def hide_quiz_elements(self):
        """Hide quiz-related widgets initially."""
        self.question_label.hide()
        self.option1.hide()
        self.option2.hide()
        self.option3.hide()
        self.option4.hide()
        self.submit_button.hide()
        self.progress_bar.hide()
        self.timer_label.hide()

    def show_quiz_elements(self):
        """Show quiz elements after username input."""
        self.question_label.show()
        self.option1.show()
        self.option2.show()
        self.option3.show()
        self.option4.show()
        self.submit_button.show()
        self.progress_bar.show()
        self.timer_label.show()

if __name__ == "__main__":
    initialize_database()
    app = QApplication(sys.argv)
    quiz_app = QuizApp()
    quiz_app.show()
    sys.exit(app.exec_())
