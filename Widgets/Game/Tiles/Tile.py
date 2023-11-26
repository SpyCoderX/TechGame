class Tile:
    def __init__(self,s,pos) -> None:
        self.__id = s
        self.__pos = list(pos)
        self.__icon = None # Add a custom object called "Icon" which has an image to render in the render function.

    def update(self,screen):
        pass
    # Leave this be, different tiles will override this.

    def render(self,screen):
        pass 
    # Add rendering code