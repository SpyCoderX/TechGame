from PyQt6.QtGui import QImage
from Utils.Images import default,load
from Widgets.Base import Widget
from Widgets.Game.Entity.Entity import Entity
from Utils.Numbers import QImage, distFromList,distFromPoint,Loc,Vector2D
ITEM_DIST = 100
COLLECT_DIST = 25
class MaterialList:
    __Materials:dict
    def __init__(self):
        self.__Materials = {}
    def addMaterial(self,mat):
        if isinstance(mat,Material):
            self.__Materials[mat.getName()] = mat
        else:
            raise ValueError("Tried to register invalid material. (Was not a material object.)")
    def getMaterial(self,name):
        name = str(name)
        val = self.__Materials.get(name,None)
        if val: return val
        else:
            raise IndexError("Unknown material "+name)
    def getAllMaterials(self):
        return self.__Materials.copy()
class Material:
    __Image = default()
    __Name = "NULL"
    __Rarity = 0 # Rarity, used for item selection and name color.
    __Damageable = False
    __Health = 10
    __StackSize = 16
    def __init__(self,img=None,name=None,rarity=None,health=None,damageable=None,stacksize=None) -> None:
        if img: self.__Image = img
        if name: self.__Name = name
        if rarity: self.__Rarity = rarity
        if health: self.__Health = health
        if damageable: self.__Damageable = damageable
        if stacksize: self.__StackSize = stacksize
    def getName(self):
        return self.__Name
    def getImage(self):
        return self.__Image
    def getRarity(self):
        return self.__Rarity
    def getHealth(self):
        return self.__Health
    def getDamageable(self):
        return self.__Damageable
class ItemStack:
    __Material:Material
    __Count:int = 16
    __Damage:int = 0
    __Unbreakable:bool = False
    def __init__(self, material, count) -> None:
        self.__Material = material
        self.__Count = int(count)
    def getCount(self):
        return self.__Count
    def getMaterial(self):
        return self.__Material
    def getHealth(self):
        return self.__Health
    def getUnbreakable(self):
        return self.__Unbreakable
    def __modify_damage(self,amount):
        if not(self.__Material.getDamageable()) or self.getUnbreakable():
            return
        self.__Damage+=amount
        if self.__Damage>self.__Material.getHealth():
            self.__Damage = self.__Material.getHealth()
        if self.__Damage<0:
            self.__Damage = 0
    def damage(self,amount):
        self.__modify_damage(amount)
        return self
    def repair(self,amount):
        self.__modify_damage(-amount)
        return self
    def setUnbreakable(self,unbreakable):
        self.__Unbreakable = unbreakable
        return self
    def setCount(self,count:int):
        self.__Count = int(count)
        return self
class Item(Entity):
    __Stack:ItemStack
    def __init__(self, stack:ItemStack):
        super().__init__(stack.getMaterial().getImage())
        self.__Stack = stack
    def getImage(self):
        return self.__Stack.getMaterial().getImage()
    def update(self, game: Widget):
        return super().update(game)
    def updateAcceleration(self,game):
        dist = distFromPoint(self.pos,game.Player.pos)
        if dist<COLLECT_DIST:
                self.collect(game)
        elif dist<ITEM_DIST:
            v = game.Player.pos.subtractPoint(self.pos).toVec().normalized().multiply((ITEM_DIST-dist)/4)
            self.velocity = self.velocity.addVec(v)
            return super().updateAcceleration(game)
        else:
            v = game.Player.pos.subtractPoint(self.pos).toVec().normalized().multiply(0.0001)
            self.velocity = self.velocity.addVec(v)
            return super().updateAcceleration(game)
    def collect(self,game):
        game.Player.inventory.add(self.__Stack)
        self.delete()
def get_item_texture(str):
    return load("Item_"+str).scaled(64,64)
MATERIALS = MaterialList()
MATERIALS.addMaterial(Material(get_item_texture("Oak_Log"),name="HMMMF"))