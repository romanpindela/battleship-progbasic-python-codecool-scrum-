# autor: Roman Pindela / roman.pindela@gmail.com
import os   #from os import system, name

from classes_additional import *

# moduł: utils

def print_authors_and_project() -> None: # authors and project info
    project_name = "Battleship"
    authors = "Roman Pindela"
    project_release_date = "Nov-2020"
    project_license = "GPL v3.0"

    print(f"{colors.b}Project name: {colors.a}{project_name: <22}{colors._}{colors.b}Authors:{colors._} {colors.a}{authors: <30}{colors._}")
    print(f"{colors.b}        Date: {colors._}{colors.a}{project_release_date: <22}{colors._}{colors.b}Licence: {colors._}{colors.a}{project_license: <30}{colors._}")

def clear_screen() -> None:
    os.system('cls' if name == 'nt' else 'clear')
