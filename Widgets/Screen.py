import PyQt6
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from Widgets.Game import Game
from Widgets.Base import Widget

class Screen(Widget):
    def __init__(self) -> None:
        super().__init__()
        self.setMinimumSize(600,400)
        self.game = Game.MainGame()
        l = QStackedLayout()
        l.addWidget(self.game)
        self.setLayout(l)
        self.keys = {"w":False,"a":False,"s":False,"d":False}
        self.key_presses = []

        
    def paintEvent(self, a0: QPaintEvent) -> None:
        self.game.tick(self)
    
    