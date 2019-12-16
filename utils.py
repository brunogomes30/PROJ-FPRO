from Enemy import Enemy
from variables import *
import random
import variables
import threading
import pygame


def collide(a, b):
    return a.mask.overlap(b.mask, (int(b.origin[0] - a.origin[0]), int(b.origin[1] - a.origin[1])))


def start_spawning():
    global can_spawn_enemy
    variables.can_spawn_enemy = True
    t = threading.Timer(1.5, start_spawning)
    t.start()

def spawn_enemy():
    global all_entities
    enemy = Enemy()
    enemy.spawn()
    
    
def inside_screen(obj):
    return  0<=obj.y<=variables.HEIGHT and 0<=obj.x<=variables.WIDTH

