# importing the libraries
import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5.QtGui import QIcon
from welcome_screen import WelcomeScreen
from quiz_screen import QuizScreen
from result_screen import ResultScreen
from questions import load_questions
from username_screen import UsernameScreen
from leaderboard_screen import LeaderboardScreen

# Database setup
DB_FILE = "quiz_scores.db"

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

# create the class for QuizApp
class QuizApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.username  = "" # store the username
        self.InitUI()
    
    # screens
        self.username_screen = UsernameScreen(self)
        self.quiz_screen = QuizScreen(self, self.questions)
        self.result_screen = None # created after the quiz
        self.leaderboard_screen = LeaderboardScreen(self)
        
    # add the screens to the stack
        self.addWidget(self.username_screen)
        self.addWidget(self.quiz_screen)
        self.addWidget(self.leaderboard_screen)
        
    # show the username screen first
        self.setCurrentWidget(self.username_screen)
        
    def InitUI(self):
        self.setWindowTitle("Quiz Application V_1.0")
        self.setGeometry(100, 100, 800, 600)
        #set icon for the app
        self.setWindowIcon(QIcon(".ico"))
        
    def start_quiz(self):
        # starts the quiz after the username is entered
        self.setCurrentWidget(self.quiz_screen)
        self.quiz_screen.reset_quiz()
        
    def show_results(self, score, total_questions):
        # show result screen and save user score
        self.result_screen = ResultScreen(score, total_questions, self)
        self.addWidget(self.result_screen)
        self.setCurrentWidget(self.result_screen)
        
    def show_leaderboard(self):
        # show leaderboard screen
        self.leaderboard_screen = LeaderboardScreen(self)
        self.addWidget(self.leaderboard_screen)
        self.setCurrentWidget(self.leaderboard_screen)
        
    # Add the objects
        # load questions
        self.questions = load_questions()
        # load the Welcome Screen
        self.welcome_screen = WelcomeScreen(self)
        # load the Quiz Screen
        self.quiz_screen = QuizScreen(self)
        # load the Result Screen
        self.result_screen = ResultScreen(self)

    # load the objects to the widgets
        self.addWidget(self.welcome_screen)
        self.addWidget(self.quiz_screen)
        self.addWidget(self.result_screen)

    # load the current widget
        self.setCurrentWidget(self.welcome_screen)

# run the quiz_app

if __name__ == "__main__":
    
    # app = QApplication([])
    # window = QuizApp()
    # window.show()
    # app.exec_()
    
    # app = QApplication(sys.argv)

    # Set up the app
    # quiz_app = QuizApp()
    # quiz_app.setWindowTitle("Quiz Application")
    # quiz_app.resize(800, 600)
    # quiz_app.show()

    # sys.exit(app.exec_())

    app = QApplication(sys.argv) # sys.argv
    main_app = QuizApp
    main_app.show()
    main_app.exec_()
    # sys.exit(app.exec_())
    
    # QuizApp.setWindowTitle("Quiz Application V_1.0")
    # QuizApp.resize( 800, 600 )