import math
import pygame
from BaseObject import BaseObject

class Enemy(BaseObject):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images\\enemy1.png')
        self.y = 0
        self.x = 0
        
        
    def move(self):
        self.rotation += 1
        super().move()
    
    