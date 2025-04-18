import pygame
from collections import deque
import heapq

def check_position(centerx, centery, level, direction, HEIGHT, WIDTH):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15
    if centerx // 30 < 29:
        if direction == 0:  # Right
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 1:  # Left
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 2:  # Up
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True
        if direction == 3:  # Down
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True
    return turns

def move_player(play_x, play_y, direction, turn_allowed, player_speed):
    if direction == 0 and turn_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turn_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turn_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turn_allowed[3]:
        play_y += player_speed
    return play_x, play_y

def check_collisions(scr, power, power_count, eaten_ghosts, player_x, player_y, level, HEIGHT, WIDTH):
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    center_x = player_x + 23
    center_y = player_y + 24
    if 0 < player_x < 870:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            scr += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            scr += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]
    return scr, power, power_count, eaten_ghosts

def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, player_x, player_y, powerup, eaten_ghost, blinky_dead, inky_dead, pinky_dead, clyde_dead):
    if player_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powerup:
        if not blinky_dead and not eaten_ghost[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky_dead and eaten_ghost[0]:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky_dead and not eaten_ghost[1]:
            ink_target = (runaway_x, player_y)
        elif not inky_dead and eaten_ghost[1]:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky_dead:
            pink_target = (player_x, runaway_y)
        elif not pinky_dead and eaten_ghost[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde_dead and not eaten_ghost[3]:
            clyd_target = (450, 450)
        elif not clyde_dead and eaten_ghost[3]:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    else:
        if not blinky_dead:
            if 340 < blink_x < 560 and 340 < blink_y:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky_dead:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky_dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde_dead:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    return [blink_target, ink_target, pink_target, clyd_target]

def reset_after_death(game):
    game.lives -= 1
    game.startup_counter = 0
    game.powerup = False
    game.power_counter = 0
    game.player_x = 430
    game.player_y = 663
    game.direction = 0
    game.blinky_x = 430
    game.blinky_y = 328
    game.blinky_direction = 0
    game.inky_x = 370
    game.inky_y = 388
    game.inky_direction = 2
    game.pinky_x = 430
    game.pinky_y = 388
    game.pinky_direction = 2
    game.clyde_x = 490
    game.clyde_y = 388
    game.clyde_direction = 2
    game.eaten_ghost = [False, False, False, False]
    game.blinky_dead = False
    game.pinky_dead = False
    game.inky_dead = False
    game.clyde_dead = False

def ucs_search(start, target, level, ghost_id, in_box, dead):
    rows = len(level)
    cols = len(level[0]) if rows > 0 else 0
    directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]  # right, left, up, down
    dir_names = [0, 1, 2, 3]
    heap = []
    heapq.heappush(heap, (0, start[0], start[1], []))
    visited = set()

    while heap:
        cost, x, y, path = heapq.heappop(heap)
        if (x, y) == target:
            return path
        if (x, y) in visited:
            continue
        visited.add((x, y))

        for i in range(4):
            dx, dy = directions[i]
            new_x = x + dx
            new_y = y + dy
            if 0 <= new_x < cols and 0 <= new_y < rows:
                cell_value = level[new_y][new_x]
                if cell_value < 3 or (cell_value == 9 and (in_box or dead)):
                    new_cost = cost + 1
                    new_path = path + [dir_names[i]]
                    heapq.heappush(heap, (new_cost, new_x, new_y, new_path))
    return []