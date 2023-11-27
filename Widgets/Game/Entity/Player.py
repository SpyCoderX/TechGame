import PyQt6
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from Widgets.Base import Object,Widget
from Utils.Numbers import Loc
from Widgets.Game.Entity.LivingEntity import LivingEntity
from Utils.Images import Anim
import os
# Importing PyQt6 stuff, and the other files.

class Player(LivingEntity):
    def __init__(self):
        self.__idle_images = Anim("PlayerIdle") # Idle Animation
        self.__walking_images = Anim("WalkingIdle")
        super().__init__(self.__idle_images[0]) # Sets up the entity. Uses the first image in __idle_images as the base image in the entity.
