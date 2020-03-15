from random import randrange
import json

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

            for h in range(-1, 2):
                for w in range(-1, 2):
                    if self.is_valid(x+w, y+h):
                        if grid[y + h][x + w] != '*':
                            grid[y + h][x + w] += 1
        return grid

    def select(self, x, y):
        if self.is_valid(x, y) and [x, y] not in self.uncovered:
            self.uncovered.append([x, y])
            if self.grid[y][x] == '*':
                self.tries_left -= 1
                if self.tries_left <= 0:
                    self.game = False
            elif self.grid[y][x] == 0:
                for h in range(-1, 2):
                    for w in range(-1, 2):
                        nx = x + w
                        ny = y + h
                        if self.is_valid(nx, ny) and not (w == 0 and h == 0):
                            if self.grid[ny][nx] == 0 and ([ny, nx] not in self.uncovered):
                                self.select(nx, ny)

            return True
        else:
            return False

    def is_valid(self, x, y):
        if isinstance(x, int) and isinstance(y, int):
            return (0 <= x < self.width) and (0 <= y < self.height)
        return False

    def get_visible(self):
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                if [x, y] in self.uncovered:
                    if self.grid[y][x] == 0:
                        row += f"   "
                    else:
                        row += f" {self.grid[y][x]} "
                else:
                    row += "[ ]"
            print(row)


if __name__ == "__main__":
    test_game = MineSweeper()
    for row in test_game.grid:
        print(" "+'  '.join(str(x) for x in row))
    test_game.get_visible()

    while test_game.game:
        print()
        x = int(input("x: "))
        y = int(input("y: "))
        test_game.select(x, y)
        test_game.get_visible()
