from typing import List
from Widgets.Game.Entity.Entity import Entity
class EntityList:
    __LIST: List[Entity]
    def __init__(self) -> None:
        self.__LIST = []
    

    def add_entity(self,entity):
        entity.setList(self)
        self.__LIST.append(entity)


    def remove_entity(self,entity):
        self.__LIST.remove(entity)


    def get_entities(self):
        return self.__LIST
    

    def clear_entities(self):
        self.__LIST = []


    def update(self,game):
        for e in self.__LIST:
            e.update(game)


    def render(self,game):
        for e in self.__LIST:
            e.render(game)

    def contains(self,entity) -> bool:
        return self.__LIST.count(entity)>0