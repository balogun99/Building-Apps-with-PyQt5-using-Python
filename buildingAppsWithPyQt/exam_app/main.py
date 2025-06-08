import sys
import json
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, 
    QRadioButton, QButtonGroup
)


class QuizApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Quiz App")
        self.setGeometry(300, 200, 500, 350)

        self.questions = self.load_questions()  # Load questions from JSON
        self.current_question_index = 0  # Track the current question
        self.score = 0  # Track correct answers
        self.time_left = 10  # Set countdown time per question

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        # Welcome Screen
        self.label = QLabel("Welcome to the Quiz App!", self)
        self.label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout.addWidget(self.label)

        # Start Quiz Button
        self.start_button = QPushButton("Start Quiz", self)
        self.start_button.setStyleSheet("font-size: 16px; padding: 10px;")
        self.start_button.clicked.connect(self.start_quiz)
        self.layout.addWidget(self.start_button)

        # Set layout
        self.central_widget.setLayout(self.layout)

    def load_questions(self):
        """Load quiz questions from a JSON file."""
        try:
            with open("exam_app/questions.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Error: 'questions.json' file not found.")
            return []

    def start_quiz(self):
        """Switch to the question screen when the Start Quiz button is clicked."""
        if not self.questions:
            self.label.setText("No questions available.")
            return

        # Remove the welcome screen elements
        self.label.hide()
        self.start_button.hide()

        # Timer Label
        self.timer_label = QLabel(f"Time Left: {self.time_left} sec", self)
        self.timer_label.setStyleSheet("font-size: 14px; color: red; font-weight: bold;")
        self.layout.addWidget(self.timer_label)

        # Set up Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Update every second

        # Display the first question
        self.display_question()

    def display_question(self):
        """Show the current question and its options."""
        self.time_left = 10  # Reset timer for each question
        self.timer_label.setText(f"Time Left: {self.time_left} sec")

        question_data = self.questions[self.current_question_index]
        question_text = question_data["question"]
        options = question_data["options"]

        # Question Label
        self.question_label = QLabel(question_text, self)
        self.question_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(self.question_label)

        # Radio Buttons for Answer Options
        self.button_group = QButtonGroup(self)  # Group radio buttons
        self.option_buttons = []

        for option in options:
            btn = QRadioButton(option, self)
            self.option_buttons.append(btn)
            self.button_group.addButton(btn)
            self.layout.addWidget(btn)

        # Next Button
        self.next_button = QPushButton("Next", self)
        self.next_button.setStyleSheet("font-size: 16px; padding: 10px;")
        self.next_button.clicked.connect(self.check_answer)
        self.layout.addWidget(self.next_button)

        self.central_widget.setLayout(self.layout)
        
    def next_question(self):
    #"""Move to the next question or end the quiz."""
        self.timer.stop()  # Stop the timer before clearing the layout
        self.current_question_index += 1

        if self.current_question_index < len(self.questions):
            # Clear the layout before loading the next question
            self.clear_layout()
            self.display_question()
        else:
            self.end_quiz()

    def check_answer(self):
        """Check if the selected answer is correct and update the score."""
        selected_button = self.button_group.checkedButton()
        
        if selected_button:
            selected_answer = selected_button.text()
            correct_answer = self.questions[self.current_question_index]["answer"]

            if selected_answer == correct_answer:
                self.score += 1  # Increase score for correct answer

        self.next_question()

    def update_timer(self):
    #"""Update the countdown timer and auto-move to next question if time runs out."""
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.setText(f"Time Left: {self.time_left} sec")
        else:
            self.timer.stop()  # Stop the timer before moving to next question
            self.next_question()
            
    def end_quiz(self):
        """Display the final score and end the quiz."""
        self.clear_layout()
        self.timer.stop()

        self.label = QLabel(f"Quiz Completed!\nYour Score: {self.score} / {len(self.questions)}", self)
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; color: green;")
        self.layout.addWidget(self.label)

    def clear_layout(self):
        """Remove all widgets from the layout."""
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuizApp()
    window.show()
    sys.exit(app.exec_())
