from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from camera.livecam import LiveCam
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
            /* --- Parent Container Slate Canvas Frame --- */
            QWidget {
                background-color: #f8fafc;        /* Soft neutral background styling */
            }

            /* --- Table Component View Box Layout --- */
            QTableView {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;        /* Sleek card border layout */
                border-radius: 8px;                /* Curved smooth layout window boundaries */
                gridline-color: #f1f5f9;           /* Soft cell separator tracks */
                selection-background-color: #eff6ff; /* Light electric blue selected row highlight */
                selection-color: #1e3a8a;          /* Deep bold text for focused rows */
                outline: none;
            }

            /* --- Modern High-Contrast Grid Header Sections --- */
            QHeaderView::section {
                background-color: #f1f5f9;        /* Structured grey header backing canvas */
                color: #475569;                    /* Professional deep slate tracking text */
                padding: 12px;
                font-weight: 700;                  /* Strong bold headers */
                font-size: 13px;
                border: none;
                border-bottom: 2px solid #cbd5e1;  /* Defining boundary bottom line track */
            }

            /* --- Clean Minimalist Scrollbars --- */
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
                background: #94a3b8;               /* Darker slate handle highlight on track hover */
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;                       /* Removes clunky legacy navigation arrow buttons */
            }
        """)
