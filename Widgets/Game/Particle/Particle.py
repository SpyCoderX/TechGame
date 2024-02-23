from PyQt6.QtGui import QImage,QColor,QPainter
from PyQt6.QtCore import QPointF, QRectF, QSizeF,Qt, QPoint, QRect, QSize
from typing import List
from Utils.Images import load
from Utils.Numbers import Loc,centerImage
class Particle:
    __Image:QImage
    __Life = 60
    __Tick = 0
    __List = None
    __Pos = Loc(0,0,0)
    __ID = "NULL"
    def __init__(self,img,ID,pos,life=None) -> None:
        self.__Image = img
        self.__ID = ID
        self.__Pos = pos
        if life: self.__Life = life
    def setList(self,particlelist):
        self.__List = particlelist
    def setPos(self,pos):
        self.__Pos = pos
    def getPos(self):
        return self.__Pos
    def getList(self):
        return self.__List
    def getLife(self):
        return self.__Life
    def getTick(self):
        return self.__Tick
    def getID(self):
        return self.__ID
    def getImage(self):
        return self.__Image
    def update(self,game):
        self.__Tick+=1
        if self.__Tick>=self.__Life:
            self.kill()
    def kill(self):
        self.__List.remove(self)
    def render(self,game):
        paint:QPainter = game.rScreen.getThisPainter()
        paint.drawImage(QRectF(centerImage(self.getPos().subtractPoint(game.camera.pos()),self.getImage()),QSizeF(self.getImage().size())),self.getImage())
    def clone(self):
        return Particle(self.getImage(),self.getID(),self.getLife())
class DamageParticle(Particle):
    def __init__(self,amount,pos) -> None:
        self.__Amount = amount
        img = QImage(len(str(amount))*10+10,30,QImage.Format.Format_ARGB32)
        img.fill(QColor(0,0,0,0))
        paint = QPainter(img)
        paint.drawText(QPointF(12,12),"-"+str(self.__Amount))
        paint.setPen(QColor(255,0,0,255))
        paint.setBrush(QColor(255,0,0,255))
        paint.drawText(QPointF(10,10),"-"+str(self.__Amount))
        super().__init__(img,"damage",pos,30)
    def clone(self,amount):
        return DamageParticle(amount,self.getPos())
    
class ParticleList:
    def __init__(self) -> None:
        self.__particles:List[Particle] = []
    def update(self,game):
        for particle in self.__particles:
            particle.update(game)
    def render(self,game):
        for particle in self.__particles:
            particle.render(game)
    def add(self,particle:Particle):
        particle.setList(self)
        self.__particles.append(particle)
    def remove(self,particle:Particle):
        self.__particles.remove(particle)

