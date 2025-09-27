import sys
import os
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel
from PyQt6.QtGui import QPixmap, QPainter, QImage
from PyQt6.QtCore import Qt


class TransparencyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("slider.ui", self)
        self.openButton.clicked.connect(self.open_image)
        self.alphaSlider.valueChanged.connect(self.update_transparency)

        self.original_pixmap = None

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self,"Выберите изображение","","Изображения (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.original_pixmap = QPixmap(file_path)
            self.update_transparency()

    def update_transparency(self):
        if self.original_pixmap is None:
            return
        alpha_percent = self.alphaSlider.value()
        alpha = alpha_percent / 100.0
        self.alphaLabel.setText(f"Прозрачность: {alpha_percent}%")
        result = QPixmap(self.original_pixmap.size())
        result.fill(Qt.GlobalColor.transparent)
        painter = QPainter(result)
        painter.setOpacity(alpha)
        painter.drawPixmap(0, 0, self.original_pixmap)
        painter.end()
        self.imageLabel.setPixmap(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransparencyApp()
    window.show()
    sys.exit(app.exec())