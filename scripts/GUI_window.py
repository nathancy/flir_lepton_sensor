'''
Filename: GUI_window.py
Description: Class to control the GUI for image processing, GPS/CSV logging, and KML generation.
Usage: python GUI_window.py
'''

from PyQt4 import QtGui, QtCore
from subprocess import call
import sys
import os
from capture import capture

class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(0, 0, 1000, 800)
        self.setWindowTitle("Flir")
        self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))
        self.resolution_value = '1'

        # Create menubar
        mainMenu = self.menuBar() 
        fileMenu = mainMenu.addMenu("&File")

        # Menubar options
        # Browse file system for CSV file
        open_CSV_file_action = QtGui.QAction("&Open CSV file", self)
        open_CSV_file_action.setShortcut("Ctrl+O")
        open_CSV_file_action.setStatusTip("Browse file system for CSV data file")
        open_CSV_file_action.triggered.connect(self.generate_KML_file)
        fileMenu.addAction(open_CSV_file_action)

        # Open latest CSV file
        open_latest_CSV_file_action = QtGui.QAction("&Convert latest CSV file", self)
        open_latest_CSV_file_action.setShortcut("Ctrl+L")
        open_latest_CSV_file_action.setStatusTip("Automatically select and convert latest CSV data file")
        open_latest_CSV_file_action.triggered.connect(self.generate_latest_KML_file)
        fileMenu.addAction(open_latest_CSV_file_action)
      
        # Close program
        exit_action = QtGui.QAction("&Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Close program")
        exit_action.triggered.connect(self.close_application)
        fileMenu.addAction(exit_action)

        self.statusBar()
        self.single_thermal_image_capture()
        self.KML_resolution()

        # Show the widgets onto the GUI, must be at the end
        self.show()
        self.KML_generator_latest_filename = "KML_generator_latest.py"
        self.KML_generator_filename = "KML_generator.py"


    def home(self):
        button = QtGui.QPushButton("Quit", self)
        button.clicked.connect(self.close_application)
        button.resize(100,100)
        button.move(100,100)
        self.show()

    # Menu option functions
    def generate_KML_file(self):
        CSV_file_path = QtGui.QFileDialog.getOpenFileName(self, 'Select CSV file', './', "Text files (*.csv)")
        call(["python", self.KML_generator_filename, CSV_file_path, self.resolution_value])

    def generate_latest_KML_file(self):
        call(["python", self.KML_generator_latest_filename, self.resolution_value])

    def close_application(self):
        sys.exit()

    # GUI elements
    def KML_resolution(self):
        self.resolution_label = QtGui.QLabel('KML Resolution Value', self)
        self.resolution_label.adjustSize()
        # horizontal, vertical
        self.resolution_label.move(15, 100)
        
        self.resolution_value_dropdown = QtGui.QComboBox(self)
        self.resolution_value_dropdown.move(300, 100)
        self.resolution_value_dropdown.addItem("1")
        self.resolution_value_dropdown.addItem("2")
        self.resolution_value_dropdown.addItem("3")
        self.resolution_value_dropdown.addItem("4")
        self.resolution_value_dropdown.addItem("5")
        self.resolution_value_dropdown.addItem("10")
        self.resolution_value_dropdown.addItem("30")
        self.resolution_value_dropdown.addItem("60")
        self.resolution_value_dropdown.addItem("120")
        self.resolution_value_dropdown.addItem("600")
        self.resolution_value_dropdown.addItem("1200")
        self.resolution_value_dropdown.addItem("3600")
        self.resolution_value_dropdown.activated[str].connect(self.set_resolution_value)

    def single_thermal_image_capture(self):
        self.single_thermal_image_capture_label = QtGui.QLabel("Single Thermal Image Capture", self)
        self.single_thermal_image_capture_label.adjustSize()
        self.single_thermal_image_capture_label.move(15, 150)

        self.single_thermal_image_capture_button = QtGui.QPushButton("Capture", self)
        self.single_thermal_image_capture_button.clicked.connect(capture)
        self.single_thermal_image_capture_button.resize(140, 35)
        self.single_thermal_image_capture_button.move(400, 150)
    # Helpers
    def set_resolution_value(self, value):
        self.resolution_value = value

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()

