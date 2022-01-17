#!/usr/bin/env python3

import sys
from collections import defaultdict
from datetime import date
from enum import Enum

class Board(defaultdict):

    class Key(Enum):
        INVALID = ' '
        OPEN = '_'
        MONTH = 'M'
        DAY = 'D'
        WEEKDAY = 'W'
        P0 = '0'
        P1 = '1'
        P2 = '2'
        P3 = '3'
        P4 = '4'
        P5 = '5'
        P6 = '6'
        P7 = '7'
        P8 = '8'
        P9 = '9'

    def __init__(self, today):
        super(Board, self).__init__(lambda: self.Key.INVALID)
        self.__init_board()
        self.__set_date(today)

    def __repr__(self):
        rows = []
        for r in range(8):
            row = []
            for c in range(7):
                row.append(self[(r, c)].value)
            rows.append(' '.join(row))
        board = '\n'.join(rows)
        return board

    def __init_board(self):
        for r in range(2):
            for c in range(6):
                self[(r, c)] = self.Key.OPEN
        for r in range(2, 7):
            for c in range(7):
                self[(r, c)] = self.Key.OPEN
        for c in range(4, 7):
            self[(7, c)] = self.Key.OPEN

    def __set_date(self, today):
        m = today.month
        self[(m // 6, m % 6)] = self.Key.MONTH

        # d is 0-based
        d = today.day - 1
        self[(d // 7 + 2, d % 7)] = self.Key.DAY

        w = today.weekday()
        if w == 6:
            self[(6, 3)] = self.Key.WEEKDAY
        else:
            self[(w // 3 + 6, w % 3 + 4)] = self.Key.WEEKDAY

if len(sys.argv) > 1:
    today = date.fromisoformat(sys.argv[1])
else:
    today = date.today()

WEEKDAYS = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
print(f'{today} {WEEKDAYS[today.weekday()]}')

board = Board(today)
print(board)
