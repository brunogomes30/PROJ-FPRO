import math
import pygame
from BaseObject import BaseObject
from variables import *

player_shot = pygame.image.load("images/shot.png")
enemy_shot = pygame.image.load("images/enemy_shot.png")
class Shot(BaseObject):
    def __init__(self, enemy = False):
        super().__init__()
        if enemy:
            self.image = enemy_shot
        else:
            self.image = player_shot
        self.mask = pygame.mask.from_surface(self.image)
        shot_sound = pygame.mixer.Sound("sounds/player_shot.wav")
        self.sound = shot_sound
        self.speed = 750
        self.damage = 50
        self.harm_player = False
        self.sender = None
    def move(self):
        super().move()
        w, h = self.image.get_size()
        box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(self.rotation) for p in box]
        min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
        origin = (self.x + min_box[0], self.y - max_box[1])
        self.origin = origin
        
        self.rect = pygame.Rect(origin[0], origin[1], self.rotated_image.get_rect().size[0], self.rotated_image.get_rect().size[1])
        
        
   
        
        