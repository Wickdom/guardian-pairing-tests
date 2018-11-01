#!/usr/bin/env python
# coding: utf-8
import sys

from errors import *

MAX_ROWS = 10
MAX_COLS = 10
MOVE_COMMANDS = {'N', 'E', 'S', 'W', 'EN', 'NW', 'ES', 'SW'}
PACKAGE_COMMANDS = {'D', 'G'}
PACKAGE_LOCATION = [(1, 1), (2, 2)]


def populate_grid_status():
    gs = [[0] * MAX_COLS for _ in range(MAX_ROWS)]
    for r, c in PACKAGE_LOCATION:
        gs[r][c] += 1
    return gs


grid_stats = populate_grid_status()


def parse_input(input_str):
    valid_commands = MOVE_COMMANDS | PACKAGE_COMMANDS
    input_sequences = input_str.split()
    invalid_commands = set(input_sequences) - valid_commands
    if invalid_commands:
        raise InvalidCommand(invalid_commands, "in the sequence", input_sequences)
    return input_sequences


def move(r, c, direction):
    # print("Moving from ({},{}) in {} to ".format(r, c, direction), end='')
    r, c = {
        'EN': (r - 1, c + 1),
        'NW': (r - 1, c - 1),
        'ES': (r + 1, c + 1),
        'SW': (r + 1, c - 1),
        'N': (r - 1, c),
        'S': (r + 1, c),
        'W': (r, c - 1),
        'E': (r, c + 1)}[direction]
    # print("({},{})".format(r, c))
    if not (0 <= r < MAX_ROWS and 0 <= c < MAX_COLS):
        raise OutOfRange("Position ({},{}) falls outside the grid!".format(r, c))
    return r, c


def handle_package(r, c, a, hs):
    def _d_or_p(r, c, stp, hs, hsErr):
        if hs: raise hsErr
        grid_stats[r][c] += stp
        return grid_stats[r][c]

    gs = _d_or_p(r, c, *{
        'D': (1, not hs, EmptyHand("No item to drop")),
        'G': (-1, hs, RoboOverload("already handling an item"))}[a])

    if a == 'D':
        # print("Dropping package at", r, c)
        if gs != 1: raise PreOccupiedSlot("Position ({},{}) already has 1 item!".format(r, c))
    else:
        # print("Grabbing  package from", r, c)
        if gs != 0: raise EmptySlot("Position ({},{}) has no item!".format(r, c))
    return not hs


def process_input(i_str, r=0, c=0):
    seq = parse_input(i_str)
    hold_status = False

    for i in range(0, len(seq), 2):
        cmds = seq[i:i + 2]
        if len(set(cmds) - PACKAGE_COMMANDS) == 2:
            cmds = [''.join(sorted(cmds))]
        for cmd in cmds:
            if cmd in MOVE_COMMANDS:
                r, c = move(r, c, cmd)
            elif cmd in PACKAGE_COMMANDS:
                hold_status = handle_package(r, c, cmd, hold_status)
            else:
                raise InvalidCommand(cmd)
    return r, c


if __name__ == '__main__':
    tests = [
        [1, 1, "E E E E", (1, 5)],
        [1, 1, "W S E E", (2, 2)],
        [1, 1, "G", (1, 1)],
        [1, 1, "G S D", (2, 1)],
        [1, 2, "W G S E E D G W W N D E", (1, 2)],
        [0, 0, "W", OutOfRange],
        [0, MAX_COLS, "E", OutOfRange],
        [0, MAX_COLS, "N", OutOfRange],
        [MAX_ROWS, 0, "S", OutOfRange],
        [1, 1, "D", EmptyHand],
        [0, 0, "G", EmptySlot],
        [1, 1, "G G", RoboOverload],
        [2, 2, "G W N D D", PreOccupiedSlot],
    ]

    for test in tests:
        grid_stats = populate_grid_status()
        r, c, input_str, expected = test
        try:
            actual = process_input(input_str, r, c)
        except Exception as e:
            actual, *info = sys.exc_info()

        if actual == expected:
            print("PASS:", test)
        else:
            print("FAIL", test, "{} != {}".format(actual, expected))