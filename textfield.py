from os import get_terminal_size, system
from sys import stdout

from readchar import readchar


def clear():
    system('clear')


def move(y, x: int = 0):
    stdout.write(f'\033[{y};{x}H')


def get_height():
    return get_terminal_size().columns


def get_width():
    return get_terminal_size().columns


def clear_line(y):
    width = get_width()

    move(y)
    print(' ' * width)
    move(y)
