from PySide6.QtWidgets import QHBoxLayout, QWidget

from .table import DatabaseTableView


class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.table = DatabaseTableView()
        self.table.setFixedWidth(1350)

        self.layout = QHBoxLayout()
        self.layout.addStretch()
        self.layout.addWidget(self.table)
        self.layout.addStretch()
        self.setLayout(self.layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #f8fafc;
            }

            QTableView {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                gridline-color: #f1f5f9;
                selection-background-color: #eff6ff;
                selection-color: #1e3a8a;
                outline: none;
            }

            QHeaderView::section {
                background-color: #f1f5f9;
                color: #475569;
                padding: 12px;
                font-weight: 700;
                font-size: 13px;
                border: none;
                border-bottom: 2px solid #cbd5e1;
            }

            QScrollBar:vertical {
                border: none;
                background: #f1f5f9;
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #cbd5e1;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #94a3b8;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
 """)
