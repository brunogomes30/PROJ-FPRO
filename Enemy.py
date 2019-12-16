import random
import math
import pygame
import variables
from variables import *
from BaseObject import BaseObject
enemy_images = list(pygame.image.load('images/enemy'+str(i)+'.png') for i in range(1,7))
print(enemy_images)

class Enemy(BaseObject):
    def __init__(self):
        super().__init__()
        self.image = enemy_images[random.randint(0,5)]
        self.mask = pygame.mask.from_surface(self.image)
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
        """
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
            
        """
        n = variables.curr_position_to_spawn
        
        if n % 2 == 0:
            #Spawn UP or DOWN
            self.y = variables.SPAWN_HEIGHT[0] if n == 0 else variables.SPAWN_HEIGHT[1]
            self.x = variables.locations_to_spawn[n][variables.positions_to_spawn[n]]
            
            if n == 0:
                #Spawn UP
                self.speed[1] = random.randint(maxspeed *0.2, maxspeed) / 100
            else:
                #Spawn DOWN
                self.speed[1] = -random.randint(maxspeed *0.2, maxspeed) / 100
            
            self.speed[0] = random.randint(-maxspeed * 0.5, maxspeed * 0.5) / 100
        else:
            #Spawn LEFT or RIGHT
            self.x = variables.SPAWN_WIDTH[0] if n == 1 else variables.SPAWN_WIDTH[1]
            self.y = variables.locations_to_spawn[n][variables.positions_to_spawn[n]]
            
            if n == 1:
                #Spawn Right
                self.speed[0] = -random.randint(maxspeed * 0.2, maxspeed) / 100
            else:
                #Spawn Left
                self.speed[0] = random.randint(maxspeed * 0.2, maxspeed) / 100
            
            self.speed[1] = random.randint(-maxspeed * 0.5, maxspeed * 0.5) / 100
            
        self.refresh_spawn_position()
        all_entities.add(self)
    
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
        self.rotated_image = pygame.transform.scale(self.image, (int(w * (self.hp + 75 )/100), int(h * (self.hp + 50)/100)))
        self.rotated_image = pygame.transform.rotate(self.rotated_image,self.rotation)
        self.rect = pygame.Rect(self.x, self.y, self.rotated_image.get_rect().size[0], self.rotated_image.get_rect().size[1])
        
    def refresh_spawn_position(self):
        pos = variables.curr_position_to_spawn
        variables.positions_to_spawn[pos] += 1
        if variables.positions_to_spawn[pos] >= len(variables.locations_to_spawn[pos]):
            variables.positions_to_spawn[pos] = 0
        variables.curr_position_to_spawn = random.randint(0,3)