from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from camera.livecam import LiveCam



class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        label = QLabel("Hello UsePanel")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
