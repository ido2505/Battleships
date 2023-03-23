from abc import ABC, abstractmethod
import struct


class PlayerCommunication(ABC):
    COMMUNICATION_PORT = 1337

    STATUS_PRE_MESSAGE = "b"
    TILE_PICK_MESSAGE = "bb"
    GAME_WIN_MESSAGE = "b"

    TILE_PICK_STATUS = 1
    GAME_WIN_STATUS = 2
    CHAT_STATUS = 3

    @property
    @abstractmethod
    def socket(self):
        pass

    def get_message(self):
        return self.socket.recv()

    def send_chosen_tile(self, x_position: int, y_position: int) -> None:
        message = struct.pack(self.STATUS_PRE_MESSAGE + self.TILE_PICK_MESSAGE, self.TILE_PICK_STATUS, x_position,
                              y_position)
        self.socket.send(message)

    def get_chosen_tile(self, data) -> (int, int):
        return struct.unpack(self.TILE_PICK_MESSAGE, data)

    def send_chat_message(self, message: str) -> None:
        message = struct.pack(self.STATUS_PRE_MESSAGE, self.CHAT_STATUS) + message.encode()
        self.socket.send(message)

    def send_game_win_message(self, status: int) -> None:
        message = struct.pack(self.STATUS_PRE_MESSAGE + self.GAME_WIN_MESSAGE, self.GAME_WIN_STATUS, status)
        self.socket.send(message)

    def close_communication(self) -> None:
        self.socket.close()
