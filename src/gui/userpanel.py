from camera.livecam import LiveCam
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class UserPanel(QWidget):
    def __init__(self):
        super().__init__()
        live = LiveCam()
        # 1. Main layout for this QWidget
        self.layout = QVBoxLayout(self)
        label = QLabel("ang Nwg")
        
        self.layout.addWidget(live)
        self.layout.addWidget(label)