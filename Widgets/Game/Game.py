import PyQt6
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from Widgets.Base import Widget
from Widgets.Game.Camera import Cam
from Widgets.Game.Entity import EntityList
from Widgets.Game.Entity.More.BaseEnemy import BaseEnemy
from Widgets.Game.Entity.Player import Player
from Widgets.Game.Level import LevelLoader,Level,LevelBuilder
from Widgets.Game.Tiles.Tile import TileBuilder,Tile,Solid,SolidNoConnect
from Widgets.Game.Tiles.TileHelp import TileReg
from Widgets.Game.Menus.MenuBases import PlayerInventoryGUI
from Widgets.Game.Item.Item import MATERIALS,ItemStack,Item,PickaxeMaterial,BlockMaterial,WeaponMaterial,ToolMaterial
from Vars.GLOBAL_VARS import GUI_SCALE
from Utils.Images import load
from Utils import Numbers
import math
from .Menu import ScreenController
from .Particle.Particle import ParticleList
#imports ^

from Vars.GLOBAL_VARS import PLAYER_SPEED,CAMERA_FRICTION_MULTIPLIER


VIGNETTE = None # Vignette effect (Pronounced Vin-ye-t)

TileReg.register(Solid(None,MATERIALS.STONE,MATERIALS.AIR))
TileReg.register(Tile(None,MATERIALS.AIR,MATERIALS.AIR))
TileReg.register(SolidNoConnect(None,MATERIALS.OAK_LOG,MATERIALS.AIR))


class MainGame(ScreenController):
    """Controls the updating and rendering of Tiles, Entities, and UIs"""
    __PlayerInvGui = None
    def __init__(self,screen) -> None:
        super().__init__(screen)
        self.baseLevel = LevelBuilder((50,50)).setWalls(MATERIALS.STONE).setFloor(MATERIALS.DARKSTONE).build() # LevelLoader("default").level()
        self.overLevel = LevelBuilder((20,20)).setWalls(MATERIALS.STONE).setFloor(MATERIALS.DARKSTONE).build() # LevelLoader("default_over").level()
        self.currentLevel = self.baseLevel
        self.Player = Player(100) # Player instance
        spawn = self.currentLevel.tileMap().spawn()
        self.Player.pos.setAll(spawn[0],spawn[1])
        self.camera = Cam(self.Player.pos) # Camera for position of all objects. NOTE: SETUP CAMERA BASED ON PLAYER SPAWN LOCATION
        self.playerMovement = {"Horizontal":0,"Vertical":0}
        self.particles = ParticleList()
        
        self.Player.inventory.setToolStack(0,ItemStack(MATERIALS.STICK_SWORD,1))
        self.Player.inventory.setToolStack(1,ItemStack(MATERIALS.STONE_PICK,1))
        self.Player.inventory.set(0,ItemStack(MATERIALS.OAK_LOG,16))
        self.Player.inventory.set(1,ItemStack(MATERIALS.STONE,16))


    def tick(self,screen:Widget):
        self.camera.setSize([self.rScreen.frameGeometry().width(),self.rScreen.frameGeometry().height()])
        super().tick(screen)
    

    def handleEvent(self,event):
        if event["type"]=="Keydown":
            key = event["key"]
            if key==Qt.Key.Key_Escape:
                if self.__PlayerInvGui:
                    self.GUIs.removeWidget(self.__PlayerInvGui)
                    self.__PlayerInvGui = None
            if key==Qt.Key.Key_W:
                self.playerMovement["Vertical"] -= 1
            if key==Qt.Key.Key_S:
                self.playerMovement["Vertical"] += 1
            if key==Qt.Key.Key_A:
                self.playerMovement["Horizontal"] -= 1
            if key==Qt.Key.Key_D:
                self.playerMovement["Horizontal"] += 1


            if key==Qt.Key.Key_G:
                point = Numbers.addPoints(self.rScreen.mousePos(),self.camera.pos())
                tile = self.currentLevel.tileMap().getTile(point.x(),point.y())
                self.currentLevel.tileMap().setTile(TileBuilder(self.currentLevel.tileMap(),MATERIALS.OAK_LOG,tile.floorMaterial()).light(tile.light()).build(),tile.pos())
            if key==Qt.Key.Key_Z:
                self.vin = not self.vin
            if key==Qt.Key.Key_T:
                point = Numbers.addPoints(self.rScreen.mousePos(),self.camera.pos())
                tile = self.currentLevel.tileMap().getTile(point.x(),point.y())
                self.currentLevel.tileMap().setTile(TileBuilder(self.currentLevel.tileMap(),MATERIALS.AIR,tile.floorMaterial()).light(tile.light()).build(),tile.pos())
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
            if key == Qt.Key.Key_U:
                base = BaseEnemy(load("enemy").scaled(64,64),20)
                base.ABBox = [64,64]
                mpos = self.rScreen.mousePos()
                base.pos.setAll(mpos.x()+self.camera.pos().x(),mpos.y()+self.camera.pos().y())
                base.setTarget(self.Player)
                self.currentLevel.entitylist().add_entity(base)
            if key == Qt.Key.Key_E:
                if self.__PlayerInvGui:
                    self.__PlayerInvGui.remove()
                    self.__PlayerInvGui = None
                else:
                    self.__PlayerInvGui = PlayerInventoryGUI(self.Player.inventory,self)
                    self.GUIs.addWidget(self.__PlayerInvGui)
            


        if event["type"]=="Keyup":
            key = event["key"]

            if key==Qt.Key.Key_W:
                self.playerMovement["Vertical"] += 1
            if key==Qt.Key.Key_S:
                self.playerMovement["Vertical"] -= 1
            if key==Qt.Key.Key_A:
                self.playerMovement["Horizontal"] += 1
            if key==Qt.Key.Key_D:
                self.playerMovement["Horizontal"] -= 1
        if event["type"]=="Scroll":
            self.Player.scrollSlot(event["val"])
        super().handleEvent(event)

    # Main update function
    def updates(self):
        if not self.__PlayerInvGui:
            self.currentLevel.update(self)
            self.updatePlayer()
            self.particles.update(self)
            self.updateCamera()
        super().updates()

    def updatePlayer(self):
        # Get player input 
        val = PLAYER_SPEED*(0.4 if self.Player.isSwinging() else 1)
        horizontal = self.playerMovement["Horizontal"]
        vertical = self.playerMovement["Vertical"]

        # Update player acceleration
        self.Player.acceleration.setAll(horizontal*val,vertical*val)

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
        r1 = [math.cos(r),math.sin(r)]
        r2 = [math.cos(math.radians(self.Player.pos.R)),math.sin(math.radians(self.Player.pos.R))]
        val = 0.05 if self.Player.isSwinging() else 0.2
        r3 = [r1[x]*val+r2[x]*(1-val) for x in range(2)]
        # Set player rotation
        self.Player.pos.R=math.degrees(math.atan2(r3[1],r3[0]))
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
    
    
    def renders(self):
        self.currentLevel.render(self)
        self.Player.render(self)
        self.particles.render(self)
        super().renders()
        self.overlay()
    def overlay(self):
        p = self.rScreen.getThisPainter()
        p.setPen(QColor(255,255,255,255))
        p.drawText(10,(self.rScreen.height()-20),100,30,0,"v1.0 - Tech-Game")
        p.drawText(self.rScreen.width()-130,(self.rScreen.height()-120),130,120,0,"Keys:\n├[WASD] - Movement\n├[Y/H] - Darkness\n├[T/G] - Block\n├[U] - Spawn Entity\n├[Z] - Toggle Vignette\n└[Left Click] - Sword")
        p.drawImage(QRectF(Numbers.centerImage(QPointF(self.rScreen.width()*0.3,self.rScreen.height()-PLAYER_TOOL_OVERLAY_IMAGE.height()/2),PLAYER_TOOL_OVERLAY_IMAGE),QSizeF(PLAYER_TOOL_OVERLAY_IMAGE.size())),PLAYER_TOOL_OVERLAY_IMAGE)
        p.drawImage(QRectF(Numbers.centerImage(QPointF(self.rScreen.width()*0.6,self.rScreen.height()-PLAYER_INV_OVERLAY_IMAGE.height()/2),PLAYER_INV_OVERLAY_IMAGE),QSizeF(PLAYER_INV_OVERLAY_IMAGE.size())),PLAYER_INV_OVERLAY_IMAGE)
        if self.Player.selected_slot<2:
            p.drawImage(QRectF(Numbers.centerImage(QPointF(self.rScreen.width()*0.3-40+self.Player.selected_slot*80,self.rScreen.height()-PLAYER_TOOL_OVERLAY_IMAGE.height()/2),PLAYER_HOVER_OVERLAY_IMAGE),QSizeF(PLAYER_HOVER_OVERLAY_IMAGE.size())),PLAYER_HOVER_OVERLAY_IMAGE)
        else:
            p.drawImage(QRectF(Numbers.centerImage(QPointF(self.rScreen.width()*0.6-160+(self.Player.selected_slot-2)*80,self.rScreen.height()-PLAYER_INV_OVERLAY_IMAGE.height()/2),PLAYER_HOVER_OVERLAY_IMAGE),QSizeF(PLAYER_HOVER_OVERLAY_IMAGE.size())),PLAYER_HOVER_OVERLAY_IMAGE)
        i = 0
        for tool in self.Player.inventory.toolSlots():
            if tool: tool.render(p,QPointF(self.rScreen.width()*0.3-40+i*80,self.rScreen.height()-PLAYER_TOOL_OVERLAY_IMAGE.height()/2),QSizeF(16,16),0.8)
            i+=1
        i = 0
        for tool in self.Player.inventory.slots()[0:5]:
            if tool: tool.render(p,QPointF(self.rScreen.width()*0.6-160+i*80,self.rScreen.height()-PLAYER_INV_OVERLAY_IMAGE.height()/2),QSizeF(16,16),0.8)
            i+=1
        if self.rScreen.geometry().width()<800 and self.rScreen.geometry().height()<800:
            p.setPen(QColor(255,0,0,255))
            p.scale(4,4)
            p.drawStaticText(int(self.rScreen.width()/16),int(self.rScreen.height()/16),QStaticText("Please fullscreen!"))
            p.scale(0.25,0.25)
            p.drawStaticText(int(self.rScreen.width()/4),int(self.rScreen.height()/2),QStaticText("If this is an error please contact the developer"))
        p.setPen(QColor(255,255,255,255))
        if self.Player.getTool():
            t = QStaticText(self.Player.getTool().getMaterial().getName())
            p.drawStaticText(int(self.rScreen.width()/2-t.size().width()/2),int(self.rScreen.height()-150-t.size().height()/2),t)
            t = QStaticText("[Left Click] to mine a block" if isinstance(self.Player.getTool().getMaterial(),PickaxeMaterial) else "[Right Click] to place" if isinstance(self.Player.getTool().getMaterial(),BlockMaterial) else "[Left Click] to attack" if isinstance(self.Player.getTool().getMaterial(),WeaponMaterial) else "")
            p.drawStaticText(int(self.rScreen.width()/2-t.size().width()/2),int(self.rScreen.height()-130-t.size().height()/2),t)
    def getATileBuilder(self,tilemap,mat,floor_mat):
        return TileBuilder(tilemap,mat,floor_mat)
def scaleBySCALE(image):
    return image.scaled(image.width()*GUI_SCALE,image.height()*GUI_SCALE)
PLAYER_TOOL_OVERLAY_IMAGE = load("PlayerToolOverlay")
PLAYER_TOOL_OVERLAY_IMAGE = scaleBySCALE(PLAYER_TOOL_OVERLAY_IMAGE)
PLAYER_INV_OVERLAY_IMAGE = load("PlayerInvOverlay")
PLAYER_INV_OVERLAY_IMAGE = scaleBySCALE(PLAYER_INV_OVERLAY_IMAGE)
PLAYER_HOVER_OVERLAY_IMAGE = load("Hover")
PLAYER_HOVER_OVERLAY_IMAGE = scaleBySCALE(PLAYER_HOVER_OVERLAY_IMAGE)
