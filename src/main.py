import sys
import cv2
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from gui.window import MainWindow

"""
class OpenCVCameraWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenCV Camera Feed")
        self.resize(800, 600)

        # Label to display video frames
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)

        # Open default camera (0)
        self.cap = cv2.VideoCapture(0)

        # Timer to read frames at ~30 FPS
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(33)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # --- YuNet or image processing can be done directly on 'frame' here ---

        # Convert BGR (OpenCV format) to RGB (Qt format)
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w

        # Create QImage and set to label
        q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(q_img))

    def closeEvent(self, event):
        self.cap.release()
        super().closeEvent(event)


import sys
from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlDatabase, QSqlTableModel
from PySide6.QtWidgets import (
    QApplication,
    QHeaderView,
    QMainWindow,
    QTableView,
    QVBoxLayout,
    QWidget,
)


class SqlTableWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt SQL Table Example")
        self.resize(800, 500)

        # 1. Connect to SQL Database
        if not self.create_connection():
            sys.exit(1)

        # 2. Setup QSqlTableModel
        self.model = QSqlTableModel(self)
        self.model.setTable("employees")

        # Set edit strategy
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        # 3. Fetch data FIRST before applying headers
        if not self.model.select():
            print(f"Table Select Error: {self.model.lastError().text()}")

        # 4. Map headers to all 5 columns created in company.db
        headers = ["ID", "Full Name", "Department", "Role", "Salary ($)"]
        for col_idx, header_name in enumerate(headers):
            self.model.setHeaderData(
                col_idx, Qt.Orientation.Horizontal, header_name
            )

        # 5. Setup QTableView
        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        # UI Improvements
        self.table_view.setAlternatingRowColors(True)

        # Dynamically stretch columns to fill the view width
        self.table_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        # 6. Set Central Layout
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(self.table_view)
        self.setCentralWidget(container)

    def create_connection(self):
        # Prevent adding duplicate connection instances
        if QSqlDatabase.contains("qt_sql_default_connection"):
            db = QSqlDatabase.database("qt_sql_default_connection")
        else:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName("company.db")

        if not db.open():
            print(f"Database Error: {db.lastError().text()}")
            return False
        return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SqlTableWindow()
    window.show()
    sys.exit(app.exec())
"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())