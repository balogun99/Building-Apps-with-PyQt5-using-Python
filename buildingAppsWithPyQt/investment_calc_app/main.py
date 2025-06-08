# load the libraries
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QMessageBox, QLineEdit, QLabel, QTreeView, QMainWindow,
                             QPushButton, QFileDialog, QCheckBox)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import os

# create a class
class FinanceApp(QMainWindow):
    def __init__(self):
        super(FinanceApp,self).__init__()
        self.setWindowTitle("Finance App")
        self.resize(800,600)
        
        main_window = QWidget()
        
        # Input Fields
        
        self.rate_text = QLabel("Interest Rate (%): ")
        self.rate_input = QLineEdit()
        
        self.initial_text = QLabel("Initial Investment: ")
        self.initial_input = QLineEdit()
        
        self.years_text = QLabel("Years to Invest")
        self.years_input = QLineEdit()
        
        # Creation of Tree View
        self.model = QStandardItemModel()
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        
        # column items
        self.calc_button = QPushButton("Calculate")
        self.clear_button = QPushButton("Clear")
        self.save_button = QPushButton("Save")
        self.dark_mode = QCheckBox("Dark Mode")


        # Chart Section
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        
        # set the layout
        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.col1 = QVBoxLayout()
        self.col2 = QVBoxLayout()
        
        # add the input fields button to row1
        self.row1.addWidget(self.rate_text)
        self.row1.addWidget(self.rate_input)
        self.row1.addWidget(self.initial_text)
        self.row1.addWidget(self.initial_input)
        self.row1.addWidget(self.years_text)
        self.row1.addWidget(self.years_input)
        self.row1.addWidget(self.dark_mode)
        
        # add the column items to col1
        self.col1.addWidget(self.tree_view)
        self.col1.addWidget(self.calc_button)
        self.col1.addWidget(self.clear_button)
        self.col1.addWidget(self.save_button)
        
        # add the figure column to col2
        self.col2.addWidget(self.canvas)
        
        # add the layout of row1 & row2 to col1 & col2
        self.row2.addLayout(self.col1, 30) # TreeView
        self.row2.addLayout(self.col2, 70) # Chart
        
        # add row1 and row2 to the master layout
        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)
        
        main_window.setLayout(self.master_layout)
        self.setCentralWidget(main_window)
        
        # add events for calculate and reset/clear buttons
        self.calc_button.clicked.connect(self.calc_interest)
        self.clear_button.clicked.connect(self.reset)
        self.save_button.clicked.connect(self.save_data)
        self.dark_mode.stateChanged.connect(self.toggle_mode)
        self.apply_styles()

    # function to add styles and dark mode to the interface
    def apply_styles(self):
        self.setStyleSheet(
            """
            FinanceApp {
            background-color: grey;
            }
            
            QLabel, QLineEdit, QPushButton {
            background-color: black;
            color: white;
            }
            
            QTreeView {
            background-color: black;
            color: white;
            }
            """
        )

        if self.dark_mode.isChecked():
            self.setStyleSheet(
                """
                FinanceApp {
                background-color: #222222;
                }
                
                QLabel, QLineEdit, QPushButton {
                background-color: #333333;
                color: blue;
                }
                
                QTreeView {
                background-color: #444444;
                color: blue;
                }
                """
            )


    def toggle_mode(self):
        self.apply_styles()

    #  function to calculate the interest
    def calc_interest(self):
        initial_investment = None
        try:
            interest_rate = float(self.rate_input.text())
            initial_investment = float(self.initial_input.text())
            num_years = int(self.years_input.text())
            
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid Input, enter a number")
            return

        self.model.clear()
        self.model.setHorizontalHeaderLabels(("Year","Total"))
        
        total = initial_investment
        for year in range(1,num_years+1):
            total += total * (interest_rate/100)
            item_year = QStandardItem(str(year))
            item_total = QStandardItem("{:.2f}".format(total))
            self.model.appendRow([item_year, item_total])

    # update chart with the data
        self.figure.clear() # clear any old charts
        # plt.style.use('seaborn')
        ax = self.figure.subplots() # created a subplots
        years = list(range(1, num_years+1)) # generated the data
        totals = [initial_investment * (1 + interest_rate / 100) ** year for year in years] # generated the data
        ax.plot(years,totals) # set the years & total to the plot
        ax.set_title("Interest")
        ax.set_xlabel("Year")
        ax.set_ylabel("Total")
        self.canvas.draw() # drew on our canvas

    # function to save image
    def save_data(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            folder_path = os.path.join(dir_path, "Saved")
            os.makedirs(folder_path, exist_ok=True)

            file_path = os.path.join(folder_path, "results.csv")
            with open(file_path, "w") as file:
                file.write("Year, Total\n")
                for row in range(self.model.rowCount()):
                    year = self.model.index(row,0).data()
                    total = self.model.index(row,1).data()
                    file.write("{},{}".format(year,total))

                plt.savefig("Saved/chart.png")

            QMessageBox.information(self, "Save Results", "Results would be save to your folder")
        else:
            QMessageBox.warning(self,"Save Results", "No Directory Found or Selected")
    
    # reset the input fields        
    def reset(self):
        self.rate_input.clear()
        self.initial_input.clear()
        self.years_input.clear()
        self.model.clear()

        self.figure.clear()
        self.canvas.draw()
        
if __name__ == "__main__":
    app = QApplication([])
    my_app = FinanceApp()
    my_app.show()
    app.exec_()        