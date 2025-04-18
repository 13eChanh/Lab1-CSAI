# game_state.py
import pygame

# Initialize pygame and screen
pygame.init()
WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE | pygame.SCALED)

# Game state variables
total_levels = 6
selected_level = 1
game_state = "menu"  # Assuming "menu" is defined in constants.py