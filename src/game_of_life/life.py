from abc import abstractmethod, ABC
from time import sleep
from collections import namedtuple


class AbstractLifeGameBoard(ABC):
    def __init__(self, width: int = 3, height: int = 3):
        pass

    def __str__(self):
        """Return a string representation of a board.

        Use small o for alive cells and period for empty cells.
        E.g. for board 3x3 with simplest oscillator:
        .o.
        .o.
        .o.
        """
        pass

    @abstractmethod
    def place_cell(self, row: int, col: int):
        """Make a cell alive."""
        pass

    @abstractmethod
    def toggle_cell(self, row: int, col: int) -> None:
        """Invert state of the cell."""
        pass

    @abstractmethod
    def next(self) -> None:
        pass

    @abstractmethod
    def is_alive(self, row: int, col: int) -> bool:
        pass


class Board(AbstractLifeGameBoard):
    def __init__(self, width: int, height: int):
        self.board = []
        for i in range(height):
            a = [0] * width
            self.board.append(a)
        self.generation = 0

    def __str__(self) -> str:
        rows = []
        for row in self.board:
            row_str = ''.join('.' if cell == 0 else 'o' for cell in row)
            rows.append(row_str)
        return '\n'.join(rows) + '\n'

    def place_cell(self, row: int, col: int):
        self.board[row][col] = 1
        pass

    def toggle_cell(self, row: int, col: int) -> None:
        self.board[row][col] = (self.board[row][col] + 1) % 2
        pass

    def next(self) -> None:
        """Coordinates of all cells that we need to toggle"""
        Position = namedtuple('Position', 'x y')
        cords_to_toggle: list[Position] = []
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                coords = Position(i, j)
                count = self.count_alive(i, j)
                if self.is_alive(i, j):
                    if (count < 2) or (count > 3):
                        cords_to_toggle.append(coords)
                else:
                    if count == 3:
                        cords_to_toggle.append(coords)
        for coords1 in cords_to_toggle:
            self.toggle_cell(coords1.x, coords1.y)
        self.generation += 1

    def count_alive(self, row: int, col: int) -> int:
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j and i == 0:
                    continue
                count += self.is_alive(row + i, col + j)
        return count

    def is_alive(self, row: int, col: int) -> bool:
        if row < 0 or col < 0 or row > len(self.board) - 1 or col > len(self.board[0]) - 1:
            return False
        return bool(self.board[row][col])
        pass


c = CELL_SYMBOL = "o"

if __name__ == "__main__":
    board = Board(3, 3)
    for i in range(3):
        board.place_cell(1, i)
    for i in range(100):
        print (board)
        board.next()
        sleep(0.5)
