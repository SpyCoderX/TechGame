import PyQt6
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from Widgets.Base import Widget
from Widgets.Game.Camera import Cam
from Widgets.Game.Entity import EntityList
from Widgets.Game.Entity.Player import Player
from Widgets.Game.Level import LevelLoader,Level,LevelBuilder
from Utils.Numbers import cnvrtLstToQPntF
import math
#imports ^

# BUILT-IN VARIABLES IN GAME

CAMERA_FRICTION_MULTIPLIER = 0.8
PLAYER_SPEED = 5




class MainGame(Widget):
    """Controls the updating and rendering of Tiles, Entities, and UIs"""

    def __init__(self) -> None:
        super().__init__()
        self.baseLevel = LevelBuilder((50,50)).setWalls("stone").setFloor("darkstone").build() # LevelLoader("default").level()
        self.overLevel = LevelBuilder((20,20)).setWalls("stone").setFloor("stone").build() # LevelLoader("default_over").level()
        self.currentLevel = self.baseLevel
        self.Player = Player(100) # Player instance
        spawn = self.currentLevel.tileMap().spawn()
        self.Player.pos.setAll(spawn[0],spawn[1])
        
        self.rScreen = None # Reference to the widget that displays to the window. Allows other objects to write to the widget easily.
        self.camera = Cam(self.Player.pos) # Camera for position of all objects. NOTE: SETUP CAMERA BASED ON PLAYER SPAWN LOCATION
        
    def tick(self,screen:Widget):
        self.rScreen = screen
        self.camera.setSize([self.rScreen.frameGeometry().width(),self.rScreen.frameGeometry().height()])
        self.fill(screen,self.getBrush(QColor(0,0,0,255)))
        self.updates()
        self.renders()
        

    # Main update function
    def updates(self):
        self.currentLevel.update(self)
        self.updatePlayer()
        self.ui_update()
        self.updateCamera()

    def updatePlayer(self):
        horizontal = self.rScreen.keys["d"]-self.rScreen.keys["a"]
        vertical = self.rScreen.keys["s"]-self.rScreen.keys["w"]
        self.Player.acceleration.setAll(horizontal,vertical)
        p1 = self.camera.pos()
        p1 = [p1.x(),p1.y()]
        p2 = self.Player.pos.getList()
        p3 = self.rScreen.mousePos()
        p3 = [p3.x(),p3.y()]
        p2 = [p2[0]-p1[0],p2[1]-p1[1]]
        r = math.atan2(p3[1]-p2[1],p3[0]-p2[0])
        self.Player.pos.R=math.degrees(r)
        self.Player.update(self)
    def updateCamera(self):
        pos = self.camera.pos()
        size = self.camera.size()
        pos = [pos.x(),pos.y()]
        pPos = self.Player.pos.getList() # Player position
        pPos = [pPos[0]-size[0]/2,pPos[1]-size[1]/2]
        
        l = [CAMERA_FRICTION_MULTIPLIER*pos[x]+(1-CAMERA_FRICTION_MULTIPLIER)*pPos[x] for x in range(2)] # Do the calculations,
        c = QPointF(l[0],l[1]) # And assign the resulting values to the camera
        # combines pos and pPos to calculate a new camera position
        self.camera.setPos(c)
    
    def ui_update(self):
        pass

    def renders(self):
        self.currentLevel.render(self)
        self.Player.render(self)
        self.ui_render(self)

    def ui_render(self,screen:Widget):
        pass