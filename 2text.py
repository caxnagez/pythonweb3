import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QTextEdit
from PyQt6.QtCore import Qt

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("text.ui", self)
        self.action_new.triggered.connect(self.new_file)
        self.action_open.triggered.connect(self.open_file)
        self.action_save.triggered.connect(self.save_file)
        self.current_file = None
        self.textEdit.textChanged.connect(self.on_text_changed)
        self.modified = False

    def on_text_changed(self):
        self.modified = True

    def new_file(self):
        if self.check_unsaved_changes():
            self.textEdit.clear()
            self.current_file = None  
            self.modified = False
            self.setWindowTitle("Новый файл")

    def open_file(self):
        if not self.check_unsaved_changes():
            return
        file_path, _ = QFileDialog.getOpenFileName(self,"Открыть файл","","Текстовые файлы (*.txt);;Все файлы (*)")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.textEdit.setPlainText(content)
                self.current_file = file_path
                self.modified = False
                self.setWindowTitle(f"{file_path} - Текстовый редактор")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл:\n{str(e)}")

    def save_file(self):
        if self.current_file:
            self._save_to_file(self.current_file)
        else:
            self.save_as()

    def save_as(self):
        file_path, _ = QFileDialog.getSaveFileName(self,"Сохранить файл как","", "Текстовые файлы (*.txt);;Все файлы (*)")
        if file_path:
            self._save_to_file(file_path)
            self.current_file = file_path
            self.setWindowTitle(f"{file_path} Редактор")

    def _save_to_file(self, file_path):
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.textEdit.toPlainText())
            self.modified = False
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл:\n{str(e)}")

    def check_unsaved_changes(self):
        if self.modified:
            reply = QMessageBox.question(
                self,"Файл был изменён. Сохранить изменения?", QMessageBox.StandardButton.Save |QMessageBox.StandardButton.Discard |QMessageBox.StandardButton.Cancel)
            if reply == QMessageBox.StandardButton.Save:
                self.save_file()
                return not self.modified
            elif reply == QMessageBox.StandardButton.Cancel:
                return False
        return True

    def closeEvent(self, event):
        if self.check_unsaved_changes():
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec())