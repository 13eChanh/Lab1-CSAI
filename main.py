import pygame
from game import Game
from render import draw_menu

pygame.init()

WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE | pygame.SCALED)
timer = pygame.time.Clock()
fps = 60
font = pygame.font.SysFont('Arial', 20)


def main():
    game = Game(screen, font)
    game_state = "menu"
    run = True

    while run:
        timer.tick(fps)

        if game_state == "menu":
            draw_menu(screen, game.selected_level, game.total_levels)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        game.selected_level = (game.selected_level % game.total_levels) + 1
                    elif event.key == pygame.K_UP:
                        game.selected_level = (game.selected_level - 2) % game.total_levels + 1
                    elif event.key == pygame.K_RETURN:
                        game.reset_game(game.selected_level)
                        game_state = "playing"
                    elif event.key == pygame.K_ESCAPE:
                        run = False

        elif game_state == "playing":
            game.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if game.selected_level == 6:
                        if event.key == pygame.K_RIGHT:
                            game.direction_command = 0
                        if event.key == pygame.K_LEFT:
                            game.direction_command = 1
                        if event.key == pygame.K_UP:
                            game.direction_command = 2
                        if event.key == pygame.K_DOWN:
                            game.direction_command = 3
                    if event.key == pygame.K_SPACE and (game.game_over or game.game_won):
                        game_state = "menu"
                    elif event.key == pygame.K_ESCAPE:
                        game_state = "menu"

                if game.selected_level == 6 and event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT and game.direction_command == 0:
                        game.direction_command = 0
                    if event.key == pygame.K_LEFT and game.direction_command == 1:
                        game.direction_command = 1
                    if event.key == pygame.K_UP and game.direction_command == 2:
                        game.direction_command = 2
                    if event.key == pygame.K_DOWN and game.direction_command == 3:
                        game.direction_command = 3
        pygame.display.flip()
    pygame.quit()
if __name__ == "__main__":
    main()