#
# Gabe Byk
# CS481: Seminar
# 13 October 2022
#

from typing import Tuple

class Move:
    # the x and y coordinates of the move on the board's grid
    _x: int
    _y: int
    # the symbol of the move to make: one of Board.X or Board.O
    _symbol: str

    def __init__(self, row: int, column: int, symbol: str):
        """
        Creates a Move
        :param row: the row number of the move, with the top being row 1 and increasing by 1 for each row down
        :param column: the column of the move, with the left being column 1 and increasing by 1 for each column right
        :param symbol: the symbol of the player that made this move
        """
        # x is the index of the move in Board's internal array
        self._x = column - 1
        self._y = row - 1
        self._symbol = symbol

    def coordinates(self) -> Tuple[int, int]:
        """
        :return: the x, y coordinates of where the move is on the board
        """
        return self._x, self._y

    def symbol(self) -> str:
        """
        :return: the symbol for this move
        """
        return self._symbol
