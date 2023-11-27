import PyQt6
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from Widgets.Base import Object,Widget
from Utils.Numbers import *
from Utils import Images

class Entity(Object):
    def __init__(self,img:QImage):
        super().__init__()

        # Image
        if img == None:
            img = Images.default()
        self.image = img

        # Animation
        self.tick = 0 # Number to record the current tick. Used for animations.

        # EntityList 
        self.__list = None # EntityList that allows deletion of this object.

        # Location setup
        self.dir = 0
        self.pos = Loc()
        self.velocity = Vector2D()
        self.acceleration = Vector2D() # This controls the acceleration, basically the change in velocity.
        self.doMovement = True # This controls whether or not to handle movement.
        self.frictionMultiplier = 0.8

        
    def setList(self,list:list): # EntityList
        self.__list = list


    def list(self): # EntityList
        if self.__list==None:
            print("Error: Entity of type "+type(self)+" does not have a EntityList registered.")
            return
        return self.__list


    def update(self,game:Widget):
        list()
        self.tick += 1 #Updates current tick
        self.updateMovement()


    def updateMovement(self):
        if self.doMovement:
            self.velocity = self.velocity.addVec(self.acceleration)
            self.velocity.multiply(self.frictionMultiplier)
            self.pos.addVec(self.velocity)

    def updateAcceleration(self):
        self.acceleration = self.acceleration.multiply(0.7)
        

    def render(self,game):
        list()
        self.drawSelf(game)


    def drawSelf(self,game): #This function renders the entity. Gets the screen, obtains the PyQt6 Painter to draw to it, draws a picture at the current position, minus the camera to move based on camera and draws this image.
        game.rScreen.getThisPainter().drawPicture(self.pos.subtractPoint(game.camera.pos()),self.getImg())


    def getImage(self): # Override this function in other entities to allow modification of the image, or for animations.
        return self.image
    

    def delete(self):
        self.list().remove(self)
        del self