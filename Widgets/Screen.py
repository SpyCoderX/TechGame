import PyQt6
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from Widgets.Game import Game
from Widgets.Game import Menu
from Widgets.Base import Widget

class Screen(Widget):
    def __init__(self) -> None:
        super().__init__()
        self.setMinimumSize(600,400)

        # References to the different controllers, so multiple instances are not created.
        self.gameController = Game.MainGame(self)
        self.mainMenuController = Menu.MainMenu(self)

        # Controller that is currently active.
        self.setController(self.gameController)

        # List of all events (Keypresses, size changes, etc.) that have occured since the last time #getEvents() was called.
        self.events = []

        
    def paintEvent(self, a0: QPaintEvent) -> None:
        self.selectedController.preTick(self)
        self.selectedController.tick(self)

    def getEvents(self):
        for event in self.events:
            yield event
        self.events.clear()

    def setController(self,controller:Menu.ScreenController):
        self.selectedController = controller
        l = QHBoxLayout()
        l.setContentsMargins(0,0,0,0)
        l.addWidget(self.selectedController)
        self.setLayout(l)
    
    