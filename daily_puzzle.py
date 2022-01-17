#!/usr/bin/env python3

import sys
from collections import defaultdict
from datetime import date

class Board(defaultdict):
    OPEN = '-'

    PIECES = (
        # 0000
        (((0,0), (0,1), (0,2), (0,3)),
         ((0,0), (1,0), (2,0), (3,0))), # r90
        # 11
        #  11
        (((0,0), (0,1), (1,1), (1,2)),
         ((0,1), (1,0), (1,1), (2,0)), # r90
         ((0,1), (0,2), (1,0), (1,1)), # flip
         ((0,0), (1,0), (1,1), (2,1))), # flip r90
        # 222
        #   2
        (((0,0), (0,1), (0,2), (1,2)),
         ((0,1), (1,1), (2,0), (2,1)), # r90
         ((0,0), (1,0), (1,1), (1,2)), # r180
         ((0,0), (0,1), (1,0), (2,0)), # r270
         ((0,0), (0,1), (0,2), (1,0)), # flip
         ((0,0), (0,1), (1,1), (2,1)), # flip r90
         ((0,2), (1,0), (1,1), (1,2)), # flip r180
         ((0,0), (1,0), (2,0), (2,1))), # flip r270
        # 333
        #  3
        #  3
        (((0,0), (0,1), (0,2), (1,1), (2,1)),
         ((0,2), (1,0), (1,1), (1,2), (2,2)), # r90
         ((0,1), (1,1), (2,0), (2,1), (2,2)), # r180
         ((0,0), (1,0), (1,1), (1,2), (2,0))), # r270
        # 444
        # 4 4
        (((0,0), (0,1), (0,2), (1,0), (1,2)),
         ((0,0), (0,1), (1,1), (2,0), (2,1)), # r90
         ((0,0), (0,2), (1,0), (1,1), (1,2)), # r180
         ((0,0), (0,1), (1,0), (2,0), (2,1))), # r270
        # 555
        # 5
        # 5
        (((0,0), (0,1), (0,2), (1,0), (2,0)),
         ((0,0), (0,1), (0,2), (1,2), (2,2)), # r90
         ((0,2), (1,2), (2,0), (2,1), (2,2)), # r180
         ((0,0), (1,0), (2,0), (2,1), (2,2))), # r270
        # 66
        #  6
        #  66
        (((0,0), (0,1), (1,1), (2,1), (2,2)),
         ((0,2), (1,0), (1,1), (1,2), (2,0)), # r90
         ((0,1), (0,2), (1,1), (2,0), (2,1)), # flip
         ((0,0), (1,0), (1,1), (1,2), (2,2))), # flip r90
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
        # 8888
        # 8
        (((0,0), (0,1), (0,2), (0,3), (1,0)),
         ((0,0), (0,1), (1,1), (2,1), (3,1)), # r90
         ((0,3), (1,0), (1,1), (1,2), (1,3)), # r180
         ((0,0), (1,0), (2,0), (3,0), (3,1)), # r270
         ((0,0), (0,1), (0,2), (0,3), (1,3)), # flip
         ((0,1), (1,1), (2,1), (3,0), (3,1)), # flip r90
         ((0,0), (1,0), (1,1), (1,2), (1,3)), # flip r180
         ((0,0), (0,1), (1,0), (2,0), (3,0))), # flip r270
        # 999
        #   99
        (((0,0), (0,1), (0,2), (1,2), (1,3)),
         ((0,1), (1,1), (2,0), (2,1), (3,0)), # r90
         ((0,0), (0,1), (1,1), (1,2), (1,3)), # r180
         ((0,1), (1,0), (1,1), (2,0), (3,0)), # r270
         ((0,1), (0,2), (0,3), (1,0), (1,1)), # flip
         ((0,0), (1,0), (1,1), (2,1), (3,1)), # flip r90
         ((0,2), (0,3), (1,0), (1,1), (1,2)), # flip r180
         ((0,0), (1,0), (2,0), (2,1), (3,1))) # flip r270
    )

    def __init__(self, today):
        super(Board, self).__init__(lambda: ' ')
        self.__init_board()
        self.__set_date(today)

    def solve(self, workingOn = 0):
        if workingOn == len(self.PIECES):
            return True

        for permutation in self.PIECES[workingOn]:
            for r, c in [(r, c) for r in range(8) for c in range(7)]:
                coords = [(r + dr, c + dc) for (dr, dc) in permutation]
                if all(self[coord] == self.OPEN for coord in coords):
                    for coord in coords:
                        self[coord] = str(workingOn)

                    if self.solve(workingOn + 1):
                        return True

                    for coord in coords:
                        self[coord] = str(self.OPEN)
        return False

    def __repr__(self):
        rows = []
        for r in range(8):
            row = []
            for c in range(7):
                row.append(self[(r, c)])
            rows.append(' '.join(row))
        board = '\n'.join(rows)
        return board

    def __init_board(self):
        for r, c in [(r, c) for r in range(2) for c in range(6)]:
            self[(r, c)] = self.OPEN
        for r, c in [(r, c) for r in range(2, 7) for c in range(7)]:
            self[(r, c)] = self.OPEN
        for c in range(4, 7):
            self[(7, c)] = self.OPEN

    def __set_date(self, today):
        # m is 0-based
        m = today.month - 1
        self[(m // 6, m % 6)] = 'M'

        # d is 0-based
        d = today.day - 1
        self[(d // 7 + 2, d % 7)] = 'D'

        w = today.weekday()
        if w == 6:
            self[(6, 3)] = 'W'
        else:
            self[(w // 3 + 6, w % 3 + 4)] = 'W'

if len(sys.argv) > 1:
    today = date.fromisoformat(sys.argv[1])
else:
    today = date.today()

WEEKDAYS = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
print(f'{today} {WEEKDAYS[today.weekday()]}')

board = Board(today)
board.solve()
print(board)
