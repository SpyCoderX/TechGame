import PyQt6
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from Widgets import Ticker,Screen,Base
class BaseW(QMainWindow,Base.Widget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Parallel Processing")
        screen = Screen.Screen()
        self.cscreen = screen
        self.setCentralWidget(self.cscreen)
        self.resize(screen.size())
        self.setWindowState(Qt.WindowState.WindowMaximized)
        self.center()
        self.timer = Ticker.Ticker(self)
        self.old_size = self.size()
    def center(self):
        """centers the window on the screen"""

        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        self.cscreen.setMousePos(a0.position().toPoint())
        return super().mouseMoveEvent(a0)
    def timerEvent(self, a0: QTimerEvent) -> None:
        if self.size()!=self.old_size:
            self.cscreen.events.append({"type":"SizeChange","size":self.size(),"oldSize":self.old_size})
        self.cscreen.update()
        self.old_size = self.size()
    def keyPressEvent(self, a0: QKeyEvent) -> None:
        self.cscreen.events.append({"type":"Keydown","key":a0.key()})
    def keyReleaseEvent(self, a0: QKeyEvent) -> None:
        self.cscreen.events.append({"type":"Keyup","key":a0.key()})
    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        self.cscreen.events.append({"type":"Scroll","val":a0.angleDelta()})
    
    