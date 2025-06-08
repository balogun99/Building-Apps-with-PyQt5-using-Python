# import libraries
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QDateEdit, QComboBox, QPushButton, QTableWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import QDate, Qt
import sys

# App Class
class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__()
        # Main App Objects & Widgets
        self.resize(550, 500)
        self.setWindowTitle("Expense Tracker App")
        
        # initialize the objects
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()
        
        self.add_button = QPushButton("Add Expense")
        self.delete_button = QPushButton("Delete Expense")
        # action buttons
        self.add_button.clicked.connect(self.add_expense)
        self.delete_button.clicked.connect(self.delete_expense)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5) #id, date, category, amount, description
        self.table.setHorizontalHeaderLabels(["Id", "Date", "Category", "Amount", "Description"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # remove the scrolling bar on the table
        # sort table in descending order
        self.table.sortByColumn(1, Qt.DescendingOrder)
        
        self.dropdown.addItems(["Food","Transportation","Rent","Shopping","Entertainment","Bills","Others"])
        
        # add CSS style to the table
        self.setStyleSheet("""
                           QWidget {
                               background-color: #b8c9e1;
                               }
                           
                           QLabel{
                               color: blue;
                               font-size: 14px;
                           }
                           
                           QLineEdit, QComboBox, QDateEdit{
                               background-color: #b8c9e1;
                               color: #333;
                               border: 1px solid #444;
                               padding; 5px;
                           }
                           
                           QTableWidget{
                               background-color: #b8c9e1;
                               color: #333;
                               border: 1px solid #444;
                               selection-background-color: #ddd;
                           }
                           
                           QPushButton{
                               background-color: #4caf50;
                               color: #fff;
                               border: none;
                               padding: 8px 16px;
                               font-size: 14px;
                           }
                           
                           QPushButton:hover{
                               background-color: #45a049;
                           }
                           """)
        
        # App Design with Layout
        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()
        
        # add text and design based on layout
        self.row1.addWidget(QLabel("Date:"))
        self.row1.addWidget(self.date_box)
        self.row1.addWidget(QLabel("Category:"))
        self.row1.addWidget(self.dropdown)
        
        self.row2.addWidget(QLabel("Amount:"))
        self.row2.addWidget(self.amount)
        self.row2.addWidget(QLabel("Description"))
        self.row2.addWidget(self.description)
        
        self.row3.addWidget(self.add_button)
        self.row3.addWidget(self.delete_button)
        
        # add rows to the master layout
        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)
        self.master_layout.addLayout(self.row3)
        
        # add the table design
        self.master_layout.addWidget(self.table)
        
        # set the final design
        self.setLayout(self.master_layout)
        
        self.load_table()
        
    def load_table(self):
        self.table.setRowCount(0)
        
        query = QSqlQuery("SELECT * FROM expenses")
        row = 0
        while query.next():
            expense_id = query.value(0)
            date = query.value(1)
            category = query.value(2)
            amount = query.value(3)
            description = query.value(4)
            
            # Add the values to the Table
            self.table.insertRow(row)
            
            # Take the values from the Database and insert it to column within the table
            self.table.setItem(row, 0,QTableWidgetItem(str(expense_id)))
            self.table.setItem(row, 1,QTableWidgetItem(date))
            self.table.setItem(row, 2,QTableWidgetItem(category))
            self.table.setItem(row, 3,QTableWidgetItem(str(amount)))
            self.table.setItem(row, 4,QTableWidgetItem(description))
            
            # create a counter for the database
            row += 1

    # Add Expense function
    def add_expense(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        category = self.dropdown.currentText()
        amount = self.amount.text()
        description = self.description.text()
        # pass # retrieve all input fields
        
        # prepare the INSERT QUERY Database
        query = QSqlQuery()
        query.prepare("""
                      INSERT INTO expenses (date, category, amount, description)
                      VALUES (?, ?, ?, ?)
                      """)
        # push and send information to the database
        query.addBindValue(date)
        query.addBindValue(category)
        query.addBindValue(amount)
        query.addBindValue(description)
        query.exec_()
        
        # clear all the fields
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()
        
        # load the new Database
        self.load_table()
        
    def delete_expense(self):
        selected_row = self.table.currentRow()
        if selected_row == -1: # if no row was not chosen from the table
            QMessageBox.warning(self, "No Expense Chosen", "Please chose an expense to delete!")
            return
        
        # if chosen a row, below code would capture the id from that row
        expense_id = int(self.table.item(selected_row, 0).text())
        
        # double check if the user want to delete the item
        confirm = QMessageBox.question(self, "Are you sure ?", "Do you want to Delete an expense ?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.No:
            return
        
        query = QSqlQuery()
        query.prepare("DELETE FROM expenses WHERE id = ?")
        query.addBindValue(expense_id)
        query.exec_()
        
        self.load_table()

# create Database
database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName("expense.db")
if not database.open():
    QMessageBox.critical(None, "Error", "Could not open your Database")
    sys.exit(1)
    
# create a Database query
query = QSqlQuery()
query.exec_("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                category TEXT,
                amount REAL,
                description TEXT
            )
            """)
        
# run the quiz_app
if __name__ in "__main__":
    app = QApplication([])
    main = ExpenseApp()
    main.show()
    app.exec_()      