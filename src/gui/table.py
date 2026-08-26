import sys , os
import sqlite3
import numpy as np
import cv2
from PySide6.QtCore import Qt, QSize,QByteArray
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView, QStyledItemDelegate
from PySide6.QtGui import QPixmap, QImage 
from PySide6.QtSql import QSqlDatabase, QSqlTableModel
from datetime import datetime


class ImageDelegate(QStyledItemDelegate):

    def __init__(self, parent=None, thumb_width=80, thumb_height=80):

        super().__init__(parent)
        self.thumb_size = QSize(thumb_width, thumb_height)

    def paint(self, painter, option, index):
        raw_value = index.data(Qt.ItemDataRole.DisplayRole)
        if hasattr(raw_value, "toByteArray"):
            blob_data = raw_value.toByteArray().data()
        elif hasattr(raw_value, "data"):
            blob_data = raw_value.data()
        else:
            blob_data = raw_value

        if blob_data and isinstance(blob_data, (bytes, bytearray, QByteArray)):
            image = QImage.fromData(blob_data)
            if not image.isNull():
                pixmap = QPixmap.fromImage(image)
                scaled_pixmap = pixmap.scaled(
                    self.thumb_size, 
                    Qt.AspectRatioMode.KeepAspectRatio, 
                    Qt.TransformationMode.SmoothTransformation
                )

                x = option.rect.x() + (option.rect.width() - scaled_pixmap.width()) // 2
                y = option.rect.y() + (option.rect.height() - scaled_pixmap.height()) // 2
                
                painter.drawPixmap(x, y, scaled_pixmap)
                return 
        super().paint(painter, option, index)

    def sizeHint(self, option, index):
        return self.thumb_size



class DatabaseTableView(QTableView):

    def __init__(self, db_path="college_club.db", table_name="club", image_column_index=0, parent=None):

        super().__init__(parent)
        
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(db_path)
        if not self.db.open():
            print("Fatal Error: Could not connect QSqlDatabase.")
            sys.exit(1)


        self.model = QSqlTableModel(self, self.db)
        self.model.setTable(table_name)
        self.model.select() 
        self.setModel(self.model)
       

        self.image_delegate = ImageDelegate(self, thumb_width=80, thumb_height=80)
        self.setItemDelegateForColumn(image_column_index, self.image_delegate)
        
        self.setColumnHidden(4, True) 

        
        self.setStyleSheet("""
            QTableView::item {
            padding: 20px 15px;  
            font-size: 14px;     
        }""")    
        
        self.verticalHeader().setDefaultSectionSize(85) 
        self.setColumnWidth(0, 220)  
        self.setColumnWidth(1, 250)  
        self.setColumnWidth(2, 250) 
        self.setColumnWidth(3, 250)
        self.setColumnWidth(5, 250)     
        #self.horizontalHeader().setStretchLastSection(True)
        self.setAlternatingRowColors(True)




def setup_mock_database():
    """Creates a temporary DB and populates it using a local image file."""
    conn = sqlite3.connect("college_club.db")
    cursor = conn.cursor()
    
    # Create the table schema
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS club (
        Image BLOB NOT NULL,
        RollNo INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        Department TEXT NOT NULL,
        embedding BLOB NOT NULL,
        Status TEXT NOT NULL,
        Timestamp TEXT NOT NULL
    )
""")

    
    # 1. Try to read your real "img.jpg" file as raw binary bytes
    image_path = "/home/abhijit71/Desktop/FaceRecon/saved_align2.jpg"
    
    if os.path.exists(image_path):
        with open(image_path, 'rb') as file:
            mock_blob = file.read()
        print(f"Successfully loaded '{image_path}' for database population.")
    else:
        # Fallback placeholder if 'img.jpg' is missing from the directory
        print(f"Warning: '{image_path}' not found! Creating a fallback placeholder image instead.")
        img = np.zeros((150, 150, 3), dtype=np.uint8)
        cv2.circle(img, (75, 75), 50, (0, 255, 0), -1)  # Green circle
        _, encoded_img = cv2.imencode('.jpg', img)
        mock_blob = encoded_img.tobytes()

    # 2. Insert fake entries if the table is completely empty
    cursor.execute("SELECT COUNT(*) FROM club")
    time = datetime.now().strftime("%H:%M:%S")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO club VALUES (?, ?, ?, ?,?,?,?)", (mock_blob,100000000000000, "Alice Smith", "Computer Science",mock_blob,"Present",time))
        cursor.execute("INSERT INTO club VALUES (?, ?, ?, ?,?,?,?)", (mock_blob , 200000000000000, "Bob Jones", "Electrical Eng", mock_blob , "Absent",time))
        cursor.execute("INSERT INTO club VALUES (?, ?, ?, ?,?,?,?)", (mock_blob,300000000000000, "Alice Smith", "Computer Science",mock_blob,"Present",time))
        cursor.execute("INSERT INTO club VALUES (?, ?, ?, ?,?,?,?)", (mock_blob , 400000000000000, "Bob Jones", "Electrical Eng", mock_blob , "Absent",time))
        cursor.execute("INSERT INTO club VALUES (?, ?, ?, ?,?,?,?)", (mock_blob,500000000000000, "Alice Smith", "Computer Science",mock_blob,"Present",time))
        cursor.execute("INSERT INTO club VALUES (?, ?, ?, ?,?,?,?)", (mock_blob , 600000000000000, "Bob Jones", "Electrical Eng", mock_blob , "Absent",time))
        conn.commit()
        print("Demo database populated with initial records.")
        
    conn.close()


# ==========================================
# 4. RUNNABLE APPLICATION MAIN ENTRY
# ==========================================
if __name__ == "__main__":
    setup_mock_database()  # Prepare data

    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Club Database Manager")
    window.resize(600, 400)

    # Initialize our custom View
    # (Pass DB File, Table Name, and the 0-based column index of your image BLOB)
    table_view = DatabaseTableView(
        db_path="college_club.db", 
        table_name="club", 
        image_column_index=0
    )

    window.setCentralWidget(table_view)
    window.show()
    sys.exit(app.exec())
