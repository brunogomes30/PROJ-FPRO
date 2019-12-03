import time
from Player import Player
from Enemy import Enemy
from Shot import Shot
from utils import *
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
        
    #for x in all_entities:
        #if(x.mask.)
    for x in all_entities:
        if not (-HEIGHT<x.y<HEIGHT*2 and -WIDTH<x.x<WIDTH*2):
            all_entities.remove(x)
    screen.fill((0,0,0))
    
    player.draw_self()
    for x in all_entities:
        x.draw_self()
    mask = player.mask
    i = enemy
    
    #print(pygame.sprite.collide_mask(player, enemy))
    #if pygame.sprite.collide_mask(player, enemy):
    #if player.mask.overlap(enemy.mask, (int(enemy.origin[0] - player.origin[0]), int(enemy.origin[1] - player.origin[1]))):
    #    print ("Collided")
    
    entities_to_remove = []
    all_entities_updated = all_entities.copy()
    for i in range(len(all_entities)):
        for j in range(i,len(all_entities)):
            a, b = all_entities[i], all_entities[j]
            if collide(a, b):
                if type(a) == Player:
                    if type(b) == Enemy:
                        print("Collided")
                else:
                    if type(a) == Shot and type(b) == Enemy or type(b) == Shot and type(a) == Enemy:
                        if type(a) == Enemy:
                            a, b = b, a
                        #a is the shot and b is the enemy
                        entities_to_remove.append(a)
                        entities_to_remove.append(b)
                        
    for x in entities_to_remove:
        all_entities.remove(x)
    pygame.display.flip()
    clock.tick(FPS)