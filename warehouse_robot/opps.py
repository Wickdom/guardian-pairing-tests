#!/usr/bin/env python
# coding: utf-8
import sys

from errors import *


class Robot:
    def __init__(self, grid_rows=10, grid_cols=10):
        self._row = 0
        self._column = 0
        self._occupancy = None
        self.max_rows = grid_rows
        self.max_cols = grid_cols
        self._occupancy = [[0] * self.max_cols for _ in range(self.max_rows)]
        self.hold = False
        self.commands = {'N', 'E', 'S', 'W', 'D', 'G'}

    def set_position(self, r, c):
        if (0 <= r < self.max_rows) and (0 <= c < self.max_cols):
            self._row = r
            self._column = c
        else:
            raise OutOfRange("Position Out of Grid Range")

    def place_item(self, r, c):
        current_pos = self.position
        self.set_position(r, c)
        self.hold = True
        self.drop()
        self.set_position(*current_pos)

    @property
    def occupancy(self):
        return self._occupancy

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    @property
    def position(self):
        return self.row, self.column

    def move(self, direction):
        new_place = {
            'N': (self.row - 1, self.column),
            'S': (self.row + 1, self.column),
            'W': (self.row, self.column - 1),
            'E': (self.row, self.column + 1)
        }[direction]
        # print("Moving in ", direction, "from", self.position, "to ", new_place)
        self.set_position(*new_place)

    def move_diagonal(self, direction):
        new_place = {
            'EN': (self.row - 1, self.column + 1),
            'NW': (self.row - 1, self.column - 1),
            'ES': (self.row + 1, self.column + 1),
            'SW': (self.row + 1, self.column - 1)
        }[direction]
        # print("Moving in ", direction, "from", self.position, "to ", new_place)
        self.set_position(*new_place)

    def drop(self):
        if not self.hold:
            raise EmptyHand("Nothing to drop")
        if self.occupancy[self.row][self.column]:
            raise PreOccupiedSlot("Position not free")
        self._occupancy[self.row][self.column] = 1
        self.hold = False

    def grab(self):
        if self.hold:
            raise RoboOverload("Already moving an item")
        if not self.occupancy[self.row][self.column]:
            raise EmptySlot("Position Empty")
        self._occupancy[self.row][self.column] = 0
        self.hold = True

    def parse_input(self, input_str):
        input_sequence = [i for i in input_str if i.strip() and i.strip() != ","]
        invalid_commands = set(input_sequence) - self.commands
        if invalid_commands:
            raise InvalidCommand(invalid_commands, "in the sequence", input_sequence)
        return input_sequence

    def process_command_seq(self, input_str):
        sequence = self.parse_input(input_str)

        for i in range(0, len(sequence), 2):
            commands = sequence[i:i + 2]
            if len(set(commands) - {'D', 'G'}) == 2:
                self.move_diagonal(''.join(sorted(commands)))
            else:
                for command in commands:
                    if command == 'D':
                        self.drop()
                    elif command == 'G':
                        self.grab()
                    else:
                        self.move(command)

        return self.position


if __name__ == '__main__':

    tests = [
        #     [inital_position,input_str,exp_pos]
        [(1, 1), "W S E E", (2, 2)],
        [(2, 3), "N E S W", (2, 3)],
        [(0, 1), "W", (0, 0)],
        [(0, 1), "E", (0, 2)],
        [(0, 1), "S", (1, 1)],
        [(1, 1), "G", (1, 1), True],
        [(1, 1), "G E D", (1, 2), False],
        [(1, 1), "G E S W N D", (1, 1), False],
        [(0, 0), "W", OutOfRange],
        [(0, 0), "D", EmptyHand],
        [(0, 0), "G", EmptySlot],
        [(0, 0), "N", OutOfRange],
        [(9, 9), "E", OutOfRange],
        [(9, 9), "S", OutOfRange],
        [(8, 7), "S E E E", OutOfRange],
        [(0, 0), "G G", EmptySlot],

    ]

    for test in tests:

        # Setup
        test.append("N/A")
        inital_position, input_str, expected, *args = test
        hold_pos, *_ = args

        robo = Robot(10, 10)
        robo.place_item(1, 1)
        robo.set_position(*inital_position)

        try:
            robo.process_command_seq(input_str)
            if robo.position != expected:
                print("Fail", test, "Position not as expected", robo.position, "!=", expected)
            if hold_pos != "N/A" and robo.hold != hold_pos:
                print("Fail", test, "Hold status not as expected", robo.hold, "!=", hold_pos)
            else:
                print("Pass", test)
        except:
            actual, *_ = sys.exc_info()
            if actual != expected:
                print("Fail", test, "Unexpected error", actual)
            else:
                print("Pass", test)