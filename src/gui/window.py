from PySide6.QtWidgets import QApplication, QLabel, QMainWindow , QTabWidget
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from .panels import UserPanel , AdminPanel

class TabView(QTabWidget):
    def __init__(self):
        super().__init__()
        self.count = 2
        self.isMovable = False
        self.addTab(UserPanel(),"user")
        self.addTab(AdminPanel(),"admin")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenCV Camera")
        #self.resize(800, 600)

        # Label to display video frames
        self.tab = TabView()
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.tab)

