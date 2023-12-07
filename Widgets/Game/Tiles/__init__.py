from .Tile import Tile,TileBuilder
from Utils.Images import load,default
import math
from PyQt6.QtCore import QRect, QPoint,QPointF
from typing import List
from .TileVARS import *

import json
import os





def LoadTileMap(name):
    name = "Levels/Level_"+name+".json" # Get file address
    if not os.path.exists("Levels"): # Check if it exists
        os.mkdir("Levels") # if not, make it
    if not os.path.isfile(name): # if file doesn't exist
        tm = TileMap(101,101) # Make it
        tm.setWalls(Tile("Stone","air",[0,0])) # and make some walls
        return tm #return it
    file = open(name)
    json_file = json.load(file)
    spawn = json_file["spawn"]
    map_list = json_file["map"]
    tm = TileMap(len(map_list[0]),len(map_list))
    for y in range(len(map_list)):
        for x in range(len(map_list[0])):
            t = map_list[y][x]
            tm.setTile(TileBuilder(t["id"],t["floor"]).build(),(x,y))
    tm.setSpawn(spawn)
    file.close()
    return tm
    
def SaveTileMap(map,name):
    name = "Levels/Level_"+name+".json" # Get file address
    if not os.path.exists("Levels"): # Check if it exists
        os.mkdir("Levels") # if not, make it
    file = open(name,"w")
    spawn = map.spawn()
    map_list:List[List] = []
    tiles:List[List[Tile]] = map.tiles()
    for y in range(len(tiles)):
        map_list.append([])
        for x in range(len(tiles[0])):
            map_list[y].append({"id":tiles[y][x].ID(),"floor":tiles[y][x].floorID()})

    json.dump({"spawn":spawn,"map":map_list},file)
    file.close()

class TileMap: # An object that holds all tiles.
    def __init__(self,sizew,sizeh) -> None: # Init
        self.__TILES = [[Tile("air","air") for x in range(sizew)] for y in range(sizeh)] # Setup an empty TileMap/list.
        self.__spawn = ((math.ceil(sizew/2)-1)*SIZE,(math.ceil(sizeh/2)-1)*SIZE) # Spawn location for this TileMap.
        self.__updates = [] # Objects to update. (Coming soon)

    # Set Spawn Location
    def setSpawn(self,pos):
        self.__spawn = tuple(pos)

    # Get Spawn Location
    def spawn(self):
        return self.__spawn
        
    # Update all tiles (Coming soon: Update only tiles that need to update.)
    def update(self,game):
        r = self.getShownRect(game)
        for y in range(r[0][1],r[1][1]):
            for x in range(r[0][0],r[1][0]):
                self.tile(x,y).update(game)
        
        
    def render(self,game):
        r = self.getShownRect(game)
        for y in range(r[0][1],r[1][1]):
            for x in range(r[0][0],r[1][0]):
                self.tile(x,y).render(game,self.getEdges(x,y))

    def isOnEdge(self,x,y):
        return (x==0 or x==len(self.__TILES[0])-1) and (y==0 or y==len(self.__TILES)-1) # Add a system for lighting.
    
    def getEdges(self,x,y):
        return ("Top" if y==0 else "Bottom" if y==len(self.__TILES)-1 else "")+("Left" if x==0 else "Right" if x==len(self.__TILES[0])-1 else "")
    
    def setWalls(self,tile):
        for x in range(len(self.__TILES[0])):
            self.setTile(tile.copy(),(x,0))
        for x in range(len(self.__TILES[len(self.__TILES)-1])):
           self.setTile(tile.copy(),(x,len(self.__TILES)-1))
        for y in range(len(self.__TILES)):
            self.setTile(tile.copy(),(0,y))
        for y in range(len(self.__TILES)):
            self.setTile(tile.copy(),(len(self.__TILES)-1,y))

    def setTiles(self,tiles:List[List[Tile]]):
        sx = len(tiles[0])
        sy = len(tiles)
        self.__TILES = [[Tile("air","air") for x in range(sx)] for y in range(sy)] # Setup an empty TileMap/list.
        for y in range(sy):
            for x in range(sx):
                self.setTile(tiles[y][x])

    def tiles(self):
        return self.__TILES
    
    def isInRange(self,x,y):
        return 0<=x<len(self.__TILES[0]) and 0<=y<len(self.__TILES)

    def setTile(self,tile,pos):
        if not self.isInRange(pos[0],pos[1]): print("Error: Unable to set tile out of bounds."); return
        tile.setPos(pos)
        self.__TILES[pos[1]][pos[0]] = tile

        # Fix the set tile.
        self.fixTile(pos[0],pos[1])
        
        # Fix the surrounding tiles.
        self.fixTile(pos[0],pos[1]-1) # Top
        self.fixTile(pos[0]+1,pos[1]) # Right
        self.fixTile(pos[0],pos[1]+1) # Bottom
        self.fixTile(pos[0]-1,pos[1]) # Left
    
    # Fix the tile connections for the selected tile.
    def fixTile(self,x,y):
        tile = self.tile(x,y)
        if self.tile(x,y).connectionMode()==NO_CONNECTION:
            return
        conns = ""
        conns += "1" if self.tileConnection(x,y-1,tile) else "0" # Top
        conns += "1" if self.tileConnection(x+1,y,tile) else "0" # Right
        conns += "1" if self.tileConnection(x,y+1,tile) else "0" # Bottom
        conns += "1" if self.tileConnection(x-1,y,tile) else "0" # Left
        tile.setConnections(conns)

    # Check if the tile at x,y connects to the tile
    def tileConnection(self,x,y,tile):
        t = self.tile(x,y)
        return tile.connectionMode()==CONNECTIONS and t.ID()==tile.ID() and t.connectionMode()==CONNECTIONS
    def tile(self,x,y): # Gets a tile using the coords of Tiles in the list.
        if self.isInRange(x,y):
            return self.__TILES[y][x]
        else:
            t = Tile("air","air")
            t.setLight(0)
            return Tile("air","air")
    
    def getTile(self,x,y) -> Tile: # gets a tile using global coords.
        return self.tile(round(x/SIZE),round(y/SIZE))
    
    def toTilePos(self,x,y):
        return [round(x/SIZE),round(y/SIZE)]
    
    def fill(self,tile):
        for y in range(len(self.__TILES)):
            for x in range(len(self.__TILES[0])):
                self.setTile(tile,(x,y))
    
    def fillFloor(self,floor_ID):
        for y in range(len(self.__TILES)):
            for x in range(len(self.__TILES[0])):
                t = self.__TILES[y][x]
                t.setFloorID(floor_ID)
                self.setTile(t,(x,y))

    
    def getShownRect(self,game) -> QRect:
        """Calculating the tiles that are on screen, \n
        which are the tiles between the camera position \n
        and the camera position + camera size."""
        cPos:QPointF = game.camera.pos() # Camera Position
        Pos = [cPos.x(),cPos.y()]
        start = [math.floor(Pos[x]/SIZE) for x in range(2)]
        start = [max(min(start[0],len(self.__TILES[0])),0),max(min(start[1],len(self.__TILES)),0)]
        sPos = game.camera.size() # Camera Size
        sPos = [sPos[0]+Pos[0],sPos[1]+Pos[1]]
        end = [math.ceil(sPos[x]/SIZE+1) for x in range(2)]
        end = [max(min(end[0],len(self.__TILES[0])),0),max(min(end[1],len(self.__TILES)),0)]
        return [[start[0],start[1]],[end[0],end[1]]]





