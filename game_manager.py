from array import *
import random


class GameManager:
    BOARD_LENGTH = 10
    BATTLE_SHIPS_LENGTHS = [5, 4, 3, 3, 2]

    EMPTY_INDEX = 0
    BATTLESHIP_INDEX = 1
    NEAR_BATTLESHIP_INDEX = 2

    def __init__(self):
        self.player_board = [[0 for i in range(self.BOARD_LENGTH)] for j in range(self.BOARD_LENGTH)]
        self.enemy_board = [[0 for i in range(self.BOARD_LENGTH)] for j in range(self.BOARD_LENGTH)]
        self.generate_player_board()

    def generate_player_board(self) -> None:
        """
        randomly generate ships in the player board.
        """
        for battleship in self.BATTLE_SHIPS_LENGTHS:
            x_position = random.randint(0, self.BOARD_LENGTH)
            y_position = random.randint(0, self.BOARD_LENGTH)
            is_vertical = bool(random.randint(0, 1))

            while not self.check_inbound_battleship_position(x_position, y_position, battleship, is_vertical) or \
                    not self.validate_battleship_position(x_position, y_position, battleship, is_vertical):
                x_position = random.randint(0, self.BOARD_LENGTH)
                y_position = random.randint(0, self.BOARD_LENGTH)
                is_vertical = bool(random.randint(0, 1))

            self.place_battleship(x_position, y_position, battleship, is_vertical)

    def check_inbound_battleship_position(self, x_position: int, y_position, battleship_length: int, is_vertical: bool) -> bool:
        """
        check if the wanted battleship position is in the player board.
        :param x_position: the wanted x position
        :param y_position: the wanted y position
        :param battleship_length: the length of the wanted battleship
        :param is_vertical: if the battleship will be places vertically
        :return: if the battleship is inbound.
        """
        if is_vertical:
            return x_position + battleship_length < 10 and y_position < 10
        else:
            return x_position < 10 and y_position + battleship_length < 10

    def validate_battleship_position(self, x_position: int, y_position: int, battleship_length: int, is_vertical: bool) -> bool:
        """
        check if the battleship position is valid and the battleship can be placed.
        :param x_position: the wanted x position
        :param y_position: the wanted y position
        :param battleship_length: the length of the wanted battleship
        :param is_vertical: if the battleship will be places vertically
        :return: if you can place the battleship in the wanted position
        """
        for index in range(0, battleship_length):
            if is_vertical:
                if self.player_board[x_position + index][y_position] != self.EMPTY_INDEX:
                    return False
                if y_position < self.BOARD_LENGTH - 1 and self.player_board[x_position + index][y_position + 1] != self.EMPTY_INDEX:
                    return False
                if y_position > 0 and self.player_board[x_position + index][y_position - 1] != self.EMPTY_INDEX:
                    return False
            elif not is_vertical:
                if self.player_board[x_position][y_position + index] != self.EMPTY_INDEX:
                    return False
                if x_position < self.BOARD_LENGTH - 1 and self.player_board[x_position + 1][y_position + index] != self.EMPTY_INDEX:
                    return False
                if x_position > 0 and self.player_board[x_position - 1][y_position + index] != self.EMPTY_INDEX:
                    return False
        return True

    def place_battleship(self, x_position: int, y_position: int, battleship_length: int, is_vertical: bool) -> None:
        """
        place battleship in the player board. also place the near battleship sings.
        :param x_position: the wanted x position
        :param y_position: the wanted y position
        :param battleship_length: the length of the wanted battleship
        :param is_vertical: if the battleship will be placed vertically
        """
        for index in range(0, battleship_length):
            if is_vertical:
                self.player_board[x_position + index][y_position] = self.BATTLESHIP_INDEX
                if y_position != self.BOARD_LENGTH - 1:
                    self.player_board[x_position + index][y_position + 1] = self.NEAR_BATTLESHIP_INDEX
                if y_position != 0:
                    self.player_board[x_position + index][y_position - 1] = self.NEAR_BATTLESHIP_INDEX

            else:
                self.player_board[x_position][y_position + index] = self.BATTLESHIP_INDEX
                if x_position != self.BOARD_LENGTH - 1:
                    self.player_board[x_position + 1][y_position + index] = self.NEAR_BATTLESHIP_INDEX
                if x_position != 0:
                    self.player_board[x_position - 1][y_position + index] = self.NEAR_BATTLESHIP_INDEX

        # Add diagonal, front and back near battleship index
        if is_vertical:
            if x_position != 0:
                self.player_board[x_position - 1][y_position] = self.NEAR_BATTLESHIP_INDEX
                if y_position != 0:
                    self.player_board[x_position - 1][y_position - 1] = self.NEAR_BATTLESHIP_INDEX
                if y_position != self.BOARD_LENGTH - 1:
                    self.player_board[x_position - 1][y_position + 1] = self.NEAR_BATTLESHIP_INDEX
            if x_position + battleship_length != self.BOARD_LENGTH:
                self.player_board[x_position + battleship_length][y_position] = self.NEAR_BATTLESHIP_INDEX
                if y_position != 0:
                    self.player_board[x_position + battleship_length][y_position - 1] = self.NEAR_BATTLESHIP_INDEX
                if y_position != self.BOARD_LENGTH - 1:
                    self.player_board[x_position + battleship_length][y_position + 1] = self.NEAR_BATTLESHIP_INDEX
        else:
            if y_position != 0:
                self.player_board[x_position][y_position - 1] = self.NEAR_BATTLESHIP_INDEX
                if x_position != 0:
                    self.player_board[x_position - 1][y_position - 1] = self.NEAR_BATTLESHIP_INDEX
                if x_position != self.BOARD_LENGTH - 1:
                    self.player_board[x_position + 1][y_position - 1] = self.NEAR_BATTLESHIP_INDEX
            if y_position + battleship_length != self.BOARD_LENGTH:
                self.player_board[x_position][y_position + battleship_length] = self.NEAR_BATTLESHIP_INDEX
                if x_position != 0:
                    self.player_board[x_position - 1][y_position + battleship_length] = self.NEAR_BATTLESHIP_INDEX
                if x_position != self.BOARD_LENGTH - 1:
                    self.player_board[x_position + 1][y_position + battleship_length] = self.NEAR_BATTLESHIP_INDEX