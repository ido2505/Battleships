import pygame
import pygame_gui
from pygame.locals import *
import select
from typing import Tuple, Optional

import client_side
from game_manager import GameManager
from player_communication import PlayerCommunication


class BattleshipsUI:
    WINDOW_HEIGHT = 510
    WINDOW_WIDTH = 1420

    CHAT_TEXT_BOX_X_POSITION = 1130
    CHAT_TEXT_BOX_Y_POSITION = 470
    CHAT_TEXT_BOX_HEIGHT = 30
    CHAT_TEXT_BOX_WIDTH = 280

    CHAT_MESSAGE_TEXT_X_POSITION = CHAT_TEXT_BOX_X_POSITION + 20
    CHAT_MESSAGE_TEXT_Y_POSITION = 30

    PLAYER_BOARD_X_POSITION = 600
    PLAYER_BOARD_Y_POSITION = 0
    ENEMY_BOARD_X_POSITION = 0
    ENEMY_BOATD_Y_POSITION = 0

    UI_CLOCK_TICKS = 30
    UI_REFRESH_RATE = UI_CLOCK_TICKS / 1000

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
    CHAT_TEXT_COLOR = (0, 0, 0)

    GAME_FONT = 'freesansbold.ttf'
    GAME_FONT_SIZE = 16

    TIMEOUT = 0

    def __init__(self, game_communication: PlayerCommunication, chat_communication: PlayerCommunication):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.Font(self.GAME_FONT, self.GAME_FONT_SIZE)

        self.chat_ui_manager = pygame_gui.UIManager((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.chat_text_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
            (self.CHAT_TEXT_BOX_X_POSITION, self.CHAT_TEXT_BOX_Y_POSITION), (self.CHAT_TEXT_BOX_WIDTH,
                                                                             self.CHAT_TEXT_BOX_HEIGHT)),
            manager=self.chat_ui_manager,
            object_id='#chat_text_entry')

        self.game_manager = GameManager()
        self.game_communication = game_communication
        self.chat_communication = chat_communication

    def run_game(self) -> None:
        """
        this function is the main game loop
        """
        # the client always start to play
        if isinstance(self.game_communication, client_side.ClientSide):
            my_turn = True
        else:
            my_turn = False
        tile_picked = False
        chat_sent_message = None
        chat_message = None

        game_running = True
        while game_running:
            # fill background
            self.screen.fill(self.BACKGROUND_COLOR)

            # draw_player_board
            self.draw_board(self.PLAYER_BOARD_X_POSITION, self.PLAYER_BOARD_Y_POSITION, self.game_manager.player_board)
            # draw_enemy board
            self.draw_board(self.ENEMY_BOARD_X_POSITION, self.ENEMY_BOATD_Y_POSITION, self.game_manager.enemy_board)

            tile_position = self.TILE_NOT_EXIST
            # check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False

                if event.type == pygame.MOUSEBUTTONUP:
                    # check if tile was clicked
                    tile_position = self.check_tile_click(*event.pos)
                    tile_picked = self.tile_clicked_handler(my_turn, tile_picked, tile_position)

                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#chat_text_entry":
                    chat_sent_message = event.text
                    self.chat_text_box.set_text("")

                # chat ui process any events
                self.chat_ui_manager.process_events(event)

            my_turn = self.turn_handler(my_turn, tile_picked, tile_position)
            tile_picked = False

            new_message = self.chat_message_handler(chat_sent_message)
            if new_message is not None:
                chat_message = new_message
            chat_sent_message = None

            # check for win or lost
            if self.game_manager.check_for_win(self.game_manager.player_board):
                # TODO: print player victory
                print("player won!")
                game_running = False

            elif self.game_manager.check_for_win(self.game_manager.enemy_board):
                # TODO: print player lost
                print("player lost!")
                game_running = False

            # display chat
            self.chat_ui_manager.update(self.UI_REFRESH_RATE)
            self.chat_ui_manager.draw_ui(self.screen)

            if chat_message is not None:
                self.display_chat_message(chat_message)

            pygame.display.update()
            self.clock.tick(self.UI_CLOCK_TICKS)

        self.game_communication.close_communication()
        pygame.quit()

    def display_chat_message(self, message_to_display: str) -> None:
        """
        get a message and print it in the chat messages position
        :param message_to_display: message to display
        """
        text = self.game_font.render(message_to_display, True, self.CHAT_TEXT_COLOR, self.BACKGROUND_COLOR)
        text_rectangle = text.get_rect()
        text_rectangle.center = (self.CHAT_MESSAGE_TEXT_X_POSITION, self.CHAT_MESSAGE_TEXT_Y_POSITION)

        self.screen.blit(text, text_rectangle)

    def chat_message_handler(self, message_to_send: str = None) -> Optional[str]:
        """
        handle chat messaging logic
        :param message_to_send: if the user have a message to send. can be None if the user don't have a message
        :return: return a message from the enemy. return None if the enemy don't have new message
        """
        ready_chat_socket = select.select([self.chat_communication.socket], [], [], self.TIMEOUT)[0]

        if message_to_send:
            self.chat_communication.send_chat_message(message_to_send)
            print("sent this message: " + message_to_send)

        if ready_chat_socket:
            chat_message = self.chat_communication.get_message().decode()[1:]
            print("new chat message: " + chat_message)
            return chat_message
        else:
            return None

    def tile_clicked_handler(self, my_turn: bool, tile_picked: bool, tile_position: Tuple[int, int]) -> bool:
        """
        handle the logic in the tile picking
        :param my_turn: if the player should play
        :param tile_picked: if the player already picked a tile
        :param tile_position: the position of the tile
        :return: the new tile_picked state
        """
        if tile_position != self.TILE_NOT_EXIST and not self.game_manager.check_if_tile_clicked(*tile_position) and \
                my_turn and not tile_picked:
            self.game_communication.send_chosen_tile(*tile_position)
            print("tile picked, position: " + str(tile_position))
            return True
        return False

    def turn_handler(self, my_turn: bool, tile_picked: bool = False, tile_position: Tuple[int, int] = None) -> bool:
        """
        Do the turn logic.
        :param my_turn: if the player should play
        :param tile_picked: if the player picked a tile
        :param tile_position: the tile that the player picked
        :return: if now the state of the turn has changed
        """

        # using select for jumping whenever the socket get a message
        ready_game_socket = select.select([self.game_communication.socket], [], [], self.TIMEOUT)[0]

        # get the tile status
        if my_turn and tile_picked:
            message = self.game_communication.get_message()
            print("got tile status, len: " + str(len(message)))
            tile_status = self.game_communication.get_tile_status(message[1:])

            self.game_manager.enemy_tile_clicked(tile_status, *tile_position)
            print("enemy turn now")
            return False

        if not my_turn:
            # waiting for the other player to play and get his message
            if ready_game_socket:
                message = self.game_communication.get_message()
                tile_position = self.game_communication.get_chosen_tile(message[1:])
                print("got enemy click, tile position: " + str(tile_position))
                tile_status = self.game_manager.player_tile_clicked(*tile_position)

                # send the chosen tile status
                self.game_communication.send_tile_status(tile_status)

                print("my turn now")
                return True

        return my_turn

    def draw_board(self, start_x_position: int, start_y_position: int, board_to_draw: list) -> None:
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
