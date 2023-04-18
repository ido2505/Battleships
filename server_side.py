import socket

from player_communication import PlayerCommunication


class ServerSide(PlayerCommunication):
    def __init__(self, target_port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("127.0.0.1", target_port))

        self.server_socket.listen()
        self._socket, self.address = self.server_socket.accept()

    @property
    def socket(self):
        return self._socket
