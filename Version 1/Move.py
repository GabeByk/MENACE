#
# Gabe Byk
# CS481: Seminar
# 13 October 2022
#

from typing import Tuple


class Move:
    # class variables that determine the character to be used for O, X, and nothing
    NOUGHT = "O"
    CROSS = "X"
    BLANK = "_"
    # this Move is made in row _row, column _column of a Board
    _row: int
    _column: int
    # the symbol of the move to make: one of Board.X or Board.O
    _symbol: str

    def __init__(self, row: int, column: int, symbol: str):
        """
        Creates a Move
        :param row: the row number of the move, with the top being row 1 and increasing by 1 for each row down
        :param column: the column of the move, with the left being column 1 and increasing by 1 for each column right
        :param symbol: the symbol of the player that made this move; should be one of Move.NOUGHT or Move.CROSS
        """
        self._row = row
        self._column = column
        self._symbol = symbol

    def position(self) -> Tuple[int, int]:
        """
        :return: the row and column of where the move is on the board
        """
        return self._row, self._column

    def symbol(self) -> str:
        """
        :return: the symbol for this move
        """
        return self._symbol
