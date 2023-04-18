import socket

from player_communication import PlayerCommunication


class ClientSide(PlayerCommunication):
    def __init__(self, target_ip, target_port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((target_ip, target_port))

    @property
    def socket(self):
        return self._socket
