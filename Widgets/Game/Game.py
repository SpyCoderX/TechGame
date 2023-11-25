import PyQt6
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from Widgets.Base import Widget

class MainGame(Widget):
    def __init__(self) -> None:
        super().__init__()
        #self.Player = Player()
    def tick(self,screen:Widget):
        self.fill(screen,self.getBrush(QColor(0,0,0,255)))
        painter = self.getPainter(screen)
        brush = self.getBrush(QColor(255,255,255,255),Qt.BrushStyle.SolidPattern)
        pen = QPen(Qt.PenStyle.SolidLine)
        pen.setWidthF(5)
        painter.setPen(pen)
        painter.setBrush(brush)
        pos = screen.mousePos()
        painter.drawEllipse(pos,20,20)