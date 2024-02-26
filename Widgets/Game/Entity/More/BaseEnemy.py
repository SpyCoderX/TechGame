from PyQt6.QtGui import QImage
from Widgets.Game.Entity.LivingEntity import LivingEntity
from PyQt6.QtCore import QPointF
import math
from Widgets.Game.Item.Item import Item,MATERIALS,ItemStack

# BaseEnemy, add some stuff specific to enemies. (Target, Pathfinding?, Search Radius, Movement speed, etc)
class BaseEnemy(LivingEntity):
    __target: LivingEntity
    def __init__(self, img: QImage, health):
        super().__init__(img, health)
        self.__target = None
    

    def setTarget(self,target:LivingEntity):
        self.__target = target

    def target(self):
        return self.__target
    
    def updateAcceleration(self,game):
        
        if self.__target!=None:
            v = self.__target.pos.subtractPoint(self.pos).toVec().normalized()
            v.setX(v.x()*0.2)
            v.setY(v.y()*0.2)
            self.acceleration = self.acceleration.addVec(v)
        else:
            dir = math.atan2(self.pos.y(),self.pos.x())
            self.acceleration = self.acceleration.addVec(QPointF(math.cos(dir)*0.2,math.sin(dir)*0.2))
        return super().updateAcceleration(game)
    def death(self):
        item = Item(ItemStack(MATERIALS.STICK,1))
        item.pos = self.pos
        self.list().add_entity(item)
    
