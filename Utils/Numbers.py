from PyQt6.QtCore import QPoint,QPointF
from typing import overload
class Loc:
    X = 0
    Y = 0
    R = 0
    @overload
    def __init__(self,X:float,Y:float,Rot:float) -> None:
        """Creates a point with an x-position, y-position, and rotation."""
        self.X=X
        self.Y=Y
        self.R=Rot
    @overload
    def __init__(self,L:list,Rot:float) -> None:
        """Creates a point with an x-position, y-position, and rotation."""
        if len(L)<2:
            raise ValueError("Location was not given enough coordinates. (list verison)")
        self.X=L[0]
        self.Y=L[1]
        self.R=Rot
    @overload
    def __init__(self,P:QPoint,Rot:float) -> None:
        """Creates a point with an x-position, y-position, and rotation."""
        self.X=P.x
        self.Y=P.y
        self.R=Rot
    

       

        