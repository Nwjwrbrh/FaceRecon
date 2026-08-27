import sqlite3
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, 
    QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, 
    QFileDialog, QMessageBox, QFrame
)
from PySide6.QtGui import QPixmap, QImage, QIntValidator
from datetime import datetime


class RegistrationForm(QWidget):

    def __init__(self, parent=None ):
        super().__init__(parent) # Links parent for memory safety
        
        self.image_bytes = None  # To hold the uploaded image binary data
        self.init_ui()

    def init_ui(self):
        
        # 1. Main Structural Layout
        main_layout = QVBoxLayout(self)
        self.setMaximumWidth(550)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Form Header Accent Text
      
        self.roll_input = QLineEdit()
        self.roll_input.setPlaceholderText("Roll Number (12-Digits)  e.g., 123456789012")
        # Restrict entry to digits only up to 15 characters max
        self.roll_input.setMaxLength(12)
        
        # Name
        #self.name_label = QLabel("Full Name:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter student name")

        # Department
        
        self.dept_dropdown = QComboBox()
        self.dept_dropdown.setPlaceholderText("Select Department...")
        self.dept_dropdown.addItems(["", "AI & Robotics", "Electrical Eng", "Mechanical Eng"])
    
        # An empty graphical canvas container to host the selected image thumbnail
        self.img_preview = QLabel()
        self.img_preview.setFixedSize(432, 288)
        self.img_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_preview.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        self.img_preview.setText("No Image Chosen")


        # 4. Action Save Button
        self.submit_btn = QPushButton("Save Record to Vault")
        self.submit_btn.clicked.connect(self.handle_submit)

        # Assemble elements cleanly down the main layout track
        main_layout.addStretch()
        main_layout.addWidget(self.img_preview, alignment=Qt.AlignmentFlag.AlignCenter)
     
        main_layout.addWidget(self.roll_input)
      
        main_layout.addWidget(self.name_input)
       
        main_layout.addWidget(self.dept_dropdown)
        
    
        main_layout.addWidget(self.submit_btn)
        main_layout.addStretch()
        # 5. Styling via QSS Stylesheet
        self.setStyleSheet("""
            QWidget {
                background-color: #f7f9fc;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                color: #333333;
            }
            QLabel {
                font-weight: bold;
                color: #4A5568;
            }
            QLabel#header {
                font-size: 18px;
                color: #1A365D;
            }
            QLineEdit, QComboBox {
                background-color: #ffffff;
                border: 1px solid #CBD5E0;
                border-radius: 6px;
                padding: 10px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #3182CE;
            }
            QPushButton {
                background-color: #0f172a;        
                color: #ffffff;                    
                border: 1px solid #1e293b;
                border-radius: 8px;                
                font-size: 14px;
                font-weight: 700;                  
                letter-spacing: 0.5px;             
                padding: 10px 24px;
                margin-top: 5px; 
            }
            QPushButton:hover {
                background-color: #1e293b;        
                border-color: #3b82f6; 
            }
            QPushButton:pressed {
                background-color: #020617;        
                padding-top: 11px;                 
                padding-bottom: 9px;
            }
        """)
        
    def handle_image_upload(self,image):
        if image:
            pixmap = QPixmap(image)
            scaled_pixmap = pixmap.scaled(
                self.img_preview.size(), 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            self.img_preview.setPixmap(scaled_pixmap)

    def handle_submit(self):
        roll = self.roll_input.text().strip()
        name = self.name_input.text().strip()
        dept = self.dept_dropdown.currentText()


        # Simple Constraints Form Validation
        if len(roll) != 12 or not roll.isdigit():
            QMessageBox.warning(self, "Validation Error", "The Roll Number must be exactly 15 digits long.")
            return
            
        if not name:
            QMessageBox.warning(self, "Validation Error", "Please provide a valid Name.")
            return

        if not self.image_bytes:
            QMessageBox.warning(self, "Validation Error", "Please upload a profile picture before saving.")
            return

        # Success Action Loop Data Extraction Packaging
        QMessageBox.information(
            self, "Form Validation Success", 
            f"Ready to Insert:\nRoll: {roll}\nName: {name}\nDept: {dept}\nImage Data: Loaded ({len(self.image_bytes)} bytes)"
        )

        conn = sqlite3.connect("records.db")
        cursor = conn.cursor()
        time = datetime.now().strftime("%H:%M:%S")
        cursor.execute("INSERT INTO club VALUES (?,?,?,?,?,?,?)", (self.image_bytes,roll,name,dept,self.embedding_bytes,"absent",time))
        conn.commit()
        conn.close()
        print(f"Ready to Insert:\nRoll: {roll}\nName: {name}\nDept: {dept}\nImage Data: Loaded ({len(self.image_bytes)} bytes)")
        # Here you would call your `cursor.execute("INSERT INTO club...")` routine!

