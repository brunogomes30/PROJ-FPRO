import time
import variables
from Player import Player
from Enemy import Enemy
from Shot import Shot
from utils import *
from pygame import *
from Label import Label
from QuadTree import QuadTree
from variables import screen,all_entities, time_delta, FPS, HEIGHT, WIDTH, can_spawn_enemy, temporary_entities
import pygame
import math

#screen = pygame.display.set_mode((800, 600))
DEBUG = True

player = Player()
player.image = pygame.image.load('images\\player.png')
pygame.init()
player.y = 300
player.x = 300
all_entities = variables.all_entities

all_entities.add(player)

clock = pygame.time.Clock()
running = True
start_spawning()
entities_to_remove = variables.entities_to_remove

variables.font = pygame.font.SysFont("Roboto", 32)
font = variables.font



while running:
    entities_to_remove = set()
    quad_tree = QuadTree(None, 0, variables.HEIGHT + 300, 0, variables.WIDTH + 300)
    if variables.can_spawn_enemy:
        variables.can_spawn_enemy = False
        spawn_enemy()
    
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
        player.turning_speed = variables.DEFAULT_TURNING_SPEED #* time_delta * 2
    else:
        player.turning_speed = variables.DEFAULT_TURNING_SPEED #* time_delta
        player.acc_forwards = 0
    if keys[K_SPACE]:
        player.fire()
        
    if keys[K_LSHIFT] and( player.score > 0 or True):
        player.score -=1
        variables.time_delta = 1 / FPS / 100
    else:
        variables.time_delta = 1 / FPS
        
    #After Input
    
    if DEBUG:
        time = pygame.time.get_ticks()
        print("Move:")
    for x in all_entities:
        x.move()
    
    if DEBUG:
        print(str(pygame.time.get_ticks() - time) + "..\n")
        time = pygame.time.get_ticks()
        print("insert to quadTree")
    for x in all_entities:
        if inside_screen(x):
            quad_tree.insert(x)
    
    if DEBUG:
        print(str(pygame.time.get_ticks() - time) + "..\n")
        time = pygame.time.get_ticks()
        print("Remove:")
    
    for x in all_entities:
        if not (-HEIGHT<x.y<HEIGHT*2 and -WIDTH<x.x<WIDTH*2):
            entities_to_remove.add(x)
    
    score_display = font.render("Score: "+str(player.score), 1, (255, 255, 255))
    lives_display = font.render("Lives: "+str(player.lives), 1, (255, 255, 255))
    
    if DEBUG:
        print(str(pygame.time.get_ticks() - time) + "..\n")
        time = pygame.time.get_ticks()
        print("Check collisions:")
    
    
    
    #Collisions
    for a in all_entities:
        if a in entities_to_remove:
            continue
        b = quad_tree.check_collisions(a)
        if b != None:
            if type(a) == Player:
                if type(b) == Enemy:
                    if not player.invulnerable:
                        if player.lives == 0:
                            running = False
                        player.get_hit()
                        new_label = Label("-1", b.y, b.x)
                        temporary_entities.add(new_label)
                    entities_to_remove.add(b)
            else:
                if type(a) == Shot and type(b) == Enemy or type(b) == Shot and type(a) == Enemy:
                    if type(a) == Enemy:
                        switched = True
                        a, b = b, a
                    #a is the shot and b is the enemy
                    entities_to_remove.add(a)
                    b.hp -= a.damage
                    if b.hp <= 0:
                        entities_to_remove.add(b)
                        player.score += b.score
                        new_label = Label("+" + str(b.score), b.y, b.x)
                        temporary_entities.add(new_label)
                    b.get_shot()
                    
                if type(a) == Enemy and type(b) == Enemy:
                    a.speed, b.speed = b.speed, a.speed
                    #a.asteroid_sound.play()
    
    all_entities -= entities_to_remove    
    
    if DEBUG:
        print(str(pygame.time.get_ticks() - time)+ "..\n")
    
    
    temps_to_remove = set()
    
    

    
    all_entities -= entities_to_remove

    entities_to_remove = set()
    #all_entities_updated = all_entities.copy()
    if DEBUG:
        time = pygame.time.get_ticks()
        print("Fill:")
    #print(len(all_entities), clock.get_fps())
    
    screen.fill((0,0,0))

    if DEBUG:
        print(str(pygame.time.get_ticks() - time) + "..\n")
        time = pygame.time.get_ticks()
        print("Draw entities")
        
    for x in all_entities:
        x.draw_self()
    
    if DEBUG:
        print(str(pygame.time.get_ticks() - time) + "..\n")
        #quad_tree.draw_self()
        time = pygame.time.get_ticks()
        print("Draw temps")
    
    for x in temporary_entities:
        x.ticksLeft-=1
        if x.ticksLeft <= 0:
            temps_to_remove.add(x)
        x.draw_self()
    
    if DEBUG:
        print(str(pygame.time.get_ticks() - time) + "..\n")
        print("-----------------------\n---------------------\n---------------")
    temporary_entities -= temps_to_remove
    
    screen.blit(score_display, (0, 0))
    screen.blit(lives_display, (0, 25))
    
    #print(str(pygame.time.get_ticks() - time) + "\n--------\n------\n")
    
    
    pygame.display.flip()
    clock.tick(FPS)