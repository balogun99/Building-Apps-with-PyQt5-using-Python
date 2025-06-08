from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit

class UsernameScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
    # UI Components
        self.title_label = QLabel("Welcome to the CBT App")
        self.name_label = QLabel("Enter your username: ")
        self.name_input = QLineEdit()
        self.start_button = QPushButton("Start Exam")
        
    # Layouts
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.start_button)
        
        self.setLayout(layout)
        
    # connect start quiz button
        self.start_button.clicked.connect(self.start_quiz)
        
    # start quiz method
    def start_quiz(self):
        # store the user username and move to the welcome screen
        username = self.name_input.text().strip()
        if username:
            self.parent.username = username
            self.parent.start_quiz()
        else:
            self.name_input.setPlaceholderText("Please enter a valid username")