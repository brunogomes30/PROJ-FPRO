import pygame

FPS = 60
time_delta = 1/FPS
WIDTH = 800
HEIGHT = 1200
DEFAULT_TURNING_SPEED = 10
screen = pygame.display.set_mode((HEIGHT, WIDTH))
all_entities = []
can_spawn_enemy = True
entities_to_remove = []
