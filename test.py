from abc import abstractmethod, ABC
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QPushButton,
    QLabel,
)
import sys


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
            row_str = "".join("." if cell == 0 else "o" for cell in row)
            rows.append(row_str)
        return "\n".join(rows) + "\n"

    def place_cell(self, row: int, col: int):
        self.board[row][col] = 1
        pass

    def toggle_cell(self, row: int, col: int) -> None:
        self.board[row][col] = (self.board[row][col] + 1) % 2
        pass

    def next(self) -> None:
        a = []
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                count = self.count_alive(i, j)
                if self.is_alive(i, j):
                    if (count < 2) or (count > 3):
                        a.append([i, j])
                else:
                    if count == 3:
                        a.append([i, j])
        for coords in a:
            self.toggle_cell(coords[0], coords[1])
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
        if (
            row < 0
            or col < 0
            or row > len(self.board) - 1
            or col > len(self.board[0]) - 1
        ):
            return False
        return bool(self.board[row][col])
        pass


class GameOfLifeGUI(QMainWindow):
    def __init__(self, width: int, height: int):
        super().__init__()
        self.setWindowTitle("Game of Life")
        self.board = Board(width, height)
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        grid_layout = QGridLayout(self.central_widget)

        self.label_board = QLabel(self)
        grid_layout.addWidget(self.label_board, 0, 0)

        self.next_button = QPushButton("Next Generation", self)
        self.next_button.clicked.connect(self.next_generation)
        grid_layout.addWidget(self.next_button, 1, 0)

        self.update_board_label()

    def update_board_label(self):
        board_str = str(self.board)
        self.label_board.setText(board_str)

    def next_generation(self):
        self.board.next()
        self.update_board_label()

    def start_game(self):
        for i in range(3):
            self.board.place_cell(1, i)
        self.update_board_label()

    def run(self):
        self.show()
        self.start_game()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = GameOfLifeGUI(120, 12)
    game.run()
    sys.exit(app.exec())
