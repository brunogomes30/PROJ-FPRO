import pygame
import variables
from variables import time_delta, screen

class Background_entity:
    
    def __init__(self):
        self.y = 0
        self.x = 0
        self.z = 0
        self.image = None
        self.speed = (0, 0, 0)
        #self.size = self.image.get_size()
        
    def move(self):
        self.y += self.speed[1] * variables.time_delta
        self.x += self.speed[0] * variables.time_delta
        self.z += self.speed[2] * variables.time_delta
        
        self.size = self.image.get_size()
        size = self.size
        scale_ratio = (1 + self.z / size[0] , 1+ self.z / size[0])
        if scale_ratio[0] < 0 or scale_ratio[1] < 0:
            scale_ratio = 0, 0
            variables.entities_to_remove.add(self)
            return
        if self.y > variables.HEIGHT or self.x > variables.WIDTH or self.y + size[1] < 0 or self.x + size[0] < 0:
            variables.entities_to_remove.add(self)
            return
        self.final_image = pygame.transform.scale(self.image, (int(scale_ratio[0] * size[0]), int(scale_ratio[1] * size[1])))
        
    def draw_self(self):
        screen.blit(self.final_image, (self.x, self.y))