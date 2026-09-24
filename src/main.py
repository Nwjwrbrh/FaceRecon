import sys

from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication

from gui.window import MainWindow
from db.initializer import dbInitializer

if __name__ == "__main__":
    app = QApplication(sys.argv)

    path = "database.db"
    dbInitializer(path)

    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor("#181818"))
    dark_palette.setColor(QPalette.ColorRole.WindowText, QColor("#ffffff"))
    dark_palette.setColor(QPalette.ColorRole.Base, QColor("#181818"))
    app.setPalette(dark_palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())