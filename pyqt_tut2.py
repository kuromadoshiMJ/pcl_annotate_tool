import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.button_is_checked = True
        self.setWindowTitle("My App")
        self.button = QPushButton("Press Me!")
        # button.setCheckable(True)
        self.button.clicked.connect(self.button_clicked)
        # button.clicked.connect(self.button_toggled)
        self.setCentralWidget(self.button)

    def button_clicked(self):
        self.button.setText("you already clicked me")
        self.button.setEnabled(False)
        self.setWindowTitle("my oneshot App")
    def button_toggled(self, checked):
        self.button_is_checked = checked
        print("Checked?", self.button_is_checked)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()