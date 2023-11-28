from Utils.Images import default
class Item:
    __Image = default()
    __Name = "NULL"
    __Rarity = 0 # Rarity, used for item selection and name color.
    def __init__(self,img,name="NULL",rarity=0) -> None:
        if img != None: self.__Image = img
        if name != None: self.__Name = name
        if rarity != None: self.__Rarity = rarity