import sys
import os
import math  # <-- добавлено для cos/sin/radians
from PyQt6 import QtWidgets, uic, QtCore, QtGui
from PyQt6.QtGui import QPen, QPainter, QColor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsLineItem, QFileDialog


class LSystemDrawer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('lsys.ui', self)
        self.system_name = ""
        self.angle_divisions = 6
        self.axiom = ""
        self.rules = {}
        self.generations = []
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.openButton.clicked.connect(self.open_lsystem_file)
        self.stepSlider.valueChanged.connect(self.on_slider_changed)

    def open_lsystem_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Открыть L-систему", "", "Текстовые файлы (*.txt);;Все файлы (*)")
        if not file_path:
            return

        try:
            self.load_lsystem(file_path)
            self.generate_up_to(5)
            self.stepSlider.setMaximum(5)
            self.stepSlider.setValue(0)
            self.on_slider_changed(0)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self,"Не удалось загрузить файл:\n{e}")

    def load_lsystem(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]

        if len(lines) < 3:
            raise ValueError("Минимум 3 строки")

        self.system_name = lines[0]
        self.angle_divisions = int(lines[1])
        self.axiom = lines[2]

        self.rules = {}
        for line in lines[3:]:
            if ' ' in line:
                parts = line.split(' ', 1)
                key = parts[0]
                value = parts[1] if len(parts) > 1 else ""
                self.rules[key] = value
            else:
                self.rules[line] = ""

        self.titleLabel.setText(f"Название: {self.system_name}")
        self.generations = [self.axiom]

    def apply_rules(self, sequence):
        return ''.join(self.rules.get(char, char) for char in sequence)

    def generate_up_to(self, max_step):
        while len(self.generations) <= max_step:
            next_seq = self.apply_rules(self.generations[-1])
            self.generations.append(next_seq)

    def draw_lsystem(self, sequence):
        self.scene.clear()
        if not sequence:
            return
        angle_step = 360.0 / self.angle_divisions
        length = 5.0
        x, y = 0.0, 0.0
        angle = 0.0
        stack = []
        pen = QPen(QColor("purple"))
        pen.setWidth(1)
        for command in sequence:
            if command == 'F':
                rad = math.radians(angle)
                x2 = x + length * math.cos(rad)
                y2 = y - length * math.sin(rad)

                line = QGraphicsLineItem(x, y, x2, y2)
                line.setPen(pen)
                self.scene.addItem(line)

                x, y = x2, y2

            elif command == '+':
                angle = (angle + angle_step) % 360
            elif command == '-':
                angle = (angle - angle_step) % 360
            elif command == '[':
                stack.append((x, y, angle))
            elif command == ']':
                if stack:
                    x, y, angle = stack.pop()
        rect = self.scene.itemsBoundingRect()
        if not rect.isEmpty():
            self.scene.setSceneRect(rect)
            self.graphicsView.fitInView(rect, Qt.AspectRatioMode.KeepAspectRatio)
            
    def on_slider_changed(self, value):
        self.stepLabel.setText(f"Шаг: {value}")
        if value >= len(self.generations):
            self.generate_up_to(value)
        seq = self.generations[value]
        self.draw_lsystem(seq)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = LSystemDrawer()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()