import sys
import os
from PyQt6 import QtWidgets, uic
import pygame


class Piano(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("piano.ui", self)
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
        self.notes = {
            'do': 'do.wav',
            're': 're.wav',
            'mi': 'mi.wav',
            'fa': 'fa.wav',
            'sol': 'sol.wav',
            'lja': 'lja.wav',
            'si': 'si.wav',
        }

        self.sounds = {}
        for note, filename in self.notes.items():
            sound_file = os.path.join('sounds', filename)
            if os.path.exists(sound_file):self.sounds[note] = pygame.mixer.Sound(sound_file)
        self.cButton.clicked.connect(lambda: self.play_note('do'))
        self.dButton.clicked.connect(lambda: self.play_note('re'))
        self.eButton.clicked.connect(lambda: self.play_note('mi'))
        self.fButton.clicked.connect(lambda: self.play_note('fa'))
        self.gButton.clicked.connect(lambda: self.play_note('sol'))
        self.aButton.clicked.connect(lambda: self.play_note('lja'))
        self.bButton.clicked.connect(lambda: self.play_note('si'))

    def play_note(self, note):
        if note in self.sounds:self.sounds[note].play()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Piano()
    window.show()
    sys.exit(app.exec())