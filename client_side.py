import socket

from player_communication import PlayerCommunication


class ClientSide(PlayerCommunication):
    def __init__(self, target_ip):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((target_ip, self.COMMUNICATION_PORT))

    @property
    def socket(self):
        return self._socket
