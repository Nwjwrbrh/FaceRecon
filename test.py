"""import onnx
model = onnx.load("src/model/face_detection_yunet_2026may.onnx")
onnx.checker.check_model(model)
print("Model is valid!")
"""


import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QLabel
from PySide6.QtGui import QMovie , QTransform
from PySide6.QtCore import Qt

class CustomButtonWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 1. Base Button
        self.button = QPushButton("Rotating GIF", self)
        self.button.setFixedSize(250, 60)
        self.button.setStyleSheet("text-align: left; padding-left: 15px; padding-top:10px; padding-bottom:10px;")

        # 2. Setup Label and Movie
        self.gif_label = QLabel(self.button)
        self.gif_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.movie = QMovie("assets/startArrow.gif")  # Replace with your path

        # 3. Intercept frame updates to rotate the image matrix
        self.rotation_angle = -90  # Set desired rotation angle (e.g., 90, 180, 270 degrees)
        self.movie.frameChanged.connect(self.apply_rotation)
        self.movie.start()

        # 4. Button Layout (Text left, GIF right)
        layout = QHBoxLayout(self.button)
        layout.setContentsMargins(0, 0, 15, 0)
        layout.addStretch()
        layout.addWidget(self.gif_label)

    def apply_rotation(self):
        # Grab current frame pixmap
        current_pixmap = self.movie.currentPixmap()
        
        # Apply rotation transformation
        transform = QTransform().rotate(self.rotation_angle)
        rotated_pixmap = current_pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation)
        
        # Set transformed image onto label
        self.gif_label.setPixmap(rotated_pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RotatedGifButton()
    window.show()
    sys.exit(app.exec())