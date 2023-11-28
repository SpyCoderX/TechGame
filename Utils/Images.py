import PyQt6
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import os
from Utils.Errors import ImageLoadError,ImageError

def convertToImagePath(str):
    return "Images\\"+str+".png"

def load(s:str) -> QImage:
    s = convertToImagePath(s)
    if os.path.isfile(s):
        return QImage(s)
    else:
        if s == convertToImagePath("Default"):
            raise ImageLoadError("DEFAULT IMAGE DOES NOT EXIST")
        print("Unable to find image \""+s+"\"")
        return default()

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
            num+=1
        
    def images(self):
        if len(self.__images)==0:
            self.__images = [default()]
        return self.__images