import PyQt6
import math
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import *
from Widgets.Base import Object,Widget
from Utils.Numbers import Loc
from Widgets.Game.Entity.Entity import Entity
class LivingEntity(Entity):
    def __init__(self, img: QImage,health):
        super().__init__(img)
        self.__health = health
        self.__maxHealth = health

    def damage(self,amount):
        self.__change_health(-amount)
    def heal(self,amount):
        self.__change_health(amount)

    def setHealth(self,amount:int):
        self.__setHealth(amount)
    def getHealth(self):
        return self.__health
    
    def setMaxHealth(self,amount:int):
        self.__maxHealth = max(amount,1)
        self.__setHealth(self.__health)
    def getMaxHealth(self):
        return self.__maxHealth

    
    def kill(self):
        self.damage(2**64)
    def death(self):
        self.__list.remove(self)
        del self

        # Functions that handle the manipulation of the health variables. This allows for built-in checks to detect if the entity dies.
    def __change_health(self,a):
        self.__setHealth(self.__health+a)

    def __setHealth(self,a):
        self.__health= max(min(a,self.__maxHealth),0)
        if self.__health==0:
            self.death()
        