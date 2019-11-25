from Player import Player
from pygame import *
from variables import screen
import pygame
import math

#screen = pygame.display.set_mode((800, 600))


player = Player()
player.image = pygame.image.load('images\\player.png')
player.y = 300
player.x = 300

clock = pygame.time.Clock()
running = True

"""
vel = 0
acc = 0
angle = 0
rotate = 0
rotation_speed = 0.01
plane_speed = 0.05

"""

keys = {K_a : False,
        K_d : False,
        K_w : False,
        K_s : False
        }
while running:
    for event in pygame.event.get():
        #keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            keys[event.key] = True
        elif event.type == pygame.KEYUP:
            keys[event.key] = False
    
    if keys[K_a]:
        player.acc_right = player.turning_speed
    elif keys[K_d]:
        player.acc_right = -player.turning_speed
    else:
        player.acc_right = 0
        
    if keys[K_w]:
        player.acc_forwards = player.boost_speed
    elif keys[K_s]:
        player.acc_forwards = player.slow_speed
    else:
        player.acc_forwards = 0
    
    player.move()
    #rotated_plane = pygame.transform.rotate(plane,angle)
    #rad_angle = angle*math.pi/180
    #x += acc*math.cos(rad_angle)
    #y += acc*math.sin(rad_angle)
    screen.fill((255,255,255))
    #screen.blit(rotated_plane, (x,y))
    player.draw_self()
    
    pygame.display.flip()
    
    clock.tick(60)