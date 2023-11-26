import PyQt6
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from Widgets.Base import Object,Widget
from Utils.Numbers import Loc
from Widgets.Game.Entity.LivingEntity import LivingEntity
import os
from Utils.Errors import ImageLoadError,ImageError

def load(s:str) -> QImage:
    s = "/Images/"+s+".png"
    if os.path.isfile(s):
        return QImage(fileName=s)
    else:
        raise ImageLoadError("Unable to find image \""+s+"\"")

def default():
    return load("Default")