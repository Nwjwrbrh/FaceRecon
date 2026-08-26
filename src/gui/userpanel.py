from camera.livecam import LiveCam
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class UserPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.live = LiveCam()
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
