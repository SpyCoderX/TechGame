import PyQt6
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from Widgets.Base import Object,Widget
from Utils.Numbers import Loc
class Entity(Object):
    def __init__(self,img:QImage):
        super().__init__()
        self.image = img
        self.__list = None # EntityList that 
        self.dir = 0
        self.pos = Loc()
    def setList(self,list):
        self.__list = list
    def list(self):
        return self.__list

    def update(self,screen:Widget):
        if self.__list==None:
            print("Error: Entity does not have a EntityList registered.")
            return
        pass

    def render(self,screen:Widget):
        if self.__list==None:
            print("Error: Entity does not have a EntityList registered.")
            return
        pass