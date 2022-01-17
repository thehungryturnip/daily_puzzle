#!/usr/bin/env python3

import sys
import time
from datetime import date

class Board(list):
    ROWS = 8
    COLS = 7
    OPEN = '-'

    PIECES = (
        # 000
        #  0
        #  0
        (((0,0), (0,1), (0,2), (1,1), (2,1)),
         ((0,2), (1,0), (1,1), (1,2), (2,2)), # r90
         ((0,1), (1,1), (2,0), (2,1), (2,2)), # r180
         ((0,0), (1,0), (1,1), (1,2), (2,0))), # r270
        # 111
        #   11
        (((0,0), (0,1), (0,2), (1,2), (1,3)),
         ((0,1), (1,1), (2,0), (2,1), (3,0)), # r90
         ((0,0), (0,1), (1,1), (1,2), (1,3)), # r180
         ((0,1), (1,0), (1,1), (2,0), (3,0)), # r270
         ((0,1), (0,2), (0,3), (1,0), (1,1)), # flip
         ((0,0), (1,0), (1,1), (2,1), (3,1)), # flip r90
         ((0,2), (0,3), (1,0), (1,1), (1,2)), # flip r180
         ((0,0), (1,0), (2,0), (2,1), (3,1))), # flip r270
        # 222
        # 2
        # 2
        (((0,0), (0,1), (0,2), (1,0), (2,0)),
         ((0,0), (0,1), (0,2), (1,2), (2,2)), # r90
         ((0,2), (1,2), (2,0), (2,1), (2,2)), # r180
         ((0,0), (1,0), (2,0), (2,1), (2,2))), # r270
        # 33
        #  3
        #  33
        (((0,0), (0,1), (1,1), (2,1), (2,2)),
         ((0,2), (1,0), (1,1), (1,2), (2,0)), # r90
         ((0,1), (0,2), (1,1), (2,0), (2,1)), # flip
         ((0,0), (1,0), (1,1), (1,2), (2,2))), # flip r90
        # 4444
        # 4
        (((0,0), (0,1), (0,2), (0,3), (1,0)),
         ((0,0), (0,1), (1,1), (2,1), (3,1)), # r90
         ((0,3), (1,0), (1,1), (1,2), (1,3)), # r180
         ((0,0), (1,0), (2,0), (3,0), (3,1)), # r270
         ((0,0), (0,1), (0,2), (0,3), (1,3)), # flip
         ((0,1), (1,1), (2,1), (3,0), (3,1)), # flip r90
         ((0,0), (1,0), (1,1), (1,2), (1,3)), # flip r180
         ((0,0), (0,1), (1,0), (2,0), (3,0))), # flip r270
        # 5555
        (((0,0), (0,1), (0,2), (0,3)),
         ((0,0), (1,0), (2,0), (3,0))), # r90
        # 666
        # 6 6
        (((0,0), (0,1), (0,2), (1,0), (1,2)),
         ((0,0), (0,1), (1,1), (2,0), (2,1)), # r90
         ((0,0), (0,2), (1,0), (1,1), (1,2)), # r180
         ((0,0), (0,1), (1,0), (2,0), (2,1))), # r270
        # 777
        # 77
        (((0,0), (0,1), (0,2), (1,0), (1,1)),
         ((0,0), (0,1), (1,0), (1,1), (2,1)), # r90
         ((0,1), (0,2), (1,0), (1,1), (1,2)), # r180
         ((0,0), (1,0), (1,1), (2,0), (2,1)), # r270
         ((0,0), (0,1), (0,2), (1,1), (1,2)), # flip
         ((0,1), (1,0), (1,1), (2,0), (2,1)), # flip r90
         ((0,0), (0,1), (1,0), (1,1), (1,2)), # flip r180
         ((0,0), (0,1), (1,0), (1,1), (2,0))), # flip r270
        # 888
        #   8
        (((0,0), (0,1), (0,2), (1,2)),
         ((0,1), (1,1), (2,0), (2,1)), # r90
         ((0,0), (1,0), (1,1), (1,2)), # r180
         ((0,0), (0,1), (1,0), (2,0)), # r270
         ((0,0), (0,1), (0,2), (1,0)), # flip
         ((0,0), (0,1), (1,1), (2,1)), # flip r90
         ((0,2), (1,0), (1,1), (1,2)), # flip r180
         ((0,0), (1,0), (2,0), (2,1))), # flip r270
        # 99
        #  99
        (((0,0), (0,1), (1,1), (1,2)),
         ((0,1), (1,0), (1,1), (2,0)), # r90
         ((0,1), (0,2), (1,0), (1,1)), # flip
         ((0,0), (1,0), (1,1), (2,1))), # flip r90
    )

    def __init__(self, today):
        self.COORDS = [(r, c) for r in range(self.ROWS) for c in range(self.COLS)]
        for r in range(self.ROWS):
            self.append([' '] * self.COLS)
        self.__init_board()
        self.__set_date(today)

    def solve(self, working_on = 0):
        if working_on == len(self.PIECES):
            return True

        for permutation in self.PIECES[working_on]:
            for r, c in self.COORDS:
                can_place, coords = self.__can_place_at(permutation, r, c)

                if can_place:
                    for pr, pc in coords:
                        self[pr][pc] = str(working_on)

                    if self.solve(working_on + 1):
                        return True

                    for pr, pc in coords:
                        self[pr][pc] = self.OPEN

        return False

    def __repr__(self):
        return '\n'.join([' '.join(r) for r in self])

    def __init_board(self):
        for r, c in [(r, c) for r in range(2) for c in range(6)]:
            self[r][c] = self.OPEN
        for r, c in [(r, c) for r in range(2, 7) for c in range(7)]:
            self[r][c] = self.OPEN
        for c in range(4, 7):
            self[7][c] = self.OPEN

    def __set_date(self, today):
        # m is 0-based
        m = today.month - 1
        self[m // 6][m % 6] = 'M'

        # d is 0-based
        d = today.day - 1
        self[d // 7 + 2][d % 7] = 'D'

        w = today.weekday()
        if w == 6:
            self[6][3] = 'W'
        else:
            self[w // 3 + 6][w % 3 + 4] = 'W'

    def __can_place_at(self, permutation, board_r, board_c):
        coords = []
        for dr, dc in permutation:
            c = board_c + dc
            if c < 0 or c >= self.COLS:
                return False, coords

            r = board_r + dr
            if r < 0 or r >= self.ROWS:
                return False, coords

            if self[r][c] != self.OPEN:
                return False, coords

            coords.append((r, c))

        return True, coords

if len(sys.argv) > 1:
    today = date.fromisoformat(sys.argv[1])
else:
    today = date.today()

WEEKDAYS = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
print(f'{today} {WEEKDAYS[today.weekday()]}')

board = Board(today)
tic = time.perf_counter()
board.solve()
toc = time.perf_counter()
print(board)
print(f'{toc - tic:0.3f}s')
