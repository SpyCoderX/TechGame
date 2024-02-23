import PyQt6
import math
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import *
from Widgets.Base import Object,Widget
from Utils.Numbers import Loc,Vector2D
from Widgets.Game.Particle.Particle import DamageParticle
from . import Entity
from random import randint
class LivingEntity(Entity):
    def __init__(self, img: QImage,health):
        super().__init__(img)
        self.__health = health
        self.__maxHealth = health
        self.__invulnerable_frames = 0
        self.__damage_frames = 0

        c = self.image.copy()
        paint = QPainter(c)
        mask = QBitmap(c.createAlphaMask())
        paint.setClipRegion(QRegion(mask))
        paint.setPen(QColor(0,0,0,0))
        paint.setBrush(QColor(255,0,0,150))
        paint.drawRect(QRectF(0,0,128,128))
        self.image_hurt = c
        

    def update(self, game: Widget):
        if self.__invulnerable_frames>0: self.__invulnerable_frames-=1
        if self.__damage_frames>0: self.__damage_frames-=1
        super().update(game)
    def getImage(self):
        return self.image_hurt if self.__damage_frames else super().getImage()
        # Modification of health
    def damage(self,amount):
        if self.iFrames()>0: return False
        self.__change_health(min(-amount,0))
        self.set_iFrames(15)
        self.__damage_frames = 5
        if self.game: self.game.particles.add(DamageParticle(amount,self.pos.addVec(Vector2D(randint(-self.ABBox[0]/2,self.ABBox[0]/2),randint(-self.ABBox[1]/2,self.ABBox[1]/2)))))
        return True

    def heal(self,amount):
        self.__change_health(max(amount,))
    def iFrames(self):
        return self.__invulnerable_frames
    def set_iFrames(self,iFrames):
        self.__invulnerable_frames = iFrames
        # Get/Set health
    def setHealth(self,amount:int):
        self.__setHealth(amount)

    def getHealth(self):
        return self.__health
    

        # Get/set max health
    def setMaxHealth(self,amount:int):
        self.__maxHealth = max(amount,1)
        self.__setHealth(self.__health)

    def getMaxHealth(self):
        return self.__maxHealth



        # Instant kill with damage
    def kill(self):
        self.damage(2**64)
    

        # Functions that handle the manipulation of the health variables. This allows for built-in checks to detect if the entity dies.
    def __change_health(self,a):
        self.__setHealth(self.__health+a)

    def __setHealth(self,a):
        self.__health= max(min(a,self.__maxHealth),0)
        if self.__health==0:
            self.death()
            self.delete()
    def death(self):
        pass
        