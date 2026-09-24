import sqlite3
import sqlite_vec
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from camera.livecam import LiveCam
from datetime import date

class UserPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.live = LiveCam()

        self.layout = QVBoxLayout(self)

        self.status_lbl = QLabel(self)
        self.status_lbl.setObjectName("statusLabel")

        self.status_lbl.setProperty("status", "idle")
        self.status_lbl.setText("Checking")

        self.layout.addStretch()
        self.layout.addWidget(self.live)
        self.layout.addWidget(self.status_lbl)
        self.layout.addStretch()

        self.setStyleSheet("""
    /* --- Base Style for the Status Label --- */
    QLabel#statusLabel {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 18px;
        font-weight: 600;
        padding: 8px 16px;
        qproperty-alignment: 'AlignCenter'; /* Force text centering via CSS */
    }

    /* --- Loading State --- */
    QLabel#statusLabel[status="loading"] {
        color: #454545;
    }

    /* --- Success State --- */
    QLabel#statusLabel[status="success"] {
        color: #a6ff63;
        font-weight: bold;
    }

    /* --- Failure State --- */
    QLabel#statusLabel[status="failure"] {
        color: #FFCDD2;
        font-weight: bold;
    }

    /* --- Idle/Hidden State --- */
    QLabel#statusLabel[status="idle"] {
        background-color: transparent;
        border: none;
    }
""")
        self.check_timer = QTimer(self)
        self.check_timer.timeout.connect(self.CaptureCheck)
        self.check_timer.start(100)

    def update_status(self, state, text):
        """Helper to change properties and force PySide to redraw the CSS stylesheet"""
        self.status_lbl.setProperty("status", state)
        self.status_lbl.setText(text)
        self.status_lbl.style().unpolish(self.status_lbl)
        self.status_lbl.style().polish(self.status_lbl)

    def CaptureCheck(self):
        """This function runs repeatedly via QTimer to scan faces against the DB."""
        # 1. Grab the current frame's embedding from your LiveCam object
        # (Adjust this method name depending on how your LiveCam exposes the current frame/embedding)
        _ , embedding = self.live.get_face_image_and_embedding()



        if embedding is None:
            # No face detected in the frame right now
            self.update_status("idle", "Searching for face o_o ...")
            return


        # 2. Compare current frame embedding against loaded database embeddings

        conn = sqlite3.connect("database.db")
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
        """,
            (embedding,),
        )

        matched_user = cursor.fetchone()

        if matched_user:
            user_id, name, roll_no, distance = matched_user

            if distance < 8.7:
                col_name = date.today().strftime('%Y-%m-%d')
                update_query = f"UPDATE Users SET '{col_name}' = 'Present' WHERE rowid = ?;"
                cursor.execute(update_query, (user_id,))
                conn.commit()
                self.update_status("success", f"Matched with : {name} ( Roll No. : {roll_no} ) , Marked Present *_* ")
            else:
                self.update_status("failure", f"None with this face found in the Database  -_- ")


        # 3. Update the UI visually based on the database check results
