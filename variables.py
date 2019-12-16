import pygame
import random
import pygame.locals
FPS = 120
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


#+000000+
#3------1
#3------1
#+222222+
for x in range(-1,WIDTH//150):
    locations_to_spawn[0].append(150 * x)
    locations_to_spawn[2].append(150 * x)

for y in range(-1, HEIGHT // 150):
    locations_to_spawn[1].append(150 * y)
    locations_to_spawn[3].append(150 * y)

SPAWN_HEIGHT = (-150, HEIGHT + 150)
SPAWN_WIDTH = (WIDTH + 150, -150)
curr_position_to_spawn = random.randint(0, 3)
positions_to_spawn = [0, 0, 0, 0]
