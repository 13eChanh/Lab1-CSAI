import pygame
import sys

from constants import *
from menu import draw_menu
from ghost import Ghost
from player import *
from utils import *
from game_state import screen, total_levels, selected_level, game_state

# Initialize pygame
# pygame.init()
# screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE | pygame.SCALED)
timer = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 20)

# Load images
player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45, 45)))

blinky_images = pygame.transform.scale(pygame.image.load('assets/ghost_images/red.png'), (45, 45))
pinky_images = pygame.transform.scale(pygame.image.load('assets/ghost_images/pink.png'), (45, 45))
inky_images = pygame.transform.scale(pygame.image.load('assets/ghost_images/blue.png'), (45, 45))
clyde_images = pygame.transform.scale(pygame.image.load('assets/ghost_images/orange.png'), (45, 45))
spooked_images = pygame.transform.scale(pygame.image.load('assets/ghost_images/powerup.png'), (45, 45))
dead_img = pygame.transform.scale(pygame.image.load('assets/ghost_images/dead.png'), (45, 45))

# Game variables
game_state = MENU
selected_level = 1
total_levels = 6


def reset_game(level_num):
    global player_x, player_y, direction, blinky_x, blinky_y, blinky_direction
    global inky_x, inky_y, inky_direction, pinky_x, pinky_y, pinky_direction
    global clyde_x, clyde_y, clyde_direction, powerup, power_counter
    global eaten_ghost, blinky_dead, pinky_dead, inky_dead, clyde_dead
    global lives, score, level, flicker, counter, startup_counter, moving
    global game_over, game_won, ghost_speeds, targets, player_speed
    global blinky_box, pinky_box, inky_box, clyde_box, direction_command
    global ghost_timers, ghost_collisions

    player_x = 430
    player_y = 663
    direction = 0
    blinky_x = 430
    blinky_y = 328
    blinky_direction = 0
    inky_x = 370
    inky_y = 388
    inky_direction = 2
    pinky_x = 430
    pinky_y = 388
    pinky_direction = 2
    clyde_x = 490
    clyde_y = 388
    clyde_direction = 2

    player_speed = 2
    blinky_box = False
    pinky_box = False
    inky_box = False
    clyde_box = False

    counter = 0
    flicker = False
    powerup = False
    power_counter = 0
    eaten_ghost = [False, False, False, False]
    blinky_dead = False
    pinky_dead = False
    inky_dead = False
    clyde_dead = False
    startup_counter = 0
    moving = False
    ghost_speeds = [2, 2, 2, 2]
    lives = 3
    score = 0
    game_over = False
    game_won = False
    direction_command = 0
    ghost_timers = {
        'blinky': {'start': 0, 'end': 0, 'active': False},
        'inky': {'start': 0, 'end': 0, 'active': False},
        'pinky': {'start': 0, 'end': 0, 'active': False},
        'clyde': {'start': 0, 'end': 0, 'active': False}
    }
    ghost_collisions = [False, False, False, False]
    level = copy.deepcopy(level_map)
    targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]


# Main game loop
def main():
    global game_state, selected_level, total_levels, counter, powerup, power_counter, game_over, game_won, startup_counter, player_x, player_y, eaten_ghost, blinky_dead, inky_dead

    run = True
    while run:
        timer.tick(FPS)

        if game_state == MENU:
            draw_menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected_level = (selected_level % total_levels) + 1
                    elif event.key == pygame.K_UP:
                        selected_level = (selected_level - 2) % total_levels + 1
                    elif event.key == pygame.K_RETURN:
                        reset_game(selected_level)
                        game_state = PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        run = False

        elif game_state == PLAYING:
            if counter < 19:
                counter += 1
                if counter > 4:
                    flicker = False
            else:
                counter = 0
                flicker = True
            if powerup and power_counter < 600:
                power_counter += 1
            elif powerup and power_counter >= 600:
                powerup = False
                power_counter = 0
                eaten_ghost = [False, False, False, False]
            if startup_counter < 180 and not game_over and not game_won:
                moving = False
                startup_counter += 1
            elif startup_counter >= 180 and not game_over and not game_won:
                for ghost_name in ghost_timers:
                    if not ghost_timers[ghost_name]['active']:
                        ghost_timers[ghost_name]['start'] = pygame.time.get_ticks()
                        ghost_timers[ghost_name]['active'] = True
                moving = True

            screen.fill('black')
            draw_board()
            center_x = player_x + 23
            center_y = player_y + 24
            if powerup:
                ghost_speeds = [1, 1, 1, 1]
            else:
                ghost_speeds = [2, 2, 2, 2]
            if eaten_ghost[0]:
                ghost_speeds[0] = 2
            if eaten_ghost[1]:
                ghost_speeds[1] = 2
            if eaten_ghost[2]:
                ghost_speeds[2] = 2
            if eaten_ghost[3]:
                ghost_speeds[3] = 2
            if blinky_dead:
                ghost_speeds[0] = 4
            if inky_dead:
                ghost_speeds[1] = 4
            if pinky_dead:
                ghost_speeds[2] = 4
            if clyde_dead:
                ghost_speeds[3] = 4

            game_won = True
            for i in range(len(level)):
                if 1 in level[i] or 2 in level[i]:
                    game_won = False

            player_circle = pygame.draw.circle(screen, 'purple', (center_x, center_y), 20, 2)
            draw_player()

            blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speeds[0], blinky_images, blinky_direction,
                           blinky_dead, blinky_box, 0)
            inky = Ghost(inky_x, inky_y, targets[1], ghost_speeds[1], inky_images, inky_direction, inky_dead, inky_box,
                         1)
            pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speeds[2], pinky_images, pinky_direction, pinky_dead,
                          pinky_box, 2)
            clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speeds[3], clyde_images, clyde_direction, clyde_dead,
                          clyde_box, 3)

            draw_mics()
            targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)
            turn_allowed = check_position(center_x, center_y)

            if moving:
                if selected_level == 6:
                    player_x, player_y = move_player(player_x, player_y)
                else:
                    pass

                if selected_level == 1:  # Only Blue Ghost (BFS)
                    if not inky.dead and not inky.in_box:
                        inky_x, inky_y, inky_direction = inky.move_inky()
                    else:
                        inky_x, inky_y, inky_direction = inky.move_clyde()

                elif selected_level == 2:  # Only Pink Ghost (DFS)
                    if not pinky.dead and not pinky.in_box:
                        pinky_x, pinky_y, pinky_direction = pinky.move_pinky_joreii()
                    else:
                        pinky_x, pinky_y, pinky_direction = pinky.move_clyde()

                elif selected_level == 3:  # Only Orange Ghost (UCS)
                    clyde_x, clyde_y, clyde_direction = clyde.move_clyde()

                elif selected_level == 4:  # Only Red Ghost (A*)
                    if not blinky.dead and not blinky.in_box:
                        blinky_x, blinky_y, blinky_direction = blinky.move_blinky_astar()
                    else:
                        blinky_x, blinky_y, blinky_direction = blinky.move_clyde()

                elif selected_level >= 5:  # All ghosts (parallel)
                    if not blinky.dead and not blinky.in_box:
                        if selected_level == 6:
                            blinky_x, blinky_y, blinky_direction = blinky.move_blinky_astar()
                        else:
                            blinky_x, blinky_y, blinky_direction = blinky.move_blinky_astar()
                    else:
                        blinky_x, blinky_y, blinky_direction = blinky.move_clyde()

                    if not inky.dead and not inky.in_box:
                        inky_x, inky_y, inky_direction = inky.move_inky()
                    else:
                        inky_x, inky_y, inky_direction = inky.move_clyde()

                    if not pinky.dead and not pinky.in_box:
                        pinky_x, pinky_y, pinky_direction = pinky.move_pinky_joreii()
                    else:
                        pinky_x, pinky_y, pinky_direction = pinky.move_clyde()

                    clyde_x, clyde_y, clyde_direction = clyde.move_clyde()

            if selected_level in [1, 2, 3, 4]:
                ghosts = [
                    ('blinky', blinky),
                    ('inky', inky),
                    ('pinky', pinky),
                    ('clyde', clyde)
                ]

                for ghost_name, ghost in ghosts:
                    if player_circle.colliderect(ghost.rect) and not ghost.dead:
                        if ghost_timers[ghost_name]['active']:
                            ghost_timers[ghost_name]['end'] = pygame.time.get_ticks()
                        game_over = True
                        moving = False
                        startup_counter = 0

                        player_x = 430
                        player_y = 663
                        direction = 0

                        if ghost_name == 'blinky':
                            blinky_x = 430
                            blinky_y = 328
                            blinky_direction = 0
                        elif ghost_name == 'inky':
                            inky_x = 370
                            inky_y = 388
                            inky_direction = 2
                        elif ghost_name == 'pinky':
                            pinky_x = 430
                            pinky_y = 388
                            pinky_direction = 2
                        elif ghost_name == 'clyde':
                            clyde_x = 490
                            clyde_y = 388
                            clyde_direction = 2

            if selected_level == 5:
                ghosts = [
                    ('blinky', blinky),
                    ('inky', inky),
                    ('pinky', pinky),
                    ('clyde', clyde)
                ]

                for i, (ghost_name, ghost) in enumerate(ghosts):
                    if player_circle.colliderect(ghost.rect) and not ghost.dead:
                        if ghost_timers[ghost_name]['active']:
                            ghost_timers[ghost_name]['end'] = pygame.time.get_ticks()
                        ghost_collisions[i] = True

                if all(ghost_collisions):
                    game_over = True
                    moving = False
                    startup_counter = 0

                    player_x = 430
                    player_y = 663
                    direction = 0

                    blinky_x = 430
                    blinky_y = 328
                    blinky_direction = 0
                    inky_x = 370
                    inky_y = 388
                    inky_direction = 2
                    pinky_x = 430
                    pinky_y = 388
                    pinky_direction = 2
                    clyde_x = 490
                    clyde_y = 388
                    clyde_direction = 2

            if selected_level == 6:
                score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter,
                                                                              eaten_ghost)

                if not powerup:
                    if (player_circle.colliderect(blinky.rect) and not blinky.dead) or \
                            (player_circle.colliderect(inky.rect) and not inky.dead) or \
                            (player_circle.colliderect(pinky.rect) and not pinky.dead) or \
                            (player_circle.colliderect(clyde.rect) and not clyde.dead):
                        if lives > 0:
                            lives -= 1
                            startup_counter = 0
                            powerup = False
                            power_counter = 0
                            player_x = 430
                            player_y = 663
                            direction = 0
                            blinky_x = 430
                            blinky_y = 328
                            blinky_direction = 0
                            inky_x = 370
                            inky_y = 388
                            inky_direction = 2
                            pinky_x = 430
                            pinky_y = 388
                            pinky_direction = 2
                            clyde_x = 490
                            clyde_y = 388
                            clyde_direction = 2
                            eaten_ghost = [False, False, False, False]
                            blinky_dead = False
                            pinky_dead = False
                            inky_dead = False
                            clyde_dead = False
                        else:
                            game_over = True
                            moving = False
                            startup_counter = 0

                if powerup and player_circle.colliderect(blinky.rect) and eaten_ghost[0] and not blinky.dead:
                    if lives > 0:
                        lives -= 1
                        startup_counter = 0
                        powerup = False
                        power_counter = 0
                        player_x = 430
                        player_y = 663
                        direction = 0
                        blinky_x = 430
                        blinky_y = 328
                        blinky_direction = 0
                        inky_x = 370
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 430
                        pinky_y = 388
                        pinky_direction = 2
                        clyde_x = 490
                        clyde_y = 388
                        clyde_direction = 2
                        eaten_ghost = [False, False, False, False]
                        blinky_dead = False
                        pinky_dead = False
                        inky_dead = False
                        clyde_dead = False
                    else:
                        game_over = True
                        moving = False
                        startup_counter = 0
                if powerup and player_circle.colliderect(inky.rect) and eaten_ghost[1] and not inky.dead:
                    if lives > 0:
                        lives -= 1
                        startup_counter = 0
                        powerup = False
                        power_counter = 0
                        player_x = 430
                        player_y = 663
                        direction = 0
                        blinky_x = 430
                        blinky_y = 328
                        blinky_direction = 0
                        inky_x = 370
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 430
                        pinky_y = 388
                        pinky_direction = 2
                        clyde_x = 490
                        clyde_y = 388
                        clyde_direction = 2
                        eaten_ghost = [False, False, False, False]
                        blinky_dead = False
                        pinky_dead = False
                        inky_dead = False
                        clyde_dead = False
                    else:
                        game_over = True
                        moving = False
                        startup_counter = 0
                if powerup and player_circle.colliderect(pinky.rect) and eaten_ghost[2] and not pinky.dead:
                    if lives > 0:
                        lives -= 1
                        startup_counter = 0
                        powerup = False
                        power_counter = 0
                        player_x = 430
                        player_y = 663
                        direction = 0
                        blinky_x = 430
                        blinky_y = 328
                        blinky_direction = 0
                        inky_x = 370
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 430
                        pinky_y = 388
                        pinky_direction = 2
                        clyde_x = 490
                        clyde_y = 388
                        clyde_direction = 2
                        eaten_ghost = [False, False, False, False]
                        blinky_dead = False
                        pinky_dead = False
                        inky_dead = False
                        clyde_dead = False
                    else:
                        game_over = True
                        moving = False
                        startup_counter = 0
                if powerup and player_circle.colliderect(clyde.rect) and eaten_ghost[3] and not clyde.dead:
                    if lives > 0:
                        lives -= 1
                        startup_counter = 0
                        powerup = False
                        power_counter = 0
                        player_x = 430
                        player_y = 663
                        direction = 0
                        blinky_x = 430
                        blinky_y = 328
                        blinky_direction = 0
                        inky_x = 370
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 430
                        pinky_y = 388
                        pinky_direction = 2
                        clyde_x = 490
                        clyde_y = 388
                        clyde_direction = 2
                        eaten_ghost = [False, False, False, False]
                        blinky_dead = False
                        pinky_dead = False
                        inky_dead = False
                        clyde_dead = False
                    else:
                        game_over = True
                        moving = False
                        startup_counter = 0
                if powerup and player_circle.colliderect(blinky.rect) and not blinky.dead and not eaten_ghost[0]:
                    blinky_dead = True
                    eaten_ghost[0] = True
                    score += (2 ** eaten_ghost.count(True)) * 100
                if powerup and player_circle.colliderect(inky.rect) and not inky.dead and not eaten_ghost[1]:
                    inky_dead = True
                    eaten_ghost[1] = True
                    score += (2 ** eaten_ghost.count(True)) * 100
                if powerup and player_circle.colliderect(pinky.rect) and not pinky.dead and not eaten_ghost[2]:
                    pinky_dead = True
                    eaten_ghost[2] = True
                    score += (2 ** eaten_ghost.count(True)) * 100
                if powerup and player_circle.colliderect(clyde.rect) and not clyde.dead and not eaten_ghost[3]:
                    clyde_dead = True
                    eaten_ghost[3] = True
                    score += (2 ** eaten_ghost.count(True)) * 100

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if selected_level == 6:  # Only process key events for player in level 6
                        if event.key == pygame.K_RIGHT:
                            direction_command = 0
                        if event.key == pygame.K_LEFT:
                            direction_command = 1
                        if event.key == pygame.K_UP:
                            direction_command = 2
                        if event.key == pygame.K_DOWN:
                            direction_command = 3

                    if event.key == pygame.K_SPACE and (game_over or game_won):
                        game_state = "menu"
                    elif event.key == pygame.K_ESCAPE:
                        game_state = "menu"

                if selected_level == 6 and event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT and direction_command == 0:
                        direction_command = 0
                    if event.key == pygame.K_LEFT and direction_command == 1:
                        direction_command = 1
                    if event.key == pygame.K_UP and direction_command == 2:
                        direction_command = 2
                    if event.key == pygame.K_DOWN and direction_command == 3:
                        direction_command = 3

            if selected_level == 6:
                for i in range(4):
                    if direction_command == i and turn_allowed[i]:
                        direction = i
                if player_x > WIDTH:
                    player_x = -47
                elif player_x < -50:
                    player_x = WIDTH - 3

            if blinky.in_box and blinky_dead:
                blinky_dead = False
            if inky.in_box and inky_dead:
                inky_dead = False
            if pinky.in_box and pinky_dead:
                pinky_dead = False
            if clyde.in_box and clyde_dead:
                clyde_dead = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()