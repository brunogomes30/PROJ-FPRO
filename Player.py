import threading
import time
import pygame
import math
from BaseObject import BaseObject
from variables import screen , time_delta
import variables
from Shot import Shot
class Player (BaseObject):
    
    def __init__(self):
        super().__init__()
        self.lives = 3
        self.score = 0
        self.invulnerable = False
        self.ialpha = 0
        self.alpha = 255
        #Movement variables
        self.momentum_y = 0
        self.momentum_x = 0
        self.vel_forwards = 0
        self.vel_right = 0
        self.acc_forwards = 0
        self.acc_right = 0
        self.rotation = 0
        
        #Speed variables
        self.turning_speed = variables.DEFAULT_TURNING_SPEED #* time_delta
        self.boost_speed = 5 #* time_delta
        self.constant_speed = 5 #* time_delta
        self.slow_speed = 5 #* time_delta
        self.max_forwards_speed = 55 #* time_delta * 100000
        self.min_forwards_speed = 0 #* time_delta
        self.max_turning_speed = 12 #* time_delta
        
        #Shot
        self.last_shot = None
        self.shot_interval = 0.2  #* 0.001
        
    def move(self):
        if self.acc_forwards == 0:
            self.reset_forwards_speed()
        else:
            self.vel_forwards += self.acc_forwards * 0.1 if self.min_forwards_speed < self.vel_forwards < self.max_forwards_speed else 0
            
        self.y -= (self.vel_forwards * math.cos( math.radians(self.rotation)) + self.momentum_y) * (variables.time_delta + 1/variables.FPS / 2) * 10
        self.x -= (self.vel_forwards * math.sin( math.radians(self.rotation)) + self.momentum_x) * (variables.time_delta + 1/variables.FPS / 2) * 10
        self.momentum_y = (-self.vel_forwards * math.cos( math.radians(self.rotation)) * 0.5 ) #* time_delta
        self.momentum_x = (-self.vel_forwards * math.sin(math.radians(self.rotation)) * 0.5 ) #* time_delta
        
        if self.acc_right == 0:
            self.reset_rotation_speed()
        else:
            self.vel_right += self.acc_right * 0.2 if -self.max_turning_speed < self.vel_right< self.max_turning_speed else 0
        
        self.rotation += self.vel_right * (abs(self.vel_forwards / 8)) * ((variables.time_delta + 1/variables.FPS/2) * 3)
        self.rotated_image = pygame.transform.rotate(self.image,self.rotation)
        
        w, h = self.image.get_size()
        box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(self.rotation) for p in box]
        min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
        self.origin = (self.x + min_box[0], self.y - max_box[1])
        self.rect = pygame.Rect(self.origin[0], self.origin[1], self.rotated_image.get_rect().size[0], self.rotated_image.get_rect().size[1])
        #rad_angle =  self.rotation *math.pi/180
        self.mask = pygame.mask.from_surface(self.rotated_image)
        
        
    def reset_forwards_speed(self):
        if self.vel_forwards > self.constant_speed:
            self.vel_forwards -= 0.1 
        elif self.vel_forwards < self.constant_speed:
            self.vel_forwards += 0.1 
    
    def draw_self(self):
        center = self.get_center()
        
        if(self.alpha < 255):
            self.rotated_image = self.rotated_image.convert()
        
        self.alpha += self.ialpha
        if self.alpha > 255:
            self.ialpha = -self.ialpha
            self.alpha  = 255
        elif self.alpha < 0:
            self.ialpha = -self.ialpha
            self.alpha = 0
        
        self.rotated_image.set_alpha(self.alpha)
        screen.blit(self.rotated_image, self.origin)
        #pygame.draw.circle(screen, (0,0,255), (int(center[1]), int(center[0])), 2)
        #pygame.draw.circle(screen, (0,0,255), (int(self.x), int(self.y)), 2)
        
        
        self.load_hitbox()
        
        
        
        
        #pygame.draw.rect(screen, (0, 255, 0), self.rect, 1)
        if self.invulnerable:
            pass
#        print(self.rect)
        
    def reset_rotation_speed(self):
        if self.vel_right > 0:
            self.vel_right -= 100 * time_delta
        elif self.vel_right <=0:
            self.vel_right += 100 * time_delta
    
    
    def fire(self):
        now = time.time()
        if(self.last_shot != None and now - self.last_shot < self.shot_interval ):
            return
        self.last_shot = now
        shot = Shot()
        
        #shot.sound.play()
        center = self.get_center()
        shot.y = center[0]
        shot.x = center[1]
        shot.rotation = self.rotation
        shot.move()
        variables.all_entities.add(shot)
        
    def get_hit(self):
        self.lives -=1
        self.invulnerable = True
        t = threading.Timer(5,self.set_vulnerable)
        self.ialpha = -5
        t.start()
        
    def set_vulnerable(self):   
        self.invulnerable = False
        self.alpha = 255
        self.ialpha = 0