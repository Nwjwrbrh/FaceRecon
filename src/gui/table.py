import sys

from PySide6.QtCore import QByteArray, QSize, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtSql import QSqlDatabase, QSqlTableModel
from PySide6.QtWidgets import QStyledItemDelegate, QTableView


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
                    Qt.TransformationMode.SmoothTransformation,
                )

                x = option.rect.x() + (option.rect.width() - scaled_pixmap.width()) // 2
                y = (
                    option.rect.y()
                    + (option.rect.height() - scaled_pixmap.height()) // 2
                )

                painter.drawPixmap(x, y, scaled_pixmap)
                return
        super().paint(painter, option, index)

    def sizeHint(self, option, index):
        return self.thumb_size


class DatabaseTableView(QTableView):
    def __init__(
        self, db_path="records.db", table_name="club", image_column_index=0, parent=None
    ):

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
        # self.horizontalHeader().setStretchLastSection(True)
        self.setAlternatingRowColors(True)

    def refreshdb(self):
        self.model.select()
