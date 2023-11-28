from Widgets.Game.Entity import EntityList
from Widgets.Game.Tiles import TileMap,LoadTileMap,Tile,TileBuilder
from typing import Tuple
class Level:
    __TileMap: TileMap
    __Entitylist: EntityList
    def __init__(self,TileMap) -> None:
        self.__Entitylist = EntityList()
        self.__TileMap = TileMap


    def update(self,game):
        self.__TileMap.update(game)
        self.__Entitylist.update(game)

    def render(self,game):
        self.__TileMap.render(game)
        self.__Entitylist.render(game)

    def entitylist(self):
        return self.__Entitylist
    
    def tileMap(self):
        return self.__TileMap
    
class LevelLoader:
    def __init__(self,name) -> None:
        self.__level = Level(LoadTileMap(name))

    def level(self):
        return self.__level
    
class LevelBuilder:
    def __init__(self,size:Tuple[int,int]):
        self.__level = Level(TileMap(size[0],size[1]))
        self.__walls = "air"
        self.__floor = "air"
    def setWalls(self,wallid):
        self.__walls = wallid
        self.__level.tileMap().setWalls(TileBuilder(self.__walls,self.__floor).build())
        return self
    def setFloor(self,floorid):
        self.__floor = floorid
        self.__level.tileMap().fillFloor(self.__floor)
        return self
    def build(self):
        return self.__level

