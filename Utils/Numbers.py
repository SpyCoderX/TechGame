from PyQt6.QtCore import *
from PyQt6.QtGui import *
from typing import overload
class Loc(QPointF):
    R = 0
    @overload
    def __init__(self,X:float,Y:float,Rot:float) -> None: ...
    @overload
    def __init__(self,L:list,Rot:float) -> None: ...
    @overload
    def __init__(self,P:QPoint,Rot:float) -> None: ...

    def __init__(self,a,b,c):
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
        
        
    

       

        