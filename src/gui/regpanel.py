from camera.livecam import LiveCam
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout , QVBoxLayout , QPushButton
from .regform import RegistrationForm
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import numpy as np

class RegPanel(QWidget):
    def __init__(self):
        super().__init__()
        
        self.live = LiveCam()
        # 1. Main layout for this QWidget
        self.layout = QHBoxLayout(self)
        self.form = RegistrationForm()
        
        
        self.left_layout = QVBoxLayout()
        self.left_layout.addStretch()
        self.left_layout.addWidget(self.live)
        self.capture_btn = QPushButton("Capture")

        self.capture_btn.clicked.connect(self.handle_capture)
        print(self.live.captured)
    
        self.capture_btn.setObjectName("captureButton") # Hooks unique style sheet target rule below
        self.capture_btn.setFixedWidth(450) 

        self.setStyleSheet("""
            QPushButton#captureButton {
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
            QPushButton#captureButton:hover {
                background-color: #1e293b;        
                border-color: #3b82f6;             
            }
            QPushButton#captureButton:pressed {
                background-color: #020617;        
                padding-top: 11px;                 
                padding-bottom: 9px;
            }
        """)
        self.left_layout.addWidget(self.capture_btn,alignment=Qt.AlignmentFlag.AlignCenter)
        self.left_layout.addStretch()
    
        
        self.layout.addLayout(self.left_layout)
        self.layout.addWidget(self.form)

    
    def handle_capture(self):
        """Processes the face in-memory and pushes it directly onto the form view."""
        # Get the aligned face snapshot and 128-D math embedding array
        img_bytes, embedding_array = self.live.get_face_image_and_embedding()
        
        if img_bytes is not None and embedding_array is not None:
            # 1. Store the binary variables safely inside your registration form object
            self.form.image_bytes = img_bytes
            self.form.embedding_bytes = embedding_array.astype(np.float32).tobytes()
            
            # 2. Instantly update the image preview canvas window on the form
            pixmap = QPixmap()
            pixmap.loadFromData(img_bytes)
            
            # Scale it cleanly down to fit the form's 200x200 box dimensions
            scaled_pixmap = pixmap.scaled(
                self.form.img_preview.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.form.img_preview.setPixmap(scaled_pixmap)
            print(f"Captured! Vector array byte footprint size: {len(self.form.embedding_bytes)} bytes.")
        else:
            print("Capture warning: Position your face inside the camera bounds.")
