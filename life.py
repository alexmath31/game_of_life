from abc import abstractmethod, ABC
from time import sleep


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
    def __init__(self, width: int = 3, height: int = 3):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        pass

    def __str__(self) -> str:
        s = ""
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    s += '.'
                else:
                    s += 'o'
            s += '\n'
        return s
        pass

    def place_cell(self, row: int, col: int):
        self.board[row][col] = 1
        pass

    def toggle_cell(self, row: int, col: int) -> None:
        self.board[row][col] = (self.board[row][col] + 1) % 2
        pass

    def next(self) -> None:
        a = []
        for i in range(3):
            for j in range(3):
                count = self.count_alive(i, j)
                if self.is_alive(i, j):
                    if (count < 2) or (count > 3):
                        a.append([i, j])
                else:
                    if count == 3:
                        a.append([i, j])
        pass
        for i in range(len(a)):
            self.toggle_cell(a[i][0], a[i][1])

    def count_alive(self, row: int, col: int) -> int:
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j and i == 0:
                    continue
                count += self.is_alive(row + i, col + j)
        return count

    def is_alive(self, row: int, col: int) -> bool:
        if row < 0 or col < 0 or row > 2 or col > 2:
            return False
        if self.board[row][col] == 1:
            return True
        return False
        pass


c = CELL_SYMBOL = "o"

if __name__ == "__main__":
    board = Board(3, 3)
    for i in range(3):
        board.place_cell(1, i)
    for i in range(100):
        print(board)
        board.next()
        sleep(0.5)
