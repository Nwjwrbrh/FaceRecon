from utils import dataPath
import sqlite3
from datetime import date

from utils import resourcePath

from PySide6.QtCore import Qt , QSize
from PySide6.QtGui import QMovie , QTransform
from PySide6.QtWidgets import QVBoxLayout , QGridLayout
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget



class GIFButtonWidget(QPushButton): 
    def __init__(self, parent=None):
        super().__init__("Launch FaceRecon ", parent)
        self.setFixedSize(360, 60)
        self.setStyleSheet("""
        QPushButton {
            text-align: left; 
            color:#1e1e1e;            
            font-size: 18px;           
            font-weight: bold;
            background-color: #daff78;
            border-radius: 12px;
            padding-left: 32px;
        }
        QPushButton:hover {
                background-color: #e6ffa4;
        }
        QLabel{
                padding-top:10px; 
                padding-bottom:10px;
        }
        """)

        self.gif_label = QLabel(self)
        self.gif_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.movie = QMovie(resourcePath("startArrow.gif"))
        self.rotation_angle = -90
        self.movie.frameChanged.connect(self.apply_rotation)
        self.movie.start()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()
        layout.addWidget(self.gif_label)

    def apply_rotation(self):
        current_pixmap = self.movie.currentPixmap()
        if not current_pixmap.isNull():
            transform = QTransform().rotate(self.rotation_angle)
            rotated_pixmap = current_pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation)
            self.gif_label.setPixmap(rotated_pixmap)



class GIFPlayer(QWidget):
    def __init__(self, width: int, height: int, path : str , parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  
        self.gif_label = QLabel(self)
        self.gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.gif_label)

        self.loader_gif = QMovie(path)
        self.loader_gif.setScaledSize(QSize(width, height))
        self.gif_label.setMovie(self.loader_gif)
        self.loader_gif.start()

    


class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        content_layout = QVBoxLayout(self)
        content_layout.setContentsMargins(10, 15, 15, 5)
        content_layout.setSpacing(25)

        rowOne_layout = QHBoxLayout()
        GIFPlayback = GIFPlayer(512,512,resourcePath("launchyourself.gif"))
        rowOne_layout.addWidget(GIFPlayback, alignment=Qt.AlignCenter)
  
        rowTwo_layout = QGridLayout()
        self.startButton = GIFButtonWidget()
        rowTwo_layout.addWidget(self.startButton, 0, 0, Qt.AlignCenter)

        content_layout.addStretch()
        content_layout.addLayout(rowOne_layout)
        content_layout.addLayout(rowTwo_layout)
        content_layout.addStretch()


    def attendanceInit(self):
        conn = sqlite3.connect(dataPath("database.db"))
        cursor = conn.cursor()
        column_name = date.today().strftime('%Y-%m-%d')
        
        try:
            query = f"ALTER TABLE Users ADD COLUMN '{column_name}' TEXT DEFAULT 'Absent';"
            cursor.execute(query)
        except sqlite3.OperationalError:
            pass

        conn.commit()
        conn.close()