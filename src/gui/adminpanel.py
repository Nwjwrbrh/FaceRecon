from PySide6.QtWidgets import QHBoxLayout, QWidget

from .table import DatabaseTableView


class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.table = DatabaseTableView()
        #self.table.setFixedWidth(1600)

        self.layout = QHBoxLayout()
        #self.layout.addStretch()
        self.layout.addWidget(self.table)
        #self.layout.addStretch()
        self.setLayout(self.layout)

        self.setStyleSheet("""
     QWidget {
        background-color: #1e1e1e;
        color: #e5e7eb;
    }

    QTableView {
        background-color: #292929;
        alternate-background-color: #252525;
        color: #e5e7eb;

        border: 1px solid #3f3f3f;
        border-radius: 8px;

        gridline-color: #494949;

        selection-background-color: #3b3b3b;
        selection-color: #ffffff;

        outline: none;
    }

    QTableView::item {
        padding: 10px 15px;
        border: none;
    }

    QTableView::item:selected {
        background-color: #404040;
        color: #ffffff;
    }

    QHeaderView::section {
        background-color: #494949;
        color: #f1f1f1;

        padding: 12px;

        font-weight: 700;
        font-size: 13px;

        border: none;
        border-bottom: 2px solid #5a5a5a;
    }

    QScrollBar:vertical {
        border: none;
        background: #292929;
        width: 10px;
        margin: 0px;
        border-radius: 5px;
    }

    QScrollBar::handle:vertical {
        background: #555555;
        min-height: 20px;
        border-radius: 5px;
    }

    QScrollBar::handle:vertical:hover {
        background: #707070;
    }

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {
        height: 0px;
    }

    QScrollBar:horizontal {
        border: none;
        background: #292929;
        height: 10px;
        margin: 0px;
        border-radius: 5px;
    }

    QScrollBar::handle:horizontal {
        background: #555555;
        min-width: 20px;
        border-radius: 5px;
    }

    QScrollBar::handle:horizontal:hover {
        background: #707070;
    }

    QScrollBar::add-line:horizontal,
    QScrollBar::sub-line:horizontal {
        width: 0px;
    }
""")

