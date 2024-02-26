from .TileHelp import TileReg
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from Utils.Numbers import centerImage,distFromPoint,distFromList,cnvrtLstToQPntF
from Vars.TileVARS import *
from Vars.GLOBAL_VARS import SIZE
import math
import random
from enum import Enum
from Widgets.Game.Item.Item import Item,MATERIALS,PickaxeMaterial


# Tile - The basis of the tile-map system. 
class Tile:
    __material = MATERIALS.AIR
    __floorMaterial = MATERIALS.AIR
    __mining_damage = 0 # Damage from mining
    def __init__(self,tilemap,material,floorMaterial) -> None:
        """A Tile object, the basis of the Tile system."""
        

        # Set Tile ID and Floor ID.
        if material != None:
            self.__material = material # Tile ID, default is "air".

        if floorMaterial != None:
            self.__floorMaterial = floorMaterial # Floor ID, default is "air".

        # Position in the TileMap
        self.__pos = (0,0) 
        


        # Collision Status
        self.__collisionStatus = NO_COLLISION 

        # Connection Mode and Connections
        self.__tile_connection_mode = NO_CONNECTION
        self.__tile_connections = "0000" # Which tiles are the same type around this tile (top,right,bottom,left)

        # Light Level, and Light Connections
        self.__light_level = 0 # Light Level
        self.__lightConnections = "00000000" # Light Connections (Starting above the tile, and going in a circle around)

        # TileMap object
        self.__LIST = tilemap

        # Game
        self.game = None

        # Setup textures
        self.__icon = TileReg.tileDict.getTileImg("air")
        self.__floorIcon =  TileReg.tileDict.getTileImg(str(self.__floorMaterial))
        self.__lightIcon = TileReg.tileDict.getTileImg("air")

        # Texture mode, used to prevent texture calculation errors while initating Tiles.
        self.___TexMode = False

    # Set Light Level
    def setLight(self,light):
        self.__light_level = light
        self.fixLight(self.lightConnections())

    def fixLight(self,s=""):
        if s!=self.lightConnections():
            self.__lightIcon = TileReg.tileDict.getTileImg("dark_"+self.lightConnections())

    # Mining
    def applyMine(self,game):
        if distFromPoint(self.gPos(),game.Player.pos)>200: return
        tool = game.Player.getTool()
        if tool==None:
            return
        mat = tool.getMaterial()
        if isinstance(mat,PickaxeMaterial):
            self.setMiningDamage(self.miningDamage()+tool.getMiningDamage())
            game.Player.mine()
            if self.miningDamage()>self.material().getDurability():
                if not self.material().getIndestructible(): self.list().setTile(TileBuilder(self.list(),MATERIALS.AIR,self.floorMaterial()).light(1).build(),self.pos())
                for drop in self.material().getDrops():
                    i = Item(drop)
                    a = random.uniform(-0.5,0.5)*SIZE
                    b = (random.randint(0,1)-0.5)*SIZE*1.1
                    if random.randint(0,1):
                        i.pos.setAll(self.gPos().x()+a,self.gPos().y()+b)
                    else:
                        i.pos.setAll(self.gPos().x()+b,self.gPos().y()+a)
                    game.currentLevel.entitylist().add_entity(i)
                self.setMiningDamage(0)
    def miningDamage(self):
        return self.__mining_damage
    def setMiningDamage(self,damage):
        self.__mining_damage = damage
   

    # Get Light Level
    def light(self):
        return self.__light_level
    
    def lightIcon(self):
        return self.__lightIcon
    
    def lightConnections(self):
        return self.__lightConnections
    
    def setLightConnections(self,conns:str):
        old_conns = self.__lightConnections
        self.__lightConnections = conns
        self.fixLight(old_conns)

    # Set Tile Connection Mode
    def setConnectionMode(self,mode):
        self.__tile_connection_mode = mode
        self.fixTexture()

    # Get Tile Connection Mode
    def connectionMode(self):
        return self.__tile_connection_mode

    # Set Tile Connections
    def setConnections(self,conns:str):
        self.__tile_connections = conns
        self.fixTexture()

    # Get Tile Connections
    def connections(self):
        return self.__tile_connections

    # Get Collision state
    def collision(self):
        return self.__collisionStatus
    

    # Set Collosion state
    def setCollision(self,c:int):
        self.__collisionStatus = c


    # Tile Grid/map position
    def pos(self):
        return self.__pos
    
    # Convert Grid position to global position.
    def gPos(self):
        return QPointF(self.pos()[0]*SIZE,self.pos()[1]*SIZE)


    # Set Tile Grid/map Position
    def setPos(self,pos):
        self.__pos = tuple(pos)


    # Get Material
    def material(self):
        return self.__material

    # Set Material
    def setMaterial(self,material):
        self.__material = material
        self.fixTexture()

    # Fix Base Texture
    def fixTexture(self):
        # Don't try to recalculate the texture while initation the Tile.
        if self.___TexMode==False:return

        # Recalculate the Tile's texture
        self.__icon = TileReg.tileDict.getTileImg(self.__material.getTileName()+("_"+self.connections() if self.connectionMode() else ""))

    # Get Floor Material
    def floorMaterial(self):
        return self.__floorMaterial
    
    # Set Floor ID
    def setFloorMaterial(self,materal):
        self.__floorMaterial = materal
        self.__floorIcon = TileReg.tileDict.getTileImg(self.__floorMaterial)

    # Set TileMap
    def setList(self,list):
        """Set the TileMap of this tile."""
        self.__LIST = list

    # Get TileMap
    def list(self):
        """Get the TileMap of this tile."""
        return self.__LIST




    # Update
    def update(self,game): # This function allows other tiles to do custom ticking, like a torch flickering, or a camera looking at the player.
        self.game = game
        if self.___TexMode==False:
            self.___TexMode = True
            self.fixTexture()
        if game.Player.breaking_tile!=self:
            self.setMiningDamage(0)
    

    # Rendering code
    def render(self,game):
        oldPos = self.pos()
        camPos = game.camera.pos()
        ppos = game.Player.pos.subtractPoint(camPos)
        mpos = game.rScreen.mousePos()
        camPos = [camPos.x(),camPos.y()]
        pos = [oldPos[x]*SIZE-camPos[x] for x in range(2)]
        if self.light()==1:
            fIcon = self.iconFloor() # Floor Icon
            game.rScreen.getThisPainter().drawImage(centerImage(QPointF(pos[0],pos[1]),fIcon),fIcon)
            if self.material()!=MATERIALS.AIR:
                icon = self.icon()
                game.rScreen.getThisPainter().drawImage(centerImage(QPointF(pos[0],pos[1]),icon),icon)
            if self.lightConnections()!="00000000":
                eIcon = self.__lightIcon
                game.rScreen.getThisPainter().drawImage(centerImage(QPointF(pos[0],pos[1]),eIcon),eIcon)
        if pos[0]-SIZE/2<mpos.x()<pos[0]+SIZE/2 and pos[1]-SIZE/2<mpos.y()<pos[1]+SIZE/2 and distFromPoint(cnvrtLstToQPntF(pos),ppos)<=200:
            paint:QPainter = game.rScreen.getThisPainter()
            paint.setPen(QColor(0,0,0,0))
            paint.setBrush(QColor(255,255,255,30))
            paint.drawRect(QRectF(QPointF(pos[0]-SIZE/2,pos[1]-SIZE/2),QSizeF(SIZE,SIZE)))
            if self.miningDamage()>0:
                paint.setBrush(QColor(255,255,255,100))
                paint.setRenderHint(QPainter.RenderHint.Antialiasing)
                paint.drawPie(QRectF(QPointF(pos[0]-SIZE*.4,pos[1]-SIZE*.4),QSizeF(SIZE*.8,SIZE*.8)),int((-(self.miningDamage()/self.material().getDurability())*180+90)*16),int(((self.miningDamage()/self.material().getDurability())*360)*16))
    
    # Allow some tiles to have an overlay to prevent tiles clipping.
    def getOverlay(self,game):
        return None
    
    

    def icon(self):
        return self.__icon
    
    def iconFloor(self):
        return self.__floorIcon
    
    # Create a new tile of the same data as this tile.
    def copy(self):
        t:Tile = TileBuilder(self.list(),self.material(),self.floorMaterial()).light(self.light()).build()
        t.setPos(self.pos())
        t.setConnections(self.connections())
        return t
    
    # Create a copy of this object, with the same ID, FloorID, and LIST. Prevents errors that arrise from circular references.
    def clone(self):
        return self.__class__(self.list(),self.material(),self.floorMaterial())
    
    # Returns a generator for IDs and Textures for this tile.
    def genorateTextures(self):
        if self.connectionMode():
            

            
            for x in range(16):
                y = bin(x)[2:]
                y = "0"*(4-len(y))+y
                v = self.material().getTileName()+"_"+y
                yield {"id":v,"file":v}
        else:
            yield {"id":self.material().getTileName(),"file":self.material().getTileName()}

    
class Solid(Tile):
    def __init__(self, tilemap,material, floorMaterial) -> None:
        super().__init__(tilemap,material, floorMaterial)
        self.setCollision(SOLID)
        self.setConnectionMode(CONNECTIONS)
class SolidNoConnect(Tile):
    def __init__(self, tilemap,material, floorMaterial) -> None:
        super().__init__(tilemap,material, floorMaterial)
        self.setCollision(SOLID)
class TileBuilder:
    def __init__(self,tilemap,id,floor) -> None:
        self.__id = id
        self.__floor = floor
        self.__tilemap = tilemap
        self.__light = None

    def light(self,val:int):
        self.__light = val
        return self
    def build(self):
        # Add code for custom tiles, like the "stair" tile.
        tile = TileReg.tile(self.__id.getTileName())
        tile.setList(self.__tilemap)
        tile.setFloorMaterial(self.__floor)
        if self.__light!=None:
            tile.setLight(self.__light)
        # if self.__coll!=None:
        #     tile.setCollision(self.__coll)
        
        return tile
