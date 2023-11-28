from Utils.Images import *
from .TileVARS import *
class TileDict:
    def __init__(self) -> None:
        self.__tiles = {
            "air":self.__findTile("Air")
        }
    def getTileImg(self,tile):
        a = self.__tiles.get(tile)
        if a == None: return default().scaled(SIZE,SIZE)
        return a
    def __findTile(self,tile):
        return load("Tile_"+tile)
    
TileDictionary = TileDict()


