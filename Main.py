import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from Widgets.Window import BaseW 


app = QApplication(sys.argv)
B = BaseW()
B.show()
app.exec()

""" 
Add more code to:

Entity 20%
LivingEntity - what am i doing with this again?
Item
Tile
BaseEnemy
Player 2%


Create:

Camera.py - DONE

PauseUI.py
OverlayUI.py
StartMenuUI.py
Mode.py (For the current mode, Sta
rt Menu, In Game, Pause Menu, Shop Menu)
Layer.py (Current layer/level (Normal/parallel))
LevelLoader.py (Level loader, loads from a built-in set of levels)
Levels/Level-<number>.json (The built-in levels)
Level.py
"""