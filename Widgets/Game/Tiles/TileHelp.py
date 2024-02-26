from Utils.Images import *
from Vars.GLOBAL_VARS import SIZE
from Vars.TileVARS import FILE_PREFIX
import os

# Default / Error texture (scaled)
dflt = default().scaled(SIZE,SIZE)
class TileDict:
    def __init__(self) -> None:
        self.__tiles = {
            "air":"air",
            "darkstone":"darkstone",

        }
        self.__images = {}
        for x in range(256):
            y = bin(x)[2:]
            y = "0"*(8-len(y))+y
            self.__tiles["dark_"+y] = "dark_"+y
    def getTileImg(self,tile:str):
        tile = str(tile)
        Name = self.__tiles.get(tile)
        if Name == None:return self.default(tile)
        Image = self.__images.get(Name)
        if Image == None: self.__images[Name] = self.__findTile(Name); Image = self.__images[Name]
        return Image.scaled(SIZE,SIZE)
    def default(self,tile):
        raise ValueError("Error: Unknown tile \""+str(tile)+"\"")
        return dflt
    def __findTile(self,tile):
        return load(FILE_PREFIX+tile)
    def addEntry(self,tile,tileFileName):
        if self.__tiles.get(tile)==None:
            self.__tiles[tile] = tileFileName
    
class TileRegistry:
    def __init__(self):
        self.__tiles = {}
        self.tileDict = TileDict()
    def register(self,tile):
        self.__tiles[tile.material().getTileName()] = tile
        for dict in tile.genorateTextures():
            self.registerTexture(dict["id"],dict["file"])

    def registerFloorTexture(self,floorID,floorFilename):
        self.tileDict.addEntry(floorID,floorFilename)
    def registerTexture(self,ID,Filename):
        self.tileDict.addEntry(ID,Filename)
    def tile(self,tile):
        tile = str(tile)
        return self.__tiles[tile].clone()
TileReg = TileRegistry()




