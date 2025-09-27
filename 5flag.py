import sys
import random
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt6.QtGui import QColor, QBrush, QPen 
from PyQt6.QtCore import Qt
from PyQt6 import uic


class FlagGenerator(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('flag.ui', self)
        self.pushButton.clicked.connect(self.generate_flag)

    def generate_flag(self):
        num_stripes = self.spinBox.value()
        if num_stripes <= 0:
            return
        self.flag_window = FlagDisplayWindow(num_stripes)
        self.flag_window.show()

class FlagDisplayWindow(QDialog):
    def __init__(self, num_stripes):
        super().__init__()
        self.setWindowTitle("Флаг")
        self.resize(400, 300)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        layout.addWidget(self.view)
        self.draw_flag(num_stripes)

    def draw_flag(self, num_stripes):
        width = 400
        height = 300
        stripe_height = height / num_stripes
        self.scene.clear()
        self.scene.setSceneRect(0, 0, width, height)
        for i in range(num_stripes):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            color = QColor(r, g, b)
            rect = QGraphicsRectItem(0, i * stripe_height, width, stripe_height)
            rect.setBrush(QBrush(color))
            rect.setPen(QPen(Qt.PenStyle.NoPen))
            self.scene.addItem(rect)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = FlagGenerator()
    dialog.show()
    sys.exit(app.exec())