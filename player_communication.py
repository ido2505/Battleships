from abc import ABC, abstractmethod
import struct

DEFAULT_GAME_PORT = 1338
DEFAULT_CHAT_PORT = 1400


class PlayerCommunication(ABC):
    STATUS_PRE_MESSAGE = "b"
    TILE_PICK_MESSAGE = "bb"
    GAME_WIN_MESSAGE = "b"
    TILE_STATUS_MESSAGE = "b"

    TILE_PICK_STATUS = 1
    TILE_STATUS_STATUS = 2
    GAME_WIN_STATUS = 3
    CHAT_STATUS = 4

    @property
    @abstractmethod
    def socket(self):
        pass

    def get_message(self):
        return self.socket.recv(1024)

    def send_chosen_tile(self, x_position: int, y_position: int) -> None:
        message = struct.pack(self.STATUS_PRE_MESSAGE + self.TILE_PICK_MESSAGE, self.TILE_PICK_STATUS, x_position,
                              y_position)
        self.socket.send(message)

    def get_chosen_tile(self, data) -> (int, int):
        return struct.unpack(self.TILE_PICK_MESSAGE, data)

    def send_tile_status(self, status: int) -> None:
        message = struct.pack(self.STATUS_PRE_MESSAGE + self.TILE_STATUS_MESSAGE, self.TILE_STATUS_STATUS, status)
        self.socket.send(message)

    def get_tile_status(self, data) -> int:
        return struct.unpack(self.TILE_STATUS_MESSAGE, data)[0]

    def send_chat_message(self, message: str) -> None:
        message = struct.pack(self.STATUS_PRE_MESSAGE, self.CHAT_STATUS) + message.encode()
        self.socket.send(message)

    def send_game_win_message(self, status: int) -> None:
        message = struct.pack(self.STATUS_PRE_MESSAGE + self.GAME_WIN_MESSAGE, self.GAME_WIN_STATUS, status)
        self.socket.send(message)

    def close_communication(self) -> None:
        self.socket.close()
