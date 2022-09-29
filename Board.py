#
# Gabe Byk
# CS481
# Board.py
#
from __future__ import annotations
from typing import List, Tuple
from copy import deepcopy

def isHomogenous(symbols: List) -> bool:
    """
    :param symbols: the list to check
    :return: whether all elements of the list are equal
    """
    startSymbol = symbols[0]
    # assume everything matches
    match = True
    # check that it does
    for symbol in symbols[1:]:
        # if the symbol doesn't match the first one, we don't have a match
        match = match and symbol == startSymbol
    # report our findings
    return match


class Board:
    # the current state of the board; "_" means no move, "X" means an X, "O" means an O
    _state = List[List[str]]

    # the character that signifies an empty spot
    empty = "_"
    # the character that signifies a move from the X player
    cross = "X"
    # the character that signifies a move from the O player
    naught = "O"

    def __init__(self, label: str = None):
        """
        Create a board
        :param label: Optional; if provided in the same format as compactStr outputs, initializes the Board to that
        state
        """
        # state is a 3x3 array
        self._state = [[Board.empty for i in range(3)] for j in range(3)]
        if label is not None and len(label) == 9:
            for i in range(len(label)):
                row = i // 3
                column = i % 3
                self._state[row][column] = label[i]

    def isLegal(self, position: Tuple[int, int]) -> bool:
        """
        :param position: the x, y position to check, with (0, 0) at the top left and (2, 2) at the bottom right
        :return: whether it's legal to move at the given position
        """
        x, y = position
        # a move is only legal if it's on the board
        if 0 <= x <= 2 and 0 <= y <= 2:
            # position x, y is row y column x
            return self._state[y][x] == Board.empty
        else:
            return False

    def addMove(self, symbol: str, position: Tuple[int, int]):
        """
        Adds the given symbol to the given position
        :param symbol: The symbol to put at the given position; should be one of Board.naught or Board.cross
        :param position: the (x, y) position of the space to fill, with top left (0, 0) and bottom right (2, 2)
        """
        from MENACE import Matchbox
        if position == Matchbox.forfeit:
            for x in range(3):
                for y in range(3):
                    self._state[y][x] = "-" * len(Matchbox.forfeit)
            self._state[1][1] = Matchbox.forfeit
        else:
            x, y = position
            # position x, y is row y column x
            self._state[y][x] = symbol

    def _getRows(self) -> List[List[str]]:
        """
        :return: the rows of the board
        """
        # self._state is the rows of the board
        return self._state[:]

    def _getColumns(self) -> List[List[str]]:
        """
        :return: the columns of the board
        """
        columns = [["" for j in range(3)] for i in range(3)]
        # the columns array is basically just the rows array flipped
        for x in range(3):
            for y in range(3):
                columns[x][y] = self._state[y][x]
        return columns

    def _getDiagonals(self) -> List[List[str]]:
        """
        :return: the diagonals of the board
        """
        diagonals = [[], []]
        for i in range(3):
            # add the main diagonal to 0
            diagonals[0].append(self._state[i][i])
            # add the other diagonal to 1
            diagonals[1].append(self._state[i][2 - i])
        return diagonals

    def getWinner(self) -> str | None:
        """
        :return: symbol has 3 in a row, excluding Board.empty, or None if there is no winner
        """
        # check the rows for matches
        for row in self._getRows():
            # the game is over if this row has all matching symbols that aren't the blank symbol
            if row[0] != Board.empty and isHomogenous(row):
                return row[0]
        for column in self._getColumns():
            # same logic as the rows but with the columns
            if column[0] != Board.empty and isHomogenous(column):
                return column[0]
        for diagonal in self._getDiagonals():
            # same logic but with diagonals
            if diagonal[0] != Board.empty and isHomogenous(diagonal):
                return diagonal[0]
        # if we're at this point, there is no winner
        return None

    def isFull(self) -> bool:
        """
        :return: True if there are no legal moves, False otherwise
        """
        # assume there are no spots left
        spotsLeft = False
        # check each spot to see if it's empty
        for row in range(3):
            for column in range(3):
                spotsLeft = spotsLeft or self._state[row][column] == Board.empty
        # if there are no spots left, the game is over
        return not spotsLeft

    def isOver(self) -> bool:
        """
        Determines if there is a 3 in a row anywhere on the board
        :return: whether the game should be over
        """
        # if there's a winner, the game is over
        if self.getWinner() is not None:
            return True
        # we know there's no winner, but if the board is full, there game is still over
        return self.isFull()

    def compactStr(self) -> str:
        """
        :return: all the current moves on the same line (e.g. _XXOX__XO)
        """
        final = []
        for row in self._state:
            for move in row:
                final.append(move)
        return "".join(final)

    def __copy__(self) -> Board:
        """
        :return: a deep copy of this Board
        """
        # return a copy of this board
        b = Board()
        b._state = deepcopy(self._state)
        return b

    def __eq__(self, other: Board) -> bool:
        """
        Two Boards are considered equivalent if their layout is exactly the same
        :param other: the Board to compare against
        :return: True if the Boards are equivalent, False otherwise
        """
        return self._state == other._state

    def __ne__(self, other: Board) -> bool:
        """
        Two Boards are considered different if any spot is different
        :param other: the Board to compare against
        :return: True if the Boards are different, False otherwise
        """
        return not self == other

    def __repr__(self) -> str:
        """
        :return: The string representation of the board
        """
        boardString = []
        for row in self._state:
            for symbol in row:
                boardString.append(symbol)
            boardString.append("\n")
        return "".join(boardString[:-1])
