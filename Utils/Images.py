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

def convertToImagePath(str):
    return "/Images/"+str+".png"

def load(s:str) -> QImage:
    s = convertToImagePath(s)
    if os.path.isfile(s):
        return QImage(fileName=s)
    else:
        raise ImageLoadError("Unable to find image \""+s+"\"")

def default():
    return load("Default")

class Anim:
    def __init__(self,id) -> None:

        self.__images = []

        loading = True
        num = 0
        while loading:
            if not os.path.isfile(convertToImagePath(id+"_"+str(num))):
                loading = False
                break
            self.__images.append(load(id+"_"+str(num)))
    def images(self):
        return self.__images