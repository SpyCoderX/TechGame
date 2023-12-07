from .TileHelp import TileDictionary
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from Utils.Numbers import centerImage
from .TileVARS import *



# Tile - The basis of the tile-map system. 
class Tile:
    __id = "air"
    __floor = "air"
    def __init__(self,id,floor) -> None:
        if id != None:
            self.__id = id # Tile ID, default is "air"
        if floor != None:
            self.__floor = floor
        self.__pos = (0,0) # Position in the TileMap
        self.__icon =  TileDictionary.getTileImg(self.__id) # Icon
        self.__floorIcon =  TileDictionary.getTileImg(self.__floor)
        self.__collisionStatus:int = NO_COLLISION # Collision Status
        self.__tile_connections = "0000" # Which tiles are the same type around this tile (top,right,bottom,left)
        self.__tile_connection_mode = NO_CONNECTION
        self.__light_level = 0 # Light Level

    # Set Light Level
    def setLight(self,light):
        self.__light_level = light

    # Get Light Level
    def light(self):
        return self.__light_level

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
    

    def gPos(self):
        return QPointF(self.pos()[0]*SIZE,self.pos()[1]*SIZE)


    # Set Tile Grid/map Position
    def setPos(self,pos):
        self.__pos = tuple(pos)


    # Get ID
    def ID(self):
        return self.__id

    # Set ID
    def setID(self,ID):
        self.__id = ID
        self.fixTexture()

    # Fix Base Texture
    def fixTexture(self):
        self.__icon = TileDictionary.getTileImg(self.__id+("_"+self.connections() if self.connectionMode() else ""))

    # Get Floor ID
    def floorID(self):
        return self.__floor
    
    # Set Floor ID
    def setFloorID(self,ID):
        self.__floor = ID
        self.__floorIcon = TileDictionary.getTileImg(self.__floor)


    # Update
    def update(self,game): # This function allows other tiles to do custom ticking, like a torch flickering, or a camera looking at the player.
        pass
    

    # Rendering code
    def render(self,game,edge):
        oldPos = self.pos()
        camPos = game.camera.pos()
        camPos = [camPos.x(),camPos.y()]
        pos = [oldPos[x]*SIZE-camPos[x] for x in range(2)]
        
        fIcon = self.iconFloor() # Floor Icon
        game.rScreen.getThisPainter().drawImage(centerImage(QPointF(pos[0],pos[1]),fIcon),fIcon)
        if self.ID()!="air":
            icon = self.icon()
            game.rScreen.getThisPainter().drawImage(centerImage(QPointF(pos[0],pos[1]),icon),icon)
        if edge!="":
            eIcon = TileDictionary.getTileImg("edge_"+edge)
            game.rScreen.getThisPainter().drawImage(centerImage(QPointF(pos[0],pos[1]),eIcon),eIcon)
        
        

    

    def icon(self):
        return self.__icon
    def iconFloor(self):
        return self.__floorIcon
    
    def copy(self):
        t = TileBuilder(self.ID(),self.floorID()).build()
        t.setPos(self.pos())
        return t
    
class Solid(Tile):
    def __init__(self, id, floor) -> None:
        super().__init__(id, floor)
        self.setCollision(SOLID)
        self.setConnectionMode(CONNECTIONS)

    
class TileBuilder:
    def __init__(self,id,floor) -> None:
        self.__id = id
        self.__floor = floor
    def build(self):
        # Add code for custom tiles, like the "stair" tile.
        if self.__id=="stone":
            tile = Solid(self.__id,self.__floor)
        else:
            tile = Tile(self.__id,self.__floor)
        
        # if self.__coll!=None:
        #     tile.setCollision(self.__coll)
        return tile