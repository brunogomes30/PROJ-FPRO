import random
import math
import pygame
import variables
from variables import *
from BaseObject import BaseObject

class Enemy(BaseObject):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images\\enemy'+str(random.randint(1,6))+'.png')
        self.asteroid_sound = pygame.mixer.Sound("sounds\\asteroids_impact.wav")
        self.y = 0
        self.x = 0
        self.speed = [0, 0]
        self.score = 20
        self.rotation_speed = random.randint(1,5)
        
    def move(self):
        self.rotation += self.rotation_speed
        super().move()
        
    def get_shot(self):
        w, h = self.image.get_size()
        
    def spawn(self):
        maxspeed = 8000
        if random.randint(0,2):
            #SPAWN DOWN
            self.y = random.randint(HEIGHT + 100, HEIGHT + 300)
            self.speed[1] = random.randint(-maxspeed, -int(maxspeed * 0.2)) /100
        else:
            #SPAWN UP
            self.y = - random.randint(100, 300)
            self.speed[1] = random.randint(maxspeed * 0.2, maxspeed) / 100
        
        if random.randint(0, 2):
            #SPAWN RIGHT
            self.x = random.randint(WIDTH + 100, WIDTH + 300)
            self.speed[0] = random.randint(-maxspeed, -maxspeed * 0.2) / 100
        else:
            #SPAWN LEFT
            self.x = - random.randint(100, 300)
            self.speed[0] = random.randint(maxspeed * 0.2, maxspeed) / 100
        all_entities.append(self)
    
    def move(self):
        self.rotation += 100 * variables.time_delta
        self.y += self.speed[1] * variables.time_delta
        self.x += self.speed[0] * variables.time_delta
        w, h = self.image.get_size()
        box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(self.rotation) for p in box]
        
        min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
        pivot = pygame.math.Vector2(w/2, -h/2)
        
        pivot_rotate = pivot.rotate(self.rotation)
        pivot_move = pivot_rotate - pivot
        origin = (self.x + min_box[0] - pivot_move[0], self.y - max_box[1] + pivot_move[1])
        self.origin = origin
        
