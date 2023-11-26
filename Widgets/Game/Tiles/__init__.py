from Widgets.Game.Tiles.Tile import Tile

class TileMap:
    def __init__(self,sizew,sizeh) -> None:
        self.__TILES = [[Tile("Air") for y in sizew] for x in sizeh]