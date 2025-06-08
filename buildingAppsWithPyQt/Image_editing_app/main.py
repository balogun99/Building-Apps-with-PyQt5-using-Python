# import libraries
import os
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLabel, QPushButton, QListWidget, QComboBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageEnhance, ImageFilter

# App Settings
app = QApplication([])
main_widow = QWidget()
main_widow.setWindowTitle("PhotoQt")
main_widow.resize(900,700)

# App Widgets/Objects
btn_folder = QPushButton("Folder")
file_list = QListWidget()

btn_left = QPushButton("Left")
btn_right = QPushButton("Right")
mirror = QPushButton("Mirror")
sharpness = QPushButton("Sharpen")
gray = QPushButton("B/W")
saturation = QPushButton("Color")
contrast = QPushButton("Contrast")
blur = QPushButton("Blur")


# DropDown Box
filter_box = QComboBox()
filter_box.addItem("Original")
filter_box.addItem("Left")
filter_box.addItem("Right")
filter_box.addItem("Mirror")
filter_box.addItem("Sharpen")
filter_box.addItem("B/W")
filter_box.addItem("Color")
filter_box.addItem("Contrast")
filter_box.addItem("Blur")

picture_box = QLabel("Image will appear here")


# App Design
master_layout = QHBoxLayout()

col1 = QVBoxLayout()
col2 = QVBoxLayout()

col1.addWidget(btn_folder)
col1.addWidget(file_list)
col1.addWidget(filter_box)
col1.addWidget(btn_left)
col1.addWidget(btn_right)
col1.addWidget(mirror)
col1.addWidget(sharpness)
col1.addWidget(gray)
col1.addWidget(saturation)
col1.addWidget(contrast)
col1.addWidget(blur)

col2.addWidget(picture_box)

# link the layout to the column
master_layout.addLayout(col1, 20)
master_layout.addLayout(col2, 80)

# display the quiz_app window
main_widow.setLayout(master_layout)

# All App Functionalities

working_directory = ""

# Filter Files and Extensions

def filter(files, extensions):
    results = []
    for file in files:
        for ext in extensions:
            if file.endswith(ext):
                results.append(file)
    return results

# Choose current work Directory

def getWorkingDirectory():
    global working_directory
    working_directory = QFileDialog.getExistingDirectory()
    extensions = ['.jpg', '.jpeg', '.png', '.svg']
    filenames = filter(os.listdir(working_directory), extensions)
    file_list.clear()
    for filename in filenames:
        file_list.addItem(filename)

# Class for Editing, Loading, and Saving Image
# Image Editing Class
class Editor():
    def __init__(self):
        self.image = None
        self.original = None
        self.filename = None
        self.save_folder = "edits/"
     
    # load image class 
    def load_image(self, filename):
        self.filename = filename
        fullname = os.path.join(working_directory, self.filename)
        self.image = Image.open(fullname)
        self.original = self.image.copy()
        
    # save image class
    def save_image(self):
        path = os.path.join(working_directory, self.save_folder)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)  
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)
        
    # show image class  # QPixmap allows us to load images in python
    def show_image(self, path):
        picture_box.hide()
        image = QPixmap(path)
        w,h = picture_box.width(), picture_box.height()
        image = image.scaled(w,h, Qt.KeepAspectRatio)
        picture_box.setPixmap(image)
        picture_box.show()
        
    # editing tools function
    # def gray(self):
    #     self.image = self.image.convert("L") # convert the image to black/white
    #     self.save_image() # save this image into the edits folder
    #     image_path = os.path.join(working_directory, self.save_folder, self.filename) # show the new edited image in a new path
    #     self.show_image(image_path) # take the show image path with the image path
        
    # def left(self):
    #     self.image = self.image.transpose(Image.ROTATE_90)
    #     self.save_image()
    #     image_path = os.path.join(working_directory, self.save_folder, self.filename)
    #     self.show_image(image_path)
        
    # def right(self):
    #     self.image = self.image.transpose(Image.ROTATE_270)
    #     self.save_image()
    #     image_path = os.path.join(working_directory, self.save_folder, self.filename)
    #     self.show_image(image_path)
        
    # def mirror(self):
    #     self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
    #     self.save_image()
    #     image_path = os.path.join(working_directory, self.save_folder, self.filename)
    #     self.show_image(image_path)
        
    # def sharpen(self):
    #     self.image = self.image.filter(ImageFilter.SHARPEN)
    #     self.save_image()
    #     image_path = os.path.join(working_directory, self.save_folder, self.filename)
    #     self.show_image(image_path)
        
    # def blur(self):
    #     self.image = self.image.filter(ImageFilter.BLUR)
    #     self.save_image()
    #     image_path = os.path.join(working_directory, self.save_folder, self.filename)
    #     self.show_image(image_path)
        
    # def color(self):
    #     self.image = ImageEnhance.Color(self.image).enhance(1.2)
    #     self.save_image()
    #     image_path = os.path.join(working_directory, self.save_folder, self.filename)
    #     self.show_image(image_path)
        
    # def contrast(self):
        self.image = ImageEnhance.Contrast(self.image).enhance(1.2)
        self.save_image()
        image_path = os.path.join(working_directory, self.save_folder, self.filename)
        self.show_image(image_path)
    
    def transformImage(self, transformation):
        transformations = {
            "B/W": lambda image:image.convert("L"),
            "Color": lambda image:ImageEnhance.Color(image).enhance(1.2),
            "Contrast": lambda image:ImageEnhance.Contrast(image).enhance(1.2),
            "Blur": lambda image: image.filter(ImageFilter.BLUR),
            "Left": lambda image: image.transpose(Image.ROTATE_90),
            "Right": lambda image: image.transpose(Image.ROTATE_270),
            "Mirror": lambda image: image.transpose(Image.FLIP_LEFT_RIGHT),
            "Sharpen": lambda image: image.filter(ImageFilter.SHARPEN)
        }
        
        transform_function = transformations.get(transformation)
        if transform_function:
            self.image = transform_function(self.image)
            self.save_image()
            
        self.save_image()
        image_path = os.path.join(working_directory, self.save_folder, self.filename)
        self.show_image(image_path)
    
    # Filter Dropdown Function   
    def apply_filter(self, filter_name):
        if filter_name == "Original":
            self.image = self.original.copy()
        else:
            mapping = { # create a lists for filter dropdown
                "B/W": lambda image:image.convert("L"),
                "Color": lambda image:ImageEnhance.Color(image).enhance(1.2),
                "Contrast": lambda image:ImageEnhance.Contrast(image).enhance(1.2),
                "Blur": lambda image: image.filter(ImageFilter.BLUR),
                "Left": lambda image: image.transpose(Image.ROTATE_90),
                "Right": lambda image: image.transpose(Image.ROTATE_270),
                "Mirror": lambda image: image.transpose(Image.FLIP_LEFT_RIGHT),
                "Sharpen": lambda image: image.filter(ImageFilter.SHARPEN)
            }
            
            filter_function = mapping.get(filter_name)
            if filter_function:
                self.image = filter_function(self.image)
                self.save_image()
                image_path = os.path.join(working_directory, self.save_folder, self.filename)
                self.show_image(image_path)
            pass
        
        self.save_image()
        image_path = os.path.join(working_directory, self.save_folder, self.filename)
        self.show_image(image_path)
        
# function to handle filter
def handle_filter():
    if file_list.currentRow() >= 0:
        select_filter = filter_box.currentText()
        main.apply_filter(select_filter) 

        
# function to display image that was clicked
def displayImage():
    if file_list.currentRow() >= 0:
        filename = file_list.currentItem().text()
        main.load_image(filename)
        main.show_image(os.path.join(working_directory, main.filename))
        
main = Editor()

#   Button Functionalities   
btn_folder.clicked.connect(getWorkingDirectory) # to display image clicked from the folder
file_list.currentRowChanged.connect(displayImage) # to display chosen image on the window
filter_box.currentTextChanged.connect(handle_filter) # to display the current text changed filter

gray.clicked.connect(lambda: main.transformImage("B/W"))
btn_left.clicked.connect(lambda: main.transformImage("Left"))
btn_right.clicked.connect(lambda: main.transformImage("Right"))
mirror.clicked.connect(lambda: main.transformImage("Mirror"))
sharpness.clicked.connect(lambda: main.transformImage("Sharpen"))
saturation.clicked.connect(lambda: main.transformImage("Color"))
contrast.clicked.connect(lambda: main.transformImage("Contrast"))
blur.clicked.connect(lambda: main.transformImage("Blur"))


# run quiz_app
main_widow.show()
app.exec_()