import pygame
import utils
from Player import Player
from Shot import Shot
from variables import screen

class QuadTree:
    
    # +---+
    #   0 1
    # 0|* *\
    # 1|* *\
    # +---+
    
    def __init__(self, parent, minh = 0,maxh = 0,minw = 0, maxw = 0):
        self.parent = parent
        self.min_height = minh
        self.max_height = maxh
        self.min_width  = minw
        self.max_width  = maxw
        self.half_height  = int((self.min_height + self.max_height)/ 2)
        self.half_width  = int((self.min_width + self.max_width)/ 2)
        self.parent = parent
        self.elements = set()
        self.min_requirement = 50
        self.quads = None
        
        
    def divide_quad(self):
        
        quad0 = QuadTree(self, self.min_height, self.half_height, self.min_width, self.half_width)
        quad1 = QuadTree(self, self.min_height, self.half_height, self.half_width, self.max_width)
        quad2 = QuadTree(self, self.half_height, self.max_height, self.min_width, self.half_width)
        quad3 = QuadTree(self, self.half_height, self.max_height, self.half_width, self.max_width)
        self.quads = [[quad0, quad1], [quad2, quad3]]
        
    def insert(self, obj):
        try:
            posy1, posy2, posx1, posx2 = self.get_coords(obj)
            if posy1 == posy2 and posx1 == posx2 and self.can_divide() and(posy1>=0 and posy2<=1 and posx1>=0 and posx2<=1):
                #Insert into one small quad
                if self.quads == None:
                    self.divide_quad()
                self.quads[posy1][posx1].insert(obj)
            else:
                #Insert into selected quad
                self.elements.add(obj)
        except Exception as e:
            print(e)
        
    def can_divide(self):
        return self.max_width - self.min_width > self.min_requirement
            
        
    def get_coords(self, obj):
        rect = obj.rect
        size = rect.size
        
        y1, x1  = int(rect.top) + 150, int(rect.left) + 150
        y2, x2 = y1 + int(size[1]), x1 + int(size[0])
    
        posy1 = y1 // (self.half_height + 300)
        posy2 = y2 // (self.half_height + 300)
        
        posx1 = x1 // (self.half_width + 300)
        posx2 = x2 // (self.half_width + 300)
        return posy1, posy2, posx1, posx2
        
        
    def draw_self(self):
        
        if self.quads != None:
            self.quads[0][0].draw_self()
            self.quads[0][1].draw_self()
            self.quads[1][0].draw_self()
            self.quads[1][1].draw_self()
        else:
            rect = pygame.Rect(self.min_width, self.min_height, self.max_width - self.min_width, self.max_height - self.min_height)
            
            pygame.draw.rect(screen, (0,0,255), rect, 2)
        
        
        
        
        
    def check_collisions(self, obj):
        posy1, posy2, posx1, posx2 = self.get_coords(obj)
        #return None
        for x in self.elements:
            if x != obj and utils.collide(obj, x):
                return x
        if self.quads != None:
            if posy1 >= 0 and posy2<=1 and posx1 >=0 and posx2 <=1:
                if posy1 == posy2 and posx1 == posx2:
                    result = self.quads[posy1][posx1].check_collisions(obj)
                    if result!= None:
                        return result
                else:
                    for y in range(0, 2):
                        for x in range(0, 2):
                            result = self.quads[y][x].check_collisions(obj)
                            if result != None:
                                return result
        return None
    