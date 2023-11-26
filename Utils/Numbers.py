from PyQt6.QtCore import QPoint,QPointF
from typing import overload
class Loc:
    X = 0
    Y = 0
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
            self.X=a.x
            self.Y=a.y
            self.R=b
        elif isinstance(a, list):
            """Creates a point with an x-position, y-position, and rotation."""
            if len(a)<2:
                raise ValueError("Location was not given enough coordinates. (list verison)")
            self.X=a[0]
            self.Y=a[1]
            self.R=b
        else:
            """Creates a point with an x-position, y-position, and rotation."""
            self.X=a
            self.Y=b
            self.R=c
        
        
    

       

        