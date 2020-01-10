import random
import math
import pygame
import variables
from variables import *
from BaseObject import BaseObject
from Shot import Shot
enemy_image = pygame.image.load('images/enemyT2.png')
class EnemyT2(BaseObject):
    
    
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.last_shot = 0
        self.shot_interval = 1.5 #s
        self.score = 100
        self.isEnemy = True
    
    def spawn(self):
        n = variables.curr_position_to_spawn
        if n % 2 == 0:
            #Spawn UP or DOWN
            self.y = variables.SPAWN_HEIGHT[0] if n == 0 else variables.SPAWN_HEIGHT[1]
            self.x = variables.locations_to_spawn[n][variables.positions_to_spawn[n]]
            #self.speed[0] = random.randint(-maxspeed * 0.5, maxspeed * 0.5) / 100
        else:
            #Spawn LEFT or RIGHT
            self.x = variables.SPAWN_WIDTH[0] if n == 1 else variables.SPAWN_WIDTH[1]
            self.y = variables.locations_to_spawn[n][variables.positions_to_spawn[n]]
        self.speed = 100
        #self.x = 200
        #self.y = 500
        player = variables.player
        center = self.get_center()
        center = (center[1], center[0])
        player_center = player.get_center()
        player_center = (player_center[1],player_center[0])
        diffx = (player_center[0] - center[0])
        diffy = (player_center[1] - center[1])
        
        self.rotation = math.degrees(math.atan(diffx/diffy))
        
        if(diffy < 0):
            self.rotation += 180
        self.rotation += 180
        
        
        
        
        self.speed = self.speed * math.sin(math.radians(self.rotation)), self.speed * math.cos(math.radians(self.rotation))
        self.refresh_spawn_position()
        variables.all_entities.add(self)
    
    def move(self):
        w, h = self.image.get_size()
        
        self.rotated_image = pygame.transform.scale(self.image, (int(w * (self.hp)/100), int(h * (self.hp)/100)))
        #self.rotated_image = pygame.transform.rotate(self.rotated_image, self.rotation)
        
        self.y -= (self.speed[1])  * variables.time_delta
        self.x -= (self.speed[0])  * variables.time_delta
        
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
        
    
    def shoot(self):
        player = variables.player
        now = variables.time
        if(self.last_shot != None and now - self.last_shot < self.shot_interval ):
            return
        self.last_shot = variables.time
        center = self.get_center()
        center = (center[1], center[0])
        shot = Shot(True)
        shot.sender = self
        shot.harm_player = True
        shot.x, shot.y = center[0], center[1]
        #Make shot follow player
        shot.speed = 250
        
        player_center = player.get_center()
        player_center = (player_center[1],player_center[0])
        diffx = (player_center[0] - center[0])
        diffy = (player_center[1] - center[1])
        
        
        shot.rotation = math.degrees(math.atan(diffx/diffy))
        if(diffy < 0):
            shot.rotation += 180
        shot.rotation += 180
        shot.move()
        
        variables.entities_to_add.add(shot)
        
    def refresh_spawn_position(self):
        pos = variables.curr_position_to_spawn
        variables.positions_to_spawn[pos] += 1
        if variables.positions_to_spawn[pos] >= len(variables.locations_to_spawn[pos]):
            variables.positions_to_spawn[pos] = 0
        variables.curr_position_to_spawn = random.randint(0,3)
        
    def get_center(self):
        if self.rotated_image != None:
            w, h = self.rotated_image.get_size()
        else:
            w, h = self.image.get_size()
        return (self.y + h/2, self.x + w/2)