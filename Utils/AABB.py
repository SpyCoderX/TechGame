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
        if tree.getCollisions(self):
            pygame.draw.rect(screen,(255,0,0),[self.rect[0][0],self.rect[0][1],self.rect[1][0]-self.rect[0][0],self.rect[1][1]-self.rect[0][1]],1)
        else:
            pygame.draw.rect(screen,(255,255,255),[self.rect[0][0],self.rect[0][1],self.rect[1][0]-self.rect[0][0],self.rect[1][1]-self.rect[0][1]],1)


class AABBBranch(AABB):
    def __init__(self,left:AABB,right:AABB) -> None:
        if left:left.ssuper = self
        self.left = left
        if right: right.ssuper = self
        self.right = right
        if self.left!=None and self.right!=None:
            super().__init__(self.left.rect[0],self.left.rect[1])
            self.expand(right)
        else:
            super().__init__([0,0],[0,0])
        

    def setLeft(self,left:AABB):
        self.left = left
        if self.right==None:
            self.rect = self.left.rect.copy()
        else:
            self.rect = self.right.rect.copy()
            self.expand(left)

    def setRight(self,right:AABB):
        self.right = right
        if self.left==None:
            self.rect = self.right.rect.copy()
        else:
            self.rect = self.left.rect.copy()
            self.expand(right)

    def add(self,AB:AABB,obj):
        self.expand(AB)
        if self.left == None:
            self.setLeft(AABBLeaf(AB,obj))
        elif self.right == None:
            self.setRight(AABBLeaf(AB,obj))
        else:
            p1 = self.left.expandCopy(AB).perimeter()
            p2 = self.right.expandCopy(AB).perimeter()
            if p1 <= p2:
                if isinstance(self.left,AABBLeaf):
                    self.setLeft(AABBBranch(self.left,AABBLeaf(AB,obj)))
                else:
                    self.left.add(AB,obj)
            else:
                if isinstance(self.right,AABBLeaf):
                    self.setRight(AABBBranch(self.right,AABBLeaf(AB,obj)))
                else:
                    self.right.add(AB,obj)
    
    def remove(self,obj,upper):
        if self.left:self.left.remove(obj,self)
        if self.right: self.right.remove(obj,self)

    def recalc(self,upper):
        if isinstance(self.left,AABBBranch): self.left.recalc(self)
        if isinstance(self.right,AABBBranch): self.right.recalc(self)
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

    def draw(self,screen):
        self.left.draw(screen)
        if self.right:self.right.draw(screen)

class AABBLeaf(AABB):
    def __init__(self,AB:AABB,obj) -> None:
        super().__init__(AB.rect[0],AB.rect[1])
        self.obj = obj
    def remove(self,obj,upper):
        if self.obj==obj:
            if upper.left==self: upper.left = None
            if upper.right==self: upper.right = None
    

class AABBTree(AABBBranch):
    def __init__(self) -> None:
        super().__init__(None,None)
        
    
    def getCollisions(self, AB):
        colls = [self] # Current objects to check for collisions... kinda
        collisions = []
        while colls: # Simpler len(colls)>0
            c = colls.pop(0)
            if c==AB:continue
            if c.collides(AB):
                if isinstance(c,AABBBranch):
                    colls.append(c.left)
                    if c.right:colls.append(c.right)
                else:
                    collisions.append(c)
        return collisions
    
    def update(self,AB,obj):
        self.remove(obj)
        self.recalc()
        self.add(AB,obj)
    def recalc(self):
        return super().recalc(self)
    def remove(self, obj):
        return super().remove(obj, self)
    
        
   
    
    
    
if __name__ == "__main__":
    # Some pygame testing code. Used to make sure the system works
    import pygame
    import random
    tree = AABBTree()
    AB = AABB([20,20],[40,40])
    # AB2 = AABB([0,0],[1000,1000])
    for x in range(1000):
        mx,my = [random.randint(0,1200),random.randint(0,800)]
        tree.add(AABB([mx-10,my-10],[mx+10,my+10]),x)
    tree.add(AB,"mouse")
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((1200,800))
    run = True
    while run:
        screen.fill((0,0,0))
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                run=False
        mx,my = pygame.mouse.get_pos()
        AB = AABB([mx-10,my-10],[mx+10,my+10])
        tree.update(AB,"mouse")
    
        tree.draw(screen)
        pygame.display.update()
        clock.tick(60)