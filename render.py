import pygame


def draw_menu(screen, selected_level, total_levels):
    screen.fill('black')
    title_font = pygame.font.SysFont('Arial', 50)
    title_text = title_font.render('PAC-MAN AI MAZE', True, 'yellow')
    screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 100))

    level_font = pygame.font.SysFont('Arial', 30)
    for i in range(1, total_levels + 1):
        color = 'white'
        if i == selected_level:
            color = 'yellow'
        level_text = level_font.render(f'Level {i}', True, color)
        screen.blit(level_text, (screen.get_width() // 2 - level_text.get_width() // 2, 200 + i * 50))

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

        desc_text = desc_font.render(desc, True, 'gray')
        screen.blit(desc_text, (screen.get_width() // 2 - desc_text.get_width() // 2, 230 + i * 50))

    instruction_font = pygame.font.SysFont('Arial', 20)
    instructions = instruction_font.render('Use UP/DOWN arrows to select, ENTER to start', True, 'white')
    screen.blit(instructions, (screen.get_width() // 2 - instructions.get_width() // 2, screen.get_height() - 100))


def draw_board(screen, level, flicker, color, HEIGHT, WIDTH, PI):
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - (0.4 * num2)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, PI / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color, [(j * num2 + (0.5 * num2)), (i * num1 + (0.5 * num1)), num2, num1],
                                PI / 2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + (0.5 * num2)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                3 * PI / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color, [(j * num2 - (0.4 * num2)) - 2, (i * num1 - (0.4 * num1)), num2, num1],
                                3 * PI / 2, 2 * PI, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)


def draw_player(screen, player_x, player_y, direction, player_images, counter):
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))


def draw_mics(screen, font, score, powerup, lives, player_images, game_over, game_won, ghost_timers, HEIGHT):
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, HEIGHT - 40))
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, HEIGHT - 20), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, HEIGHT - 35))
    if game_over:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300], 0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Game Over! Space bar to restart', True, 'red')
        screen.blit(gameover_text, (100, 300))
        y_offset = 350
        for ghost_name, timer in ghost_timers.items():
            if timer['end'] > 0:
                time_taken = (timer['end'] - timer['start']) / 1000
                timer_text = font.render(f"{ghost_name.capitalize()} Time: {time_taken:.2f}s", True, 'red')
                screen.blit(timer_text, (100, y_offset))
                y_offset += 30
    if game_won:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300], 0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gamewon_text = font.render('Victory! Space bar to restart', True, 'green')
        screen.blit(gamewon_text, (100, 300))