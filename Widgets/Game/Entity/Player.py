import PyQt6
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from Widgets.Base import Object,Widget
from Utils.Numbers import Loc
from Widgets.Game.Entity.LivingEntity import LivingEntity
from Utils.Images import Anim,load
from Utils.Numbers import Vector2D
from typing import List
from Utils.AABB import AABB
from Widgets.Game.Menus.MenuBases import PlayerInventory
import os
import math
DAGGER = load("dagger")
# Importing PyQt6 stuff, and the other files.

class Player(LivingEntity):
    def __init__(self,health):
        self.__attack_integral = -1
        self.__attack_points = [[0,0],[0,0],[0,0]]
        self.__attack_cooldown = 0
        self.__isAttacking = False
        self.__selected_item = None # Note: Use self.inventory().held_item() in future once added.
        self.__idle_images = Anim("PlayerIdle") # Idle Animation
        self.__walking_images = Anim("PlayerWalk") # Walking Animation
        p = self.__idle_images.images()[0].scaled(128,128)
        self.inventory = PlayerInventory()
        
        super().__init__(p,health) # Sets up the entity. Uses the first image in __idle_images as the base image in the entity.
        

    def update(self, game: Widget):
        self.setList(game.currentLevel.entitylist())
        if game.rScreen.mouseButton(0) and not self.__isAttacking and self.__attack_cooldown==0:
            self.attack()
        if self.__attack_integral!=-1:
            self.__attack_integral += (-1-self.__attack_integral)/30
            self.__attack_points[0] = [math.cos(math.radians(self.pos.R)+self.__attack_integral*math.pi-math.pi*0.5)*32,math.sin(math.radians(self.pos.R)+self.__attack_integral*math.pi-math.pi*0.5)*32]
            self.__attack_points[1] = [math.cos(math.radians(self.pos.R)+self.__attack_integral*math.pi-math.pi*0.5)*80,math.sin(math.radians(self.pos.R)+self.__attack_integral*math.pi-math.pi*0.5)*80]
            self.__attack_points[2] = [math.cos(math.radians(self.pos.R)+self.__attack_integral*math.pi-math.pi*0.5)*128,math.sin(math.radians(self.pos.R)+self.__attack_integral*math.pi-math.pi*0.5)*128]

            if self.__attack_integral<0:
                self.__attack_integral = -1
                self.__isAttacking = False
                self.__attack_cooldown = 10
            else:
                pos1 = [self.__attack_points[0][0]+self.pos.x(),self.__attack_points[0][1]+self.pos.y()]
                pos2 = [self.__attack_points[1][0]+self.pos.x(),self.__attack_points[1][1]+self.pos.y()]
                pos3 = [self.__attack_points[2][0]+self.pos.x(),self.__attack_points[2][1]+self.pos.y()]
                ABs:List = game.currentLevel.entitylist().tree.getCollisions(AABB(pos1,pos3).expandBy(20))
                for AB in ABs:
                    ent = AB.obj
                    if isinstance(ent,LivingEntity):
                        vec = ent.pos.subtractPoint(self.pos.toPoint()).toVec().normalized().multiply(8)
                        if (math.sqrt((ent.pos.x()-pos1[0])**2+(ent.pos.y()-pos1[1])**2)<=20+min(ent.ABBox)/2 or
                            math.sqrt((ent.pos.x()-pos2[0])**2+(ent.pos.y()-pos2[1])**2)<=20+min(ent.ABBox)/2 or
                            math.sqrt((ent.pos.x()-pos3[0])**2+(ent.pos.y()-pos3[1])**2)<=20+min(ent.ABBox)/2):
                            if ent.damage(5): ent.acceleration = ent.acceleration.addVec(vec)
        else:
            if self.__attack_cooldown>0:
                self.__attack_cooldown-=1
        return super().update(game)
    
    def render(self, game):
        if self.__isAttacking:
            p:QPainter = game.rScreen.getThisPainter()
            p2:QPen = p.pen()
            p2.setColor(QColor(255,255,255))
            p.setPen(p2)
            p.translate(self.pos.subtractPoint(game.camera.pos()))
            # for x in self.__attack_points:
            #     p  .drawEllipse(int(x[0])-10,int(x[1])-10,20,20)
            p.rotate(self.pos.R+self.__attack_integral*180-90)
            # rectangle = QRectF(0, -15, 40.0, 30.0)
            # startAngle = int(-22.5 * 16)
            # spanAngle = 45 * 16
            # p.drawArc(rectangle, startAngle, spanAngle)
            # rectangle = QRectF(50, -30, 80.0, 60.0)
            # startAngle = -45 * 16
            # spanAngle = 90 * 16
            # p.drawArc(rectangle, startAngle, spanAngle)
            p.drawImage(QRectF(30,-64,128,128),DAGGER)
        super().render(game)

    def use_item(self):
        pass

    def attack(self):
        self.__attack_integral = 1
        self.__isAttacking = True

    def isAttacking(self):
        return self.__isAttacking
    
    def attackVal(self):
        return self.__attack_integral
    