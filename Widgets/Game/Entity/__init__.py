class EntityList:
    
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


    def update(self,screen):
        for e in self.__LIST:
            e.update(screen)


    def render(self,screen):
        for e in self.__LIST:
            e.render(screen)