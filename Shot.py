import math
import pygame
from variables import *


class Shot:
    def __init__(self):
        self.y = 0
        self.x = 0
        self.speed = 15
        self.rotation = 0
        self.shot = None
        self.rotated_shot = None
        
    def move(self):
        self.rotated_shot = pygame.transform.rotate(self.shot,self.rotation)
        self.y -= self.speed* math.cos( math.radians(self.rotation)) 
        self.x -= self.speed * math.sin(math.radians(self.rotation)) 
    
    
    def draw_self(self):
        screen.blit(self.rotated_shot, (self.x,self.y))
        