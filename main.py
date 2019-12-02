import time
from Player import Player
from Enemy import Enemy
from pygame import *
from variables import screen,all_entities, time_delta, FPS, HEIGHT, WIDTH
import pygame
import math

#screen = pygame.display.set_mode((800, 600))


player = Player()
player.image = pygame.image.load('images\\player.png')
pygame.init()
player.y = 300
player.x = 300
all_entities.append(player)
enemy = Enemy() 
enemy.y = 500
enemy.x = 500
all_entities.append(enemy)
clock = pygame.time.Clock()
running = True

while running:
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
               break
    
    #Input
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
        
    #After Input
    
    for x in all_entities:
        x.move()
    for x in all_entities:
        if not (-HEIGHT<x.y<HEIGHT*2 and -WIDTH<x.x<WIDTH*2):
            all_entities.remove(x)
    screen.fill((0,0,0))
    
    player.draw_self()
    for x in all_entities:
        x.draw_self()
    
    
    pygame.display.flip()
    
    clock.tick(FPS)