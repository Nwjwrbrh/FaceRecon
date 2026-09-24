import sqlite3
import sqlite_vec
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class RegistrationForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_bytes = None
        self.image_embeddings = None
        self.init_ui()



    def init_ui(self):
        main_layout = QVBoxLayout(self)
        self.setMaximumWidth(550)
        main_layout.setContentsMargins(30, 30, 30, 30)

        self.roll_input = QLineEdit()
        self.roll_input.setPlaceholderText("Roll Number (12-Digits)  e.g., 123456789012")
        self.roll_input.setMaxLength(12)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter student name")
        self.dept_dropdown = QComboBox()
        self.dept_dropdown.setPlaceholderText("Select Department...")
        self.dept_dropdown.addItems(
            ["", "Content", "Design","Event","Media and PR","Research and Project","Technical","Web and IT","Workshop"]
        )
        self.position_dropdown = QComboBox()
        self.position_dropdown.setPlaceholderText("Select Position...")
        self.position_dropdown.addItems(
            ["", "Convenor", "Co-ordinator", "Member"]
        )
        self.img_preview = QLabel()
        self.img_preview.setFixedSize(432, 288)
        self.img_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_preview.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        self.img_preview.setText("No Image Chosen")
        self.submit_btn = QPushButton("Register User")
        self.submit_btn.clicked.connect(self.handle_submit)

        main_layout.setSpacing(20)
        main_layout.addStretch()
        main_layout.addWidget(self.img_preview, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.roll_input)
        main_layout.addWidget(self.name_input)
        main_layout.addWidget(self.dept_dropdown)
        main_layout.addWidget(self.position_dropdown)
        main_layout.addWidget(self.submit_btn)
        main_layout.addStretch()

        self.setStyleSheet("""
            QWidget {
                background-color: #292929;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                color: #dcdcdc;
            }
            QLabel {
                font-weight: bold;
                color: #dcdcdc;
            }
            QLabel#header {
                font-size: 18px;
                color: #dcdcdc;
            }
            QLineEdit, QComboBox {
                background-color: #292929;
                border-radius: 6px;
                padding: 10px;
                selection-background-color: #454545;
            }
            QLineEdit:focus, QComboBox:focus {
                background-color: #454545;
            }
            QPushButton {
                background-color: #abc662;
                color: #1e1e1e;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 700;
                letter-spacing: 0.5px;
                padding: 10px 24px;
                margin-top: 5px;
            }
            QPushButton:hover {
                background-color: #daff78;
            }
            QPushButton:pressed {
                background-color: #daff78;
                padding-top: 11px;
                padding-bottom: 9px;
            }
        """)



    def handle_image_upload(self, image):
        if image:
            pixmap = QPixmap(image)
            scaled_pixmap = pixmap.scaled(
                self.img_preview.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.img_preview.setPixmap(scaled_pixmap)



    def handle_submit(self):
        roll = self.roll_input.text().strip()
        name = self.name_input.text().strip()
        dept = self.dept_dropdown.currentText()
        position = self.position_dropdown.currentText()


        if len(roll) != 12 or not roll.isdigit():
            QMessageBox.warning(
                self,
                "Validation Error",
                "The Roll Number must be exactly 12 digits long.",
            )
            return
        if not name:
            QMessageBox.warning(
                self, "Validation Error", "Please provide a valid Name."
            )
            return
        if not self.image_bytes:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Please upload a profile picture before saving.",
            )
            return
        QMessageBox.information(
            self,
            "Form Validation Success",
            f"Ready to Register:\nRoll: {roll}\nName: {name}\nDept: {dept}\nPosition: {position}\nImage Data: Loaded ({len(self.image_bytes)} bytes)",
        )

        conn = sqlite3.connect("database.db")
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        conn.enable_load_extension(False)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Users (Image, RollNo, Name, Department, Position)
            VALUES (?, ?, ?, ?, ?)
        """,(self.image_bytes, roll, name, dept, position))

        user_id = cursor.lastrowid
        cursor.execute(
            """
            INSERT INTO FaceVectors(rowid, embedding)
            VALUES (?, ?)
        """,(user_id, self.image_embeddings))
        conn.commit()
        conn.close()
