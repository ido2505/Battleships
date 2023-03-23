import pygame
from pygame.locals import *

from game_manager import GameManager


class BattleshipsUI:
    WINDOW_HEIGHT = 510
    WINDOW_WIDTH = 1200

    TILE_SIZE = 40
    TILE_X_MARGIN = 10
    TILE_Y_MARGIN = 10

    TILE_EMPTY_COLOR = (0, 207, 0)
    TILE_NEAR_BATTLESHIP_COLOR = (255, 255, 0)
    TILE_BATTLESHIP_COLOR = (255, 0, 0)
    TILE_COLOR_CHOICES = [TILE_EMPTY_COLOR, TILE_BATTLESHIP_COLOR, TILE_NEAR_BATTLESHIP_COLOR]

    TILE_NOT_EXIST = (-1, -1)

    BACKGROUND_COLOR = (255, 255, 255)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_manager = GameManager()

        self.run_game()

        pygame.quit()

    def run_game(self) -> None:
        """
        this function is the main game loop
        """
        game_running = True
        while game_running:
            # fill background
            self.screen.fill(self.BACKGROUND_COLOR)

            # draw_player_board
            self.draw_board(0, 600, self.game_manager.player_board)

            # draw_enemy board
            self.draw_board(0, 0, self.game_manager.enemy_board)

            pygame.display.flip()

            # check for other events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    tile_position = self.check_tile_click(*event.pos)
                    print(tile_position)
                    if tile_position != self.TILE_NOT_EXIST:
                        # self.game_manager.tile_clicked()
                        pass

    def draw_board(self, start_x_position: int, start_y_position: int, board_to_draw) -> None:
        """
        Function draws the game board.
        """
        # draws the grids depending on its state
        for tile_x in range(GameManager.BOARD_LENGTH):
            for tile_y in range(GameManager.BOARD_LENGTH):
                pygame.draw.rect(self.screen,
                                 self.TILE_COLOR_CHOICES[board_to_draw[tile_x][tile_y]],
                                 (start_y_position + tile_y * self.TILE_SIZE + self.TILE_Y_MARGIN * (tile_y + 1),
                                  start_x_position + tile_x * self.TILE_SIZE + self.TILE_X_MARGIN * (tile_x + 1),
                                  self.TILE_SIZE,
                                  self.TILE_SIZE,
                                  ))

    def check_tile_click(self, x_position: int, y_position: int) -> (int, int):
        """
        check if the click was on a tile.
        :param x_position: the mouse x position click
        :param y_position: the mouse y position click
        :return: x tile index, y tile index
        """
        x_tile_clicked = x_position // (self.TILE_X_MARGIN + self.TILE_SIZE)
        y_tile_clicked = y_position // (self.TILE_Y_MARGIN + self.TILE_SIZE)

        # check if click out of bound
        if x_tile_clicked >= 10 or y_tile_clicked >= 10:
            return self.TILE_NOT_EXIST

        # check if the click is in the margin
        if x_position - x_tile_clicked * (self.TILE_SIZE + self.TILE_X_MARGIN) < self.TILE_X_MARGIN or \
                y_position - y_tile_clicked * (self.TILE_SIZE + self.TILE_Y_MARGIN) < self.TILE_Y_MARGIN:
            return self.TILE_NOT_EXIST

        return x_tile_clicked, y_tile_clicked
