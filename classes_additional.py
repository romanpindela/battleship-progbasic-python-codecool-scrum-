# autor: Roman Pindela / roman.pindela@gmail.com
from os import system, name

from utils import *

# moduł: classes_additional
class colors: # colors used in game
    '''Colors class:
    reset all colors with colors.reset
    two subclasses fg for foreground and bg for background.
    use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.green
    also, the generic bold, disable, underline, reverse, strikethrough,
    and invisible work with the main class
    i.e. colors.bold
    '''
    reset='\033[0m'
    bold='\033[01m'
    disable='\033[02m'
    underline='\033[04m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'
    class fg:
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'
    class bg:
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        lightgrey='\033[47m'
    a = text_format_for_active_player_turn = "".join(f"{bold}{bg.black}{fg.lightgrey}")
    _ = text_format_for_reset = "".join(f"{reset}")
    b = text_format_for_active_player_turn = "".join(f"{bold}{bg.black}{fg.darkgrey}")

class Settings:
    print_header_project = True
    print_turn_limits = True
    print_legend = True

    default_game_board_size = 10
    default_ships_number = 2
    default_turn_limits = -1 # -1 - no turn limits
    default_player_name = "Player"

    ships_number_min = 2
    ships_number_max = 3
    board_size_min = 5
    board_size_max = 10
    turns_limit_min = 5
    turns_limit_max = 50
    player_name_max_length = 20 
    player_name_min_length = 1
    

    abort_command = "abort"

    #used in ai-ai mode and human-ai
    default_ai_name = "AI"
    default_ai_1_name = "AI One"
    default_ai_2_name = "AI Second"

    def toggle_print_header_project() -> None:
        Settings.print_header_project = not Settings.print_header_project

    def toggle_print_turn_limits() -> None:
        Settings.print_turn_limits = not Settings.print_turn_limits

    def toggle_print_legend() -> None:
        Settings.print_legend = not Settings.print_legend

    def print_available_settings() -> None:
        print("Change settings for printing information:")
        print(f"[{'X' if Settings.print_header_project == True else ' '}] {colors.fg.yellow}1{colors.reset} - printing header project")
        print(f"[{'X' if Settings.print_turn_limits == True else ' '}] {colors.fg.yellow}2{colors.reset} - printing turn limits")
        print(f"[{'X' if Settings.print_legend == True else ' '}] {colors.fg.yellow}3{colors.reset} - printing legend")
        print(f"{colors.fg.yellow}exit{colors.reset} for exiting to main menu")
    
    def change_settings() -> None:
        user_wants_to_exit_settings = False
        while not user_wants_to_exit_settings:
            os.system('cls' if name == 'nt' else 'clear')
            #clear_screen()
            Settings.print_available_settings()
            user_input = input(f"type option {colors.fg.yellow}number{colors.reset} to toggle it: ")
            if user_input == "1":
                Settings.toggle_print_header_project()
            elif user_input == "2":
                Settings.toggle_print_turn_limits()
            elif user_input == "3":
                Settings.toggle_print_legend()
            elif user_input == "exit":
                user_wants_to_exit_settings = True
            else:
                print(f"{colors.fg.red}Wrong setting number, please choose among 1, 2 and 3{colors.reset}")

class Board_signs:
    ship_sign = "#"
    missed_sign = "M"
    hit_sign = "H"
    sunk_sign = "S"
    empty_sign = "0" 

    def __init__(self) -> None:
        pass
    
    def print_legend_for_used_signs() -> None:
        print("Legend: ", end="")
        ship_sign_formatted = Board_signs.cell_print(Board_signs.ship_sign)
        missed_sign_formatted = Board_signs.cell_print(Board_signs.missed_sign)
        hit_sign_formatted = Board_signs.cell_print(Board_signs.hit_sign)
        sunk_sign_formatted = Board_signs.cell_print(Board_signs.sunk_sign)
        empty_sign_formatted = Board_signs.cell_print(Board_signs.empty_sign)
        
        print(f"{ship_sign_formatted}-Ship  {hit_sign_formatted}-Hit  {sunk_sign_formatted}-Sunk  {empty_sign_formatted}-Empty  {missed_sign_formatted}-Missed")

    def cell_print(cell: str) -> str: # function returns cell with text formating
        M = "".join(f"{colors.fg.darkgrey}{cell}{colors.reset}") # Missed cell
        H = "".join(f"{colors.fg.red}{cell}{colors.reset}") # Hitted ship
        S = "".join(f"{colors.fg.lightgrey}{colors.bg.red}{cell}{colors.reset}") # Sunk ship
        O = "".join(f"{colors.fg.lightcyan}{cell}{colors.reset}") # empty cell
        SS = "".join(f"{colors.fg.yellow}{cell}{colors.reset}")

        color_scheme = {Board_signs.missed_sign: M, Board_signs.empty_sign: O, Board_signs.sunk_sign:S, Board_signs.hit_sign:H, Board_signs.ship_sign:SS}
        return color_scheme[cell]

