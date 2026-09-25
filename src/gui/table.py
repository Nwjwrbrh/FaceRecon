import sys

from utils import dataPath

from PySide6.QtCore import QByteArray, QSize, Qt
from PySide6.QtGui import QImage, QPixmap , QColor
from PySide6.QtSql import QSqlDatabase, QSqlTableModel
from PySide6.QtWidgets import QStyledItemDelegate, QTableView , QHeaderView , QStyle



class ImageDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, thumb_width=80, thumb_height=80):
        super().__init__(parent)
        self.thumb_size = QSize(thumb_width, thumb_height)

    def paint(self, painter, option, index):
        raw_value = index.data(Qt.ItemDataRole.DisplayRole)

        blob_data = None
        if isinstance(raw_value, (bytes, bytearray)):
            blob_data = raw_value
        elif isinstance(raw_value, QByteArray):
            blob_data = raw_value.data()
        elif hasattr(raw_value, "toByteArray"):
            blob_data = raw_value.toByteArray().data()
        elif hasattr(raw_value, "data"):
            blob_data = raw_value.data()

        if isinstance(blob_data, memoryview):
            blob_data = blob_data.tobytes()

        if blob_data:
            image = QImage.fromData(blob_data)
            if not image.isNull():
                painter.save()
                style = (option.widget.style())
                style.drawPrimitive(
                    QStyle.PrimitiveElement.PE_PanelItemViewItem,
                    option,
                    painter,
                    option.widget,
                )
                pixmap = QPixmap.fromImage(image)
                scaled_pixmap = pixmap.scaled(
                    self.thumb_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                x = (
                    option.rect.x()
                    + (option.rect.width() - scaled_pixmap.width()) // 2
                )
                y = (
                    option.rect.y()
                    + (option.rect.height() - scaled_pixmap.height()) // 2
                )
                painter.drawPixmap(x, y, scaled_pixmap)
                painter.restore()
                return
        super().paint(painter, option, index)

    def sizeHint(self, option, index):
        return QSize(self.thumb_size.width() + 10, self.thumb_size.height() + 10)




class StatusHighlightDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        text = str(index.data(Qt.ItemDataRole.DisplayRole) or "")
        if text.strip().lower() == "absent":
            painter.save()
            option.palette.setColor(option.palette.ColorRole.Text, QColor("#FFCDD2"))
            painter.restore()
        if text.strip().lower() == "present":
            painter.save()
            option.palette.setColor(option.palette.ColorRole.Text, QColor("#a6ff63"))
            painter.restore()
        super().paint(painter, option, index)




class ReadOnlySqlModel(QSqlTableModel):
    def flags(self, index):
        return super().flags(index) & ~Qt.ItemIsEditable




class DatabaseTableView(QTableView):
    def __init__(
        self,
        table_name="Users",
        image_column_index=1,
        parent=None,
    ):

        super().__init__(parent)
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(dataPath("database.db"))
        if not self.db.open():
            print("Fatal Error: Could not connect QSqlDatabase.")
            sys.exit(1)
        self.model = ReadOnlySqlModel(self, self.db)
        self.model.setTable(table_name)
        self.model.select()
        self.setModel(self.model)

        self.image_delegate = ImageDelegate(self, thumb_width=80, thumb_height=80)
        self.setItemDelegateForColumn(image_column_index, self.image_delegate)
        self.status_delegate = StatusHighlightDelegate(self)
        self.setItemDelegate(self.status_delegate)

        self.setColumnHidden(0, True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setDefaultSectionSize(85)
        self.setAlternatingRowColors(True)


    def refreshdb(self):
        self.model.select()
