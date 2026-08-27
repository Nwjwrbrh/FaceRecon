from camera.livecam import LiveCam
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
import sqlite3
import numpy as np
from PySide6.QtCore import QTimer


class UserPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.live = LiveCam()
        self.loadEmbeddings()
        # 1. Main layout for this QWidget
        self.layout = QVBoxLayout(self)
        # 1. Create a regular QLabel
        self.status_lbl = QLabel(self)
        self.status_lbl.setObjectName("statusLabel")

# 2. Initialize it to the hidden "idle" state
        self.status_lbl.setProperty("status", "idle")
        self.status_lbl.setText("Checking")

# Drop it into your layout track


        self.layout.addStretch()
        self.layout.addWidget(self.live)
        self.layout.addWidget(self.status_lbl)
        self.layout.addStretch()

        self.setStyleSheet("""
    /* --- Base Style for the Status Label --- */
    QLabel#statusLabel {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
        font-weight: 600;
        border-radius: 6px;
        padding: 8px 16px;
        qproperty-alignment: 'AlignCenter'; /* Force text centering via CSS */
    }

    /* --- Loading State --- */
    QLabel#statusLabel[status="loading"] {
        color: #2563eb;
        background-color: #eff6ff;
        border: 1px solid #bfdbfe;
    }

    /* --- Success State --- */
    QLabel#statusLabel[status="success"] {
        color: #166534;
        background-color: #f0fdf4;
        border: 1px solid #bbf7d0;
        font-weight: bold;
    }

    /* --- Failure State --- */
    QLabel#statusLabel[status="failure"] {
        color: #991b1b;
        background-color: #fef2f2;
        border: 1px solid #fecaca;
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


    def loadEmbeddings(self):
        conn = sqlite3.connect("/home/abhijit71/Desktop/FaceRecon/records.db")
        cursor = conn.cursor()
        cursor.execute("SELECT embedding FROM club;")
        raw_rows = cursor.fetchall()
        print(raw_rows)
        conn.close()

        self.embeddings = []
        for row in raw_rows:
            print(row)
            blob = row[0]
            print(blob)
            if blob:
                # Assuming embeddings were saved using np.save() bytes or similar raw float buffers
                arr = np.frombuffer(blob, dtype=np.float32).flatten()
                self.embeddings.append(arr)
    
    
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
        current_embedding = self.live.get_current_embedding() 
        
        if current_embedding is None:
            # No face detected in the frame right now
            self.update_status("idle", "Searching for face...")
            return

        self.update_status("loading", "Matching with records...")

        # 2. Compare current frame embedding against loaded database embeddings
        match_found = False
        threshold = 0.6 # Adjust this based on your facial model (e.g., Facenet/InsightFace)

        for known_emb in self.known_embeddings:
            # Example using Euclidean distance; switch to Cosine similarity if your model prefers it
            dist = np.linalg.norm(current_embedding - known_emb)
            if dist < threshold:
                match_found = True
                break

        # 3. Update the UI visually based on the database check results
        if match_found:
            self.update_status("success", "Access Granted ✔")
        else:
            self.update_status("failure", "Unknown User ❌")
