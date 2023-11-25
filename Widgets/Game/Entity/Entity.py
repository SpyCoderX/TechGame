import PyQt6
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from Widgets.Base import Object
from Utils.Numbers import Loc
class Entity(Object):
    def __init__(self,img:QImage,):
        super().__init__()
        self.image = img
        self.dir = 0
        self.pos = Loc()