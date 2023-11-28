from PyQt6.QtCore import *
from PyQt6.QtGui import *

class Cam:
    def __init__(self,pos:QPointF) -> None:
        self.__pos = pos
        self.__size = [64,64]
    
    def setPos(self,pos:QPointF):
        self.__pos = QPointF(pos.x(),pos.y())

    def pos(self):
        return self.__pos
    
    def setSize(self,size):
        self.__size = size
        
    def size(self):
        return self.__size