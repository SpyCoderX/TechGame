import PyQt6
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from Widgets.Base import Object,Widget
from Utils.Numbers import Loc
from Utils import Images

class Entity(Object):
    def __init__(self,img:QImage):
        super().__init__()
        if img == None:
            img = Images.default()
        self.image = img
        self.__list = None # EntityList that allows deletion of this object.
        self.dir = 0
        self.pos = Loc()
    def setList(self,list:list): # EntityList
        self.__list = list
    def list(self): # EntityList
        if self.__list==None:
            print("Error: Entity of type "+type(self)+" does not have a EntityList registered.")
            return
        return self.__list

    def update(self,screen:Widget):
        list()
        pass

    def render(self,screen:Widget):
        list()
        pass
    def delete(self):
        self.list().remove(self)
        del self