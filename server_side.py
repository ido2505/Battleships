import socket

from player_communication import PlayerCommunication


class ServerSide(PlayerCommunication):
    def __init__(self):
        # get the hostname
        host = socket.gethostname()

        self.server_socket = socket.socket()
        self.server_socket.bind((host, self.COMMUNICATION_PORT))

        self.server_socket.listen()
        self._socket, self.address = self.server_socket.accept()

    @property
    def socket(self):
        return self.socket
