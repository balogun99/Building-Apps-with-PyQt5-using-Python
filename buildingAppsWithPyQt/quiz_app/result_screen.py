from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
# from docutils.parsers.rst.directives import percentage

class ResultScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout()

        # Result Message
        self.result_label = QLabel("Your Results will appear here")
        self.result_label.setStyleSheet("font-size: 20px; font-weight: bold; text-align: center;")

        self.layout.addWidget(self.result_label)

        # Play Again Button
        play_again_button = QPushButton("Play Again")
        play_again_button.setStyleSheet("font-size: 16px; background-color: #4CAF50; color: white; padding: 10px")

        play_again_button.clicked.connect(self.play_again)
        self.layout.addWidget(play_again_button)

        # Exit Button
        exit_button = QPushButton("Exit")
        exit_button.setStyleSheet("font-size: 16px; background-color: #f44336; color: white; padding: 10px")

        exit_button.clicked.connect(self.exit_app)
        
        self.layout.addWidget(exit_button)
        self.setLayout(self.layout)

    def display_results(self, score, total_questions):
        percentage = (score / total_questions) * 100
        self.result_label.setText(f"You scored {score}/{total_questions} ({percentage: .2f}%)")

    def play_again(self):
        self.parent.welcome_screen.category_dropdown.setCurrentIndex(0)
        self.parent.setCurrentWidget(self.parent.welcome_screen)

    def exit_app(self):
        self.parent.close()