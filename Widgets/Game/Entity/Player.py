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
    def __init__(self,health):
        self.__idle_images = Anim("PlayerIdle") # Idle Animation
        self.__walking_images = Anim("PlayerWalk") # Walking Animation
        super().__init__(self.__idle_images.images()[0].scaled(128,128),health) # Sets up the entity. Uses the first image in __idle_images as the base image in the entity.
        
    def update(self, game: Widget):
        self.setList(game.currentLevel.entitylist())
        return super().update(game)