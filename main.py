import time
from Player import Player
from pygame import *
from variables import screen,all_entities
import pygame
import math

#screen = pygame.display.set_mode((800, 600))


player = Player()
player.image = pygame.image.load('images\\player.png')

player.y = 300
player.x = 300
all_entities.append(player)
clock = pygame.time.Clock()
running = True

while running:
    
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
    
    
    if keys[K_a]:
        player.acc_right = player.turning_speed
        if player.vel_right < 0:
            player.vel_right = 0
        player.acc_forwards = player.turning_speed
    elif keys[K_d]:
        player.acc_right = -player.turning_speed
        if player.vel_right > 0:
            player.vel_right = 0
        player.acc_forwards = player.turning_speed
    else:
        player.acc_right = 0
        
    if keys[K_w]:
        player.acc_forwards = player.boost_speed
    elif keys[K_s]:
        player.acc_forwards = - player.slow_speed
    else:
        player.acc_forwards = 0
    
    if keys[K_SPACE]:
        player.fire()
    
    player.move()
    for x in all_entities:
        x.move()
    
    screen.fill((255,255,255))
    
    player.draw_self()
    for x in all_entities:
        x.draw_self()
    
    
    pygame.display.flip()
    
    clock.tick(60)