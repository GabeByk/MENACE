#
# Gabe Byk
# CS481: Seminar
# 13 October 2022
#

from __future__ import annotations
from Move import Move
from typing import List
from Transformation import Transformation

class Board:

    # this Board is a _size by _size grid
    _size: int
    # a list containing the state of each of the _size x _size cells in the board.
    # element 0 is row 1, column 1; the first _size elements form row 1, and each _size elements thereafter are the
    # next row.
    _grid: List[str]

    def __init__(self, size: int = 3):
        """
        Creates a new Tic-Tac-Toe Board of the given size
        :param size: the number of cells across the board; defaults to 3 (the usual board size) if not provided.
        """
        self._size = size
        self._grid = [Move.BLANK for i in range(size * size)]

    def isLegal(self, move: Move) -> bool:
        """
        :param move: The move to check
        :return: True if the move is legal on this board, False otherwise
        """
        row, column = move.position()
        return self._grid[column - 1 + self._size * (row - 1)] == Move.BLANK

    def makeMove(self, move: Move):
        """
        Mutates this Board so it contains the given Move
        :param move: The Move to make
        """
        row, column = move.position()
        self._grid[column - 1 + (row - 1) * self._size] = move.symbol()

    def applyTransformation(self, t: Transformation) -> None:
        """
        Applies the given Transformation to this Board.
        :param t: the Transformation to apply
        """

    def transformationTo(self, other: Board) -> Transformation | None:
        """
        Determines the Transformation that would take this Board to the given Board, if one exists.
        :param other: the Board that we should get to
        :return: The Transformation that would take us to the Board, or None if no such transformation exists.
        """

    def __repr__(self) -> str:
        """
        :return: the string representation of this Board
        """
        result = []
        for row in range(self._size):
            for column in range(self._size):
                result.append(self._grid[column + row * self._size])
            result.append("\n")
        return "".join(result)

def main():
    size = 4
    b = Board(size)
    print(b)
    for row in range(1, size + 1):
        for column in range(1, size + 1):
            pos = column + size * (row - 1)
            if pos % 2 == 0:
                symbol = Move.CROSS
            else:
                symbol = Move.NOUGHT
            b.makeMove(Move(row, column, symbol))
            print(b)


if __name__ == "__main__":
    main()
