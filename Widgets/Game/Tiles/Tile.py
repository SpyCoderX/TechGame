from .TileHelp import TileDictionary
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from Utils.Numbers import centerImage
from .TileVARS import *
from Vars.GLOBAL_VARS import SIZE



# Tile - The basis of the tile-map system. 
class Tile:
    __id = "air"
    __floor = "air"
    def __init__(self,tilemap,id,floor="air") -> None:
        """A Tile object, the basis of the Tile system."""

        # Set Tile ID and Floor ID.
        if id != None:
            self.__id = id # Tile ID, default is "air".

        if floor != None:
            self.__floor = floor # Floor ID, default is "air".

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

        # Setup textures
        self.__icon = TileDictionary.getTileImg("air")
        self.__floorIcon =  TileDictionary.getTileImg(self.__floor)
        self.__lightIcon = TileDictionary.getTileImg("air")

        # Texture mode, used to prevent texture calculation errors while initating Tiles.
        self.___TexMode = False

    # Set Light Level
    def setLight(self,light):
        self.__light_level = light
        self.fixLight(self.lightConnections())

    def fixLight(self,s=""):
        if s!=self.lightConnections():
            self.__lightIcon = TileDictionary.getTileImg("dark_"+self.lightConnections())

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


    # Get ID
    def ID(self):
        return self.__id

    # Set ID
    def setID(self,ID):
        self.__id = ID
        self.fixTexture()

    # Fix Base Texture
    def fixTexture(self):
        # Don't try to recalculate the texture while initation the Tile.
        if self.___TexMode==False:return

        # Recalculate the Tile's texture
        self.__icon = TileDictionary.getTileImg(self.__id+("_"+self.connections() if self.connectionMode() else ""))

    # Get Floor ID
    def floorID(self):
        return self.__floor
    
    # Set Floor ID
    def setFloorID(self,ID):
        self.__floor = ID
        self.__floorIcon = TileDictionary.getTileImg(self.__floor)

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
        if self.___TexMode==False:
            self.___TexMode = True
            self.fixTexture()
    

    # Rendering code
    def render(self,game):
        oldPos = self.pos()
        camPos = game.camera.pos()
        camPos = [camPos.x(),camPos.y()]
        pos = [oldPos[x]*SIZE-camPos[x] for x in range(2)]
        if self.light()==1:
            fIcon = self.iconFloor() # Floor Icon
            game.rScreen.getThisPainter().drawImage(centerImage(QPointF(pos[0],pos[1]),fIcon),fIcon)
            if self.ID()!="air":
                icon = self.icon()
                game.rScreen.getThisPainter().drawImage(centerImage(QPointF(pos[0],pos[1]),icon),icon)
            if self.lightConnections()!="00000000":
                eIcon = self.__lightIcon
                game.rScreen.getThisPainter().drawImage(centerImage(QPointF(pos[0],pos[1]),eIcon),eIcon)

    # Allow some tiles to have an overlay to prevent tiles clipping.
    def getOverlay(self,game):
        return None
    
    

    def icon(self):
        return self.__icon
    
    def iconFloor(self):
        return self.__floorIcon
    
    # Create a new tile of the same data as this tile.
    def copy(self):
        t = TileBuilder(self.list(),self.ID(),self.floorID()).build()
        t.setPos(self.pos())
        t.setConnections(self.connections())
        t.setLight(self.light())
        return t
    
class Solid(Tile):
    def __init__(self, tilemap,id, floor) -> None:
        super().__init__(tilemap,id, floor)
        self.setCollision(SOLID)
        self.setConnectionMode(CONNECTIONS)

    
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
        if self.__id=="stone":
            tile = Solid(self.__tilemap,self.__id,self.__floor)
        else:
            tile = Tile(self.__tilemap,self.__id,self.__floor)
        if self.__light!=None:
            tile.setLight(self.__light)
        # if self.__coll!=None:
        #     tile.setCollision(self.__coll)
        return tile