import battleships_ui
import player_communication
import client_side
import server_side
import menu_ui

import numpy
import sys


def main():
    menu = menu_ui.MenuUI()
    connection_type, ip_address = menu.run_menu()
    print(connection_type)

    if connection_type == "Server":
        game_communication = server_side.ServerSide(player_communication.DEFAULT_GAME_PORT)
        chat_communication = server_side.ServerSide(player_communication.DEFAULT_CHAT_PORT)
    elif connection_type == "Connect":
        game_communication = client_side.ClientSide(ip_address, player_communication.DEFAULT_GAME_PORT)
        chat_communication = client_side.ClientSide(ip_address, player_communication.DEFAULT_CHAT_PORT)
    else:
        raise Exception("Invalid connection type")

    game = battleships_ui.BattleshipsUI(game_communication, chat_communication)
    game.run_game()


if __name__ == "__main__":
    main()
