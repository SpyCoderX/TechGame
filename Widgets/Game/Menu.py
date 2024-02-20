import PyQt6
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import QPaintEvent
from PyQt6.QtWidgets import *
from Widgets.Base import Widget
from Utils.Images import load
import math
from typing import List
from .UI.Gui import Gui
#imports ^


VIGNETTE = None # Vignette effect (Pronounced Vin-ye-t)


class ScreenController(Widget):
    """Base class for the main menu, game, and other screens."""
    vin = False
    def __init__(self,screen) -> None:
        super().__init__()
        self.firstTick = True
        self.rScreen:Widget = screen # Reference to the widget that displays to the window. Allows other objects to write to the widget easily.
        self.GUIs = QStackedLayout()
        self.GUIs.setContentsMargins(0,0,0,0)
        self.setLayout(self.GUIs)

    def preTick(self,screen:Widget):
        if self.firstTick:
            self.recalcVignette()
            self.firstTick = False
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
        pass

    def renders(self):
        self.vignette()
        pass

    def vignette(self):
        if self.vin: return
        p:QPainter = self.rScreen.getThisPainter()
        p.drawImage(QPoint(0,0),VIGNETTE)

    

class MainMenu(ScreenController):
    def __init__(self,screen) -> None:
        super().__init__(screen)
        w = Widget()
        l = QVBoxLayout()
        l.setContentsMargins(0,0,0,0)
        class Banner(Widget):
            def paintEvent(self, a0: QPaintEvent) -> None:
                self.fillThis(QBrush(QColor(0,0,0,100)))
        w2 = Banner()
        w2.setFixedHeight(200)
        t = QPushButton()
        t.setText("Title (Placeholder)")
        l2 = QHBoxLayout()
        w3 = QWidget()
        w3.setFixedHeight(100)
        l2.addWidget(w3)
        l2.addWidget(t)
        w3 = QWidget()
        l2.addWidget(QWidget())
        l2.addWidget(QPushButton())
        l2.addWidget(QWidget())
        w2.setLayout(l2)
        w3 = QWidget()
        w3.setFixedHeight(600)
        l.addWidget(w3)
        l.addWidget(w2)
        l.addWidget(QWidget())
        w.setLayout(l)
        self.GUIs.addWidget(w)
    def renders(self):
        screenSize = self.rScreen.frameGeometry()
        p = self.rScreen.getThisPainter()
        brush = self.getBrush(QColor(100,100,100,255))
        p.setBrush(brush)
        p.drawRect(screenSize)
        return super().renders()



