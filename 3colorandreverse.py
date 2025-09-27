import sys
import os
import numpy as np
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtGui import QImage, QPixmap, QTransform
from PyQt6.QtCore import Qt


class ImageEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("image.ui", self)
        self.actionRed.triggered.connect(lambda: self.apply_channel(0))
        self.actionGreen.triggered.connect(lambda: self.apply_channel(1))
        self.actionBlue.triggered.connect(lambda: self.apply_channel(2))
        self.actionOriginal.triggered.connect(self.show_original)
        self.actionRotateLeft.triggered.connect(lambda: self.rotate_image(-90))
        self.actionRotateRight.triggered.connect(lambda: self.rotate_image(90))
        self.original_image = None
        self.current_image = None
        self.is_loaded = False
        self.load_initial_image()

    def load_initial_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self,"Выберите квадратное изображение","","Изображения (*.png *.jpg *.jpeg *.bmp)")
        if not file_path:
            sys.exit(0)
        self.load_image(file_path)

    def load_image(self, file_path):
        image = QImage(file_path)
        if image.isNull():
            QMessageBox.critical(self, "Не удалось загрузить изображение.")
            sys.exit(1)
            return
        self.original_image = image.copy()
        self.current_image = image.copy()
        self.is_loaded = True
        self.display_image(self.current_image)

    def display_image(self, qimage):
        pixmap = QPixmap.fromImage(qimage)
        self.imageLabel.setPixmap(pixmap.scaled(
            self.imageLabel.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))

    def apply_channel(self, channel_idx):
        if not self.is_loaded:
            return
        img = self.original_image.convertToFormat(QImage.Format.Format_RGB888)
        w, h = img.width(), img.height()
        ptr = img.bits()
        ptr.setsize(img.sizeInBytes())
        arr = np.frombuffer(ptr, np.uint8).reshape((h, w, 3)).copy()
        if channel_idx == 0:
            arr[:, :, 1] = 0
            arr[:, :, 2] = 0
        elif channel_idx == 1:
            arr[:, :, 0] = 0
            arr[:, :, 2] = 0
        elif channel_idx == 2:
            arr[:, :, 0] = 0 
            arr[:, :, 1] = 0  
        new_img = QImage(arr.data, w, h, 3 * w, QImage.Format.Format_RGB888)
        new_img = new_img.copy()
        self.current_image = new_img
        self.display_image(self.current_image)

    def show_original(self):
        if self.is_loaded:
            self.current_image = self.original_image.copy()
            self.display_image(self.current_image)

    def rotate_image(self, degrees):
        if not self.is_loaded:
             return
        transform = QTransform().rotate(degrees)
        rotated = self.current_image.transformed(transform, Qt.TransformationMode.SmoothTransformation)
        self.current_image = rotated
        self.display_image(self.current_image)

    def resizeEvent(self, event):
        if self.is_loaded:
            self.display_image(self.current_image)
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageEditor()
    window.show()
    sys.exit(app.exec())