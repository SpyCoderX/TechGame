from typing import List
class AABB:
    def __init__(self,p1,p2) -> None:
        self.rect = [[min(p1[0],p2[0]),min(p1[1],p2[1])],[max(p1[0],p2[0]),max(p1[1],p2[1])]]
        
    def collides(self,AB):
        # Long collision checks,
        # but simple logic:
        # If self.min_x > AB.max_x: return false
        # Continue this for each side.
        return AB.rect[0][0]<=self.rect[1][0] and AB.rect[1][0]>=self.rect[0][0] and AB.rect[0][1]<=self.rect[1][1] and AB.rect[1][1]>=self.rect[0][1]
    def fixRect(self):
        # Recalculates the rect to make sure the points are the minimum and maximum.
        self.rect = [[min(self.rect[0][0],self.rect[1][0]),min(self.rect[0][1],self.rect[1][1])],[max(self.rect[0][0],self.rect[1][0]),max(self.rect[0][1],self.rect[1][1])]] 
        return self
    def expand(self,AB):
        self.fixRect()
        AB.fixRect()
        
        # Expands this object to fit AB, same equation as the init.
        self.rect = [[min(self.rect[0][0],AB.rect[0][0]),
                        min(self.rect[0][1],AB.rect[0][1])],
                        [max(self.rect[1][0],AB.rect[1][0]),
                         max(self.rect[1][1],AB.rect[1][1])]]
        
        return self
    def expandCopy(self,AB):
        # Copies this object, and expands it.
        return AABB(self.rect[0],self.rect[1]).expand(AB)
    def perimeter(self):
        return (self.rect[1][0]-self.rect[0][0])*2+(self.rect[1][1]-self.rect[0][1])*2
    def contains(self,AB):
        return AB.rect[0][0]>=self.rect[0][0] and AB.rect[0][1]>=self.rect[0][1] and AB.rect[1][0]<=self.rect[1][0] and AB.rect[1][1]<=self.rect[1][1]
    def draw(self,screen):
        if tree.getCollisions(self) and isinstance(self,AABBLeaf):
            pygame.draw.rect(screen,(255,0,0),[self.rect[0][0],self.rect[0][1],self.rect[1][0]-self.rect[0][0],self.rect[1][1]-self.rect[0][1]],1)
        else:
            pygame.draw.rect(screen,(255,255,255),[self.rect[0][0],self.rect[0][1],self.rect[1][0]-self.rect[0][0],self.rect[1][1]-self.rect[0][1]],1)
    def expandBy(self,val:int):
        self.fixRect() 
        self.rect = [[self.rect[0][0]-val,self.rect[0][1]-val],[self.rect[1][0]+val,self.rect[1][1]+val]]
        return self

class AABBBranch(AABB):
    def __init__(self,upper,left:AABB,right:AABB) -> None:
        self.upper = upper
        if left:left.upper = self
        self.left = left
        if right: right.upper = self
        self.right = right
        if self.left!=None:
            super().__init__(self.left.rect[0],self.left.rect[1])
            if self.right!=None:
                self.expand(right)
        elif self.right!=None:
            super().__init__(self.right.rect[0],self.right.rect[1])
        else:
            super().__init__([0,0],[0,0])
        
            
    def setLeft(self,left:AABB):
        left.upper = self
        self.left = left

        if self.right==None:
            self.rect = self.left.rect.copy()
        else:
            self.right.upper = self
            self.rect = self.right.rect.copy()
            self.expand(left)
            

    def setRight(self,right:AABB):
        right.upper = self
        self.right = right
        if self.left==None:
            self.rect = self.right.rect.copy()
        else:
            self.left.upper = self
            self.rect = self.left.rect.copy()
            self.expand(right)

    def add(self,AB:AABB,obj):
        self.expand(AB)
        if self.left == None:
            self.setLeft(AABBLeaf(self,AB,obj))
        elif self.right == None:
            self.setRight(AABBLeaf(self,AB,obj))
        else:
            p1 = self.left.expandCopy(AB).perimeter()
            p2 = self.right.expandCopy(AB).perimeter()
            if p1 <= p2:
                if isinstance(self.left,AABBLeaf):
                    self.setLeft(AABBBranch(self,self.left,AABBLeaf(self,AB,obj)))
                else:
                    self.left.add(AB,obj)
            else:
                if isinstance(self.right,AABBLeaf):
                    self.setRight(AABBBranch(self,self.right,AABBLeaf(self,AB,obj)))
                else:
                    self.right.add(AB,obj)
    
    def remove(self,obj,upper):
        if self.left: self.left.remove(obj,self)
        if self.right: self.right.remove(obj,self)
        

    def recalcDown(self,upper):
        if isinstance(self.left,AABBBranch): self.left.recalcDown(self)
        if isinstance(self.right,AABBBranch): self.right.recalcDown(self)
        if not self.left:
            if self.right:
                left = self.right
                self.right = None
                self.setLeft(left)
            else:
                if upper.left==self: upper.left = None
                if upper.right==self: upper.right = None
        else:
            self.setLeft(self.left)

    def recalcUp(self):
        self.recalc()
        if not isinstance(self,AABBTree):
            self.upper.recalcUp()
    
    def recalc(self):
        if not self.left:
            if self.right:
                left = self.right
                self.right = None
                self.setLeft(left)
            else:
                if self.upper.left==self: self.upper.left = None
                if self.upper.right==self: self.upper.right = None
        else:
            self.setLeft(self.left)
        if self.left and not self.right:
            if self.upper.left==self: self.upper.setLeft(self.left)
            if self.upper.right==self: self.upper.setRight(self.left)
            return

    def draw(self,screen):
        super().draw(screen)
        mx,my = pygame.mouse.get_pos()
        if self.contains(AABB([mx,my],[mx,my])) and not isinstance(self,AABBTree):
            pygame.draw.rect(screen,(0,0,150),[self.upper.rect[0][0],
                                               self.upper.rect[0][1],
                                               self.upper.rect[1][0]-self.upper.rect[0][0],
                                               self.upper.rect[1][1]-self.upper.rect[0][1],],3)
        self.left.draw(screen)
        if self.right:self.right.draw(screen)

class AABBLeaf(AABB):
    def __init__(self,upper,AB:AABB,obj) -> None:
        super().__init__(AB.rect[0],AB.rect[1])
        self.obj = obj
        self.upper = upper
    def remove(self,obj,upper):
        if self.obj==obj:
            if upper.left==self: upper.left = None
            if upper.right==self: upper.right = None
            upper.recalcUp()
            
    def draw(self, screen):
        super().draw(screen)
        mx,my = pygame.mouse.get_pos()
        if self.contains(AABB([mx,my],[mx,my])):
            pygame.draw.rect(screen,(0,0,255),[self.upper.rect[0][0],
                                               self.upper.rect[0][1],
                                               self.upper.rect[1][0]-self.upper.rect[0][0],
                                               self.upper.rect[1][1]-self.upper.rect[0][1],],3)
    

class AABBTree(AABBBranch):
    def __init__(self) -> None:
        super().__init__(None,None,None)
        
    
    def getCollisions(self, AB):
        colls = [self] # Current objects to check for collisions... kinda
        collisions = []
        while len(colls)>0: # Simpler len(colls)>0
            c = colls.pop(0)
            if c==AB:continue
            if c==None:continue
            if c.collides(AB):
                if isinstance(c,AABBBranch):
                    colls.append(c.left)
                    if c.right:colls.append(c.right)
                else:
                    collisions.append(c)
        return collisions
    
    def update(self,AB,obj):
        self.remove(obj)
        #self.recalcDown()
        self.add(AB,obj)
    def recalcDown(self):
        return super().recalcDown(self)
    def recalc(self):
        if not self.left:
            if self.right:
                left = self.right
                self.right = None
                self.setLeft(left)
        else:
            if self.right:
                self.setLeft(self.left)
    def remove(self, obj):
        return super().remove(obj,self)
    
        
   
    
    
    
if __name__ == "__main__":
    # Some pygame testing code. Used to make sure the system works
    import pygame
    import random
    tree = AABBTree()
    AB = AABB([20,20],[40,40])
    tree.add(AB,"mouse")
    for x in range(10):
        mx,my = (random.randint(20,700),random.randint(20,700))
        AB = AABB([mx-10,my-10],[mx+10,my+10])
        tree.add(AB,"mo")
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((1200,800))
    run = True
    down = False
    while run:
        screen.fill((0,0,0))
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                run=False
        mx,my = pygame.mouse.get_pos()
        AB = AABB([mx-10,my-10],[mx+10,my+10])
        if pygame.mouse.get_pressed()[0]:
            tree.update(AB,"mouse")
        
            
    
        tree.draw(screen)
        pygame.display.update()
        clock.tick(60)