import PyQt6
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from Widgets.Base import Widget
from Widgets.Game.Entity import EntityList
from Widgets.Game.Entity.Player import Player
#imports ^


class MainGame(Widget):
    """Controls the updating and rendering of Tiles, Entities, and UIs"""

    def __init__(self) -> None:
        super().__init__() # init function
        self.entities = EntityList() # Entitylist, basically a glorified list object
        self.Player = Player() # Player instance, allows the game to function

    def tick(self,screen:Widget):
        self.fill(screen,self.getBrush(QColor(0,0,0,255)))
        self.updates(screen)
        self.renders(screen)
        

    # Main update function
    def updates(self,screen):
        self.tiles_update(screen)
        self.entities_update(screen)
        self.ui_update(screen)

    def tiles_update(self,screen:Widget):
        pass

    def entities_update(self,screen:Widget):
        self.entities.update(screen)

    def ui_update(self,screen:Widget):
        pass

    def render(self,screen):
        self.tiles_render(screen)
        self.entities_render(screen)
        self.ui_render(screen)

    def tiles_render(self,screen:Widget):
        pass

    def entities_render(self,screen:Widget):
        self.entities.render(screen)

    def ui_render(self,screen:Widget):
        pass