import PyQt6
from PyQt6 import QtCore
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
class Ticker(QBasicTimer):
    def __init__(self,w) -> None:
        super().__init__()
        self.start(16,w)