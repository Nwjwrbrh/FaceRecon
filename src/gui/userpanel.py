import sqlite3
import sqlite_vec
from datetime import date

from utils import dataPath
from camera.livecam import LiveCam

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class UserPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.live = LiveCam()
        self.status_lbl = QLabel(self)
        self.status_lbl.setObjectName("statusLabel")
        self.status_lbl.setProperty("status", "idle")
        self.status_lbl.setText("Checking")

        self.layout = QVBoxLayout(self)
        self.layout.addStretch()
        self.layout.addWidget(self.live)
        self.layout.addWidget(self.status_lbl)
        self.layout.addStretch()
        self.setStyleSheet("""
        QLabel#statusLabel {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 18px;
                font-weight: 600;
                padding: 8px 16px;
                qproperty-alignment: 'AlignCenter';
        }
        QLabel#statusLabel[status="loading"] {
                color: #454545;
        }
        QLabel#statusLabel[status="success"] {
                color: #a6ff63;
                font-weight: bold;
        }
        QLabel#statusLabel[status="failure"] {
                color: #FFCDD2;
                font-weight: bold;
        }
        QLabel#statusLabel[status="idle"] {
                background-color: transparent;
                border: none;
        }
        """)

        self.check_timer = QTimer(self)
        self.check_timer.timeout.connect(self.CaptureCheck)
        self.check_timer.start(100)



    def update_status(self, state, text):
        self.status_lbl.setProperty("status", state)
        self.status_lbl.setText(text)
        self.status_lbl.style().unpolish(self.status_lbl)
        self.status_lbl.style().polish(self.status_lbl)



    def CaptureCheck(self):
        _ , embedding = self.live.get_face_image_and_embedding()
        if embedding is None:
            self.update_status("idle", "Searching for face o_o ...")
            return

        conn = sqlite3.connect(dataPath("database.db"))
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        conn.enable_load_extension(False)
        cursor = conn.cursor()
        cursor.execute(
        """
        SELECT
            u.rowid,
            u.Name,
            u.RollNo,
            v.distance
        FROM FaceVectors v
        JOIN Users u ON u.rowid = v.rowid
        WHERE v.embedding MATCH ?
          AND k = 1
        ORDER BY v.distance
        """,(embedding))

        matched_user = cursor.fetchone()
        if matched_user:
            user_id, name, roll_no, distance = matched_user
            if distance < 9:
                col_name = date.today().strftime('%Y-%m-%d')
                update_query = f"UPDATE Users SET '{col_name}' = 'Present' WHERE rowid = ?;"
                cursor.execute(update_query, (user_id,))
                conn.commit()
                self.update_status("success", f"Matched with : {name} ( Roll No. : {roll_no} ) , Marked Present *_* ")
            else:
                self.update_status("failure", f"None with this face found in the Database  -_- ")

