from PySide6.QtCore import (
    QEasingCurve,
    QParallelAnimationGroup,
    QPropertyAnimation,
)
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (
    QButtonGroup,
    QLabel,
    QPushButton,
    QStyle,
    QStyleOption,
    QVBoxLayout,
    QWidget,
)


class SideBar(QWidget):
    def __init__(self, parent=None):

        super().__init__(parent)

        # State vars
        self.open = True
        self.animation_group = None
        self.setFixedWidth(220)
        self.setObjectName("sidebar")

        # button group
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        # main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 20, 10, 10)
        self.main_layout.setSpacing(10)

        # Header
        self.title_label = QLabel("FaceRecon")
        self.title_label.setObjectName("sidebarTitle")
        self.main_layout.addWidget(self.title_label)

        # Nav Items
        self.nav_layout = QVBoxLayout()
        self.nav_layout.setContentsMargins(10, 0, 10, 0)
        self.nav_layout.setSpacing(5)
        # home button
        self.home = QPushButton("Home")
        self.home.setCheckable(True)
        self.button_group.addButton(self.home)
        self.nav_layout.addWidget(self.home)
        # regumnet translation button
        self.reg = QPushButton("Register")
        self.reg.setCheckable(True)
        self.button_group.addButton(self.reg)
        self.nav_layout.addWidget(self.reg)
        # voice translation button
        self.admin = QPushButton("Admin")
        self.admin.setCheckable(True)
        self.button_group.addButton(self.admin)
        self.nav_layout.addWidget(self.admin)

        self.button_group.buttons()[0].setChecked(True)
        self.main_layout.addLayout(self.nav_layout)
        self.main_layout.addStretch()

        self.setStyleSheet("""
            QWidget#sidebar {
                background-color: #292929;
                border-radius: 16px;
            }
            QLabel#sidebarTitle {
                color: #ffffff;
                font-size: 18px;
                font-weight: bold;
                padding: 20px 15px;
                background-color: transparent;
            }
            QPushButton {
                color: #ecf0f1;
                background-color: transparent;
                border: none;
                padding: 14px 15px;
                font-size: 14px;
                text-align: left;
                font-weight: bold;
                border-radius:16px;
            }
            QPushButton:hover {
                background-color: #7f9051;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #daff78;
                color: #1e1e1e;
            }
            QPushButton:checked {
                background-color: #daff78;
                color: #1e1e1e;
            }
        """)

   