import PyQt6
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from Widgets.Base import Object,Widget
from Utils.Numbers import Loc
from Widgets.Game.Entity.LivingEntity import LivingEntity
# Importing PyQt6 stuff, and the other files.

class Player(LivingEntity):
    def __init__(self, img: QImage):
        super().__init__(img)