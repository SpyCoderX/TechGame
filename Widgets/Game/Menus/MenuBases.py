from Widgets.Base import Widget
from PyQt6.QtGui import QImage, QPaintEvent,QPainter,QColor, QRegion, QBitmap
from PyQt6.QtCore import QRectF,QPointF,QSizeF,Qt
from Utils.Numbers import centerImage
from Utils.AABB import AABBTree,AABB
from Utils.Images import load
import math
SCALE = 8
class Menu(Widget):
    Game = None
    def __init__(self) -> None:
        super().__init__()
        self.__updated = False
        
    def getTexture(self):
        return self.__Texture.scaled(self.geometry().width(),self.geometry().height())
    def paintEvent(self, a0: QPaintEvent) -> None:
        self.update()
        self.render()
    def update(self):
        self.Game = self.parentWidget()
        self.__updated = True

    def render(self):
        if not self.__updated: raise RuntimeError("Must run super().update() in self.update()!")
        painter:QPainter = self.getThisPainter()
        painter.setPen(QColor(0,0,0,0))
        painter.setBrush(QColor(0,0,0,100))
        painter.drawRect(self.geometry())
class InventoryGUI(Menu):
    def __init__(self,inventory,game) -> None:
        super().__init__()
        self.tree = AABBTree()
        self.Slots = []
        self.Inventory = inventory
        self.Game = game
        self.createSlots()
    def createSlots(self):
        pass
    def createSlot(self,slot):
        self.tree.add(slot.AABB(),slot)
        self.Slots.append(slot)
    def renderBackground(self):
        pass
    def render(self):
        super().render()
        self.renderBackground()
        self.renderSlots()
    def renderSlots(self):
        for slot in self.Slots:
            slot.render(self)
    def updateSlots(self):
        for slot in self.Slots:
            slot.update(self)
    def updateBackground(self):
        pass
    def update(self):
        super().update()
        self.updateBackground()
        self.updateSlots()
    
PLAYER_INV_IMAGE = load("Player_GUI")
PLAYER_INV_IMAGE = PLAYER_INV_IMAGE.scaled(PLAYER_INV_IMAGE.width()*SCALE,PLAYER_INV_IMAGE.height()*SCALE)
class PlayerInventoryGUI(InventoryGUI):
    def __init__(self, inventory,game) -> None:
        super().__init__(inventory,game)
    def createSlots(self):
        for x in range(len(self.Inventory.slots())):
            self.createSlot(Slot([(x%5)*(SCALE*16+16)-(SCALE*16+16)*2,math.floor(x/5)*(SCALE*16+16)-(SCALE*8+8)*3],[SCALE*16,SCALE*16],x,self))
    def renderBackground(self):
        paint = self.getThisPainter()
        paint.drawImage(QRectF(centerImage(QPointF(self.Game.rScreen.width()/2,self.Game.rScreen.height()/2),PLAYER_INV_IMAGE),QSizeF(PLAYER_INV_IMAGE.size())),PLAYER_INV_IMAGE)
    def renderSlots(self):
        super().renderSlots()
        paint = self.getThisPainter()
        pos = self.Game.rScreen.mousePos()
        if self.Inventory.mouseSlot(): 
            paint.drawImage(QRectF(QPointF(pos.x()-SCALE*15*0.5,pos.y()-SCALE*16*0.5),QSizeF(SCALE*16,SCALE*16)),self.Inventory.mouseSlot().getMaterial().getImage())
            paint.scale(4,4)
            paint.setPen(QColor(200,200,200,255))
            paint.drawText(QPointF((pos.x()-SCALE*15*0.5-8)/4,(pos.y()+SCALE*16*0.5)/4),str(self.Inventory.mouseSlot().getCount()))
            
class Inventory:
    __Slots = []
    __Size = 0
    __Name = ""
    def __init__(self,name,slots) -> None:
        self.__Name = name
        self.__Size = slots
        for x in range(slots):
            self.__Slots.append(None)
    def slots(self):
        return self.__Slots.copy()
    def get(self,slot):
        if slot>=len(self.__Slots): return None
        return self.__Slots[slot]
    def set(self,slot,itemStack):
        if slot>=len(self.__Slots): return None
        self.__Slots[slot] = itemStack
    def add(self,itemStack):
        x = 0
        for slot in self.__Slots:
            if itemStack.getCount()<1:
                return True
            if slot:
                if slot.getMaterial()==itemStack.getMaterial():
                    count = slot.getCount()+itemStack.getCount()
                    size = slot.getMaterial().getStacksize()
                    overflow = count-size
                    slot.setCount(count if count<=size else size)
                    itemStack.setCount(overflow)
            else:
                if itemStack.getCount()>itemStack.getMaterial().getStacksize():
                    stack = itemStack.copy()
                    stack.setCount(stack.getMaterial().getStacksize())
                    self.__Slots[x] = stack
                    itemStack.setCount(itemStack.getCount()-itemStack.getMaterial().getStacksize())
                else:
                    self.__Slots[x] = itemStack
                    return True
            x+=1
        return False
        
            
    def drop(self,itemStack):
        pass
    # Do smth
    def remove(self,itemStack):
        if self.__Slots.count(itemStack):
            self.__Slots.remove(itemStack)
    def clear(self,material=None):
        if material:
            for i in range(len(self.__Slots)):
                if self.__Slots[i]:
                    if self.__Slots[i].getMaterial()==material:
                        self.__Slots[i] = None
        else:
            self.__Slots = [None for x in range(len(self.__Slots))]
class PlayerInventory(Inventory):
    __mouse = None
    def __init__(self) -> None:
        super().__init__("Inventory",20)
    def mouseSlot(self):
        return self.__mouse
    def setMouseSlot(self,itemStack):
        self.__mouse = itemStack
    
    
SLOT_IMAGE = load("Slot")
SLOT_IMAGE = SLOT_IMAGE.scaled(SLOT_IMAGE.width()*SCALE,SLOT_IMAGE.height()*SCALE)
SLOT_IMAGE_HOVER = SLOT_IMAGE.copy()
p = QPainter(SLOT_IMAGE_HOVER)
m = QBitmap(SLOT_IMAGE_HOVER.createAlphaMask())
p.setClipRegion(QRegion(m))
p.setPen(QColor(0,0,0,0))
p.setBrush(QColor(255,255,255,50))
p.drawRect(SLOT_IMAGE_HOVER.rect())
class Slot:
    __ItemStack = None
    __Pos = None
    __Size = None
    __Index = 0
    __Inventory = None
    __Pressed = False
    def __init__(self,pos:list,size:list,index,inv) -> None:
        self.setPos(pos)
        self.setSize(size)
        self.setIndex(index)
        self.setInventory(inv)
        self.hovered = False
    # Position
    def setPos(self,pos:list):
        self.__Pos = list(pos)
        return self
    def pos(self):
        return self.__Pos
    
    # MouseSlot - Extend from Player's Inventory
    def setMouseSlot(self,itemStack):
        self.inventory().Game.Player.inventory.setMouseSlot(itemStack)
        return self
    def mouseSlot(self):
        return self.inventory().Game.Player.inventory.mouseSlot()
    
    # ItemStack
    def setItemStack(self,itemStack):
        self.__ItemStack = itemStack
        self.inventory().Inventory.set(self.index(),self.__ItemStack)
    def itemStack(self):
        return self.__ItemStack
    
    # Size
    def setSize(self,size):
        self.__Size = list(size)
        return self
    def size(self):
        return self.__Size
    
    # Inventory
    def setInventory(self,inv):
        self.__Inventory = inv
    def inventory(self):
        return self.__Inventory

    # Index
    def setIndex(self,index):
        self.__Index = index
    def index(self):
        return self.__Index
    
    # AABB
    def AABB(self):
        p = self.inventory().Game.rScreen.size()
        p = [p.width()/2,p.height()/2]
        return AABB([self.pos()[x]-self.size()[x]/2+p[x] for x in range(2)],[self.pos()[x]+self.size()[x]/2+p[x] for x in range(2)])
    
    # Update
    def update(self,inventory):
        self.setInventory(inventory)
        if inventory.Inventory.get(self.index())!=self.itemStack():
            self.__ItemStack = inventory.Inventory.get(self.index())
        pos = inventory.Game.rScreen.mousePos()
        colls = inventory.tree.getCollisions(AABB([pos.x(),pos.y()],[pos.x()+1,pos.y()+1]))
        objs = [obj.obj for obj in colls]
        if objs.count(self):
            self.hovered = True
        else:
            self.hovered = False
        if inventory.Game.rScreen.mouseButton(0) or inventory.Game.rScreen.mouseButton(2):
            if inventory.Game.rScreen.mouseButton(0):
                if not self.__Pressed and self.hovered:
                    item = self.itemStack()
                    if self.mouseSlot():
                        if item:
                            if item.getMaterial()==self.mouseSlot().getMaterial():
                                count = item.getCount()+self.mouseSlot().getCount()
                                maxcount = self.mouseSlot().getMaterial().getStacksize()
                                if count<=maxcount:
                                    self.itemStack().setCount(count)
                                    self.setMouseSlot(None)
                                else:
                                    self.itemStack().setCount(maxcount)
                                    self.mouseSlot().setCount(count-maxcount)
                            else:
                                self.setItemStack(self.mouseSlot())
                                self.setMouseSlot(item)
                        else:
                            self.setItemStack(self.mouseSlot())
                            self.setMouseSlot(item)
                    else:
                        self.setItemStack(self.mouseSlot())
                        self.setMouseSlot(item)
            else:
                if not self.__Pressed and self.hovered:
                    item = self.itemStack()
                    
                    if self.mouseSlot():
                        if item:
                            if self.mouseSlot().getMaterial()==item.getMaterial():
                                if item.getCount()<item.getMaterial().getStacksize():
                                    if self.mouseSlot().getCount()<=1:
                                        self.itemStack().setCount(item.getCount()+self.mouseSlot().getCount())
                                    else:
                                        self.itemStack().setCount(item.getCount()+1)
                                        self.mouseSlot().setCount(self.mouseSlot().getCount()-1)
                            else:
                                self.setItemStack(self.mouseSlot())
                                self.setMouseSlot(item)
                        else:
                            self.setItemStack(self.mouseSlot().clone().setCount(1))
                            self.mouseSlot().setCount(self.mouseSlot().getCount()-1)
                            if self.mouseSlot().getCount()<=0:
                                self.setMouseSlot(None)
                    elif item:
                        count = self.itemStack().getCount()
                        diff = math.ceil(count/2)
                        self.setMouseSlot(self.itemStack().clone().setCount(diff))
                        if count-diff>0:
                            self.itemStack().setCount(count-diff)
                        else:
                            self.setItemStack(None)
            self.__Pressed = True
        elif not inventory.Game.rScreen.mouseButton(0):
            self.__Pressed = False
            
    def render(self,inventory):
        paint:QPainter = inventory.getThisPainter()
        pos = inventory.Game.rScreen.size()
        pos = QPointF(pos.width()/2,pos.height()/2)
        paint.translate(pos)
        paint.drawImage(QRectF(QPointF(self.pos()[0]-self.size()[0]/2,self.pos()[1]-self.size()[1]/2),QSizeF(self.size()[0],self.size()[0])),SLOT_IMAGE_HOVER if self.hovered else SLOT_IMAGE)
        if self.itemStack(): 
            paint.drawImage(QRectF(QPointF(self.pos()[0]-self.size()[0]*0.4,self.pos()[1]-self.size()[1]*0.4),QSizeF(self.size()[0]*0.8,self.size()[1]*0.8)),self.itemStack().getMaterial().getImage())
            paint.scale(4,4)
            paint.setPen(QColor(200,200,200,255))
            paint.drawText(QPointF((self.pos()[0]-self.size()[0]*0.4-8)/4,(self.pos()[1]+self.size()[1]*0.4)/4),str(self.itemStack().getCount()))
            