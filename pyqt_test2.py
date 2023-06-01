from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QGridLayout
import numpy as np
import pptk
import win32gui
from PyQt6 import QtGui
# Only needed for access to command line arguments
import sys

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        # self.setWindowTitle("My App")
        # button = QPushButton("Press Me!")
        # self.setCentralWidget(button)
        widget = QWidget()
        layout = QGridLayout(widget)
        self.setCentralWidget(widget)

        self.cloudpoint = np.random.rand(100, 3)
        self.v = pptk.viewer(self.cloudpoint)
        hwnd = win32gui.FindWindowEx(0, 0, None, "viewer")
        self.window = QtGui.QWindow.fromWinId(hwnd)    
        self.windowcontainer = self.createWindowContainer(self.window, widget)

        layout.addWidget(self.windowcontainer, 0, 0)

app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = MainWindow()
window.setWindowTitle('PPTK Embed')
window.setGeometry(100, 100, 600, 500)
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
sys.exit(app.exec())
