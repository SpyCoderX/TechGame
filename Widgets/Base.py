import PyQt6
from typing import overload
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
class Object:
    def __init__(self):
        self.instanced=True
        
    
    
    def getBrush(self,A:QColor|None=None,B=None):
        if A == None:
            return QBrush()
        if B == None:
            return QBrush(A)
        return QBrush(A,B)
    
    def getPainter(self,a0:QPaintDevice):
        return QPainter(a0)
    
    
    
    
    def fill(self,a0:QPaintDevice,a1:QBrush):
        painter = self.getPainter(a0)
        rect = QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, a1)
    
class Widget(QWidget,Object):
    def __init__(self) -> None:
        super().__init__()
        self.__mouse_pos__ = QPoint(0,0)
        self.setMouseTracking(True)
        self.__mousedown = [False,False,False]
    def setMousePos(self,pos:QPoint):
        self.__mouse_pos__ = pos
    def mousePos(self):
        return self.__mouse_pos__
    def mousePressEvent(self, a0: QMouseEvent) -> None:
        if a0.button()==Qt.MouseButton.LeftButton:
            self.__mousedown[0] = True
        elif a0.button()==Qt.MouseButton.MiddleButton:
            self.__mousedown[1] = True
        elif a0.button()==Qt.MouseButton.RightButton:
            self.__mousedown[2] = True
        return super().mousePressEvent(a0)
    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        if a0.button()==Qt.MouseButton.LeftButton:
            self.__mousedown[0] = False
        elif a0.button()==Qt.MouseButton.MiddleButton:
            self.__mousedown[1] = False
        elif a0.button()==Qt.MouseButton.RightButton:
            self.__mousedown[2] = False
        return super().mouseReleaseEvent(a0)
    def getThisPainter(self):
        return self.getPainter(self)
    def fillThis(self,a0:QBrush):
        self.fill(self,a0)
    def mouseButton(self,num):
        return self.__mousedown[num]