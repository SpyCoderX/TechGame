from typing import List
from Widgets.Game.Entity.Entity import Entity
from Utils.AABB import AABBTree
class EntityList:
    __LIST: List[Entity]
    def __init__(self) -> None:
        self.__LIST = []
        self.tree = AABBTree()
    

    def add_entity(self,entity:Entity):
        entity.setList(self)
        self.__LIST.append(entity)
        self.tree.add(entity.getAB(),entity)


    def remove_entity(self,entity):
        self.__LIST.remove(entity)


    def get_entities(self):
        return self.__LIST
    

    def clear_entities(self):
        self.__LIST = []


    def update(self,game):
        for e in self.__LIST:
            e.update(game)
            self.tree.update(e.getAB(),e)


    def render(self,game):
        for e in self.__LIST:
            e.render(game)

    def contains(self,entity) -> bool:
        return self.__LIST.count(entity)>0