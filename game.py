from board import boards
import pygame
import copy
from ghost import Ghost
from render import draw_board, draw_player, draw_mics
from utils import check_position, move_player, check_collisions, get_targets, reset_after_death


class Game:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.WIDTH = 900
        self.HEIGHT = 950
        self.level_map = copy.deepcopy(boards)
        self.color = 'blue'
        self.PI = 3.14159265359
        self.player_images = []
        for i in range(1, 5):
            self.player_images.append(
                pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45, 45)))
        self.blinky_images = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (45, 45))
        self.pinky_images = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (45, 45))
        self.inky_images = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (45, 45))
        self.clyde_images = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (45, 45))
        self.spooked_images = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (45, 45))
        self.dead_images = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (45, 45))
        self.selected_level = 1
        self.total_levels = 6
        self.reset_game(6)

    def reset_game(self, level_num):
        # (50,578)
        self.player_x = 685
        self.player_y = 50
        self.direction = 1
        self.blinky_x = 430
        self.blinky_y = 328
        self.blinky_direction = 1
        self.inky_x = 370
        self.inky_y = 388
        self.inky_direction = 2
        self.pinky_x = 430
        self.pinky_y = 388
        self.pinky_direction = 2
        self.clyde_x = 490
        self.clyde_y = 388
        self.clyde_direction = 2
        self.player_speed = 2
        self.blinky_box = False
        self.pinky_box = False
        self.inky_box = False
        self.clyde_box = False
        self.counter = 0
        self.flicker = False
        self.powerup = False
        self.power_counter = 0
        self.eaten_ghost = [False, False, False, False]
        self.blinky_dead = False
        self.pinky_dead = False
        self.inky_dead = False
        self.clyde_dead = False
        self.startup_counter = 0
        self.moving = False
        self.ghost_speeds = [2, 2, 2, 2]
        self.lives = 3
        self.score = 0
        self.game_over = False
        self.game_won = False
        self.direction_command = 0
        self.ghost_timers = {
            'blinky': {'start': 0, 'end': 0, 'active': False},
            'inky': {'start': 0, 'end': 0, 'active': False},
            'pinky': {'start': 0, 'end': 0, 'active': False},
            'clyde': {'start': 0, 'end': 0, 'active': False}
        }
        self.ghost_collisions = [False, False, False, False]
        self.level = copy.deepcopy(self.level_map)
        self.targets = [(self.player_x, self.player_y), (self.player_x, self.player_y), (self.player_x, self.player_y),
                        (self.player_x, self.player_y)]

    def update(self):
        if self.counter < 19:
            self.counter += 1
            if self.counter > 4:
                self.flicker = False
        else:
            self.counter = 0
            self.flicker = True
        if self.powerup and self.power_counter < 600:
            self.power_counter += 1
        elif self.powerup and self.power_counter >= 600:
            self.powerup = False
            self.power_counter = 0
            self.eaten_ghost = [False, False, False, False]
        if self.startup_counter < 180 and not self.game_over and not self.game_won:
            self.moving = False
            self.startup_counter += 1
        elif self.startup_counter >= 180 and not self.game_over and not self.game_won:
            for ghost_name in self.ghost_timers:
                if not self.ghost_timers[ghost_name]['active']:
                    self.ghost_timers[ghost_name]['start'] = pygame.time.get_ticks()
                    self.ghost_timers[ghost_name]['active'] = True
            self.moving = True

        self.screen.fill('black')
        draw_board(self.screen, self.level, self.flicker, self.color, self.HEIGHT, self.WIDTH, self.PI)
        self.center_x = self.player_x + 23
        self.center_y = self.player_y + 24
        if self.powerup:
            self.ghost_speeds = [1, 1, 1, 1]
        else:
            self.ghost_speeds = [2, 2, 2, 2]
        if self.eaten_ghost[0]:
            self.ghost_speeds[0] = 2
        if self.eaten_ghost[1]:
            self.ghost_speeds[1] = 2
        if self.eaten_ghost[2]:
            self.ghost_speeds[2] = 2
        if self.eaten_ghost[3]:
            self.ghost_speeds[3] = 2
        if self.blinky_dead:
            self.ghost_speeds[0] = 4
        if self.inky_dead:
            self.ghost_speeds[1] = 4
        if self.pinky_dead:
            self.ghost_speeds[2] = 4
        if self.clyde_dead:
            self.ghost_speeds[3] = 4

        self.game_won = True
        for i in range(len(self.level)):
            if 1 in self.level[i] or 2 in self.level[i]:
                self.game_won = False

        self.player_circle = pygame.draw.circle(self.screen, 'purple', (self.center_x, self.center_y), 20, 2)
        draw_player(self.screen, self.player_x, self.player_y, self.direction, self.player_images, self.counter)

        # Pass self.screen to Ghost instances
        blinky = Ghost(self.blinky_x, self.blinky_y, self.targets[0], self.ghost_speeds[0], self.blinky_images,
                       self.blinky_direction, self.blinky_dead, self.blinky_box, 0, self.level, self.powerup,
                       self.eaten_ghost, self.spooked_images, self.dead_images, self.HEIGHT, self.WIDTH, self.screen)
        inky = Ghost(self.inky_x, self.inky_y, self.targets[1], self.ghost_speeds[1], self.inky_images,
                     self.inky_direction, self.inky_dead, self.inky_box, 1, self.level, self.powerup, self.eaten_ghost,
                     self.spooked_images, self.dead_images, self.HEIGHT, self.WIDTH, self.screen)
        pinky = Ghost(self.pinky_x, self.pinky_y, self.targets[2], self.ghost_speeds[2], self.pinky_images,
                      self.pinky_direction, self.pinky_dead, self.pinky_box, 2, self.level, self.powerup,
                      self.eaten_ghost, self.spooked_images, self.dead_images, self.HEIGHT, self.WIDTH, self.screen)
        clyde = Ghost(self.clyde_x, self.clyde_y, self.targets[3], self.ghost_speeds[3], self.clyde_images,
                      self.clyde_direction, self.clyde_dead, self.clyde_box, 3, self.level, self.powerup,
                      self.eaten_ghost, self.spooked_images, self.dead_images, self.HEIGHT, self.WIDTH, self.screen)

        draw_mics(self.screen, self.font, self.score, self.powerup, self.lives, self.player_images, self.game_over,
                  self.game_won, self.ghost_timers, self.HEIGHT)
        self.targets = get_targets(self.blinky_x, self.blinky_y, self.inky_x, self.inky_y, self.pinky_x, self.pinky_y,
                                   self.clyde_x, self.clyde_y, self.player_x, self.player_y, self.powerup,
                                   self.eaten_ghost, self.blinky_dead, self.inky_dead, self.pinky_dead, self.clyde_dead)
        turn_allowed = check_position(self.center_x, self.center_y, self.level, self.direction, self.HEIGHT, self.WIDTH)

        if self.moving:
            if self.selected_level == 6:
                self.direction = self.direction_command  # Sync direction with user input
                self.player_x, self.player_y = move_player(self.player_x, self.player_y, self.direction,
                                                               turn_allowed, self.player_speed)
            if self.selected_level == 1:
                if not inky.dead and not inky.in_box:
                    self.inky_x, self.inky_y, self.inky_direction = inky.move_inky()
                else:
                    self.inky_x, self.inky_y, self.inky_direction = inky.move_clyde()
            elif self.selected_level == 2:
                if not pinky.dead and not pinky.in_box:
                    self.pinky_x, self.pinky_y, self.pinky_direction = pinky.move_pinky_joreii()
                else:
                    self.pinky_x, self.pinky_y, self.pinky_direction = pinky.move_clyde()
            elif self.selected_level == 3:
                self.clyde_x, self.clyde_y, self.clyde_direction = clyde.move_clyde()
            elif self.selected_level == 4:
                if not blinky.dead and not blinky.in_box:
                    self.blinky_x, self.blinky_y, self.blinky_direction = blinky.move_blinky_astar()
                else:
                    self.blinky_x, self.blinky_y, self.blinky_direction = blinky.move_clyde()
            elif self.selected_level >= 5:
                if not blinky.dead and not blinky.in_box:
                    self.blinky_x, self.blinky_y, self.blinky_direction = blinky.move_blinky_astar()
                else:
                    self.blinky_x, self.blinky_y, self.blinky_direction = blinky.move_clyde()
                if not inky.dead and not inky.in_box:
                    self.inky_x, self.inky_y, self.inky_direction = inky.move_inky()
                else:
                    self.inky_x, self.inky_y, self.inky_direction = inky.move_clyde()
                if not pinky.dead and not pinky.in_box:
                    self.pinky_x, self.pinky_y, self.pinky_direction = pinky.move_pinky_joreii()
                else:
                    self.pinky_x, self.pinky_y, self.pinky_direction = pinky.move_clyde()
                self.clyde_x, self.clyde_y, self.clyde_direction = clyde.move_clyde()

        if self.selected_level in [1, 2, 3, 4]:
            ghosts = [
                ('blinky', blinky),
                ('inky', inky),
                ('pinky', pinky),
                ('clyde', clyde)
            ]
            for ghost_name, ghost in ghosts:
                if self.player_circle.colliderect(ghost.rect) and not ghost.dead:
                    if self.ghost_timers[ghost_name]['active']:
                        self.ghost_timers[ghost_name]['end'] = pygame.time.get_ticks()
                    self.game_over = True
                    self.moving = False
                    self.startup_counter = 0
                    self.player_x = 430
                    self.player_y = 663
                    self.direction = 0
                    if ghost_name == 'blinky':
                        self.blinky_x = 430
                        self.blinky_y = 328
                        self.blinky_direction = 0
                    elif ghost_name == 'inky':
                        self.inky_x = 370
                        self.inky_y = 388
                        self.inky_direction = 2
                    elif ghost_name == 'pinky':
                        self.pinky_x = 430
                        self.pinky_y = 388
                        self.pinky_direction = 2
                    elif ghost_name == 'clyde':
                        self.clyde_x = 490
                        self.clyde_y = 388
                        self.clyde_direction = 2

        if self.selected_level == 5:
            ghosts = [
                ('blinky', blinky),
                ('inky', inky),
                ('pinky', pinky),
                ('clyde', clyde)
            ]
            for i, (ghost_name, ghost) in enumerate(ghosts):
                if self.player_circle.colliderect(ghost.rect) and not ghost.dead:
                    if self.ghost_timers[ghost_name]['active'] and self.ghost_timers[ghost_name]['end'] == 0:
                        self.ghost_timers[ghost_name]['end'] = pygame.time.get_ticks()
                    self.ghost_collisions[i] = True
            if all(self.ghost_collisions):
                self.game_over = True
                self.moving = False
                self.startup_counter = 0
                self.player_x = 430
                self.player_y = 663
                self.direction = 0
                self.blinky_x = 430
                self.blinky_y = 328
                self.blinky_direction = 0
                self.inky_x = 370
                self.inky_y = 388
                self.inky_direction = 2
                self.pinky_x = 430
                self.pinky_y = 388
                self.pinky_direction = 2
                self.clyde_x = 490
                self.clyde_y = 388
                self.clyde_direction = 2

        if self.selected_level == 6:
            self.score, self.powerup, self.power_counter, self.eaten_ghost = check_collisions(self.score, self.powerup,
                                                                                              self.power_counter,
                                                                                              self.eaten_ghost,
                                                                                              self.player_x,
                                                                                              self.player_y, self.level,
                                                                                              self.HEIGHT, self.WIDTH)
            if not self.powerup:
                if (self.player_circle.colliderect(blinky.rect) and not blinky.dead) or \
                        (self.player_circle.colliderect(inky.rect) and not inky.dead) or \
                        (self.player_circle.colliderect(pinky.rect) and not pinky.dead) or \
                        (self.player_circle.colliderect(clyde.rect) and not clyde.dead):
                    if self.lives > 0:
                        reset_after_death(self)
                    else:
                        self.game_over = True
                        self.moving = False
                        self.startup_counter = 0
            if self.powerup and self.player_circle.colliderect(blinky.rect) and self.eaten_ghost[0] and not blinky.dead:
                if self.lives > 0:
                    reset_after_death(self)
                else:
                    self.game_over = True
                    self.moving = False
                    self.startup_counter = 0
            if self.powerup and self.player_circle.colliderect(inky.rect) and self.eaten_ghost[1] and not inky.dead:
                if self.lives > 0:
                    reset_after_death(self)
                else:
                    self.game_over = True
                    self.moving = False
                    self.startup_counter = 0
            if self.powerup and self.player_circle.colliderect(pinky.rect) and self.eaten_ghost[2] and not pinky.dead:
                if self.lives > 0:
                    reset_after_death(self)
                else:
                    self.game_over = True
                    self.moving = False
                    self.startup_counter = 0
            if self.powerup and self.player_circle.colliderect(clyde.rect) and self.eaten_ghost[3] and not clyde.dead:
                if self.lives > 0:
                    reset_after_death(self)
                else:
                    self.game_over = True
                    self.moving = False
                    self.startup_counter = 0
            if self.powerup and self.player_circle.colliderect(blinky.rect) and not blinky.dead and not \
            self.eaten_ghost[0]:
                self.blinky_dead = True
                self.eaten_ghost[0] = True
                self.score += (2 ** self.eaten_ghost.count(True)) * 100
            if self.powerup and self.player_circle.colliderect(inky.rect) and not inky.dead and not self.eaten_ghost[1]:
                self.inky_dead = True
                self.eaten_ghost[1] = True
                self.score += (2 ** self.eaten_ghost.count(True)) * 100
            if self.powerup and self.player_circle.colliderect(pinky.rect) and not pinky.dead and not self.eaten_ghost[
                2]:
                self.pinky_dead = True
                self.eaten_ghost[2] = True
                self.score += (2 ** self.eaten_ghost.count(True)) * 100
            if self.powerup and self.player_circle.colliderect(clyde.rect) and not clyde.dead and not self.eaten_ghost[
                3]:
                self.clyde_dead = True
                self.eaten_ghost[3] = True
                self.score += (2 ** self.eaten_ghost.count(True)) * 100

        if self.player_x > self.WIDTH:
            self.player_x = -47
        elif self.player_x < -50:
            self.player_x = self.WIDTH - 3

        if blinky.in_box and self.blinky_dead:
            self.blinky_dead = False
        if inky.in_box and self.inky_dead:
            self.inky_dead = False
        if pinky.in_box and self.pinky_dead:
            self.pinky_dead = False
        if clyde.in_box and self.clyde_dead:
            self.clyde_dead = False