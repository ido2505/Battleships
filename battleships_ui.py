import pygame
from pygame.locals import *
import select

import client_side
from game_manager import GameManager
from player_communication import PlayerCommunication


class BattleshipsUI:
    WINDOW_HEIGHT = 510
    WINDOW_WIDTH = 1120

    TILE_SIZE = 40
    TILE_X_MARGIN = 10
    TILE_Y_MARGIN = 10

    TILE_EMPTY_COLOR = (0, 207, 0)
    TILE_NEAR_BATTLESHIP_COLOR = (255, 255, 0)
    TILE_BATTLESHIP_COLOR = (255, 0, 0)
    TILE_DAMAGED_BATTLESHIP_COLOR = (0, 0, 0)
    TILE_UNKNOWN_COLOR = (220, 220, 220)
    TILE_COLOR_CHOICES = [TILE_EMPTY_COLOR, TILE_BATTLESHIP_COLOR, TILE_NEAR_BATTLESHIP_COLOR,
                          TILE_DAMAGED_BATTLESHIP_COLOR, TILE_UNKNOWN_COLOR]

    TILE_NOT_EXIST = (-1, -1)

    BACKGROUND_COLOR = (255, 255, 255)

    TIMEOUT = 0

    def __init__(self, player_communication: PlayerCommunication):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.game_manager = GameManager()
        self.player_communication = player_communication

        # using select for jumping whenever the socket get a message
        self.ready_socket = select.select([self.player_communication.socket], [], [], self.TIMEOUT)[0]

        self.run_game()

    def run_game(self) -> None:
        """
        this function is the main game loop
        """
        if isinstance(self.player_communication, client_side.ClientSide):
            my_turn = 1
        else:
            my_turn = 0

        picked_tile = 0

        game_running = True
        while game_running:
            # fill background
            self.screen.fill(self.BACKGROUND_COLOR)

            # draw_player_board
            self.draw_board(600, 0, self.game_manager.player_board)

            # draw_enemy board
            self.draw_board(0, 0, self.game_manager.enemy_board)

            # using select for jumping whenever the socket get a message
            ready_socket = select.select([self.player_communication.socket], [], [], self.TIMEOUT)[0]
            # ready_socket = True

            tile_position = self.TILE_NOT_EXIST
            # check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                    pygame.quit()

                elif event.type == pygame.MOUSEBUTTONUP:
                    # check if tile was clicked
                    tile_position = self.check_tile_click(*event.pos)
                    if tile_position != self.TILE_NOT_EXIST and my_turn:
                        if picked_tile == 0:
                            self.player_communication.send_chosen_tile(*tile_position)
                            print("tile picked, position: " + str(tile_position))
                            picked_tile = 1

            # get the tile status
            if my_turn == 1 and picked_tile == 1:
                message = self.player_communication.get_message()
                print("got tile status, len: " + str(len(message)))
                tile_status = self.player_communication.get_tile_status(message[1:])

                self.game_manager.enemy_tile_clicked(tile_status, *tile_position)
                my_turn = 0
                picked_tile = 0
                print("enemy turn now")

            if my_turn == 0:
                # waiting for the other player to play and get his message
                if ready_socket:
                    message = self.player_communication.get_message()
                    tile_position = self.player_communication.get_chosen_tile(message[1:])
                    print("got enemy click, tile position: " + str(tile_position))
                    tile_status = self.game_manager.player_tile_clicked(*tile_position)

                    # send the chosen tile status
                    self.player_communication.send_tile_status(tile_status)

                    my_turn = 1
                    print("my turn now")

            pygame.display.update()
            self.clock.tick(30)

    def draw_board(self, start_x_position: int, start_y_position: int, board_to_draw: [int][int]) -> None:
        """
        Function draws the game board.
        """
        # draws the grids depending on its state
        for tile_x in range(GameManager.BOARD_LENGTH):
            for tile_y in range(GameManager.BOARD_LENGTH):
                pygame.draw.rect(self.screen,
                                 self.TILE_COLOR_CHOICES[board_to_draw[tile_x][tile_y]],
                                 (start_x_position + tile_x * self.TILE_SIZE + self.TILE_X_MARGIN * (tile_x + 1),
                                  start_y_position + tile_y * self.TILE_SIZE + self.TILE_Y_MARGIN * (tile_y + 1),
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
