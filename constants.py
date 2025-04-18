import pygame
import math
import copy
from board import boards

WIDTH = 900
HEIGHT = 950
PI = math.pi
FPS = 60

# Colors
BLACK = 'black'
WHITE = 'white'
YELLOW = 'yellow'
BLUE = 'blue'
RED = 'red'
GREEN = 'green'
GRAY = 'gray'
DARK_GRAY = 'dark gray'
PURPLE = 'purple'

# Game states
MENU = "menu"
PLAYING = "playing"

# Ghost IDs
BLINKY = 0
INKY = 1
PINKY = 2
CLYDE = 3

# Directions
RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3

level_map = copy.deepcopy(boards)