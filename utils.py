from Enemy import Enemy
from EnemyT2 import EnemyT2
from Player import Player
from variables import *
import random
import variables
import threading
import pygame


def start_new_game():
    variables.is_playing = True
    variables.player = Player()
    variables.player.image = pygame.image.load('images/player.png')
    variables.player.y = 300
    variables.player.x = 300
    variables.all_entities = set()
    variables.all_entities.add(variables.player)
    variables.entities_to_remove = set()
    variables.entities_to_remove = set()
    variables.entities_to_add = set()
    variables.temporary_entities = set()
    variables.start_time = variables.time 
    
def read_highscore():
    hs = open("highscore.txt", "r")
    variables.highscore = hs.readline()
    
def end_game():
    variables.is_playing = False
    variables.game_ended = True
    if variables.player.score > int(variables.highscore):
        highscore_file = open("highscore.txt", "w")
        highscore_file.write(str(variables.player.score))
        variables.highscore = str(variables.player.score)
        
    
    
def exit_game():
    variables.running = False

def collide(a, b):
    if a.mask == None or b.mask == None:
        return False
    return a.mask.overlap(b.mask, (int(b.origin[0] - a.origin[0]), int(b.origin[1] - a.origin[1])))


def start_spawning():
    global can_spawn_enemy
    variables.can_spawn_enemy = True
    t = threading.Timer(0.2, start_spawning)
    #t.start()

def spawn_enemy():
    global all_entities
    #print(variables.time - variables.start_time)
    diff = variables.time - variables.start_time
    if diff > 20:
        if diff < 60:
            a = random.randint(1,6)
        else:
            a = random.randint(1,4)
        if a == 1:
            enemy = EnemyT2()
        else:
            enemy = Enemy()
    else:
        enemy = Enemy()
    enemy.spawn()
    
    
def inside_screen(obj):
    return  0<=obj.y<=variables.HEIGHT and 0<=obj.x<=variables.WIDTH

