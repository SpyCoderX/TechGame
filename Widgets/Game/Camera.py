from PyQt6.QtCore import *
from PyQt6.QtGui import *

class Cam:
    def __init__(self,pos:QPointF) -> None:
        self.__pos = pos
    
    def setPos(self,pos:QPointF):
        self.__pos = pos

    def pos(self):
        return self.__pos