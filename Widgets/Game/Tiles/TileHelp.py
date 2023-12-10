from Utils.Images import *
from Vars.GLOBAL_VARS import SIZE
import os

# Default / Error texture (scaled)
dflt = default().scaled(SIZE,SIZE)
class TileDict:
    def __init__(self) -> None:
        self.__tiles = {
            "air":"Air",
            "darkstone":"Darkstone",
            "stone_0000":"Stone-0000",
            "stone_0001":"Stone-0001",
            "stone_0010":"Stone-0010",
            "stone_0011":"Stone-0011",
            "stone_0100":"Stone-0100",
            "stone_0101":"Stone-0101",
            "stone_0110":"Stone-0110",
            "stone_0111":"Stone-0111",
            "stone_1000":"Stone-1000",
            "stone_1001":"Stone-1001",
            "stone_1010":"Stone-1010",
            "stone_1011":"Stone-1011",
            "stone_1100":"Stone-1100",
            "stone_1101":"Stone-1101",
            "stone_1110":"Stone-1110",
            "stone_1111":"Stone-1111"
        }
        self.__images = {}
        for x in range(256):
            y = bin(x)[2:]
            y = "0"*(8-len(y))+y
            self.__tiles["dark_"+y] = "Dark_"+y
    def getTileImg(self,tile:str):
        Name = self.__tiles.get(tile)
        if Name == None:return self.default(tile)
        Image = self.__images.get(Name)
        if Image == None: self.__images[Name] = self.__findTile(Name); Image = self.__images[Name]
        return Image.scaled(SIZE,SIZE)
    def default(self,tile):
        print("Error: Unknown tile \""+tile+"\"")
        return dflt
    def __findTile(self,tile):
        return load("Tile_"+tile)
    
    
TileDictionary = TileDict()




