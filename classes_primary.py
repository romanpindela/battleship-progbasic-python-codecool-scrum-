# autor: Roman Pindela / roman.pindela@gmail.com
from os import system, name
import numpy
#import pandas #used for Board.print_board()
import random
from random import choice 

import time
from classes_additional import *
from utils import *
import string

# moduł: main_classes

class Board:
    def __init__(self, size: int =  5) -> None:
        self.rows = size
        self.columns = size
        self.board = [[Board_signs.empty_sign for row in range(self.rows)] for column in range(self.columns)]

        self.rows_labels = [letter for letter in string.ascii_uppercase if string.ascii_uppercase.index(letter) < self.columns]
        self.columns_labels = [number+1 for number in range(self.rows)]

    # def print_board(self) -> None: # for tests only
    #     board_to_print = pandas.DataFrame(self.board,columns=self.columns_labels,index=self.rows_labels)
    #     print(board_to_print)

    def is_cell_empty(self, cell_01: list) -> bool: # test if cell in 01 format is empty (for phase_ships_shooting)
        return True if self.board[cell_01[0]][cell_01[1]] == Board_signs.empty_sign else False


class Ship:
    types_of_ships = {1:[Board_signs.ship_sign,Board_signs.ship_sign,Board_signs.ship_sign,Board_signs.ship_sign,Board_signs.ship_sign],2:[Board_signs.ship_sign,Board_signs.ship_sign,Board_signs.ship_sign,Board_signs.ship_sign],3:[Board_signs.ship_sign,Board_signs.ship_sign,Board_signs.ship_sign],4:[Board_signs.ship_sign,Board_signs.ship_sign]}
    orientation = {"v":"vertical", "h":"horizontal"}
    
    def __init__(self, ship_type: int, orientation: str, start_coordination: str) -> None:
        self.start_coordination = start_coordination
        self.ship_type = ship_type
        self.orientation = orientation

        self.ship_spots_coordinations = [] # list of coordinations of ship's spots i.e. [[2,3],[2,4]]

    def get_ship_init_values(self) -> list: # for tests only
        return [self.ship_type, self.orientation, self.start_coordination]

class Ships:
    ships_types = Ship.types_of_ships
    ship_orientation = Ship.orientation

    def __init__(self, ships_number: int = 2 , board_size: int = 5) -> None:
        self.ships_number = ships_number
        self.chosen_placed_ships_number = ships_number

        self.chosen_ships = []

        self.ships_board = Board(board_size) # board with ships and hits
        self.board_size = board_size
        self.rows_labels = [letter for letter in string.ascii_uppercase if string.ascii_uppercase.index(letter) < self.board_size]
        self.columns_labels = [number+1 for number in range(self.board_size)]

    def are_ships_sunk(self) -> bool:   # checks all ships if they're sunk and indirectly if player's owner of this board lost game
        sunk_ships = 0
        ships_count = len(self.chosen_ships)
        for ship_id in range(0, len(self.chosen_ships)):
            if self.is_ship_sunk(self.chosen_ships[ship_id]) == True:
                sunk_ships += 1
        return True if sunk_ships == ships_count else False

    def is_ship_sunk(self, ship_to_check: Ship) -> bool: # checks one ship if it's sunk
        ship_lenght = len(Ship.types_of_ships[ship_to_check.ship_type])
        hit_spots_count = 0
        row = 0
        column = 1
        hit_counts = 0
        for spot_coordination in ship_to_check.ship_spots_coordinations:
            if self.ships_board.board[spot_coordination[row]][spot_coordination[column]] == Board_signs.hit_sign or self.ships_board.board[spot_coordination[row]][spot_coordination[column]] == Board_signs.sunk_sign:
                hit_counts += 1 
        sunk_ship_condition = hit_counts == ship_lenght
        return True if sunk_ship_condition else False

    def print_board(self) -> None: # for now only for test uses
        board_to_print = pandas.DataFrame(self.ships_board,columns=self.columns_labels,index=self.rows_labels)
        print(board_to_print)

    def show_available_ships_set(self) -> None:

        print(f"{colors.b}Here's list of available ship types:{colors._}")
        print(f"No.  Class of ship	Size (in cells)")
        print(f"1.   {colors.fg.green}Carrier{colors.reset}\t\t{colors.fg.yellow}5{colors.reset} [{colors.fg.green}S S S S S{colors.reset}]")
        print(f"2.   {colors.fg.green}Battleship{colors.reset}\t\t{colors.fg.yellow}4{colors.reset} [{colors.fg.green}S S S S{colors.reset}]")
        print(f"3.   {colors.fg.green}Destroyer{colors.reset}\t\t{colors.fg.yellow}3{colors.reset} [{colors.fg.green}S S S{colors.reset}]")
        print(f"4.   {colors.fg.green}Patrol Boat{colors.reset}\t{colors.fg.yellow}2{colors.reset} [{colors.fg.green}S S{colors.reset}]")

    def ask_for_ship(self, ship_id: int = 1, mode_human_or_ai: str = 'human') -> bool:   #, random_ai_ship: list = []
        player_wants_to_place_ship = True
        ship_is_not_placed = True # if user want's to quit placing one of a ship
        while player_wants_to_place_ship and ship_is_not_placed:
            if mode_human_or_ai == 'human':
                print(f"{colors.fg.orange}You're choosing {ship_id}\'th ship. You've decided to place total of {self.chosen_placed_ships_number} ships.{colors.reset}")
                # 1st ask for ship type
                ship_type = self.ask_for_type_of_ship(force_correct_input=True)
                # 2nd ask for ship placement of choosen ship type
                ship_orientation = self.ask_for_orientation_of_ship(force_correct_input=True)
                # 3th ask for ship start (corner) coordination
                ship_start_coordination = self.ask_for_start_coordination_of_ship(force_correct_input=True)
                # 4th try to place ship in current player board
            elif mode_human_or_ai == 'ai':
                ai_ship = Game_mode_questions.ai_ai_get_random_ship(self)
                ship_type = ai_ship[0]
                ship_orientation = ai_ship[1]
                ship_start_coordination = ai_ship[2]

            if self.place_ship_on_board(ship_type, ship_orientation, ship_start_coordination):
                ship_is_not_placed = False
            else: #user's input for new ship can't place ship on current board, ask if want to try again
                if mode_human_or_ai == 'human':
                    question = f"{colors.fg.green}Ship No: {colors.reset}{colors.fg.yellow}{ship_id}{colors.reset}{colors.fg.green} can't be placed on current board.Try again ? (Y/N): {colors._}: "
                    user_choice = input(question)
                    while not (user_choice.upper() in ['N', 'Y']):
                        user_choice = input(question)

                    if user_choice.upper() == 'N':
                        if self.chosen_placed_ships_number > 0: # only if user doesn't want to place one of at least 2 ships
                            player_wants_to_place_ship = False 
                            self.chosen_placed_ships_number -= 1 
                        else:
                            print(f"{colors.fg.green}Sorry, You must place at least 1 ship!{colors._}")
                    else:
                        player_wants_to_place_ship = True
        return False if ship_is_not_placed == False else True # user either placed a ship or resigned of placing it 
           
    def place_ship_on_board(self, ship_type: int, ship_orientation: str, ship_start_coordination_a1: str)  -> bool: # check if it's possible to place given ship's data, it it is correct it places ship mark sign on player's ships board
        lenght_of_ship = len(Ships.ships_types[ship_type])
        direction_in_orientation = {"left":-1,"right":1, "up":-1, "down":1}
        row = 0
        column = 1

        start_coordination = self.convert_coordinates_a1_to_00(ship_start_coordination_a1)

        is_not_nearby = True
        is_not_nearby_tail_head = True
        if ship_orientation.lower() == "h":
            #1st check and determine direction for orientation for given lenght so that ship fits in board (left or right / up or down)
            if start_coordination[row] + lenght_of_ship <= self.board_size: # ship fits verticaly from start cell to right
                direction = direction_in_orientation["down"]
            else:
                direction = direction_in_orientation["up"]
            #2nd check if proposed cells ship'spots are empty
            for next_ship_spot in range(0,len(Ship.types_of_ships[ship_type])):
                if self.ships_board.board[start_coordination[row]+next_ship_spot*direction][start_coordination[column]] ==  Board_signs.empty_sign:
                    is_cell_empty = True
                else:
                    return False # Cell is taken so there is no use checking the rest

            #3th check if nearby cells are taken by another ship's spots (besides corner spots, corners can meet)
                
                #3.1 check cells around body are empty of ship's cells are place near board border
                is_out_of_board = -1
                is_not_next_body_spot_out_of_board = True # defauult value for test below 
                upper_spot = self.ships_board.board[start_coordination[row]+next_ship_spot*direction][start_coordination[column]+1] if self.is_valid_coordination_01([start_coordination[row]+next_ship_spot*direction, start_coordination[column]+1]) else is_out_of_board # it's ok, near cell is out of board
                lower_spot = self.ships_board.board[start_coordination[row]+next_ship_spot*direction][start_coordination[column]-1] if self.is_valid_coordination_01([start_coordination[row]+next_ship_spot*direction, start_coordination[column]-1]) else is_out_of_board # it's ok, near cell is out of board
                is_not_nearby = True if ((upper_spot == Board_signs.empty_sign or upper_spot == is_out_of_board) and is_not_nearby)  else False
                is_not_nearby = True if ((lower_spot == Board_signs.empty_sign or lower_spot == is_out_of_board) and is_not_nearby) else False  
                #3.2 in addition check head
                if next_ship_spot == 0 and is_not_nearby and is_not_nearby_tail_head: #head of ship
                    before_head_spot = self.ships_board.board[start_coordination[row]+next_ship_spot*direction-direction][start_coordination[column]] if self.is_valid_coordination_01([start_coordination[row]+next_ship_spot*direction-direction, start_coordination[column]]) else is_out_of_board # it's ok, near cell is out of board
                    is_not_nearby_tail_head = True if (before_head_spot == Board_signs.empty_sign or before_head_spot == is_out_of_board) else False
                #3.3 in addition check tail
                elif (next_ship_spot == len(Ship.types_of_ships[ship_type]))-1 and is_not_nearby and is_not_nearby_tail_head: #tail of ship
                    after_tail_spot = self.ships_board.board[start_coordination[row]+next_ship_spot*direction+direction][start_coordination[column]] if self.is_valid_coordination_01([start_coordination[row]+next_ship_spot*direction+direction, start_coordination[column]]) else is_out_of_board # it's ok, near cell is out of board 
                    is_not_nearby_tail_head = True if (after_tail_spot == Board_signs.empty_sign or after_tail_spot == is_out_of_board) else False
                else: # check if body spot of ship is out of board, prevents to place half ship in right side and next part in left side
                    is_not_next_body_spot_out_of_board = True if self.is_valid_coordination_01([start_coordination[row]+next_ship_spot*direction, start_coordination[column]]) else is_out_of_board

            if is_cell_empty and is_not_nearby  and is_not_nearby_tail_head and is_not_next_body_spot_out_of_board: # it means we can place ship on player's board
                new_ship = Ship(ship_type, ship_orientation, ship_start_coordination_a1)
                for next_ship_spot in range(0,len(Ship.types_of_ships[ship_type])):
                        # 1st mark Ship.sign on Ships.ships_board 
                        spot_row = start_coordination[row]+next_ship_spot*direction
                        spot_col = start_coordination[column]
                        self.ships_board.board[spot_row][spot_col] = Board_signs.ship_sign
                        #self.ships_board.board[start_coordination[row]+next_ship_spot*direction][start_coordination[column]] = Board_signs.ship_sign
                        # 2st save ship's coordination to new ship object and save it to list of chosen ships
                        #new_ship = Ship(ship_type, ship_orientation, ship_start_coordination_a1)
                        new_ship.ship_spots_coordinations.append([spot_row, spot_col])
                #we append ship object to chosen_ships by player
                self.chosen_ships.append(new_ship)  
                #print(new_ship.ship_spots_coordinations)      
            else:
                return False
            return True

        elif ship_orientation.lower() == "v": # the same checks but for responding horizontal orientation
            #1st check and determine direction for orientation for given lenght so that ship fits in board (left or right / up or down)
            if start_coordination[column] + lenght_of_ship <= self.board_size: # ship fits verticaly from start cell to right
                direction = direction_in_orientation["right"]
            else:
                direction = direction_in_orientation["left"]
            #2nd check if proposed cells ship'spots are empty
            is_not_nearby = True
            is_not_nearby_tail_head = True
            for next_ship_spot in range(0,len(Ship.types_of_ships[ship_type])):
                if self.ships_board.board[start_coordination[row]][start_coordination[column]+next_ship_spot*direction] == Board_signs.empty_sign:
                    is_cell_empty = True
                else:
                    return False # Cell is taken so there is no use checking the rest

            #3th check if nearby cells are taken by another ship's spots (besides corner spots, corners can meet)
                
                #3.1 check cells around body are empty of ship's cells are place near board border
                is_out_of_board = -1
                is_not_next_body_spot_out_of_board = True # defauult value for test below 
                down_spot = self.ships_board.board[start_coordination[row]+1][start_coordination[column]+next_ship_spot*direction] if self.is_valid_coordination_01([start_coordination[row]+1, start_coordination[column]+next_ship_spot*direction]) else is_out_of_board # it's ok, near cell is out of board
                up_spot = self.ships_board.board[start_coordination[row]-1][start_coordination[column]+next_ship_spot*direction] if self.is_valid_coordination_01([start_coordination[row]-1, start_coordination[column]+next_ship_spot*direction]) else is_out_of_board # it's ok, near cell is out of board
                is_not_nearby = True if ((down_spot == Board_signs.empty_sign or down_spot == is_out_of_board) and is_not_nearby) else False
                is_not_nearby = True if ((up_spot == Board_signs.empty_sign or up_spot == is_out_of_board) and is_not_nearby) else False  
                #3.2 in addition check head
                if next_ship_spot == 0 and is_not_nearby and is_not_nearby_tail_head: #head of ship
                    before_head_spot = self.ships_board.board[start_coordination[row]][start_coordination[column]+next_ship_spot*direction-direction] if self.is_valid_coordination_01([start_coordination[row], start_coordination[column]+next_ship_spot*direction-direction]) else is_out_of_board # it's ok, near cell is out of board
                    is_not_nearby_tail_head = True if (before_head_spot == Board_signs.empty_sign or before_head_spot == is_out_of_board) else False
                #3.3 in addition check tail
                elif next_ship_spot == len(Ship.types_of_ships[ship_type])-1 and is_not_nearby and is_not_nearby_tail_head: #tail of ship
                    after_tail_spot = self.ships_board.board[start_coordination[row]][start_coordination[column]+next_ship_spot*direction+direction] if self.is_valid_coordination_01([start_coordination[row], start_coordination[column]+next_ship_spot*direction+direction]) else is_out_of_board # it's ok, near cell is out of board 
                    is_not_nearby_tail_head = True if (after_tail_spot == Board_signs.empty_sign or after_tail_spot == is_out_of_board) else False
                else: # check if body spot of ship is out of board, prevents to place half ship in right side and next part in left side
                    is_not_next_body_spot_out_of_board = True if self.is_valid_coordination_01([start_coordination[row]+next_ship_spot*direction, start_coordination[column]]) else is_out_of_board


            if is_cell_empty and is_not_nearby and is_not_nearby_tail_head  and is_not_next_body_spot_out_of_board: # mark Ship.sign on Ships.ships_board 
                new_ship = Ship(ship_type, ship_orientation, ship_start_coordination_a1)             
                for next_ship_spot in range(0,len(Ship.types_of_ships[ship_type])):
                        # 1st mark Ship.sign on Ships.ships_board 
                        spot_row = start_coordination[row]
                        spot_col = start_coordination[column]+next_ship_spot*direction
                        self.ships_board.board[spot_row][spot_col] = Board_signs.ship_sign
                        #self.ships_board.board[start_coordination[row]+next_ship_spot*direction][start_coordination[column]] = Board_signs.ship_sign
                        # 2st save ship's coordination to new ship object and save it to list of chosen ships
                        #new_ship = Ship(ship_type, ship_orientation, ship_start_coordination_a1)
                        new_ship.ship_spots_coordinations.append([spot_row, spot_col])
                #we append ship object to chosen_ships by player
                self.chosen_ships.append(new_ship)  
                #print(self.chosen_ships[-1].ship_spots_coordinations)     

            
            else:
                return False
            return True

    def convert_coordinates_a1_to_00(self, cordinates_a1: str) -> list: # converts A1 to [0,0]
        try:
            coordinates_row_dict = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8, 'j':9}
            row = coordinates_row_dict[str(cordinates_a1[0]).lower()]
            column = int(cordinates_a1[1])-1
            return [row, column]
        except:
            return False
    
    def ask_for_start_coordination_of_ship(self,force_correct_input: bool = True)-> str or bool: # ask for i.e. A3 as head of ship
        question = f"{colors.b}# Start coordination of ship - type in i.e. {colors.fg.green}A3{colors.reset}: "
        if force_correct_input:
            invalid_input = True
            while invalid_input:
                print(question, end="")
                user_input = input()
                if self.is_valid_coordination_a1(user_input):
                    valided_start_coordination_of_ship = user_input
                    invalid_input = False
                else:
                    print(f"{colors.fg.red}Error: Invalid start coordination of ship!{colors.reset}")
        else: # ask only one time for type of ship
                print(question, end="")
                user_input = input()
                if self.is_valid_coordination_a1(user_input):
                    valided_start_coordination_of_ship = user_input
                    invalid_input = False
                else:
                    print(f"{colors.fg.red}Error: Invalid start coordination of ship!{colors.reset}")
                    valided_start_coordination_of_ship = False
        return valided_start_coordination_of_ship

    def ask_for_type_of_ship(self,force_correct_input: bool = True)-> int or bool: # asks for id of type of ship i.e. 1,2,3,4
        question = f"{colors.b}# Type of ship - type in i.e. {colors.fg.green}2{colors.b} [1-4]{colors.reset}: "
        if force_correct_input:
            invalid_input = True
            while invalid_input:
                print(question, end="")
                user_input = input()
                if self.is_valid_ship_type(user_input):
                    valided_type_of_ship = int(user_input)
                    invalid_input = False
                else:
                    print(f"{colors.fg.red}Error: Invalid number for Type of ship!{colors.reset}")
        else: # ask only one time for type of ship
                print(question, end="")
                user_input = input()
                if self.is_valid_ship_type(user_input):
                    valided_type_of_ship = int(user_input)
                    invalid_input = False
                else:
                    print(f"{colors.fg.red}Error: Invalid number for Type of ship!{colors.reset}")
                    valided_type_of_ship = False
        return valided_type_of_ship

    def is_valid_ship_type(self, user_input: str) -> bool:  # check's if ship's id types is correct
        try: 
            valided_type_of_ship = int(user_input)
            return True if valided_type_of_ship in range(1,len(self.ships_types)+1) else False
        except:
            return False

    def ask_for_orientation_of_ship(self, force_correct_input: bool=True) -> str or bool: # asks user for orientation v/h for a ship
        question = f"{colors.b}# Orientation of ship  - type in {colors.fg.green}v{colors.b}-vertical / {colors.fg.green}h{colors.b}-horizontal{colors.reset}: "
        if force_correct_input:
            invalid_input = True
            while invalid_input:
                print(question, end="")
                user_input = input()
                if self.is_valid_ship_orientation(user_input):
                    valided_orientation_of_ship = user_input
                    invalid_input = False
                else:
                    print(f"{colors.fg.red}Error: Invalid orientation for the ship!{colors.reset}")
        else: # ask only one time for type of ship
                print(question, end="")
                user_input = input()
                if self.is_valid_ship_orientation(user_input):
                    valided_orientation_of_ship = user_input
                    invalid_input = False
                else:
                    print(f"{colors.fg.red}Error: Invalid orientation for the ship!{colors.reset}")
                    valided_orientation_of_ship = False
        return valided_orientation_of_ship

    def is_valid_coordination_a1(self, coordinates_a1: str) -> bool: # checks if coordinates in a1 format are on board
        try:
            is_hit_valid_a = True if (coordinates_a1[0].upper() in self.rows_labels) else False
            is_hit_valid_1 = True if 0 < int(coordinates_a1[1:]) <= self.board_size else False
            if is_hit_valid_a and is_hit_valid_1:
                return True
            else:
                print(f"{colors.fg.orange}Wrong input: Coordinates must be on boards !{colors.reset}")
                return False
        except:
            print(f"{colors.fg.red}Error: Invalid user input for coordinates!{colors.reset}")
            return False

    def is_valid_coordination_01(self, coordinates_01: list) -> bool: # checks if coordinates in 01 format on board
        try:
            is_hit_valid_a = True if 0 <= coordinates_01[0] < self.board_size else False
            is_hit_valid_1 = True if 0 <= coordinates_01[1] < self.board_size else False
            if is_hit_valid_a and is_hit_valid_1:
                return True
            else:
                #print(f"{colors.fg.orange}Wrong input: Coordinates must be on boards !{colors.reset}")
                return False
        except:
            print(f"{colors.fg.red}Error: Invalid user input for coordinates!{colors.reset}")
            return False

    def is_valid_ship_orientation(self, user_input: str) -> bool:
        return True if user_input in Ships.ship_orientation else False

class Player:
    def __init__(self, name: str = "Player") -> None:
        self.name = name
        self.last_move = ""
        
        #for ai logic
        self.ai_last_hit_spot_01 = []
        self.ai_list_of_nearby_hits = []


    def ai_nearby_hit_change_orientation(self):
        possible_changes = [Ship]
        self.ai_direction_of_next_try_hit = Ship.orientation


class Battleship: # Battleship logic 
    def __init__(self, player1: Player = Player(), player2: Player = Player(), turn_limit: int = 0, board_size = 5, ships_number: int = 2) -> None:
        #If the given turn limit is out of range (5-50) then the error message Invalid input! (must be between 5-50) is displayed
        #If the number of turns left reaches zero the message No more turns, it's a draw! is displayed and the game ends
        self.board_size = board_size

        self.player1 = player1
        self.player2 = player2
        self.player1_hit_board = Board(board_size)
        self.player2_hit_board = Board(board_size)
        self.player1_ships = Ships(ships_number, board_size)
        self.player2_ships = Ships(ships_number, board_size)

        self.board_do_not_peak = Board(board_size) #board that's shown while one of player is choosing his ships
        self.board_do_not_peak_init(self.board_do_not_peak) # draw's "X" sign on empty board

        self.players = [] # for iteration purpose in methods
        self.players.append(self.player1)
        self.players.append(self.player2)

        self.players_boards = [] # for iteration purpose in methods
        self.players_boards.append(self.player1_hit_board)
        self.players_boards.append(self.player2_hit_board)

        self.players_ships = [] # for iteration purpose in methods
        self.players_ships.append(self.player1_ships)
        self.players_ships.append(self.player2_ships)

        self.player_turn = self.player1.name    # player's name that currently hit's a opposite player's ship board
        self.turn_limit = turn_limit # 0 is for no limits
        self.turn_counter = turn_limit # counts for turn limits

        self.quit_game = False # for purpose of ask_for_hit_coordinates_or_quit()

    def board_do_not_peak_init(self, board_do_not_peak: Board) -> None: # method draws "X" mark on board so that user doesn't peak
        #format 1 - diagonal Missed cross
        #for index_diagonal in range(0, board_do_not_peak.columns):
        #    board_do_not_peak.board[index_diagonal][index_diagonal] = Board_signs.missed_sign
        #    board_do_not_peak.board[index_diagonal][board_do_not_peak.columns-index_diagonal-1] = Board_signs.missed_sign
        
        #format 2 - all board in Missed sings
        for row in range(0, board_do_not_peak.rows):
            for col in range(0, board_do_not_peak.columns):
                board_do_not_peak.board[row][col] = Board_signs.missed_sign


    def show_boards_for_ships_placing(self, player_id_placing_ships: int) -> None:
        if player_id_placing_ships == 0:
            self.print_both_boards(self.players_ships[player_id_placing_ships].ships_board, self.board_do_not_peak) 
        else:
            self.print_both_boards(self.board_do_not_peak, self.players_ships[player_id_placing_ships].ships_board) 


    def print_both_boards(self, board1: Board, board2: Board) -> None: # print given both boards with cell_print format scheme
  
        #variables for text formating
        separator_board = "\t"
        separator_border = "  "
        separator_player_name = "".join(" "*((board1.columns*2-1 - len(self.player1.name)))) # formula for ideal separting space between player's name 

        text_format_for_active_player_turn = "".join(f"{colors.bold}{colors.bg.lightgrey}{colors.fg.red}")
        text_format_for_reset = "".join(f"{colors.reset}")

        #printing content of both boards
        for row in range(board1.rows):
            if row == 0: #printig columns indexes etc. 1, 2, 3.. for each board

                #marking player's turn by text formating
                if not self.player_turn == self.player1.name: # Player's 1 turn
                    print(f"{separator_border}{text_format_for_active_player_turn} {self.player1.name} {text_format_for_reset}{separator_player_name}{separator_board}{separator_border}{self.player2.name}")
                else:
                    print(f"{separator_border}{self.player1.name}{separator_player_name}{separator_board}{separator_border}{text_format_for_active_player_turn} {self.player2.name} {text_format_for_reset}")

                # printing columns labels for player1's board
                print(separator_border, end = "")
                for column in range(board1.columns):           
                    print(f"{board1.columns_labels[column]} ", end = "")
                print(separator_board + separator_border, end = "")

                # printing columns labels for player2's board
                for column in range(board2.columns):           
                    print(f"{board2.columns_labels[column]} ", end = "")
                print("\n", end = "")

            # now printing content of both boards, printing for row each columns, and next row... and so on
            # 1th board
            print(f"{board1.rows_labels[row]} ", end = "") # printing player1_board row's label - A, B, C ..
            for column in range(board1.columns):    # printing 1th row's board1
                print(Board_signs.cell_print(board1.board[row][column]), "", end ="") 
            print(separator_board, end = "")
            # 2nd board
            print(f"{board2.rows_labels[row]} ", end = "") # printing player2_board row's label - A, B, C ..
            for column in range(board2.columns):    # printing 2nd row's board2
                print(Board_signs.cell_print(board2.board[row][column]), "", end ="")    
            print("\n", end = "")
    
    def determine_which_player_turn(self) -> Player:
        return self.player1 if self.player_turn == self.player1.name else self.player2

    def ask_for_hit_coordinates_or_quit(self, force_valid_input = True) -> list or bool:
        #If user enters invalid input (outside range), then the error message Invalid input! is displayed and the program asks again for an input (shooting twice at the same spot is a valid but unnecessary move)
        question = f"{colors.fg.yellow}{self.player_turn}{colors.reset} {colors.underline}A3{colors.reset} or {colors.underline}quit{colors.reset} {colors.b}(last: {self.determine_which_player_turn().last_move}){colors._}: "

        are_coordinates_valid = False
        if force_valid_input:
            while (not are_coordinates_valid or self.quit_game):
                user_input = input(question)
                if user_input == 'quit':
                    self.quit_game = True
                    return False 
                elif not user_input == "":
                    are_coordinates_valid = self.is_valid_input_coordinates(user_input)
            valided_coordinates_a1 = user_input
            self.determine_which_player_turn().last_move = valided_coordinates_a1
            return valided_coordinates_a1
        else:
            user_input = input(question)
            if user_input == 'quit':
                self.quit_game = True
                return False 
            elif not user_input == "":
                are_coordinates_valid = self.is_valid_input_coordinates(user_input)
                if are_coordinates_valid:
                    valided_coordinates_a1 = user_input
                    self.determine_which_player_turn().last_move = valided_coordinates_a1
                    return valided_coordinates_a1
                else:
                    return False
            else:
                return False

    def convert_coordinates_a1_to_00(self, cordinates_a1: str) -> list or bool: # converts A1 to [0,0]
        try:
            coordinates_row_dict = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8, 'j':9}
            row = coordinates_row_dict[str(cordinates_a1[0]).lower()]
            column = int(cordinates_a1[1:])-1
            return [row, column]
        except:
            return False

    def is_valid_input_coordinates(self, coordinates_a1: str) -> bool: # checks if hit is on board
        #check if hit is on board, regardless which player
        #is_hit_valid = bool()
        try:
            row = coordinates_a1[0]
            column_index = int(coordinates_a1[1:])
            is_hit_valid_a = True if row.upper() in self.player1_hit_board.rows_labels else False
            is_hit_valid_1 = True if 0 < column_index <= len(self.player1_hit_board.columns_labels) else False
            if is_hit_valid_a and is_hit_valid_1:
                return True
            else:
                print(f"{colors.fg.orange}Wrong input: Coordinates must be on boards !{colors.reset}")
                return False
        except:
            print(f"{colors.fg.red}Error: Invalid user input for coordinates!{colors.reset}")
            return False

    def mark_hit_board(self, hit_player_id: int, hit_spot: list) -> None: # player who currently hit opponent board and his/her hit_spot
        #Both players' 5x5 board is shown after each shooting like below, where 0 indicates an undiscovered tile, M indicates a missed shot, H indicates a hit ship part and S indicates a sunk ship part
        #Hitting, missing and sinking ship (parts) results in a message displayed as You've hit a ship!, You've missed! and You've sunk a ship! respectively
        row = 0
        column = 1
        opponent_player_id = 1 if hit_player_id == 0 else 0
        
        if self.players_boards[opponent_player_id].board[hit_spot[row]][hit_spot[column]] == Board_signs.empty_sign:
            if self.players_ships[opponent_player_id].ships_board.board[hit_spot[row]][hit_spot[column]] == Board_signs.ship_sign:
                # mark hit ship spot
                
                self.players_boards[opponent_player_id].board[hit_spot[row]][hit_spot[column]] = Board_signs.hit_sign
                self.players_ships[opponent_player_id].ships_board.board[hit_spot[row]][hit_spot[column]] = Board_signs.hit_sign
                self.players[hit_player_id].ai_last_hit_spot_01.append(hit_spot) # for ai moves
                # check if hit ship's is sunk
                is_hit_ship_sunk = False
                for ship in self.players_ships[opponent_player_id].chosen_ships:
                    is_hit_ship_sunk = self.players_ships[opponent_player_id].is_ship_sunk(ship)
                    if is_hit_ship_sunk:
                    #if hit_spot in ship.ship_spots_coordinations:
                    #    is_hit_ship_sunk = ship.is_ship_sunk()
                    #    if is_hit_ship_sunk:
                            for ship_spot in ship.ship_spots_coordinations:
                                self.players_boards[opponent_player_id].board[ship_spot[row]][ship_spot[column]] = Board_signs.sunk_sign 
                                self.players_ships[opponent_player_id].ships_board.board[ship_spot[row]][ship_spot[column]] = Board_signs.sunk_sign  
            else:
                self.players_boards[opponent_player_id].board[hit_spot[row]][hit_spot[column]] = Board_signs.missed_sign       


class Game: # Game's flow and logic
    game_menu_options = {'human-human':"1", 'human-ai':"2", 'ai-ai':"3", 'game_settings':"4", 'quit':"quit"}

    def __init__ (self, Battleship_game: Battleship , current_game_phase: int = 0) -> None:
        #data for flow of game
        self.game_phases = {'main_menu':0, 'setting_game_mode':1, 'ships_placement':2, 'ships_shooting':3, 'game_over':4, 'quit_game':5, 'game_settings':6}
        self.current_game_phase = current_game_phase
        self.current_game_mode = ""
        self.end_game_with_winner = False
        self.winner_name = ""
        self.exit_game = False # for exiting program game
        self.reached_turns_limit = False
        self.game = Battleship_game

        # user_wants_to_quit = False
        # game_is_over = False

        #settings for current game
        self.this_game_board_size = Settings.default_game_board_size
        self.this_game_ships_number = Settings.default_ships_number
        self.this_game_turn_limits = Settings.default_turn_limits
        self.this_game_name_of_player1 = Settings.default_ai_1_name
        self.this_game_name_of_player2 = Settings.default_ai_2_name

    def play(self) -> None:
        # Players change turns after each shot
        # It is clearly indicated, whose turn is happening actually
        # If user enters invalid input (outside range), then the error message Invalid input! is displayed and the program asks again for an input (shooting twice at the same spot is a valid but unnecessary move)
        # Hitting, missing and sinking ship (parts) results in a message displayed as You've hit a ship!, You've missed! and You've sunk a ship! respectively
        # If one of the players sinks all ships of the other player then the message Player <n> wins! is displayed where is the number of the player who wins and the game ends
        
        # Game's flow logi in main game's phases
        while not self.exit_game:
            if self.current_game_phase == self.game_phases['main_menu']: # user can reach through main menu by entering "start game"
                self.phase_main_menu()
            if self.current_game_phase == self.game_phases['setting_game_mode']: # user can reach through main menu by entering "start game"
                self.phase_setting_game_mode()
            elif self.current_game_phase == self.game_phases['ships_placement']: # user can't reach through menu / phase is set via game's logic
                self.phase_ships_placement()
            elif self.current_game_phase == self.game_phases['ships_shooting']: # user can't reach through menu / phase is set via game's logic
                self.phase_ships_shooting()
            elif self.current_game_phase == self.game_phases['game_over']: # phase is set via game's logic
                self.phase_game_over()
            elif self.current_game_phase == self.game_phases['quit_game']: # user can type in "quit" to quit game while playing
                self.phase_quit_game()
            elif self.current_game_phase == self.game_phases['game_settings']: # user can reach through main menu
                self.phase_game_settings()
        

    def phase_main_menu(self) -> None: # method modifies self.current_game_mode i.e. human-ai
        clear_screen()
        wrong_choice_happend = False # used for printing info about wrong choice (below)
        correct_choice = False # used for exiting main menu
        chosen_game_mode = "" # return game mode so that game was properly set later
        
        while not correct_choice:
            self.show_main_menu()
            if wrong_choice_happend:
                print(f"{colors.fg.red}Wrong choice. Please, enter your choice again!{colors.reset}")
            user_input = input(f"Enter your choice i.e. {Game.game_menu_options['game_settings']}: ")

            if user_input == Game.game_menu_options['human-human']:
                correct_choice = True
                chosen_game_mode = 'human-human'
                self.change_game_phase('setting_game_mode')
                wrong_choice_happend = False
            elif user_input == Game.game_menu_options['human-ai']:
                correct_choice = True
                chosen_game_mode = 'human-ai'
                self.change_game_phase('setting_game_mode')
                wrong_choice_happend = False
            elif user_input == Game.game_menu_options['ai-ai']:
                correct_choice = True
                chosen_game_mode = 'ai-ai'
                self.change_game_phase('setting_game_mode')
                wrong_choice_happend = False
            elif user_input == Game.game_menu_options['game_settings']:
                correct_choice = True
                self.change_game_phase('game_settings')
                wrong_choice_happend = False
            elif user_input == "quit":
                correct_choice = True
                self.change_game_phase('quit_game')
                wrong_choice_happend = False
            else:
                wrong_choice_happend = True

            if not chosen_game_mode == "":
                self.current_game_mode =  chosen_game_mode
            
            self.game.quit_game = False


    def phase_setting_game_mode(self) -> None:
        clear_screen()
        user_wants_to_abort = False
        setting_game_mode_correct = False

        print(f"You've chose option nr: {colors.fg.yellow}{Game.game_menu_options[self.current_game_mode]}{colors.reset} Preparing game in mode: : {colors.fg.pink}{self.current_game_mode}{colors.reset}")
        print(f"Type in {colors.fg.yellow}{Settings.abort_command}{colors.reset} to abort setting the game at any moment\n")
        
        if Game.game_menu_options[self.current_game_mode] == Game.game_menu_options['human-human']:
            user_does_not_want_to_abort = self.change_default_values_for_this_game(2)
            if user_does_not_want_to_abort:
                input(f"\nPress any key to start playing..")
                self.change_game_phase('ships_placement')
            else:
                input(f"\nPress any key to exit to main menu..")
                self.change_game_phase('main_menu')
        if Game.game_menu_options[self.current_game_mode] == Game.game_menu_options['human-ai']:
            user_does_not_want_to_abort = self.change_default_values_for_this_game(1)  
            if user_does_not_want_to_abort:
                input(f"\nPress any key to start playing..")
                self.change_game_phase('ships_placement')
            else:
                input(f"\nPress any key to exit to main menu..")
                self.change_game_phase('main_menu')
        if Game.game_menu_options[self.current_game_mode] == Game.game_menu_options['ai-ai']:
                Game_mode_questions.ai_ai_get_random_game_values(self)
                input(f"\nPress any key to start playing..")
                self.change_game_phase('ships_placement')                



    def phase_ships_placement(self) -> None:
        clear_screen()
        player1 = 0
        player2 = 1

        # clearing boards in case user enter many times menu and shipps placement phase
        new_ships_board_for_player1 = Ships(self.this_game_ships_number, self.this_game_board_size)
        new_ships_board_for_player2 = Ships(self.this_game_ships_number, self.this_game_board_size)
        self.game.player1_ships = new_ships_board_for_player1
        self.game.player2_ships = new_ships_board_for_player2
        self.game.players_ships[player1] = self.game.player1_ships
        self.game.players_ships[player2] = self.game.player2_ships

        for player in (player1, player2):
            self.game.player_turn = self.game.players[player].name
            if player == player1: 
                input(f"{colors.fg.yellow}{colors.bold}{self.game.players[player1].name}{colors.reset} Prepare, Press any [enter] to start placing ships..{colors.reset}\n")
            for ship_id in range(1, self.game.players_ships[player].ships_number + 1):
                clear_screen()
                current_player_info = f"{colors.fg.yellow}{colors.bold}{self.game.players[player].name}{colors.reset} Placing ships {colors.underline}{ship_id}{colors.reset} of {self.this_game_ships_number}..{colors.reset}\n"
                print(current_player_info)
                if Game.game_menu_options[self.current_game_mode] == Game.game_menu_options['human-human']:
                    self.game.players_ships[player].ask_for_ship(ship_id)
                    self.game.show_boards_for_ships_placing(player)
                if Game.game_menu_options[self.current_game_mode] == Game.game_menu_options['human-ai']:
                    if player == 0:
                        self.game.players_ships[player].ask_for_ship(ship_id)
                        self.game.show_boards_for_ships_placing(player)
                    else:
                        self.game.players_ships[player].ask_for_ship(ship_id, mode_human_or_ai = 'ai')
                        self.game.show_boards_for_ships_placing(player)
                if Game.game_menu_options[self.current_game_mode] == Game.game_menu_options['ai-ai']:
                    self.game.players_ships[player].ask_for_ship(ship_id, mode_human_or_ai = 'ai')
                    self.game.show_boards_for_ships_placing(player)
                if not ship_id == self.game.players_ships[player].ships_number:
                    input(f"\nPress any key to place another ship..")    
            if player == player1: 
                input(f"\nPress any key to change player to {colors.fg.yellow}{self.game.players[player2].name}{colors.reset}..")    
        input(f"\nPress any key to start playing..")
        self.change_game_phase('ships_shooting') 
        #self.change_game_phase('ships_shooting')

    def get_oponent_player_id(self, current_player) -> int:
        return 1 if current_player == 0 else 0

    def phase_ships_shooting(self) -> None:
        player_1 = 0
        player_2 = 1
        current_player = player_1
        self.game.player_turn = self.game.players[current_player].name

        turns_local_counter = 0

        while not self.end_game_with_winner and not self.game.quit_game and not self.reached_turns_limit: #self.game.quit_game is set to True in method ask_for_hit_coordinates_or_quit()
            self.show_play(self.game.player1_hit_board, self.game.player2_hit_board) #showing current boards state
            
            if Game.game_menu_options[self.current_game_mode] == Game.game_menu_options['human-human']:
                player_hit_coordinations_a1 = self.game.ask_for_hit_coordinates_or_quit() #asking current player for hit coordinates or quit gama
            if Game.game_menu_options[self.current_game_mode] == Game.game_menu_options['human-ai']:
                if current_player == player_2:
                    player_hit_coordinations_a1 = Game_mode_questions.get_ai_move_easy_shoot_near_hit(self)
                else:
                    player_hit_coordinations_a1 = self.game.ask_for_hit_coordinates_or_quit() #asking current player for hit coordinates or quit gama

            if Game.game_menu_options[self.current_game_mode] == Game.game_menu_options['ai-ai']:
                    player_hit_coordinations_a1 = Game_mode_questions.get_ai_move_easy_shoot_near_hit(self)

            if not (player_hit_coordinations_a1 == False): # player type in correct coordinations and doesn't want to quit
                if not self.game.quit_game:
                    player_hit_coordinations_01 = self.game.convert_coordinates_a1_to_00(player_hit_coordinations_a1)
                    is_hit_spot_empty = self.game.players_boards[current_player].is_cell_empty(player_hit_coordinations_01)
                    #mark hit on current opposite ships_board
                    self.game.mark_hit_board(current_player, player_hit_coordinations_01)
            else:
                self.game.quit_game = True
            if self.game.players_ships[self.get_oponent_player_id(current_player)].are_ships_sunk(): #checks if opponents ships are sunk
                self.end_game_with_winner = True
                self.winner_name = self.game.player_turn

            turns_local_counter += 0.5
            if turns_local_counter == 1:
                turns_local_counter = 0
                self.game.turn_counter -= 1
            if self.game.turn_counter == 0:
                self.reached_turns_limit = True

            current_player = self.get_oponent_player_id(current_player)    
            self.game.player_turn = self.game.players[current_player].name
 
        
        if self.end_game_with_winner: 
            self.change_game_phase('game_over')
        elif self.reached_turns_limit:
            self.change_game_phase('game_over')
        else:
            self.change_game_phase('main_menu')
        

    def phase_game_over(self) -> None: 
        self.show_play(self.game.player1_hit_board, self.game.player2_hit_board)
        if self.reached_turns_limit == True:
            input(f"{colors.bg.red}It's a draw !{colors.reset}")
        else:
            input(f"{colors.bg.red}{self.winner_name} won game !{colors.reset}")
        self.change_game_phase('main_menu')
        self.end_game_with_winner = False
        self.end_game_with_winner = ""
        self.reached_turns_limit = False
        self.game.turn_counter = self.game.turn_limit

    def phase_quit_game(self) -> None: 
        self.exit_game = True
        input(f"Press any key to continue..")
        clear_screen()
        
    def phase_game_settings(self) -> None:
        clear_screen()
        Settings.change_settings()
        self.change_game_phase('main_menu')
        clear_screen()

    def show_play(self, board1: Board, board2: Board) -> None:
        clear_screen()
        #The number of turns left is constantly displayed above the boards (e.g. Turns left: 18)
        if Settings.print_header_project == True: # printing header
            print_authors_and_project()
            print("\n")
        
        if not self.game.turn_limit == -1 and Settings.print_turn_limits == True :
            print(f"{colors.bold}{self.game.turn_limit} turn limits: left: {colors.reset}",end="")
            print(f"{colors.fg.red}{colors.bold}{self.game.turn_counter}{colors.reset}")
             
        print("\n")
        self.game.print_both_boards(board1, board2) # printing given boards
        
        if Settings.print_legend == True:
            Board_signs.print_legend_for_used_signs()   # printing legends:
        print("\n") 


    def shooting(self) -> None:
        #User can place ships with at least two different sizes (e.g. 1 block long and 2 blocks long)
        #The program keeps asking for input until all ships are placed
        #If user wants to place two ships next to each other (touching corners are okay), then the error message Ships are too close!  is displayed and the program asks again for an input

        #After one player is finished with the placement phase, a waiting screen is displayed with no boards just with the message Next player's placement phase
        #If the user presses any button on the waiting screen, the second player's placement phase begins
        pass


    def is_game_over(self) -> bool:
    #If one of the players sinks all ships of the other player then the message Player <n> wins! is displayed where is the number of the player who wins and the game ends

        pass


    def change_game_phase(self, next_game_phase: str) -> bool:            
        if next_game_phase in self.game_phases:
            self.current_game_phase = self.game_phases[next_game_phase]
            return True
        else:
            return False


    def show_main_menu(self) -> None:
        clear_screen()
        
        if Settings.print_header_project == True: # printing header
            print_authors_and_project()
        print("\n") 

        print ("╦ ╦┌─┐┬  ┌─┐┌─┐┌┬┐┌─┐")     
        print ("║║║├┤ │  │  │ ││││├┤ ")       
        print ("╚╩╝└─┘┴─┘└─┘└─┘┴ ┴└─┘ ")      
        print ("          ┌┬┐┌─┐       ")     
        print ("           │ │ │       ")     
        print ("           ┴ └─┘        ")    
        print (f"{colors.fg.blue}╔╗ ┌─┐┌┬┐┌┬┐┬  ┌─┐┌─┐┬ ┬┬┌─┐{colors.reset}")
        print (f"{colors.fg.blue}╠╩╗├─┤ │  │ │  ├┤ └─┐├─┤│├─┘{colors.reset}")
        print (f"{colors.fg.blue}╚═╝┴ ┴ ┴  ┴ ┴─┘└─┘└─┘┴ ┴┴┴ {colors.reset}\n")

        print(f"{colors.fg.yellow}{Game.game_menu_options['human-human']}{colors.reset} - start playing game ({colors.fg.green}multiplayer{colors.reset}) {colors.fg.pink}human{colors.reset}-{colors.fg.pink}human{colors.reset}")
        print(f"{colors.fg.yellow}{Game.game_menu_options['human-ai']}{colors.reset} - start playing game ({colors.fg.green}singleplayer{colors.reset}) {colors.fg.pink}human{colors.reset}-{colors.fg.pink}ai{colors.reset}")
        print(f"{colors.fg.yellow}{Game.game_menu_options['ai-ai']}{colors.reset} - start playing game ({colors.fg.green}computer{colors.reset}) {colors.fg.pink}ai{colors.reset}-{colors.fg.pink}ai{colors.reset}")        
        print(f"{colors.fg.yellow}{Game.game_menu_options['game_settings']}{colors.reset} - change game settings")
        print(f"{colors.fg.yellow}{Game.game_menu_options['quit']}{colors.reset} - quit game\n")

    def change_default_values_for_this_game(self, players_number:int = 2) -> bool:
        # 1st question, board size question
        currrent_user_input = Game_mode_questions.ask_for_board_size()
        if not currrent_user_input == Settings.abort_command:
            self.this_game_board_size = currrent_user_input
            print(f"{colors.fg.green}> corrent! board size = {self.this_game_board_size}{colors.reset}")
        else:
            return False

        # 2nd question, ships number question
        currrent_user_input = Game_mode_questions.ask_for_ships_number()
        if not currrent_user_input == Settings.abort_command:
            self.this_game_ships_number = currrent_user_input
            print(f"{colors.fg.green}> correct! ships number = {self.this_game_ships_number}{colors.reset}")
        else:
            return False

        # 3th question, turn limits question
        currrent_user_input = Game_mode_questions.ask_for_turns_limit()
        if not currrent_user_input == Settings.abort_command:
            self.this_game_turn_limits = currrent_user_input
            print(f"{colors.fg.green}> correct! turns limit = {self.this_game_turn_limits}{colors.reset}")
        else:
            return False

        # 4th question, Player 1 question
        currrent_user_input = Game_mode_questions.ask_for_player_name(4,1)
        if not currrent_user_input == Settings.abort_command:
            self.this_game_name_of_player1 = currrent_user_input
            self.game.player1.name = self.this_game_name_of_player1         
            print(f"{colors.fg.green}> correct! Player 1's name = {self.this_game_name_of_player1}{colors.reset}")
        else:
            return False

        if players_number == 2:
            # 5th question, Player 2 question
            currrent_user_input = Game_mode_questions.ask_for_player_name(5,2)
            if not currrent_user_input == Settings.abort_command:
                self.this_game_name_of_player2 = currrent_user_input
                self.game.player2.name = self.this_game_name_of_player2      
                print(f"{colors.fg.green}> correct! Player 2's name = {self.this_game_name_of_player2}{colors.reset}")
            else:
                return False
        else: #human-ai mode
            self.game.player2.name = Settings.default_ai_name
            print(f"{colors.fg.green}> correct! Player 2's name = {self.this_game_name_of_player2}{colors.reset}")

        #creating new Battleship logic for this game
        self.game = Battleship(Player(self.this_game_name_of_player1), Player(self.this_game_name_of_player2), self.this_game_turn_limits, self.this_game_board_size, self.this_game_ships_number)
        self.game.end_game_with_winner = False
        return True



class Game_mode_questions: # class for collecting the answers from user or getting ai moves or ai random settings depending how to start battleship game mode
    def __init__(self) -> None:
        pass


    def get_ai_move_easy_shoot_near_hit(this_game: Game) -> str:   
        # OPTIONAL Extend the game so there is a single player mode where the user can play against the computer
        # Before the placement phase the game mode is asked from the user as user input and by printing a menu with two items (1. Single player, 2. Multiplayer)
        # If the given choice is out of range (1-2) then the error message Invalid input! is displayed
        # If multiplayer is chosen as game mode then game works with two players as in the above tasks
        # If single player is chosen as game mode then both during placement and shooting phases Player 2 is the computer and generates its moves
        
        board_size = this_game.game.board_size

        player1_id = 0
        player2_id = 1
        current_player_id_turn = player1_id if this_game.game.player_turn == this_game.game.players[player1_id].name else player2_id
        opponent_player_id = player1_id if current_player_id_turn == player2_id else player2_id

        is_empty_random_hit_spot = False
        while not is_empty_random_hit_spot:
            random_column = choice(this_game.game.player1_hit_board.columns_labels)
            random_row = choice(this_game.game.player1_hit_board.rows_labels)
            random_cell_a1 = f"{random_row}{random_column}"
            
            random_cell_01 = this_game.game.convert_coordinates_a1_to_00(random_cell_a1)
            is_empty_random_hit_spot = this_game.game.players_boards[opponent_player_id].is_cell_empty(random_cell_01)

        row = 0
        column = 1
        #this.game.mark_hit_board(current_player_id_turn, random_cell_01)

        # fullfill nearby spots that are empty and in board
        if not len(this_game.game.players[current_player_id_turn].ai_last_hit_spot_01) == 0:
            if len(this_game.game.players[current_player_id_turn].ai_list_of_nearby_hits) == 0:
                # we fullfil spots that are worth to try (empty and on board)
                last_hit_spot_01 = this_game.game.players[current_player_id_turn].ai_last_hit_spot_01
                board_size = this_game.game.board_size
                for row_nearby in [-1,0,0,1]:
                    for column_nearby in [-1,0,0,1]: 
                        new_nearby_row = (last_hit_spot_01[0][row]) + row_nearby
                        new_nearby_column = (last_hit_spot_01[0][column]) + column_nearby
                        if (0 <= new_nearby_row < board_size) and (0 <= new_nearby_column < board_size) : # check if nearby spot is on board
                            nearby_spot_01 = [new_nearby_row, new_nearby_column]
                            if this_game.game.players_boards[opponent_player_id].board[nearby_spot_01[row]][nearby_spot_01[column]] == Board_signs.empty_sign:  # check if nearby spot is empty
                                this_game.game.players[current_player_id_turn].ai_list_of_nearby_hits.append(nearby_spot_01)
                #we take first nearby spot to check
                if len(this_game.game.players[current_player_id_turn].ai_list_of_nearby_hits) > 0 :
                    nearby_spot_to_try_01 = this_game.game.players[current_player_id_turn].ai_list_of_nearby_hits.pop(0)
            else: # ai hit spot appended on ai_list_of_nearby_hits and waiting to be tried
                if len(this_game.game.players[current_player_id_turn].ai_list_of_nearby_hits) > 0 :
                    nearby_spot_to_try_01 = this_game.game.players[current_player_id_turn].ai_list_of_nearby_hits.pop(0)

            if len(this_game.game.players[current_player_id_turn].ai_list_of_nearby_hits) > 0 :
                nearby_spot_to_try_01 = this_game.game.players[current_player_id_turn].ai_list_of_nearby_hits.pop(0)

                row_a1 = this_game.game.players_boards[current_player_id_turn].rows_labels[nearby_spot_to_try_01[row]]
                column_a1 = nearby_spot_to_try_01[column] + 1

                random_cell_a1 = f"{row_a1}{column_a1}"

        time.sleep(0.1)
        return random_cell_a1

    def is_asked_board_size_correct(user_input: str) -> bool or str:
        try:
            if user_input.lower() == Settings.abort_command or user_input == "":
                return user_input.lower()
            else:
                correct_user_input_int = int(user_input)
                if Settings.board_size_max >= correct_user_input_int >= Settings.board_size_min:
                    return correct_user_input_int
                else:
                    print(f"{colors.fg.yellow}Invalid input! (must be between {Settings.board_size_min}-{Settings.board_size_max}){colors.reset}")
                    return False
        except:
            print(f"{colors.fg.red}Wrong user input for board size! Please enter valid number!{colors.reset}")
            return False
    def ask_for_board_size(question_number: int = 1) -> int:
            correct_input = False
            while not correct_input:
                user_input = input(f"{question_number}. Type in number between [{colors.fg.pink}{Settings.board_size_min}-{Settings.board_size_max}{colors.reset}] for {colors.underline}board size{colors.reset} / {colors.fg.green}[press enter] for default size {Settings.default_game_board_size}{colors.reset}: ")
                valided_user_input = Game_mode_questions.is_asked_board_size_correct(user_input)
                if valided_user_input == Settings.abort_command:
                    return valided_user_input
                elif valided_user_input == "": # default value
                    return Settings.default_game_board_size
                elif valided_user_input == False:
                    pass
                else: 
                    return int(valided_user_input)

    def is_asked_turn_limits_correct(user_input: str) -> bool or str:
        try:
            if user_input.lower() == Settings.abort_command or user_input == "":
                return user_input.lower()
            else:
                correct_user_input_int = int(user_input)
                if Settings.turns_limit_max >= correct_user_input_int >= Settings.turns_limit_min:
                    return correct_user_input_int
                else:
                    print(f"{colors.fg.yellow}Invalid input! (must be between {Settings.turns_limit_min}-{Settings.turns_limit_max}) {colors.reset}")
                    return False
        except:
            print(f"{colors.fg.red}Wrong user input for turn limit! Please enter valid number!{colors.reset}")
            return False
    def ask_for_turns_limit(question_number: int = 3) -> int:
            correct_input = False
            while not correct_input:
                user_input = input(f"{question_number}. Type in number between [{colors.fg.pink}{Settings.turns_limit_min}-{Settings.turns_limit_max}{colors.reset}] for {colors.underline}turns limit{colors.reset} / {colors.fg.green}[press enter] for default size ({Settings.default_turn_limits} - no limit){colors.reset}: ")
                valided_user_input = Game_mode_questions.is_asked_turn_limits_correct(user_input)
                if valided_user_input == Settings.abort_command:
                    return valided_user_input
                elif valided_user_input == "": # default value
                    return Settings.default_turn_limits
                elif valided_user_input == False:
                    pass
                else: 
                    return int(valided_user_input)

    def is_asked_ships_number_correct(user_input: str) -> bool or str:
        try:
            if user_input.lower() == Settings.abort_command or user_input == "":
                return user_input.lower()
            else:
                correct_user_input_int = int(user_input)
                if Settings.ships_number_max >= correct_user_input_int >= Settings.ships_number_min:
                    return correct_user_input_int
                else:
                    print(f"{colors.fg.yeloow}Invalid input! (must be between {Settings.ships_number_min}-{Settings.ships_number_max}){colors.reset}")
                    return False
        except:
            print(f"{colors.fg.red}Wrong user input for board size! Please enter valid number!{colors.reset}")
            return False
    def ask_for_ships_number(question_number: int = 2) -> int:
            correct_input = False
            while not correct_input:
                user_input = input(f"{question_number}. Type in number between [{colors.fg.pink}{Settings.ships_number_min}-{Settings.ships_number_max}{colors.reset}] for {colors.underline}ships number{colors.reset} / {colors.fg.green}[press enter] for default size {Settings.default_ships_number}{colors.reset}: ")
                valided_user_input = Game_mode_questions.is_asked_ships_number_correct(user_input)
                if valided_user_input == Settings.abort_command:
                    return valided_user_input
                elif valided_user_input == "": # default value
                    return Settings.default_ships_number
                elif valided_user_input == False:
                    pass
                else: 
                    return int(valided_user_input)


    def is_asked_player_name_correct(user_input: str) -> bool or str:
        try:
            if user_input.lower() == Settings.abort_command or user_input == "":
                return user_input.lower()
            else:
                if Settings.player_name_max_length >= len(user_input) >= Settings.player_name_min_length:
                    return user_input
                else:
                    print(f"{colors.fg.yellow}Invalid input! (must be between {Settings.player_name_min_length}-{Settings.player_name_max_length}){colors.reset}")
                    return False
        except:
            print(f"{colors.fg.red}Wrong user input for player name! Please enter valid name!{colors.reset}")
            return False
    def ask_for_player_name(question_number: int = 4, player_id: int = 1) -> str:
            correct_input = False
            while not correct_input:
                user_input = input(f"{question_number}. Type in Player {player_id} name. Name length between [{colors.fg.pink}{Settings.player_name_min_length}-{Settings.player_name_max_length}{colors.reset}] for {colors.underline}Player name{colors.reset} / {colors.fg.green}[press enter] for default name {Settings.default_player_name}{colors.reset}: ")
                valided_user_input = Game_mode_questions.is_asked_player_name_correct(user_input)
                if valided_user_input == Settings.abort_command:
                    return valided_user_input
                elif valided_user_input == "": # default value
                    return f"{Settings.default_player_name} {player_id}"
                elif valided_user_input == False:
                    pass
                else: 
                    return valided_user_input


    def ai_ai_get_random_game_values(this_game: Game) -> None:
        this_game.this_game_turn_limits = random.randint(Settings.turns_limit_min, Settings.turns_limit_max)
        this_game.this_game_board_size = random.randint(Settings.board_size_min, Settings.board_size_max)

        if this_game.this_game_board_size <= 6:
                    this_game.this_game_ships_number = random.randint(Settings.ships_number_min, Settings.ships_number_min)
        else:
                    this_game.this_game_ships_number = random.randint(Settings.ships_number_min, Settings.ships_number_max)


        this_game.this_game_name_of_player1 = Settings.default_ai_1_name
        this_game.game.player1.name = Settings.default_ai_1_name
        this_game.this_game_name_of_player2 = Settings.default_ai_2_name
        this_game.game.player2.name = Settings.default_ai_2_name
        print(f"{colors.fg.green}> correct! board size = {this_game.this_game_board_size}{colors.reset}")
        print(f"{colors.fg.green}> correct! ships number = {this_game.this_game_ships_number}{colors.reset}")
        print(f"{colors.fg.green}> correct! turns limit = {this_game.this_game_turn_limits}{colors.reset}")
        print(f"{colors.fg.green}> correct! Player 1's name = {this_game.this_game_name_of_player1}{colors.reset}")
        print(f"{colors.fg.green}> correct! Player 2's name = {this_game.this_game_name_of_player2}{colors.reset}")

        #creating new Battleship logic for this game
        this_game.game = Battleship(Player(this_game.this_game_name_of_player1), Player(this_game.this_game_name_of_player2), this_game.this_game_turn_limits, this_game.this_game_board_size, this_game.this_game_ships_number)
        this_game.quit_game = False

    def ai_ai_get_random_ship(ships_board: Ships) -> list:
        
        random_ship_type = choice((tuple(Ship.types_of_ships.keys())))
        random_ship_orientation = choice((tuple(Ship.orientation.keys()))) 
        
        random_column = choice(tuple(ships_board.columns_labels))
        random_row = choice(tuple(ships_board.rows_labels))
        random_ship_start_coordination = f"{random_row}{random_column}"
        return [random_ship_type, random_ship_orientation, random_ship_start_coordination]


