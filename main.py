# autor: Roman Pindela / roman.pindela@gmail.com
import os   #from os import system, name
from time import sleep
import random

# import project modules
from utils import *
from classes_additional import *
from classes_primary import *


def main() -> None:

    clear_screen()

    Battleship_game = Battleship(Player("Player1"),Player("Player2"),turn_limit=10, board_size=10, ships_number=2)
    game = Game(Battleship_game)
    game.play()

if __name__ == '__main__':
    main()