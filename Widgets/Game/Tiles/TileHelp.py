from Utils.Images import *
from .TileVARS import *
class TileDict:
    def __init__(self) -> None:
        self.__tiles = {
            "air":self.__findTile("Air"),
            "stone":self.__findTile("Stone"),
            "darkstone":self.__findTile("Darkstone")
        }
    def getTileImg(self,tile):
        a = self.__tiles.get(tile).scaled(SIZE,SIZE)
        if a == None: return default().scaled(SIZE,SIZE)
        return a
    def __findTile(self,tile):
        return load("Tile_"+tile)
    
TileDictionary = TileDict()


