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
from Widgets.Game.Tiles.Tile import TileBuilder
from Utils.Images import load
from Utils import Numbers
import math
#imports ^

from Vars.GLOBAL_VARS import PLAYER_SPEED,CAMERA_FRICTION_MULTIPLIER


VIGNETTE = None # Vignette effect (Pronounced Vin-ye-t)


class MainGame(Widget):
    """Controls the updating and rendering of Tiles, Entities, and UIs"""
    vin = False
    def __init__(self) -> None:
        super().__init__()
        self.baseLevel = LevelBuilder((50,50)).setWalls("stone").setFloor("darkstone").build() # LevelLoader("default").level()
        self.overLevel = LevelBuilder((20,20)).setWalls("stone").setFloor("darkstone").build() # LevelLoader("default_over").level()
        self.currentLevel = self.baseLevel
        self.Player = Player(100) # Player instance
        spawn = self.currentLevel.tileMap().spawn()
        self.Player.pos.setAll(spawn[0],spawn[1])
        global VIGNETTE
        
        self.rScreen = None # Reference to the widget that displays to the window. Allows other objects to write to the widget easily.
        self.camera = Cam(self.Player.pos) # Camera for position of all objects. NOTE: SETUP CAMERA BASED ON PLAYER SPAWN LOCATION
        
    def tick(self,screen:Widget):
        if self.rScreen==None:
            global VIGNETTE
            VIGNETTE = load("Vignette").scaled(screen.frameGeometry().size())
        self.rScreen = screen
        self.camera.setSize([self.rScreen.frameGeometry().width(),self.rScreen.frameGeometry().height()])
        self.fill(screen,self.getBrush(QColor(0,0,0,255)))
        self.updates()
        self.renders()
        

    # Main update function
    def updates(self):
        for x in range(len(self.rScreen.key_presses)):
            key = self.rScreen.key_presses.pop(0)
            if key==Qt.Key.Key_G:
                point = Numbers.addPoints(self.rScreen.mousePos(),self.camera.pos())
                tile = self.currentLevel.tileMap().getTile(point.x(),point.y())
                self.currentLevel.tileMap().setTile(TileBuilder(self.currentLevel.tileMap(),"stone",tile.floorID()).light(tile.light()).build(),tile.pos())
            if key==Qt.Key.Key_Z:
                self.vin = not self.vin
            if key==Qt.Key.Key_T:
                point = Numbers.addPoints(self.rScreen.mousePos(),self.camera.pos())
                tile = self.currentLevel.tileMap().getTile(point.x(),point.y())
                self.currentLevel.tileMap().setTile(TileBuilder(self.currentLevel.tileMap(),"air",tile.floorID()).light(tile.light()).build(),tile.pos())
            if key==Qt.Key.Key_Y:
                point = Numbers.addPoints(self.rScreen.mousePos(),self.camera.pos())
                tile = self.currentLevel.tileMap().getTile(point.x(),point.y())
                tile.setLight(0)
                self.currentLevel.tileMap().setTile(tile,tile.pos())
            if key==Qt.Key.Key_H:
                point = Numbers.addPoints(self.rScreen.mousePos(),self.camera.pos())
                tile = self.currentLevel.tileMap().getTile(point.x(),point.y())
                tile.setLight(1)
                self.currentLevel.tileMap().setTile(tile,tile.pos())
        self.currentLevel.update(self)
        self.updatePlayer()
        self.ui_update()
        self.updateCamera()

    def updatePlayer(self):
        # Get player input 
        horizontal = self.rScreen.keys["d"]-self.rScreen.keys["a"]
        vertical = self.rScreen.keys["s"]-self.rScreen.keys["w"]

        # Update player acceleration
        self.Player.acceleration.setAll(horizontal*PLAYER_SPEED,vertical*PLAYER_SPEED)

        # Grab camera position
        p1 = self.camera.pos()
        # Convert from Loc() to list
        p1 = [p1.x(),p1.y()]
        # Grab Player position
        p2 = self.Player.pos.getList()
        # Grab mouse position
        p3 = self.rScreen.mousePos()
        # Convert from Loc() to list
        p3 = [p3.x(),p3.y()]
        # Calculate player position on screen
        p2 = [p2[0]-p1[0],p2[1]-p1[1]]
        # Calculate direction from player to mouse
        r = math.atan2(p3[1]-p2[1],p3[0]-p2[0])
        # Set player rotation
        self.Player.pos.R=math.degrees(r)
        # Update Player
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
        self.vignette()
        self.ui_render(self)

    def vignette(self):
        if self.vin: return
        p:QPainter = self.rScreen.getThisPainter()
        p.drawImage(QPoint(0,0),VIGNETTE)

    def ui_render(self,screen:Widget):
        pass