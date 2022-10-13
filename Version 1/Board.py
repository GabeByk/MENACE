#
# Gabe Byk
# CS481: Seminar
# 13 October 2022
#

from Move import Move
from typing import List

class Board:
    # the symbols that go on the board
    X: str = "X"
    O: str = "O"
    empty: str = "_"
    # the grid that stores the moves made
    _grid: List[List[str]]
    # the board is size x size spots long
    _size: int

    def __init__(self, size: int = 3):
        self._size = size
        self.reset()

    def reset(self):
        """
        Resets the board to an empty state
        """
        self._grid = [[Board.empty for row in range(self._size)] for column in range(self._size)]

    def isWinner(self) -> bool:
        """
        :return: True if someone won, False otherwise
        """
        mainDiagonalSymbol = self._grid[0][0]
        offDiagonalSymbol = self._grid[0][self._size - 1]
        mainDiagonalWinner = mainDiagonalSymbol != Board.empty
        offDiagonalWinner = offDiagonalSymbol != Board.empty
        for i in range(self._size):
            # check if there is a winner in row i
            rowWinner = True
            rowSymbol = self._grid[i][0]
            if rowSymbol != Board.empty:
                for x in range(1, self._size):
                    rowWinner = rowWinner and self._grid[i][x] == rowSymbol
                # end execution early if this row has a winner
                if rowWinner:
                    return True

            # check if there is a winner in column i
            columnSymbol = self._grid[0][i]
            columnWinner = True
            if columnSymbol != Board.empty:
                for y in range(1, self._size):
                    columnWinner = columnWinner and self._grid[y][i] == columnSymbol
                # end execution early if this column has a winner
                if columnWinner:
                    return True

            # check if there's a winner in each diagonal
            mainDiagonalWinner = mainDiagonalWinner and mainDiagonalSymbol == self._grid[i][i]
            offDiagonalWinner = offDiagonalWinner and offDiagonalSymbol == self._grid[i][self._size - 1 - i]
        # we've already returned if there was a winner in a row or a column, so there's only a winner if they're in
        # a diagonal
        return mainDiagonalWinner or offDiagonalWinner

    def isFull(self) -> bool:
        """
        :return: True if there are no legal moves left, False otherwise
        """
        for row in self._grid:
            if Board.empty in row:
                return False
        return True

    def gameOver(self) -> bool:
        """
        :return: True if there is a winner or there are no moves left to make, False otherwise
        """
        return self.isWinner() or self.isFull()

    def isLegal(self, move: Move) -> bool:
        """
        :param move: the Move to check
        :return: True if the Move is legal, False otherwise
        """
        x, y = move.coordinates()
        if 0 <= x < self._size and 0 <= y < self._size:
            return self._grid[y][x] == Board.empty
        else:
            return False

    def makeMove(self, move: Move) -> None:
        """
        Makes the given move on the board
        :param move: the Move to make
        """
        x, y = move.coordinates()
        if self.isLegal(move):
            self._grid[y][x] = move.symbol()

    def __repr__(self) -> str:
        result = []
        for row in self._grid:
            for ch in row:
                result.append(ch)
            result.append("\n")
        return "".join(result[0:-1])

def main():
    size = 5
    b = Board(size)
    print(b)
    print(b.isWinner())
    print(b.isFull())
    print()
    symbols = (Board.X, Board.O)
    for rowNum in range(1, size + 1):
        for columnNum in range(1, size + 1):
            move = Move(rowNum, columnNum, symbols[(rowNum + columnNum) % 2])
            b.makeMove(move)
            print(b)
            print(b.isWinner())
            print(b.isFull())
            print()


if __name__ == "__main__":
    main()
