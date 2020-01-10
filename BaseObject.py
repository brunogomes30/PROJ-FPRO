import pygame
import math
import variables
from variables import screen, time_delta
from HitBox import HitBox

class BaseObject(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.y = 0
        self.x = 0
        self.rotation = 0
        self.speed = 0
        self.rotated_image = None
        self.image = None
        self.hitbox = None
        self.mask = None
        self.hp = 100
        self.isEnemy = False
        
    def move(self):
        w, h = self.image.get_size()
        self.rotated_image = pygame.transform.scale(self.image, (int(w * (self.hp + 75 )/100), int(h * (self.hp + 50)/100)))
        self.rotated_image = pygame.transform.rotate(self.rotated_image, self.rotation)
        
        self.y -= (self.speed * math.cos(math.radians(self.rotation)))  * variables.time_delta
        self.x -= (self.speed * math.sin(math.radians(self.rotation)))  * variables.time_delta
        
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
        self.rect = pygame.Rect(origin[0], origin[1], w, h)
    
    def draw_self(self):
        w, h = self.image.get_size()
        #self.rotated_image = pygame.transform.scale(self.image, (int(w * (self.hp + 75 )/100), int(h * (self.hp + 50)/100)))
        #self.rotated_image = pygame.transform.rotate(self.rotated_image,self.rotation)
        screen.blit(self.rotated_image, self.origin)
        self.mask = pygame.mask.from_surface(self.rotated_image)
        #pygame.draw.rect(screen, (0, 255, 0), self.rect, 1)
        #pygame.draw.circle(screen, (0,255,0), (int(self.x), int(self.y)), 2)
        
    
    def load_hitbox(self):
        self.hitbox = HitBox(self.rotated_image.get_rect())
    
    def get_center(self):
        width, height = self.image.get_size()
        inner_angle = math.atan(height/width) + math.pi*0.5 - 0.25
        hyp = ((width ** 2 + height ** 2) ** 0.5 )/2
        radians = math.radians(self.rotation) + inner_angle
        real_y = self.y + hyp * math.sin(radians)
        real_x = self.x - hyp * math.cos(radians)
        return real_y, real_x