from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout, QComboBox
import numpy as np
import pptk
import win32gui, win32con
from PyQt6 import QtGui
# Only needed for access to command line arguments
import sys

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
class PointcloudProcessor():
    def __init__(self):
        self.pointcloud_path = ""
        self.pointcloud = np.random.rand(100, 3)
        self.labels_idx = np.zeros(100)
        self.label_dict ={'label1':1, 'label2':2, 'label3':3}
        self.pointcloud_viewer= pptk.viewer(self.pointcloud)
        self.pointcloud_viewer.set(point_size = 0.01)
    def change_labels(self, label):
        selected_indices = self.pointcloud_viewer.get('selected')
        self.labels_idx[selected_indices] = self.label_dict[label]
    def update_viewer(self):
        self.pointcloud_viewer.attributes(self.labels_idx)
        self.pointcloud_viewer.set(selected = [])
    
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.pointcloud_processor = PointcloudProcessor()
        
        viewer_layout = QHBoxLayout()
        widget = QWidget()
        console_layout = QVBoxLayout()
        console_layout.setSpacing(0)

        # Embed ppptk Window
        hwnd = win32gui.FindWindowEx(0, 0, None, "viewer")
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        self.window = QtGui.QWindow.fromWinId(hwnd)    
        self.windowcontainer = self.createWindowContainer(self.window, widget)
        self.windowcontainer.resize(400,300)

        #create combobox
        self.combobox = QComboBox()
        self.labels_list = ['label1', 'label2', 'label3']        
        self.combobox.addItems(self.labels_list)
        self.combobox.setFixedWidth(150)

        #crete change label buttoon
        self.button = QPushButton("Change Label")
        self.button.setFixedWidth(100)
        self.button.clicked.connect(self.click_change_labels)

        # Format Layout
        console_layout.addWidget(self.combobox)
        console_layout.addWidget(self.button)
        console_layout.addStretch()
        viewer_layout.addWidget(self.windowcontainer)
        viewer_layout.addLayout(console_layout)
        # layout.addWidget(self.button)
        widget.setLayout(viewer_layout)
        self.setCentralWidget(widget)

    def click_change_labels(self):

        cur_label_key = self.combobox.currentText()
        self.pointcloud_processor.change_labels(cur_label_key)
        self.pointcloud_processor.update_viewer()

app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = MainWindow()
window.setWindowTitle('PPTK Embed')
window.setGeometry(100, 100, 600, 500)
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
sys.exit(app.exec())
