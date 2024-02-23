import PyQt6
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from Widgets.Base import Object,Widget
from Utils.Numbers import *
from Utils import Images
from Utils.AABB import AABB
from Widgets.Game.Tiles.TileVARS import SOLID
from Vars.GLOBAL_VARS import SIZE
from Utils.Images import load

ENTITY_SHADOW = load("Entity_Shadow")

class Entity(Object):
    def __init__(self,img:QImage):
        super().__init__()


        # Image
        if img == None:
            img = Images.default()
        self.image = img
        c = self.image.copy()
        paint = QPainter(c)
        mask = QBitmap(c.createAlphaMask())
        paint.setClipRegion(QRegion(mask))
        paint.setPen(QColor(0,0,0,0))
        paint.setBrush(QColor(0,0,0,200))
        paint.drawRect(QRectF(0,0,128,128))
        self.image_dark = c
        self.game = None
            


        # Animation
        self.tick = 0 # Number to record the current tick. Used for animations.


        # EntityList 
        self.__list = None # EntityList that allows deletion of this object.


        # Location setup
        self.dir = 0
        self.pos = Loc(0,0,0)
        self.velocity = Vector2D()
        self.acceleration = Vector2D() # This controls the acceleration, basically the change in velocity.
        self.doMovement = True # This controls whether or not to handle movement.
        self.frictionMultiplier = 0.8

        self.ABBox = [64,64]
        self.shadow = ENTITY_SHADOW.scaled(self.ABBox[0],self.ABBox[1])
        """ [---] END OF INIT [---] """
        
    def setList(self,list): # EntityList
        self.__list = list

    def setABBox(self,boxx,boxy):
        self.ABBox = [boxx,boxy]

    def getAB(self):
        pos = self.pos.getList()
        vel = self.velocity
        return AABB([pos[0]-self.ABBox[0]/2,pos[1]-self.ABBox[1]/2],[pos[0]+self.ABBox[0]/2,pos[1]+self.ABBox[1]/2]).expand(AABB((vel.x()*self.ABBox[0]/2,vel.y()*self.ABBox[1]/2),(vel.x()*self.ABBox[0]/2,vel.y()*self.ABBox[1]/2)))

    def list(self): # EntityList
        if self.__list==None:
            print("Error: Entity of type "+str(type(self))+" does not have a EntityList registered.")
            return
        return self.__list


    def update(self,game:Widget):
        self.game = game
        self.list()
        self.tick += 1 #Updates current tick
        self.updateMovement(game)


    def updateMovement(self,game):
        def check(self,po:QPointF,cx=True):
            x = po.x()
            y = po.y()
            SIZ = SIZE/2
            modX = x%SIZ
            modY = y%SIZ
            tile = game.currentLevel.tileMap().getTile(x,y)
            if tile == None:
                return po
            if tile.collision()==SOLID:
                if cx:
                    if self.velocity.x() < 0:
                        x += SIZ - modX + 0.00001
                    elif self.velocity.x() > 0:
                        x += -0.00001 - modX
                if not cx:
                    if self.velocity.y() < 0:
                        y += SIZ - modY + 0.00001
                    elif self.velocity.y() > 0:
                        y += -0.00001 - modY
            return QPointF(x,y)
        if self.doMovement:
            self.velocity = self.velocity.addVec(self.acceleration).multiply(self.frictionMultiplier)

            pos = self.pos.addVec(self.velocity)

            c = check(self,QPointF(pos.x(),self.pos.y()))
            pos.setX(c.x())
            c = check(self,pos,False)
            pos.setY(c.y())
            self.pos = pos
            self.updateAcceleration(game)

    def updateAcceleration(self,game):
        self.acceleration = self.acceleration.multiply(0.7)
        

    def render(self,game):
        self.list()
        self.check_sizes()
        self.drawSelf(game)

    def check_sizes(self):
        if self.shadow.size().width()!=self.ABBox[0] or self.shadow.size().height()!=self.ABBox[1]:
            self.shadow = ENTITY_SHADOW.scaled(self.ABBox[0],self.ABBox[1])

    def drawSelf(self,game): #This function renders the entity. Gets the screen, obtains the PyQt6 Painter to draw to it, draws a picture at the current position, minus the camera to move based on camera and draws this image.
        # t = QtGui.QTransform()
        # t.rotate(self.pos.R)
        #.transformed(t)
        img = self.getImage()
        
        p:QPainter = game.rScreen.getThisPainter()
        p.translate(self.pos.subtractPoint(game.camera.pos()))
        p.drawImage(centerImage(QPoint(0,0),self.shadow),self.shadow)
        p.rotate(self.pos.R)
        p.drawImage(centerImage(QPoint(0,0),img),img)
        p.rotate(-self.pos.R)
        p.drawEllipse(QRectF((-self.ABBox[0]/2),
                          (-self.ABBox[1]/2),
                          (self.ABBox[0]),
                          (self.ABBox[1])))
        


    def getImage(self): # Override this function in other entities to allow modification of the image, or for animations.
        t = self.game.currentLevel.tileMap().getTile(self.pos.x(),self.pos.y())
        if t:
            if not t.light():
                return self.getImageDark()
        return self.image
    def getImageDark(self):
        return self.image_dark
    

    def delete(self):
        self.list().remove_entity(self)
        del self