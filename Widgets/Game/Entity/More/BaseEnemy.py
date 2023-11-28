from PyQt6.QtGui import QImage
from Widgets.Game.Entity.LivingEntity import LivingEntity
import math

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
    
    def updateAcceleration(self):
        if self.__target!=None:
            self.acceleration = self.acceleration.addVec(self.__target.pos.subtractPoint(self.pos).toVec().normalized())
        else:
            self.acceleration = self.acceleration.addVec(math.atan2(self.pos.y(),self.pos.x()))
        return super().updateAcceleration()
