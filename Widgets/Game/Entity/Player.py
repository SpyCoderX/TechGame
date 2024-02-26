import PyQt6
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from Widgets.Base import Object,Widget
from Utils.Numbers import Loc
from Widgets.Game.Entity.LivingEntity import LivingEntity
from Widgets.Game.Item.Item import PickaxeMaterial,WeaponMaterial
from Utils.Images import Anim,load
from Utils.Numbers import Vector2D
from typing import List
from Utils.AABB import AABB
from Widgets.Game.Menus.MenuBases import PlayerInventory
import os
import math
DAGGER = load("item_oak_log")
# Importing PyQt6 stuff, and the other files.

class Player(LivingEntity):
    def __init__(self,health):
        self.__swing_integral = -1
        self.__attack_points = [[0,0],[0,0],[0,0]]
        self.__swing_cooldown = 0
        self.__use_cooldown = 0
        self.__isSwinging = False
        self.__selected_item = None # Note: Use self.inventory().held_item() in future once added.
        self.__idle_images = Anim("PlayerIdle") # Idle Animation
        self.__walking_images = Anim("PlayerWalk") # Walking Animation
        p = self.__idle_images.images()[0].scaled(128,128)
        self.inventory = PlayerInventory() # The player's inventory (not gui, just the inventory)
        self.breaking_tile = None # The current tile being mined.
        self.selected_slot = 1
        
        super().__init__(p,health) # Sets up the entity. Uses the first image in __idle_images as the base image in the entity.
        
    def getTool(self):
        return self.inventory.getToolStack(self.selected_slot) if self.selected_slot<2 else self.inventory.get(self.selected_slot-2)
    def setTool(self,tool):
        return self.inventory.setToolStack(self.selected_slot,tool) if self.selected_slot<2 else self.inventory.set(self.selected_slot-2,tool)
    def isAttackMode(self):
        return isinstance(self.getTool().getMaterial(),WeaponMaterial)
    def update(self, game: Widget):
        self.setList(game.currentLevel.entitylist())
        if game.rScreen.mouseButton(0) and not self.__isSwinging and self.__swing_cooldown==0 and self.isAttackMode():
            self.attack()
        if game.rScreen.mouseButton(2) and self.__use_cooldown==0:
            self.use()
            if self.getTool(): 
                if self.getTool().getMaterial().use(self.game):
                    self.getTool().setCount(self.getTool().getCount()-1)
                    if self.getTool().getCount()<=0: self.setTool(None)
        if self.__swing_integral!=-1:
            self.__swing_integral += (-1-self.__swing_integral)/30
            if self.isAttackMode():
                self.__attack_points[0] = [math.cos(math.radians(self.pos.R)+self.__swing_integral*math.pi-math.pi*0.5)*32,math.sin(math.radians(self.pos.R)+self.__swing_integral*math.pi-math.pi*0.5)*32]
                self.__attack_points[1] = [math.cos(math.radians(self.pos.R)+self.__swing_integral*math.pi-math.pi*0.5)*48,math.sin(math.radians(self.pos.R)+self.__swing_integral*math.pi-math.pi*0.5)*48]
                self.__attack_points[2] = [math.cos(math.radians(self.pos.R)+self.__swing_integral*math.pi-math.pi*0.5)*64,math.sin(math.radians(self.pos.R)+self.__swing_integral*math.pi-math.pi*0.5)*64]

            if self.__swing_integral<0:
                self.__swing_integral = -1
                self.__isSwinging = False
                self.__swing_cooldown = 10
            elif self.isAttackMode():
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
            if self.__swing_cooldown>0:
                self.__swing_cooldown -= 1
        if self.__use_cooldown>0:
            self.__use_cooldown -= 1
        return super().update(game)
    
    def render(self, game):
        if self.isSwinging() and self.getTool():
            p:QPainter = game.rScreen.getThisPainter()
            p2:QPen = p.pen()
            p2.setColor(QColor(255,255,255))
            p.setPen(p2)
            p.translate(self.pos.subtractPoint(game.camera.pos()))
            # for x in self.__attack_points:
            #     p  .drawEllipse(int(x[0])-10,int(x[1])-10,20,20)
            p.rotate(self.pos.R+self.__swing_integral*180-45)
            # rectangle = QRectF(0, -15, 40.0, 30.0)
            # startAngle = int(-22.5 * 16)
            # spanAngle = 45 * 16
            # p.drawArc(rectangle, startAngle, spanAngle)
            # rectangle = QRectF(50, -30, 80.0, 60.0)
            # startAngle = -45 * 16
            # spanAngle = 90 * 16
            # p.drawArc(rectangle, startAngle, spanAngle)
            p.drawImage(QRectF(10,-74,64,64),self.getTool().getMaterial().getImage())
        super().render(game)

    def use_item(self):
        pass

    def attack(self):
        self.swing()

    def isSwinging(self):
        return self.__isSwinging
    
    def swingVal(self):
        return self.__swing_integral
    def swing(self):
        if not self.__isSwinging and self.__swing_cooldown==0:
            self.__swing_integral = 1
            self.__isSwinging = True
    def mine(self):
        self.swing()
    def use(self):
        self.__use_cooldown = 15
    def useVal(self):
        return self.__use_cooldown
    def scrollSlot(self,val):
        self.selected_slot-=val.y()
        self.selected_slot%=7