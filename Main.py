import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from Widgets.Window import Base 


app = QApplication(sys.argv)
B = Base()
B.show()
app.exec()

""" 
Add more code to:

Entity
LivingEntity
Item
Tile
BaseEnemy
Player


Create:

Camera.py
PauseUI.py
OverlayUI.py
StartMenuUI.py
Mode.py (For the current mode, Start Menu, In Game, Pause Menu, Shop Menu)
Layer.py (Current layer/level (Normal/parallel))
LevelLoader.py (Level loader, loads from a built-in set of levels)
Levels/Level-<number>.json (The built-in levels)
Level.py
Tiles/__init__.py (The level, so this NEEDS to be made)
"""