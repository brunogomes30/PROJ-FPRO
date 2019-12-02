import math
import pygame
from BaseObject import BaseObject
from variables import *


class Shot(BaseObject):
    def __init__(self):
        super().__init__()
        self.sound = pygame.mixer.Sound("sounds\\player_shot.wav")
        self.speed = 15
    
    def draw_self(self):
        w, h = self.image.get_size()
        box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(self.rotation) for p in box]
        min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
        origin = (self.x + min_box[0], self.y - max_box[1])
        self.rotated_image = pygame.transform.rotate(self.image, self.rotation)
        screen.blit(self.rotated_image, origin)
        