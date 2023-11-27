import PyQt6
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from Widgets.Base import Widget
from Widgets.Game.Camera import Cam
from Widgets.Game.Entity import EntityList
from Widgets.Game.Entity.Player import Player
#imports ^

# BUILT-IN VARIABLES IN GAME

CAMERA_FRICTION_MULTIPLIER = 0.8





class MainGame(Widget):
    """Controls the updating and rendering of Tiles, Entities, and UIs"""

    def __init__(self) -> None:
        super().__init__()
        self.entities = EntityList() # List of every entity in the current level/game.
        self.Player = Player() # Player instance
        self.rScreen = None # Reference to the widget that displays to the window. Allows other objects to write to the widget easily.
        self.camera = Cam(QPointF(0,0)) # Camera for position of all objects. NOTE: SETUP CAMERA BASED ON PLAYER SPAWN LOCATION

    def tick(self,screen:Widget):
        self.rScreen = screen
        self.fill(screen,self.getBrush(QColor(0,0,0,255)))
        self.updates()
        self.renders()
        

    # Main update function
    def updates(self):
        self.tiles_update(self)
        self.entities_update(self)
        self.ui_update(self)
        self.updateCamera()

    def updateCamera(self):
        pos = self.camera.pos()
        pPos = self.Player.pos # Player position
        c = [CAMERA_FRICTION_MULTIPLIER*pos[x]+(1-CAMERA_FRICTION_MULTIPLIER)*pPos[x] for x in range(2)]
        # combines pos and pPos to calculate a new camera position
        self.camera.setPos(c)

    def tiles_update(self):
        pass

    def entities_update(self):
        self.entities.update(self)

    def ui_update(self):
        pass

    def renders(self):
        self.tiles_render(self)
        self.entities_render(self)
        self.ui_render(self)

    def tiles_render(self,screen:Widget):
        pass

    def entities_render(self,screen:Widget):
        self.entities.render(screen)

    def ui_render(self,screen:Widget):
        pass