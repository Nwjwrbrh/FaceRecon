from .adminpanel import AdminPanel
from .regpanel import RegPanel
from .userpanel import UserPanel
from .sidebar import SideBar
from .home import HomePage

from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QStackedWidget, QWidget


class TabView(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.home = HomePage()
        self.userPanel =UserPanel()
        self.adminPanel = AdminPanel()
        self.regPanel = RegPanel()
        self.addWidget(self.home)
        self.addWidget(self.userPanel)
        self.addWidget(self.regPanel)
        self.addWidget(self.adminPanel)
        
        self.currentChanged.connect(self.handle_tab_switch)
        self.home.startButton.clicked.connect(lambda: self.setCurrentIndex(1))
        self.home.startButton.clicked.connect(lambda: self.home.attendanceInit())
 
    def handle_tab_switch(self, index):
        if index == 1:
            if hasattr(self.regPanel, "live"):
                self.regPanel.live.stop_cam()
            self.userPanel.live.start_cam()
        elif index == 2 if hasattr(self.regPanel, "live") else False:
            self.userPanel.live.stop_cam()
            self.regPanel.live.start_cam()
        elif index == 3:
            self.adminPanel.table.refreshdb()

    


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FaceRecon")
        self.setStyleSheet("""
            QMainWindow {
                background-color: #181818;
            }
        """)

        self.mainWidget = QWidget()
        self.sidebar = SideBar()
        self.tab = TabView()

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.sidebar)
        self.layout.addWidget(self.tab)
        self.mainWidget.setLayout(self.layout)

        self.sidebar.home.clicked.connect(lambda: self.tab.setCurrentIndex(0))
        self.sidebar.reg.clicked.connect(lambda: self.tab.setCurrentIndex(2))
        self.sidebar.admin.clicked.connect(lambda: self.tab.setCurrentIndex(3))

        self.setCentralWidget(self.mainWidget)
