import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton, QColorDialog
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush
from PyQt6.QtCore import Qt, QRect
from PyQt6 import uic


class SmileyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.smiley_color = QColor(215, 2, 247)
        self.scale = 1.0

    def set_smiley_color(self, color: QColor):
        self.smiley_color = color
        self.update()

    def set_scale(self, scale_value: int):
        self.scale = scale_value / 100.0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        center = self.rect().center()
        base_size = min(self.width(), self.height()) * 0.6
        size = base_size * self.scale
        face_rect = QRect(int(center.x() - size // 2), int(center.y() - size // 2), int(size), int(size))
        painter.setBrush(QBrush(self.smiley_color))
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        painter.drawEllipse(face_rect)
        eye_size = size * 0.15
        eye_offset = size * 0.25
        painter.setBrush(QBrush(Qt.GlobalColor.black))
        painter.drawEllipse(int(center.x() - eye_offset - eye_size // 2), int(center.y() - eye_size // 2), int(eye_size), int(eye_size))
        painter.drawEllipse(int(center.x() + eye_offset - eye_size // 2), int(center.y() - eye_size // 2), int(eye_size),int(eye_size))
        mouth_rect = QRect(int(center.x() - size * 0.3), int(center.y() + size * 0.1), int(size * 0.6), int(size * 0.4))
        painter.setPen(QPen(Qt.GlobalColor.black, 3))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawArc(mouth_rect, 0, -360 * 16)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('smile.ui', self)
        self.smiley_view = SmileyWidget()
        layout = self.verticalLayout
        placeholder = self.placeholder
        layout.replaceWidget(placeholder, self.smiley_view)
        placeholder.deleteLater()
        self.scaleSlider.valueChanged.connect(self.smiley_view.set_scale)
        self.colorButton.clicked.connect(self.choose_color)

    def choose_color(self):
        color = QColorDialog.getColor(self.smiley_view.smiley_color,self,"Выберите цвет смайлика")
        if color.isValid():
            self.smiley_view.set_smiley_color(color)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())