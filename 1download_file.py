import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("downloadfile.ui", self)
        self.load_button.clicked.connect(self.load_file)
        self.save_button.clicked.connect(self.save_file)
        self.results = {}

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите текстовый файл", "", "Text Files (*.txt)"
        )
        if not file_path:
            return
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = file.read()
                numbers = []
                for word in data.split():
                    try:
                        numbers.append(int(word))
                    except ValueError:
                        QMessageBox.critical(self, "Ошибка", f"Неверный формат данных: '{word}'")
                        return
                if not numbers:
                    QMessageBox.warning(self, "Ошибка", "Файл пуст")
                    return
                self.results = {
                    'min': min(numbers),
                    'max': max(numbers),
                    'avg': sum(numbers) / len(numbers)
                }
                self.min_label.setText(f"Минимум: {self.results['min']}")
                self.max_label.setText(f"Максимум: {self.results['max']}")
                self.avg_label.setText(f"Среднее: {self.results['avg']:.2f}")
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка чтения файла", f"Ошибка: {str(e)}")

    def save_file(self):
        if not self.results:
            QMessageBox.warning(self, "Предупреждение", "Нет данных для сохранения")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить результаты", "", "Text Files (*.txt)"
        )
        if not file_path:
            return
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(
                    f"Минимальное значение: {self.results['min']}\n"
                    f"Максимальное значение: {self.results['max']}\n"
                    f"Среднее значение: {self.results['avg']:.2f}\n"
                )
            QMessageBox.information(self, "Файл успешно сохранен")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка сохранения", f"Ошибка: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())