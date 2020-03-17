from random import randrange
import json
from os import system

from time import sleep


class MineSweeper:
    # Global difficulty variables.
    #   first list value is the multiplier for bombs (total tiles * multiplier = # of bombs)
    #   second index is the max number of errors before game over!
    with open('config.json') as config_file:
        _CONFIG = json.load(config_file)
    _DIFFICULTY = _CONFIG["difficulty"]

    def __init__(self, height=10, width=10, difficulty=None, mines=None, tries=None):
        self.height = height
        self.width = width
        if difficulty not in self._DIFFICULTY.keys():
            difficulty = self._CONFIG["default"]["difficulty"]
        self.tot_mines = round(self.height * self.width * self._DIFFICULTY[difficulty][0])
        self.max_tries = self._DIFFICULTY[difficulty][1]
        self.flagged = []
        self.bombs = []

        if isinstance(mines, int):
            if 0 < mines < self.height * self.width:
                self.tot_mines = mines
            else:
                print("WARNING: Invalid mines parameter! Remember, mines is optional! "
                      "If you wish to set the number of mines, use a valid int! (height * width > mines > 0)")
        if isinstance(tries, int):
            if -1 <= tries:
                self.max_tries = tries
            else:
                print("WARNING: Invalid tries parameter! Remember, tries is optional! "
                      "If you wish to set the number of tries, use a valid int greater than 0!")

        self.tries_left = self.max_tries
        self.grid = self.build_grid()
        self.uncovered = []
        self.game = True

    def build_grid(self):
        grid = [[0]*self.width for _ in range(self.height)]
        for i in range(self.tot_mines):
            y, x = randrange(0, self.height), randrange(0, self.width)
            while grid[y][x] == '*':
                y, x = randrange(0, self.height), randrange(0, self.width)
            grid[y][x] = '*'
            self.bombs.append([y, x])
            for h in range(-1, 2):
                for w in range(-1, 2):
                    if self.is_valid(x+w, y+h):
                        if grid[y + h][x + w] != '*':
                            grid[y + h][x + w] += 1
        return grid

    def select(self, y, x, s=None):
        if self.is_valid(y, x) and [y, x] not in self.uncovered:
            if s is None:
                self.uncovered.append([y, x])
            if self.grid[y][x] == '*':
                if s is None:
                    self.tries_left -= 1
                    if self.tries_left <= 0:
                        self.game = False
                else:
                    self.flagged.append([y, x])
            elif self.grid[y][x] == 0:
                if s is None:
                    self.check_nearby_empty(y, x)
                else:
                    self.flagged.append([y, x])
            for bomb in self.bombs:
                if bomb in self.uncovered or bomb in self.flagged:
                    self.game = False

            return True
        else:
            return False

    def check_nearby_empty(self, y, x):
        # x and y offset!
        for yo in range(-1, 2):
            for xo in range(-1, 2):
                if self.is_valid(y+yo, x+xo):
                    if self.grid[y+yo][x+xo] == 0 and (not [y+yo, x+xo] in self.uncovered):
                        self.uncovered.append([y+yo, x+xo])
                        self.check_nearby_empty(y+yo, x+xo)

    def is_valid(self, y, x):
        if isinstance(x, int) and isinstance(y, int):
            return (0 <= x < self.width) and (0 <= y < self.height)
        return False

    def get_visible(self):
        row = "y|"
        for i in range(self.width):
            row += f"_{i}_"
        print(row+"x")
        for y in range(self.height):
            row = f"{y}|"
            for x in range(self.width):
                if [y, x] in self.uncovered:
                    if self.grid[y][x] == 0:
                        row += f"   "
                    else:
                        row += f" {self.grid[y][x]} "
                elif [y, x] in self.flagged:
                    row += "[>]"
                else:
                    row += "[ ]"
            print(row)


if __name__ == "__main__":
    test_game = MineSweeper()
    # for row in test_game.grid:
    #     print(" "+'  '.join(str(x) for x in row))
    # test_game.get_visible()
    system('clear')

    while test_game.game:
        print(f"Tries: {test_game.tries_left}/{test_game.max_tries}")
        test_game.get_visible()
        try:
            select = input("'m' to mark bomb, or enter to uncover a square: ").lower()
            if select == 'm':
                x = int(input("x: "))
                y = int(input("y: "))
                test_game.select(y, x, 'm')
            elif select == '':
                x = int(input("x: "))
                y = int(input("y: "))
                test_game.select(y, x)
        except:
            system('clear')
            print('invalid response!')
    test_game.get_visible()
    print("Game Over!")
