import pygame
import math
from variables import screen
class Player:
    
    def __init__(self):
        self.lives = 3
        #position
        self.y = 0
        self.x = 0
        self.image = None
        self.rotated_player = None
        
        #Movement variables
        self.vel_forwards = 0
        self.vel_right = 0
        self.acc_forwards = 0
        self.acc_right = 0
        self.rotation = 0
        
        #Speed variables
        self.turning_speed = 2
        self.boost_speed = 1
        self.constant_speed = 2
        self.slow_speed = 1
        self.max_forwards_speed = 6
        self.max_turning_speed = 4
        
        
    def move(self):
        print(self.vel_forwards)
        if self.acc_forwards == 0:
            self.reset_forwards_speed()
        else:
            self.vel_forwards += self.acc_forwards * 0.1 if self.vel_forwards < self.max_forwards_speed else 0
            
            
        self.y -= self.vel_forwards * math.cos( math.radians(self.rotation))
        self.x -= self.vel_forwards * math.sin(math.radians(self.rotation))
        
        if self.acc_right == 0:
            self.reset_rotation_speed()
        else:
            self.vel_right += self.acc_right * 0.1 if self.vel_forwards < self.max_turning_speed else 0
            
        self.rotation += self.vel_right
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
        elif self.vel_right <0:
            self.vel_right += 0.1
    
    
    def draw_self(self):
        screen.blit(self.rotated_player, (self.x,self.y))
    
    
    