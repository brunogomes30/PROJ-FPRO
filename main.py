import time
import variables
from Button import Button
from Player import Player
from Enemy import Enemy
from EnemyT2 import EnemyT2
from Shot import Shot
from utils import *
from pygame import *
from Label import Label
from QuadTree import QuadTree
from variables import screen,all_entities, time_delta, FPS, HEIGHT, WIDTH, can_spawn_enemy, temporary_entities
from Background_entity import Background_entity
import pygame



DEBUG = False
player = Player()
variables.player = player
player.image = pygame.image.load('images/player.png')
pygame.init()
player.y = 300
player.x = 300

#all_entities.add(player)



clock = pygame.time.Clock()
entities_to_remove = variables.entities_to_remove
variables.font = pygame.font.SysFont("Roboto", 32)
font = variables.font

last_spawn = 0 

#Create buttons:

menu_buttons = set()
start_new_button = Button(variables.WIDTH//4,variables.HEIGHT//6 * 2,variables.WIDTH//2,50,"Start new Game")
start_new_button.onclick = start_new_game
menu_buttons.add(start_new_button)

exit_button = Button(variables.WIDTH//4,variables.HEIGHT//6 * 2 + 65,variables.WIDTH//2,50,"Exit Game",(255, 255, 255), (255, 0,0 ))
exit_button.onclick = exit_game
menu_buttons.add(exit_button)

#Create texts
help_text = "Use WASD to move, SpaceBar to shoot and LeftShift to  slow down time (Spends score)"
help_label = variables.font.render(help_text, 1, (255, 255, 255))
help_x = 20 
help_y = variables.HEIGHT//12 * 11

read_highscore()
score_text = "Score: "+str(player.score)
score_label = variables.font.render(score_text, 1, (255, 255, 255))

high_score_text = "Highscore: " + variables.highscore
highscore_label = variables.font.render(high_score_text, 1, (255, 255, 255))

score_x = variables.WIDTH//12 * 5
score_y = variables.HEIGHT//6 + 35
highscore_x = variables.WIDTH//12 * 5
highscore_y = variables.HEIGHT//6 

gameover_text = "Game over"
gameover_label = variables.font.render(gameover_text, 1,(255, 255, 255))


gameover_x = variables.WIDTH//12 * 5
gameover_y = variables.HEIGHT//6 - 35

while variables.running:
    #print(variables.time)
    variables.time += variables.time_delta
    all_entities = variables.all_entities
    player = variables.player
    entities_to_remove = set()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            variables.running = False
            break
            
    if variables.is_playing:
        for x in variables.entities_to_add:
            all_entities.add(x)
        variables.entities_to_add = set()
        quad_tree = QuadTree(None, 0, variables.HEIGHT, 0, variables.WIDTH)
        ticks = pygame.time.get_ticks()
        if variables.time - last_spawn > 0.8 and variables.time - variables.start_time < 50 or variables.time - last_spawn > 0.4 and variables.time - variables.start_time >= 50:
            spawn_enemy()
            last_spawn = variables.time

        keys = pygame.key.get_pressed()
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
            #player.vel_right = 0
            player.turning_speed = variables.DEFAULT_TURNING_SPEED
        elif keys[K_s]:
            player.acc_forwards = - player.slow_speed
            player.vel_right *= 1
            player.turning_speed = variables.DEFAULT_TURNING_SPEED #* time_delta * 2
        else:
            player.turning_speed = variables.DEFAULT_TURNING_SPEED #* time_delta
            player.acc_forwards = 0
        if keys[K_SPACE]:
            player.fire()
            
            
        if keys[K_LSHIFT] and( player.score > 0 ):
            player.score -= 1
            variables.time_delta = 1 / FPS / 100
        else:
            variables.time_delta = 1 / FPS
            
        
        
        #Move everything
        
        
        if DEBUG:
            time = pygame.time.get_ticks()
            print("Move:")
        
        for x in variables.background_entities:
            x.move()
        
        for x in all_entities:
            x.move()
            if type(x) == EnemyT2:
                enemy = x
                if pygame.time.get_ticks() -  enemy.last_shot > enemy.shot_interval:
                        enemy.shoot()
        
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
                    if b.isEnemy:
                        if not player.invulnerable:
                            if player.lives == 1:
                                end_game()
                            
                            player.get_hit()
                            new_label = Label("-1 life", b.y, b.x)
                            temporary_entities.add(new_label)
                        entities_to_remove.add(b)
                    elif type(b) == Shot and b.harm_player:
                        if not player.invulnerable:
                            if player.lives == 1:
                                end_game()
                            player.get_hit()
                            new_label = Label("-1 life", b.y, b.x)
                            temporary_entities.add(new_label)
                        entities_to_remove.add(b)
                else:
                    if type(a) == Shot and b.isEnemy or type(b) == Shot and a.isEnemy:
                        if type(a) == Enemy or type(a) == EnemyT2:
                            a, b = b, a
                        # a = shot 
                        #b is the enemy
                        if a.sender == b:
                            continue
                        entities_to_remove.add(a)
                        b.hp -= a.damage
                        if b.hp <= 0:
                            entities_to_remove.add(b)
                            if not a.harm_player:
                                player.score += b.score
                                new_label = Label("+" + str(b.score), b.y, b.x)
                                temporary_entities.add(new_label)
                        #b.get_shot()
                    elif type(a) == Shot and type(b) == Shot and((a.harm_player and not b.harm_player) or (not a.harm_player and b.harm_player)):
                        entities_to_remove.add(a)
                        entities_to_remove.add(b)
                    #elif type(a) == Enemy and type(b) == Enemy:
                    elif a.isEnemy and b.isEnemy:
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
        
        #Draw everything
        screen.fill((0,0,0))
    
        if DEBUG:
            print(str(pygame.time.get_ticks() - time) + "..\n")
            time = pygame.time.get_ticks()
            print("Draw entities")
        
        for x in variables.background_entities:
            x.draw_self()
            
        for x in all_entities:
            x.draw_self()
        #quad_tree.draw_self()
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
        #quad_tree.draw_self()
        if DEBUG:
            print(str(pygame.time.get_ticks() - time) + "..\n")
            print("-----------------------\n---------------------\n---------------")
        temporary_entities -= temps_to_remove
        
        screen.blit(score_display, (0, 0))
        screen.blit(lives_display, (0, 25))
    else:
        #Main menu
        mouse_pos = pygame.mouse.get_pos()
        for x in menu_buttons:
            x.hover_state = x.check_collision(mouse_pos)
        for event in events:
             if event.type == pygame.MOUSEBUTTONUP:
                 for x in menu_buttons:
                     if x.hover_state:
                         x.onclick()
        screen.fill((0,0,0))
        for x in menu_buttons:
            x.draw_self()
        if variables.game_ended:
            variables.screen.blit(gameover_label ,(gameover_x, gameover_y))
            variables.screen.blit(score_label, (score_x, score_y))
        high_score_text = "Highscore: " + variables.highscore
        highscore_label = variables.font.render(high_score_text, 1, (255, 255, 255))
        variables.screen.blit(highscore_label, (highscore_x, highscore_y))
        variables.screen.blit(help_label, (help_x, help_y))
    
    pygame.display.flip()
    clock.tick(FPS)