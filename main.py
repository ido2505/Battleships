import battleships_ui
import player_communication
import client_side
import server_side
import menu_ui

import numpy
import sys


def main():
    # menu_ui.MenuUI()
    if sys.argv[1] == 'server':
        game_communication = server_side.ServerSide(player_communication.DEFAULT_GAME_PORT)
        chat_communication = server_side.ServerSide(player_communication.DEFAULT_CHAT_PORT)
    elif sys.argv[1] == 'client':
        game_communication = client_side.ClientSide(sys.argv[2], player_communication.DEFAULT_GAME_PORT)
        chat_communication = client_side.ClientSide(sys.argv[2], player_communication.DEFAULT_CHAT_PORT)
    else:
        raise Exception

    game = battleships_ui.BattleshipsUI(game_communication, chat_communication)
    game.run_game()


if __name__ == "__main__":
    main()
