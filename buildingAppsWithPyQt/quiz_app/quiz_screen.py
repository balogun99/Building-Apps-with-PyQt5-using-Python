# import libraries
# from tkinter.messagebox import QUESTION

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QButtonGroup, QRadioButton, QProgressBar
from PyQt5.QtCore import QTimer

# create a class for quiz screen
class QuizScreen(QWidget):
    def __init__(self):
    # def __init__(self, parent: object, questions: object, username: object) -> None:
        super().__init__()
        # self.parent = parent
        # self.questions = questions
        # self.username = username
        self.current_question_index = 0
        self.score = 0
        self.timer = QTimer()
        self.time_left = 10
        self.setup_ui()

# set the UI as vertical
    def setup_ui(self):
        self.layout = QVBoxLayout()

        # Question Label
        self.question_label = QLabel("Question will appear here") #"Question will appear here"
        self.question_label.setStyleSheet("font-size: 30px; padding: 30px; text-align: center;")
        self.layout.addWidget(self.question_label)

        # Options
        self.options_group = QButtonGroup()
        self.option_buttons = []
        for i in range(4):
            radio_button = QRadioButton()
            self.options_group.addButton(radio_button)
            self.option_buttons.append(radio_button)
            self.layout.addWidget(radio_button)
            
        # Applying the stylesheet to each button
        for btn in self.option_buttons:
            btn.setStyleSheet(radio_style)

        # Timer
        self.timer_label = QPushButton("Time Left: 10 Seconds")
        self.timer_label.setStyleSheet("font-size: 16px; color: red;")
        self.layout.addWidget(self.timer_label)

        self.timer.timeout.connect(self.update_timer)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(len(self.questions))
        self.layout.addWidget(self.progress_bar)

        # Next Button
        self.next_button = QPushButton("Next")
        self.next_button.setStyleSheet("font-size: 16px; background-color: #2196F3; color: white; padding: 10px;")
        self.next_button.clicked.connect(self.next_question)
        self.layout.addWidget(self.next_button)

        self.setLayout(self.layout)
        self.load_question()

    def load_question(self):
        if self.current_question_index < len(self.questions):
            question_data = self.questions[self.current_question_index]
            self.question_label.setText(question_data['question'])
            
        #     # remove previous buttons
        #     for btn in self.option_buttons:
        #         self.layout().removeWidget(btn)
        #         btn.deleteLater()
        
        # # create a new radio button for options
        # self.option_buttons = []
        # for option in question_data['questions']:
        #     btn = QRadioButton(option)
        #     self.option_buttons.append(btn)
        #     self.layout.addWidget(btn)
            
        # # ensure the first button is checked by default
        # if self.option_buttons:
        #     self.option_buttons[0].Checked(True)

            for i, option in enumerate(question_data['options']):
                self.option_buttons[i].setText(option)
                self.option_buttons[i].setChecked(False)

            self.progress_bar.setValue(self.current_question_index)

            self.time_left = 10
            self.timer_label.setText(f"Time Left: {self.time_left} seconds")
            self.timer.start(1000)
        else:
            self.finish_quiz()

    def update_timer(self):
        self.time_left -= 1
        self.timer_label.setText(f"Time Left: {self.time_left} seconds")

        if self.time_left <= 0:
            self.timer.stop()
            self.next_question()

    def next_question(self):
        self.timer.stop()
        selected_button = self.options_group.checkedButton()
        if selected_button:
            selected_answer = selected_button.text()
            correct_answer = self.questions[self.current_question_index]['answer']
            if selected_answer == correct_answer:
                self.score += 1

            self.current_question_index += 1
            self.load_question()

    def finish_quiz(self):
        self.parent.result_screen.display_results(self.score, len(self.questions))
        self.parent.setCurrentWidget(self.parent.result_screen)

    def filter_questions(self, category):
        if category == "All":
            self.questions = self.parent.questions
        else:
            self.questions = [q for q in self.parent.questions if q['category'] == category]
        self.current_question_index = 0
        self.score = 0
        self.load_question()
        
# Applying a stylesheet to the Radio Buttons
radio_style = """
        QRadioButton {
        font-size: 16px;
        color: white;
        spacing: 10px;
        padding: 5px;
    }
    QRadioButton::indicator {
        width: 18px;
        height: 18px;
        border-radius: 9px;
        border: 2px solid #555;
        background: white;
    }
    QRadioButton::indicator:checked {
        background: #4CAF50;  /* Green background when selected */
        border: 2px solid #2E7D32;
    }
"""