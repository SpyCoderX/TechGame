from PyQt6.QtCore import *
from PyQt6.QtGui import *
from typing import overload

from PyQt6.QtGui import QVector2D
from Vars.GLOBAL_VARS import SIZE
import math

def centerImage(Point:QPoint,Image:QImage,scale=1):
    return QPointF(Point.x()-Image.width()*(0.5*scale),Point.y()-Image.height()*(0.5*scale))

def cnvrtLstToQPntF(list): #Convert List To QPointF (Convert Cnvrt, List Lst, To To, QPointF QPntf)
    return QPointF(list[0],list[1])

def addPoints(p1,p2):
    return QPointF(p1.x()+p2.x(),p1.y()+p2.y())

def toTilePos(pos):
    return [round(pos[0]/SIZE),round(pos[1]/SIZE)]

def tileToGlobalPos(x,y):
    return [x*SIZE,y*SIZE]

def smoothAngles(a,b,val):
    """Returnes an angle that is between a and b."""
    diff = ((b-a)%360)
    if diff > 180: diff -= 180
    c = (a-diff)*val+a*(1-val)
    return c

def distFromList(a,b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

def distFromPoint(a,b):
    return math.sqrt((a.x()-b.x())**2+(a.y()-b.y())**2)

class Loc(QPointF):
    R = 0
    @overload
    def __init__(self,X:float,Y:float,Rot:float) -> None: ...
    @overload
    def __init__(self,L:list,Rot:float) -> None: ...
    @overload
    def __init__(self,P:QPoint,Rot:float) -> None: ...

    def __init__(self,a,b,c):
        super().__init__()
        if isinstance(a,QPoint) or isinstance(a,QPointF):
            """Creates a point with an x-position, y-position, and rotation."""
            self.setX(a.x)
            self.setY(a.y)
            self.R=b
        elif isinstance(a, list):
            """Creates a point with an x-position, y-position, and rotation."""
            if len(a)<2:
                raise ValueError("Location was not given enough coordinates. (list verison)")
            self.setX(a[0])
            self.setY(a[1])
            self.R=b
        else:
            """Creates a point with an x-position, y-position, and rotation."""
            self.setX(a)
            self.setY(b)
            self.R=c
    def addVec(self,a):
        b = Loc(self.x()+a.x(),self.y()+a.y(),self.R)
        return b
    def subtractPoint(self,a:QPointF):
        b = Loc(self.x()-a.x(),self.y()-a.y(),self.R)
        return b
    def toVec(self):
        return Vector2D(self.x(),self.y())
    def getList(self):
        return [self.x(),self.y()]
    def setAll(self,x,y):
        self.setX(x)
        self.setY(y)
class Vector2D(QVector2D):
    def setAll(self,x,y):
        self.setX(x)
        self.setY(y)
    def multiply(self,a:float):
        """Multiply the X & Y by A and return the resulting point/vector."""
        b = Vector2D(self.x()*a,self.y()*a)
        return b
    def addVec(self,a):
        """Adds this vector and A together and returns the result."""
        b = Vector2D(self.x()+a.x(),self.y()+a.y())
        return b
    def add(self,a,b):
        self.setAll(self.x()+a,self.y()+b)
    
        return self
    def normalized(self):
        vec = super().normalized()
        new = Vector2D(vec.x(),vec.y())
        return new
        
        
    

       

        