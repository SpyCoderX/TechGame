import PyQt6
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from Widgets import Ticker,Screen,Base
class Base(QMainWindow,Base.Widget):
    def __init__(self) -> None:
        super().__init__()
        self.setBaseSize(1200,800)
        self.timer = Ticker.Ticker(self)
        self.setWindowTitle("Widgets App")
        screen = Screen.Screen()
        self.cscreen = screen
        self.setCentralWidget(screen)
        self.resize(screen.size())
        self.center()
    def center(self):
        """centers the window on the screen"""

        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        self.cscreen.setMousePos(a0.position())
        return super().mouseMoveEvent(a0)
    def timerEvent(self, a0: QTimerEvent) -> None:
        self.cscreen.update()