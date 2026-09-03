from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QMainWindow, QTabWidget

from .adminpanel import AdminPanel
from .regpanel import RegPanel
from .userpanel import UserPanel


class TabView(QTabWidget):
    def __init__(self):
        super().__init__()
        self.count = 2
        self.isMovable = False
        self.userpnl = UserPanel()
        self.regpnl = RegPanel()
        self.adminpnl = AdminPanel()
        self.addTab(self.userpnl, "User")
        self.addTab(self.regpnl, "Register")
        self.addTab(self.adminpnl, "Admin")

        self.currentChanged.connect(self.handle_tab_switch)
        self.userpnl.live.start_cam()

    def handle_tab_switch(self, index):
        self.userpnl.live.stop_cam()
        if hasattr(self.regpnl, "live"):
            self.regpnl.live.stop_cam()

        if index == 0:
            self.userpnl.live.start_cam()
        elif index == 1 if hasattr(self.regpnl, "live") else False:
            self.regpnl.live.start_cam()
        elif index == 2:
            self.adminpnl.table.refreshdb()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenCV Camera")
        # self.resize(800, 600)

        # Label to display video frames
        self.tab = TabView()
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.tab)
