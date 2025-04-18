import pygame
from constants import *
from game_state import screen, total_levels, selected_level


def draw_menu():
    screen.fill(BLACK)
    title_font = pygame.font.SysFont('Arial', 50)
    title_text = title_font.render('PAC-MAN AI MAZE', True, YELLOW)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

    level_font = pygame.font.SysFont('Arial', 30)
    for i in range(1, total_levels + 1):
        color = WHITE
        if i == selected_level:
            color = YELLOW
        level_text = level_font.render(f'Level {i}', True, color)
        screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 200 + i * 50))

        desc_font = pygame.font.SysFont('Arial', 16)
        if i == 1:
            desc = "Blue Ghost (BFS)"
        elif i == 2:
            desc = "Pink Ghost (DFS)"
        elif i == 3:
            desc = "Orange Ghost (UCS)"
        elif i == 4:
            desc = "Red Ghost (A*)"
        elif i == 5:
            desc = "All Ghosts (Parallel)"
        elif i == 6:
            desc = "Full Game (User Control)"

        desc_text = desc_font.render(desc, True, GRAY)
        screen.blit(desc_text, (WIDTH // 2 - desc_text.get_width() // 2, 230 + i * 50))

    instruction_font = pygame.font.SysFont('Arial', 20)
    instructions = instruction_font.render('Use UP/DOWN arrows to select, ENTER to start', True, WHITE)
    screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT - 100))