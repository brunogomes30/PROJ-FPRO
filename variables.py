import pygame

import pygame.locals
FPS = 60
time_delta = 1/FPS
WIDTH = 1000
HEIGHT = 800
DEFAULT_TURNING_SPEED = 10
flags = pygame.locals.DOUBLEBUF
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
all_entities = set()
can_spawn_enemy = True
entities_to_remove = set()
temporary_entities = set()
font = None

locations_to_spawn = [[], [], [], []]

#for x in range(WIDTH//150):
#    for y in range(HEIGHT // 150):
#        locations_to_spawn.append()
position_to_spawn = [0, 0, 0, 0]
