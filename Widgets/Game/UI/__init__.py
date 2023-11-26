import PyQt6
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from Widgets.Base import Widget

class UIList:
    def __init__(self) -> None:
        self.__ui = None
    def update(self,screen):
        if self.__ui!=None:
            self.__ui.update(screen)
    def render(self,screen):
        if self.__ui!=None:
            self.__ui.render(screen)
    def get_ui(self):
        return self.__ui
    def set_ui(self,ui):
        self.__ui = ui
    def clear_ui(self):
        self.__ui = None

class UI(Widget):
    def __init__(self) -> None:
        super().__init__()
    def update(self, screen:Widget):
        pass
    def render(self,screen:Widget):
        pass