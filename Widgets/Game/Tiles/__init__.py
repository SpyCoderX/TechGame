from .Tile import Tile,TileBuilder
from Utils.Images import load,default
import math
from PyQt6.QtCore import QRect, QPoint,QPointF
from typing import List
from .TileVARS import SIZE
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

class TileMap:
    def __init__(self,sizew,sizeh) -> None:
        self.__TILES = [[Tile("air","air") for y in range(sizew)] for x in range(sizeh)]
        self.__spawn = (math.ceil(sizew/2)-1,math.ceil(sizeh/2)-1)

    def setSpawn(self,pos):
        self.__spawn = tuple(pos)

    def spawn(self):
        return self.__spawn
        
    
    def update(self,game):
        r = self.getShownRect(game)
        for y in range(r[0][1],r[1][1]):
            for x in range(r[0][0],r[1][0]):
                self.tile(x,y).update(game)
        
        
    def render(self,game):
        r = self.getShownRect(game)
        for y in range(r[0][1],r[1][1]):
            for x in range(r[0][0],r[1][0]):
                self.tile(x,y).render(game)
        for y in range(r[0][1],r[1][1]):
            for x in range(r[0][0],r[1][0]):
                self.tile(x,y).overlay(game)

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
        self.__TILES = tiles

    def tiles(self):
        return self.__TILES
    
    def setTile(self,tile,pos):
        tile.setPos(pos)
        self.__TILES[pos[1]][pos[0]] = tile

    def tile(self,x,y):
        return self.__TILES[y][x]
    
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
        start = [max(min(start[0],len(self.__TILES[0])-1),0),max(min(start[1],len(self.__TILES)-1),0)]
        sPos = game.camera.size() # Camera Size
        sPos = [sPos[0]+Pos[0],sPos[1]+Pos[1]]
        end = [math.ceil(sPos[x]/SIZE) for x in range(2)]
        end = [max(min(end[0],len(self.__TILES[0])-1),0),max(min(end[1],len(self.__TILES)-1),0)]
        return [[start[0],start[1]],[end[0],end[1]]]




