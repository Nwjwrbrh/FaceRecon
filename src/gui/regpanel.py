import numpy as np

from camera.livecam import LiveCam
from .regform import RegistrationForm

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QHBoxLayout , QVBoxLayout , QPushButton



class RegPanel(QWidget):
    def __init__(self):
        super().__init__()
        
        self.live = LiveCam()
        self.form = RegistrationForm()

        self.layout = QHBoxLayout(self)
        self.left_layout = QVBoxLayout()
        self.left_layout.addStretch()
        self.left_layout.addWidget(self.live)

        self.capture_btn = QPushButton("Capture Face Photo")
        self.capture_btn.clicked.connect(self.handle_capture)
        self.capture_btn.setObjectName("captureButton") 
        self.capture_btn.setFixedWidth(450) 
        self.setStyleSheet("""
            QPushButton {
                background-color: #abc662;
                color: #1e1e1e;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
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

        self.left_layout.addWidget(self.capture_btn,alignment=Qt.AlignmentFlag.AlignCenter)
        self.left_layout.addStretch()
        self.layout.addLayout(self.left_layout)
        self.layout.addWidget(self.form)
 
    
    def handle_capture(self):
        img_bytes, embedding = self.live.get_face_image_and_embedding()
        
        if img_bytes is not None and embedding is not None:
            self.form.image_bytes = img_bytes
            self.form.image_embeddings = np.asarray(embedding,dtype=(np.float32)).reshape(-1)
            
            pixmap = QPixmap()
            pixmap.loadFromData(img_bytes)
            scaled_pixmap = pixmap.scaled(
                self.form.img_preview.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.form.img_preview.setPixmap(scaled_pixmap)
        else:
            print("Capture warning: Position your face inside the camera bounds.")
