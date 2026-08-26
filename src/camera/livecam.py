import cv2
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy



class LiveCam(QWidget):



    def __init__(self):

        super().__init__()

        self.label = QLabel(self)  #label for rendering img
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.label.setMinimumSize(1080, 720)


        self.layout = QVBoxLayout(self) #layout/vertical div
        self.layout.addStretch()
        self.layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addStretch()


        self.cap = cv2.VideoCapture(0)  #video capt.

        self.timer = QTimer(self)   #time-frame updater
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(33)  # ~30 FPS




    def update_frame(self):

        ret, frame = self.cap.read()  #camera frames
        if not ret:
            return
        frame = cv2.flip(frame, 1)


        detector = cv2.FaceDetectorYN.create(            #detector node
            "/home/abhijit71/Desktop/FaceRecon/src/gui/face_detection_yunet_2026may.onnx",
            "",
            (320, 320),
            0.9,
            0.3,
            5000,
        )
        detector.setInputSize(frame.shape[1::-1])
        _, faces = detector.detect(frame)
        if faces is not None:
            for face in faces:
                x, y, w, h = face[:4].astype(int)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (128, 0, 128), 2)


        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  #color formatting from cv to qt
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w


        q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        scaled_pixmap = pixmap.scaled(
            self.label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.label.setPixmap(scaled_pixmap)

