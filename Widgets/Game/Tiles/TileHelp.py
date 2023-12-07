from Utils.Images import *
from .TileVARS import *

# Default / Error texture (scaled)
dflt = default().scaled(SIZE,SIZE)
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
            "edge_BottomRight":self.__findTile("Dark-BottomRight"),
            "stone_0000":self.__findTile("Stone-0000"),
            "stone_0001":self.__findTile("Stone-0001"),
            "stone_0010":self.__findTile("Stone-0010"),
            "stone_0011":self.__findTile("Stone-0011"),
            "stone_0100":self.__findTile("Stone-0100"),
            "stone_0101":self.__findTile("Stone-0101"),
            "stone_0110":self.__findTile("Stone-0110"),
            "stone_0111":self.__findTile("Stone-0111"),
            "stone_1000":self.__findTile("Stone-1000"),
            "stone_1001":self.__findTile("Stone-1001"),
            "stone_1010":self.__findTile("Stone-1010"),
            "stone_1011":self.__findTile("Stone-1011"),
            "stone_1100":self.__findTile("Stone-1100"),
            "stone_1101":self.__findTile("Stone-1101"),
            "stone_1110":self.__findTile("Stone-1110"),
            "stone_1111":self.__findTile("Stone-1111")
        }
    def getTileImg(self,tile):
        a = self.__tiles.get(tile)
        if a == None: return self.default(tile)
        return a
    def default(self,tile):
        print("Error: Unknown tile \""+tile+"\"")
        return dflt
    def __findTile(self,tile):
        return load("Tile_"+tile).scaled(SIZE,SIZE)
    
TileDictionary = TileDict()




