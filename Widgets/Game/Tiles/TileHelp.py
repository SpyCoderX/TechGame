from Utils.Images import *
from .TileVARS import *
class TileDict:
    def __init__(self) -> None:
        self.__tiles = {
            "air":self.__findTile("Air"),
            "stone":self.__findTile("Stone-0000"),
            "darkstone":self.__findTile("Darkstone"),
            "edge_Top":self.__findTile("Dark-Top"),
            "edge_Bottom":self.__findTile("Dark-Bottom"),
            "edge_Left":self.__findTile("Dark-Left"),
            "edge_Right":self.__findTile("Dark-Right"),
            "edge_TopLeft":self.__findTile("Dark-TopLeft"),
            "edge_TopRight":self.__findTile("Dark-TopRight"),
            "edge_BottomLeft":self.__findTile("Dark-BottomLeft"),
            "edge_BottomRight":self.__findTile("Dark-BottomRight")
        }
    def getTileImg(self,tile):
        a = self.__tiles.get(tile)
        if a == None: return default().scaled(SIZE,SIZE)
        return a
    def __findTile(self,tile):
        return load("Tile_"+tile).scaled(SIZE,SIZE)
    
TileDictionary = TileDict()




