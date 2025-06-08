from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox

class WelcomeScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setup_ui()

    # vertical layout UI setup
    def setup_ui(self):
        layout = QVBoxLayout()

    # Welcome Message
        welcome_label = QLabel("Select any Category to GET STARTED 📚")
        welcome_label.setStyleSheet("font-size: 34px; font-weight: bold; text-align: center; padding: 20px; background-color: gray; margin: 40px;")
        layout.addWidget(welcome_label)

    # Category Selection
        self.category_dropdown = QComboBox()
        self.category_dropdown.addItems(["All", "Science", "Art", "Computing", "English"])
        self.category_dropdown.setStyleSheet("font-size: 24px; padding: 10px; margin: 5px;")
        layout.addWidget(self.category_dropdown)

    # Start Button
        start_button = QPushButton("Start Quiz")
        start_button.setStyleSheet("font-size: 24px; background-color: #4CAF50; color: white; padding: 10px;")
        start_button.clicked.connect(self.start_quiz)
        
        layout.addWidget(start_button)

    # add the layout
        self.setLayout(layout)

#   start quiz method
    def start_quiz(self):
        selected_category = self.category_dropdown.currentText()
        self.parent.quiz_screen.filter_questions(selected_category) #sorted
        self.parent.setCurrentWidget(self.parent.quiz_screen)



