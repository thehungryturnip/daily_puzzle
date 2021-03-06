#!/usr/bin/env python3

import sqlite3
import time
from argparse import ArgumentParser
from datetime import date

WEEKDAYS = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')

class Board(list):
    ROWS = 8
    COLS = 7
    OPEN = '-'
    DB_NAME = 'daily_puzzle.db'
    MD_NAME = 'solutions.md'

    PIECES = (
        # 000
        #   00
        (((0,0), (0,1), (0,2), (1,2), (1,3)),
         ((0,1), (1,1), (2,0), (2,1), (3,0)), # 90
         ((0,0), (0,1), (1,1), (1,2), (1,3)), # 180
         ((0,1), (1,0), (1,1), (2,0), (3,0))), # 270
        # 111
        # 1
        # 1
        (((0,0), (0,1), (0,2), (1,0), (2,0)),
         ((0,0), (0,1), (0,2), (1,2), (2,2)), # 90
         ((0,2), (1,2), (2,0), (2,1), (2,2)), # 180
         ((0,0), (1,0), (2,0), (2,1), (2,2))), # 270
        # 22
        #  2
        #  22
        (((0,0), (0,1), (1,1), (2,1), (2,2)),
         ((0,2), (1,0), (1,1), (1,2), (2,0))), # 90
        # 333
        # 3 3
        (((0,0), (0,1), (0,2), (1,0), (1,2)),
         ((0,0), (0,1), (1,1), (2,0), (2,1)), # 90
         ((0,0), (0,2), (1,0), (1,1), (1,2)), # 180
         ((0,0), (0,1), (1,0), (2,0), (2,1))), # 270
        # 444
        #  4
        #  4
        (((0,0), (0,1), (0,2), (1,1), (2,1)),
         ((0,2), (1,0), (1,1), (1,2), (2,2)), # 90
         ((0,1), (1,1), (2,0), (2,1), (2,2)), # 180
         ((0,0), (1,0), (1,1), (1,2), (2,0))), # 270
        # 5555
        #    5
        (((0,0), (0,1), (0,2), (0,3), (1,3)),
         ((0,1), (1,1), (2,1), (3,0), (3,1)), # 90
         ((0,0), (1,0), (1,1), (1,2), (1,3)), # 180
         ((0,0), (0,1), (1,0), (2,0), (3,0))), # 270
        # 666
        # 66
        (((0,0), (0,1), (0,2), (1,0), (1,1)),
         ((0,0), (0,1), (1,0), (1,1), (2,1)), # 90
         ((0,1), (0,2), (1,0), (1,1), (1,2)), # 180
         ((0,0), (1,0), (1,1), (2,0), (2,1))), # 270
        # 7777
        (((0,0), (0,1), (0,2), (0,3)),
         ((0,0), (1,0), (2,0), (3,0))), # 90
        # 888
        #   8
        (((0,0), (0,1), (0,2), (1,2)),
         ((0,1), (1,1), (2,0), (2,1)), # 90
         ((0,0), (1,0), (1,1), (1,2)), # 180
         ((0,0), (0,1), (1,0), (2,0))), # 270
        #  99
        # 99
        (((0,1), (0,2), (1,0), (1,1)),
         ((0,0), (1,0), (1,1), (2,1))), # 90
    )

    def __init__(self, args):
        self._args = args

        self.COORDS = [(r, c) for r in range(self.ROWS) for c in range(self.COLS)]
        self.__init_board(args.today)

        self.__db_init()

    def do(self):
        if self._args.delete:
            self.__db_delete()
            return 'DELETED'

        if self._args.replace or not self.__db_get():
            self.__solve()
            self.__db_put()
        
        if self._args.append:
            self.__md_append()

        return str(self)

    def __solve(self, working_on = 0):
        if self._args.verbose:
            print(self)
        if working_on == len(self.PIECES):
            return True

        for permutation in self.PIECES[working_on]:
            for r, c in self.COORDS:
                can_place, coords = self.__can_place_at(permutation, r, c)

                if can_place:
                    for pr, pc in coords:
                        self[pr][pc] = str(working_on)

                    if self.__solve(working_on + 1):
                        return True

                    for pr, pc in coords:
                        self[pr][pc] = self.OPEN

        return False

    def __repr__(self):
        return '\n'.join([' '.join(r) for r in self])

    def __init_board(self, today):
        for r in range(self.ROWS):
            self.append([' '] * self.COLS)

        for r, c in [(r, c) for r in range(2) for c in range(6)]:
            self[r][c] = self.OPEN
        for r, c in [(r, c) for r in range(2, 7) for c in range(7)]:
            self[r][c] = self.OPEN
        for c in range(4, 7):
            self[7][c] = self.OPEN

        self.__set_date(today)

    def __set_date(self, today):
        self._db_id = f'{today.month}:{today.day}:{today.weekday()}'

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

    def __db_init(self):
        self._db = sqlite3.connect(self.DB_NAME)
        with self._db as db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS solutions (
                    id STRING NOT NULL PRIMARY KEY,
                    solution STRING
                );""")

    def __db_put(self):
        query = 'INSERT OR REPLACE INTO solutions (id, solution) values(?, ?)'
        params = (self._db_id, '\n'.join([''.join(r) for r in self]))
        with self._db as db:
            db.execute(query, params)

    def __db_get(self):
        query = 'SELECT * FROM solutions WHERE id = :id'
        params = {'id': self._db_id}
        with self._db as db:
            entries = db.execute(query, params).fetchall()

            if not entries:
                return False

            solution = entries[0][1]
            solution = solution.split('\n')
            for r, c in self.COORDS:
                self[r][c] = solution[r][c]
            return True

    def __db_delete(self):
        query = 'DELETE FROM solutions WHERE id = :id'
        params = {'id': self._db_id}
        with self._db as db:
            db.execute(query, params)

    def __md_append(self):
        with open(self.MD_NAME, 'a') as f:
            f.write(f'\n# {self._args.today} {WEEKDAYS[self._args.today.weekday()]}\n```\n{self}\n```\n')

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

parser = ArgumentParser()
parser.add_argument('today', help='the day the puzzle should be solved for', nargs='?', default=date.today())
parser.add_argument('-v', '--verbose', help='verbose mode (prints progress)', action='store_true')

parser.add_argument('-d', '--delete', help='deletes database entry for spceific date', action='store_true')
parser.add_argument('-r', '--replace', help='replace the entry in the database (if exists)', action='store_true')

parser.add_argument('-a', '--append', help='appends result to text file', action='store_true')

args = parser.parse_args()
if isinstance(args.today, str):
    args.today = date.fromisoformat(args.today)

print(f'{args.today} {WEEKDAYS[args.today.weekday()]}')

board = Board(args)
tic = time.perf_counter()
print(board.do())
toc = time.perf_counter()
print(f'{toc - tic:0.3f}s')
