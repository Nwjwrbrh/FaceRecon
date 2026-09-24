import sys

from PySide6.QtCore import QByteArray, QSize, Qt
from PySide6.QtGui import QImage, QPixmap , QColor
from PySide6.QtSql import QSqlDatabase, QSqlTableModel
from PySide6.QtWidgets import QStyledItemDelegate, QTableView , QHeaderView , QSizePolicy


from PySide6.QtCore import QByteArray, QSize, Qt 
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QStyle, QStyledItemDelegate


class ImageDelegate(QStyledItemDelegate):

    def __init__(self, parent=None, thumb_width=80, thumb_height=80):
        super().__init__(parent)
        self.thumb_size = QSize(thumb_width, thumb_height)

    def paint(self, painter, option, index):
        # 1. Fetch raw value from model
        raw_value = index.data(Qt.ItemDataRole.DisplayRole)

        # 2. Safely extract raw bytes from PySide/PyQt wrappers
        blob_data = None
        if isinstance(raw_value, (bytes, bytearray)):
            blob_data = raw_value
        elif isinstance(raw_value, QByteArray):
            blob_data = raw_value.data()
        elif hasattr(raw_value, "toByteArray"):  # Older PyQt QVariant wrapper
            blob_data = raw_value.toByteArray().data()
        elif hasattr(raw_value, "data"):
            blob_data = raw_value.data()

        # Handle memoryview objects returned by some SQLite drivers
        if isinstance(blob_data, memoryview):
            blob_data = blob_data.tobytes()

        # 3. Try parsing image from bytes
        if blob_data:
            image = QImage.fromData(blob_data)
            if not image.isNull():
                painter.save()

                # Draw selection/background highlight so selected rows render correctly
                style = (
                    option.widget.style()
                )
                style.drawPrimitive(
                    QStyle.PrimitiveElement.PE_PanelItemViewItem,
                    option,
                    painter,
                    option.widget,
                )

                # Scale and center pixmap
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

        # Fallback to default delegate only if blob_data is empty or invalid
        super().paint(painter, option, index)

    def sizeHint(self, option, index):
        # Add 10px padding around the thumbnail so table cell borders don't clip the image
        return QSize(self.thumb_size.width() + 10, self.thumb_size.height() + 10)


class StatusHighlightDelegate(QStyledItemDelegate):

    def paint(self, painter, option, index):
        # Fetch display value
        text = str(index.data(Qt.ItemDataRole.DisplayRole) or "")

        # Check if cell contains "Absent"
        if text.strip().lower() == "absent":
            painter.save()
            # Draw light red background
            #painter.fillRect(option.rect, QColor("#FFCDD2"))
            option.palette.setColor(
                option.palette.ColorRole.Text, QColor("#FFCDD2")
            )
            painter.restore()

        if text.strip().lower() == "present":
            painter.save()
            # Draw light red background
            #painter.fillRect(option.rect, QColor("#a6ff63"))
            option.palette.setColor(
                option.palette.ColorRole.Text, QColor("#a6ff63")
            )
            painter.restore()

        # Call default painting (draws standard text, selection highlight, etc.)
        super().paint(painter, option, index)


class ReadOnlySqlModel(QSqlTableModel):
    def flags(self, index):
        return super().flags(index) & ~Qt.ItemIsEditable


class DatabaseTableView(QTableView):
    def __init__(
        self,
        db_path="database.db",
        table_name="Users",
        image_column_index=1,
        parent=None,
    ):

        super().__init__(parent)

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(db_path)
        if not self.db.open():
            print("Fatal Error: Could not connect QSqlDatabase.")
            sys.exit(1)

        self.model = ReadOnlySqlModel(self, self.db)
        self.model.setTable(table_name)
        self.model.select()
        self.setModel(self.model)

        self.image_delegate = ImageDelegate(self, thumb_width=80, thumb_height=80)
        self.setItemDelegateForColumn(image_column_index, self.image_delegate)

        # Apply status highlight delegate to ALL columns by default
        self.status_delegate = StatusHighlightDelegate(self)
        self.setItemDelegate(self.status_delegate)

        self.setColumnHidden(0, True)
        self.setSelectionMode(QTableView.SelectionMode.NoSelection)
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )


        # ---------- COLUMN SIZE ----------
        header = self.horizontalHeader()

        # All columns have equal width
        header.setSectionResizeMode(QHeaderView.Stretch)

       
        self.verticalHeader().setDefaultSectionSize(85)
        
        self.setAlternatingRowColors(True)

    def refreshdb(self):
        self.model.select()
