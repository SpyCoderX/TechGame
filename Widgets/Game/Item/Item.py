from PyQt6.QtGui import *
from PyQt6.QtCore import *
from Utils.Images import default,load
from Widgets.Base import Widget
from Widgets.Game.Entity.Entity import Entity
from Utils.Numbers import QImage, distFromList,distFromPoint,Loc,Vector2D,centerImage
from Vars.TileVARS import FILE_PREFIX as TILE_FILE_PREFIX
from Vars.GLOBAL_VARS import GUI_SCALE
from enum import Enum
class Rarity(Enum):
    NULL = 0

    COMMON = 1
    UNCOMMON = 2

    RARE = 3
    EPIC = 4
    MYTHIC = 5

    LEGENDARY = 6
    MYTHOLOGICAL = 7
    UNOBTAINABLE = 8

    DEV = 9
    ERROR = 10

ITEM_DIST = 100
COLLECT_DIST = 25
# class MaterialList(Enum):
    # __Materials:dict
    # def __init__(self):
    #     self.__Materials = {}
    # def addMaterial(self,mat):
    #     if isinstance(mat,Material):
    #         self.__Materials[mat.getName()] = mat
    #     else:
    #         raise ValueError("Tried to register invalid material. (Was not a material object.)")
    # def getMaterial(self,name):
    #     name = str(name)
    #     val = self.__Materials.get(name,None)
    #     if val: return val
    #     else:
    #         raise IndexError("Unknown material "+name)
    # def getAllMaterials(self):
    #     return self.__Materials.copy()
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
    def getStacksize(self):
        return self.__StackSize
    def __add__(self, o):
        return self.getName()+o
    def __str__(self):
        return self.getName()
    def use(self,game):
        pass
class BlockMaterial(Material):
    __Durability = 1
    __BlastResistance = 1
    __ToolLevel = 1
    __AllowPlacing = False
    __AllowMining = False
    __Indestructible = False
    __Drops = []
    __TileName = "NULL"
    def __init__(self, img_name=None,tile_name=None, name=None, durability=None, blast_res=None,tool_lvl=None,allow_place=None,allow_mining=None,indestructible=None,drops=None, stacksize=None) -> None:
        super().__init__(load(TILE_FILE_PREFIX+img_name), name, 1, 1, False, stacksize)
        if tile_name: self.__TileName = tile_name
        if durability: self.__Durability = durability
        if tool_lvl: self.__ToolLevel = tool_lvl
        if allow_place: self.__AllowPlacing = allow_place
        if allow_mining: self.__AllowMining = allow_mining
        if indestructible: self.__Indestructible = indestructible
        if drops: self.__Drops = drops
        else: self.__Drops = [ItemStack(self,1)]
    def getDurability(self):
        return self.__Durability
    def getBlastResistance(self):
        return self.__BlastResistance
    def getToolLevel(self):
        return self.__ToolLevel
    def getAllowPlacing(self):
        return self.__AllowPlacing
    def getAllowMining(self):
        return self.__AllowMining
    def getIndestructible(self):
        return self.__Indestructible
    def getDrops(self):
        return self.__Drops
    def getTileName(self):
        return self.__TileName
    def __str__(self):
        return self.getTileName()
    def use(self, game):
        mpos = game.rScreen.mousePos()
        cpos = game.camera.pos()
        mpos = QPointF(mpos.x()+cpos.x(),mpos.y()+cpos.y())
        tile = game.currentLevel.tileMap().getTile(mpos.x(),mpos.y())
        mat:BlockMaterial = tile.material()
        if mat.getAllowPlacing() and distFromPoint(tile.gPos(),game.Player.pos)<=200 and tile!=game.currentLevel.tileMap().getTile(game.Player.pos.x(),game.Player.pos.y()):
            game.currentLevel.tileMap().setTile(game.getATileBuilder(game.currentLevel.tileMap(),self,tile.floorMaterial()).light(tile.light()).build(),tile.pos(),True)
            return True
class ToolMaterial(Material):
    def __init__(self, img=None, name=None, rarity=None, health=None) -> None:
        super().__init__(img, name, rarity, health, True, 1)

class WeaponMaterial(ToolMaterial):
    __AttackDamage = 1
    __AttackCooldown = 15
    def __init__(self, img=None, name=None, rarity=None, health=None, damage=None,cooldown=None) -> None:
        super().__init__(img, name, rarity, health)
    def getAttackDamage(self):
        return self.__AttackDamage
    def getAttackCooldown(self):
        return self.__AttackCooldown

class PickaxeMaterial(ToolMaterial):
    __MiningStrength = 1
    def __init__(self, img=None, name=None, rarity=None, health=None, strength=None) -> None:
        super().__init__(img, name, rarity, health)
    def getMiningStrength(self):
        return self.__MiningStrength
    

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
    def getDamage(self):
        return self.__Damage
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
    def clone(self):
        i = ItemStack(self.getMaterial(),self.getCount())
        i.damage(self.getDamage())
        i.setUnbreakable(self.getUnbreakable())
        return i
    def getMiningDamage(self):
        if isinstance(self.getMaterial(),PickaxeMaterial):
            return self.getMaterial().getMiningStrength()
        return 1
    def render(self,paint,pos,size,scale):
        v = GUI_SCALE*scale
        m = .5
        multi = m*v
        paint.drawImage(QRectF(QPointF(pos.x()-size.width()*v*0.5,pos.y()-size.height()*v*0.5),QSizeF(size.width()*v,size.height()*v)),self.getMaterial().getImage())
        paint.scale(multi,multi)
        txt = QStaticText(str(self.getCount()))
        pos = QPointF((pos.x()+size.width()*v*0.5-txt.size().width()*multi)/(multi),(pos.y()+size.height()*v*0.5-txt.size().height()*multi)/(multi))
        # paint.drawRect(QRectF(pos,txt.size()))
        paint.setPen(QColor(200,200,200,255))
        paint.drawStaticText(pos,txt)
        paint.scale(1/multi,1/multi)
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
        if game.Player.inventory.add(self.__Stack): 
            self.delete()
        else:
            self.velocity = self.velocity.multiply(-1)
            self.acceleration = self.acceleration.multiply(-1)
def get_item_texture(str):
    return load("Item_"+str).scaled(64,64)

class MATERIALS:
    STICK = Material(get_item_texture("Oak_Log"),name="Oak_log")
    STICK_SWORD = WeaponMaterial(get_item_texture("Oak_Log"),name="Stick Sword")
    OAK_LOG = BlockMaterial("Log","log","Oak Log",40,2,0,allow_mining=True)
    AIR = BlockMaterial("air","air","Air",allow_place=True)
    STONE = BlockMaterial("stone","stone","Stone",100,5,0,allow_mining=True)
    DARKSTONE = BlockMaterial("darkstone","darkstone","Darkstone")
    STONE_PICK = PickaxeMaterial(get_item_texture("Pickaxe_0"),"Stone Pickaxe",Rarity.COMMON,10,2)