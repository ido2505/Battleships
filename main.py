import game_manager
import battleships_ui
import player_communication
import client_side
import server_side
import menu_ui

import numpy
import sys


def main():
    # menu_ui.MenuUI()
    communication = None
    if sys.argv[1] == 'server':
        communication = server_side.ServerSide()
    elif sys.argv[1] == 'client':
        communication = client_side.ClientSide(sys.argv[2])
    else:
        raise Exception

    battleships_ui.BattleshipsUI(communication)


if __name__ == "__main__":
    main()
