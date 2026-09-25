import cv2

from utils import modelPath

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget


class LiveCam(QWidget):


    def __init__(self):
        super().__init__()

        self.label = QLabel(self)  # label for rendering img
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.label.setMinimumSize(1080, 720)

        self.layout = QVBoxLayout(self)  
        self.layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addStretch()

        self.cap = None  # video capt.
        self.current_raw_frame = None
        self.captured = None
        self.latest_face_data = None

        self.timer = QTimer(self)  
        self.timer.timeout.connect(self.update_frame)
        
        # YuNet model node 
        self.detector = cv2.FaceDetectorYN.create(  
            modelPath("face_detection_yunet_2026may.onnx"),
            "",
            (320, 320),
            0.9,
            0.3,
            5000,
        )





    # Start update frame loop (~30 FPS)
    def start_cam(self):
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
            self.timer.start(33) 





   # Clear the last stale fr , prevent race cond.
    def stop_cam(self):
        self.timer.stop()
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.label.clear()  




    
    # updates frame with a rectangle around : numpy calc
    def update_frame(self):
        ret, frame = self.cap.read()  # bool , camera frames
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        self.current_raw_frame = frame.copy()
        self.detector.setInputSize(frame.shape[1::-1])
        _, faces = self.detector.detect(frame)

        if faces is not None and len(faces) > 0:
            self.latest_face_data = faces[0]  # Store closest active face
            x, y, w, h = self.latest_face_data[:4].astype(int)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (128, 0, 128), 2)
        else:
            self.latest_face_data = None

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # color formatting from cv to qt
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


    


    # To capture for Registration
    def capture_photo(self):
        if self.current_raw_frame is not None:
            success, encoded_img = cv2.imencode(".jpg", self.current_raw_frame)
            if success:
                self.captured = encoded_img.tobytes()





    # To get image and embedding for db wrrite
    def get_face_image_and_embedding(self):
        # recognizer model sface node
        recognizer = cv2.FaceRecognizerSF.create(
            modelPath("face_recognition_sface_2021dec.onnx"),
            "",
        )

        if self.current_raw_frame is None or self.latest_face_data is None:
            return None, None

        try:
            aligned_face = recognizer.alignCrop(self.current_raw_frame, self.latest_face_data)
            embedding = recognizer.feature(aligned_face)
            success, encoded_img = cv2.imencode(".jpg", aligned_face)

            if success:
                return encoded_img.tobytes(), embedding

        except Exception as e:
            print(f"SFace Pipeline Error: {str(e)}")

        return None, None
