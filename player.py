import pygame
from constants import *

def draw_player():
    if direction == RIGHT:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == LEFT:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == UP:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == DOWN:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))

def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15
    if centerx // 30 < 29:
        if direction == RIGHT:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[LEFT] = True
        if direction == LEFT:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[RIGHT] = True
        if direction == UP:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[DOWN] = True
        if direction == DOWN:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[UP] = True

        if direction == UP or direction == DOWN:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[DOWN] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[UP] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[LEFT] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[RIGHT] = True
        if direction == RIGHT or direction == LEFT:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[DOWN] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[UP] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[LEFT] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[RIGHT] = True
    else:
        turns[RIGHT] = True
        turns[LEFT] = True

    return turns

def move_player(play_x, play_y):
    if direction == RIGHT and turn_allowed[RIGHT]:
        play_x += player_speed
    elif direction == LEFT and turn_allowed[LEFT]:
        play_x -= player_speed
    if direction == UP and turn_allowed[UP]:
        play_y -= player_speed
    elif direction == DOWN and turn_allowed[DOWN]:
        play_y += player_speed
    return play_x, play_y