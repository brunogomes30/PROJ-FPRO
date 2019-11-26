import time
import pygame
import math
from variables import screen
import variables
from Shot import Shot
class Player:
    
    def __init__(self):
        self.lives = 3
        #position
        self.y = 0
        self.x = 0
        self.image = None
        self.rotated_player = None
        
        #Movement variables
        self.momentum_y = 0
        self.momentum_x = 0
        self.vel_forwards = 0
        self.vel_right = 0
        self.acc_forwards = 0
        self.acc_right = 0
        self.rotation = 0
        
        #Speed variables
        self.turning_speed = 3
        self.boost_speed = 3
        self.constant_speed = 5
        self.slow_speed = 1
        self.max_forwards_speed = 8
        self.min_forwards_speed = 1
        self.max_turning_speed = 3
        
        #Shot
        self.last_shot = None
        self.shot_interval = 0.2
        
    def move(self):
        if self.acc_forwards == 0:
            self.reset_forwards_speed()
        else:
            self.vel_forwards += self.acc_forwards * 0.1 if self.min_forwards_speed < self.vel_forwards < self.max_forwards_speed else 0
            
            
        self.y -= self.vel_forwards * math.cos( math.radians(self.rotation)) + self.momentum_y
        self.x -= self.vel_forwards * math.sin(math.radians(self.rotation)) + self.momentum_x
        self.momentum_y = -self.vel_forwards * math.cos( math.radians(self.rotation)) * 0.5
        self.momentum_x = -self.vel_forwards * math.sin(math.radians(self.rotation)) * 0.5
        
        if self.acc_right == 0:
            self.reset_rotation_speed()
        else:
            self.vel_right += self.acc_right * 0.5 if -self.max_turning_speed < self.vel_right< self.max_turning_speed else 0
        
        self.rotation += self.vel_right * (abs(self.vel_forwards / 8))
        self.rotated_player = pygame.transform.rotate(self.image,self.rotation)
        
        #rad_angle =  self.rotation *math.pi/180
        
    def reset_forwards_speed(self):
        if self.vel_forwards > self.constant_speed:
            self.vel_forwards -= 0.1
        elif self.vel_forwards < self.constant_speed:
            self.vel_forwards += 0.1
        
    def reset_rotation_speed(self):
        if self.vel_right > 0:
            self.vel_right -= 0.1
        elif self.vel_right <=0:
            self.vel_right += 0.1
    
    
    def fire(self):
        now = time.time()
        if(self.last_shot != None and now - self.last_shot < self.shot_interval ):
            return
        self.last_shot = now
        shot = Shot()
        shot.shot = pygame.image.load("images\\shot.png")
        shot.y = self.y
        shot.x = self.x
        shot.rotation = self.rotation
        #shot.move()
        variables.all_entities.append(shot)
        
    
    def draw_self(self):
        screen.blit(self.rotated_player, (self.x,self.y))
    
    
    