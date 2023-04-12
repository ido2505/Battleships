from array import *
import random


class GameManager:
    BOARD_LENGTH = 10
    BATTLE_SHIPS_LENGTHS = [5, 4, 3, 3, 2]

    EMPTY_INDEX = 0
    BATTLESHIP_INDEX = 1
    NEAR_BATTLESHIP_INDEX = 2
    DAMAGED_BATTLESHIP_INDEX = 3
    UNKNOWN_INDEX = 4

    def __init__(self):
        self.player_board = [[self.EMPTY_INDEX for i in range(self.BOARD_LENGTH)] for j in range(self.BOARD_LENGTH)]
        self.enemy_board = [[self.UNKNOWN_INDEX for i in range(self.BOARD_LENGTH)] for j in range(self.BOARD_LENGTH)]
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

    def enemy_tile_clicked(self, tile_status: int, x_position: int, y_position: int) -> None:
        print("enemy tile status: " + str(tile_status))
        self.enemy_board[x_position][y_position] = tile_status

    def player_tile_clicked(self, x_position: int, y_position: int) -> int:
        """
        update the player board on the enemy action and check the status of the enemy chosen tile
        :param x_position: the chosen tile x position
        :param y_position: the chosen tile y position
        :return: the status of the chosen tile.
        if a battleship was hit the board updates to damaged battleship but return battleship index
        """
        # check if a battleship got hit
        if self.player_board[x_position][y_position] == self.BATTLESHIP_INDEX:
            self.player_board[x_position][y_position] = self.DAMAGED_BATTLESHIP_INDEX
            return self.BATTLESHIP_INDEX

        return self.player_board[x_position][y_position]

    def check_for_win(self, board_to_check: list) -> bool:
        """
        check if the current board won
        :param board_to_check: the board to check the winning
        :return: True if the board won
        """
        num_of_damaged_battleships = 0

        for i in range(0, self.BOARD_LENGTH):
            for j in range(0, self.BOARD_LENGTH):
                if board_to_check[i][j] == self.DAMAGED_BATTLESHIP_INDEX:
                    num_of_damaged_battleships += 1

        return num_of_damaged_battleships == sum(self.BATTLE_SHIPS_LENGTHS)
