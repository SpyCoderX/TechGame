import PyQt6
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from Widgets.Base import Widget
from Utils.Images import load
import math
#imports ^


VIGNETTE = None # Vignette effect (Pronounced Vin-ye-t)


class ScreenController(Widget):
    """Base class for the main menu, game, and other screens."""
    vin = False
    def __init__(self) -> None:
        super().__init__()
        self.rScreen:Widget = None # Reference to the widget that displays to the window. Allows other objects to write to the widget easily.
        
    def preTick(self,screen:Widget):
        if self.rScreen==None:
            self.rScreen = screen
            self.recalcVignette()
        else:
            self.rScreen = screen
    def recalcVignette(self):
        global VIGNETTE
        VIGNETTE = load("Vignette").scaled(self.rScreen.frameGeometry().size())

    def tick(self,screen:Widget):
        self.fill(screen,self.getBrush(QColor(0,0,0,255)))
        self.handleEvents()
        self.updates()
        self.renders()
        
    def handleEvents(self):
        for event in self.rScreen.getEvents():
            self.handleEvent(event)
    def handleEvent(self,event):
        if event["type"]=="SizeChange":
            self.recalcVignette()

    # Main update function
    def updates(self):
        self.ui_update()

    
    def ui_update(self):
        pass

    def renders(self):
        self.vignette()
        self.ui_render()

    def vignette(self):
        if self.vin: return
        p:QPainter = self.rScreen.getThisPainter()
        p.drawImage(QPoint(0,0),VIGNETTE)

    def ui_render(self):
        pass

class MainMenu(ScreenController):
    def __init__(self) -> None:
        super().__init__()