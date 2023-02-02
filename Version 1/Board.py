#
# Gabe Byk
# CS481: Seminar
# 13 October 2022
#

from __future__ import annotations
from copy import copy
from Move import Move
from typing import List
from Transformation import Transformation, Rotation, Reflection, Translation
from util import IllegalMoveError


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
        self.reset()

    def reset(self) -> None:
        """
        Resets the board to an empty state
        """
        self._grid = [Move.BLANK for i in range(self._size * self._size)]

    def size(self) -> int:
        """
        :return: The size of the board n, where the board is n by n.
        """
        return self._size

    def legalMove(self, move: Move) -> bool:
        """
        :param move: The move to check
        :return: True if the move is legal on this board, False otherwise
        """
        row, column = move.position()
        try:
            return self._grid[column - 1 + self._size * (row - 1)] == Move.BLANK
        except IndexError:
            return False

    def makeMove(self, move: Move):
        """
        Mutates this Board to contain the given Move
        :param move: The Move to make
        :raises IllegalMoveError: If the move to be made was illegal
        """
        if self.legalMove(move):
            row, column = move.position()
            # move's row and column numbers are 1 off of the index, so we need to adjust them
            self._grid[column - 1 + (row - 1) * self._size] = move.symbol()
        else:
            raise IllegalMoveError(f"Move {move} is illegal with game state: \n{self}")

    def sum(self) -> int:
        """
        Calculates the number of turns that have been taken on this Board
        :return: The number of non-empty cells on the board (i.e. the number of cells that aren't Move.BLANK)
        """
        total = 0
        for symbol in self._grid:
            if symbol != Move.BLANK:
                total += 1
        return total

    def winner(self) -> str | None:
        """
        Determines if there is a winner of the game
        :return: Which symbol won (one of Move.NOUGHT or Move.CROSS), or None if there is no winner or there's a draw
        """
        # check for a winner in the rows
        for row in range(self._size):
            # if there's a winner, they have to match the first symbol in the row
            winner = self._grid[row * self._size]
            won = True
            # if the first cell is blank, we can skip this row
            if winner != Move.BLANK:
                # check each cell in this row to see if it's the same as the first entry
                for column in range(1, self._size):
                    won = won and self._grid[column + self._size * row] == winner
                # if every cell matched, we have a winner
                if won:
                    return winner

        # check for a winner in the columns
        for column in range(self._size):
            # essentially just the same as above but with the rows and columns flipped
            winner = self._grid[column]
            won = True
            if winner != Move.BLANK:
                for row in range(1, self._size):
                    won = won and self._grid[column + self._size * row] == winner
                if won:
                    return winner
        # check for a winner in the diagonals
        # grab the first entry of the diagonal
        mainDiagonalWinner = self._grid[0]
        alternateDiagonalWinner = self._grid[(self._size - 1) * self._size]
        # we can only have won if the first cell isn't blank
        mainDiagonalWon = mainDiagonalWinner != Move.BLANK
        alternateDiagonalWon = alternateDiagonalWinner != Move.BLANK
        # check each of the remaining cells
        for i in range(1, self._size):
            # to go from one cell in the main diagonal (top left to bottom right) to the next, add self._size + 1
            mainDiagonalWon = mainDiagonalWon and self._grid[i * (self._size + 1)] == mainDiagonalWinner
            # to go from one cell in the alternate diagonal (bottom left to top right) to the next,
            # subtract self._size - 1
            alternateDiagonalWon = alternateDiagonalWon and self._grid[(self._size - 1) * self._size -
                                                                       i * (self._size - 1)] == alternateDiagonalWinner
        # see if either diagonal won
        if mainDiagonalWon:
            return mainDiagonalWinner
        elif alternateDiagonalWon:
            return alternateDiagonalWinner
        # if there was no winner anywhere, there is no winner
        return None

    def isOver(self) -> bool:
        """
        Determines if the game is over
        :return: True if there is a winner or it's a draw, False otherwise
        """
        # a drawn game is over
        if Move.BLANK not in self._grid:
            return True
        # if the game isn't drawn, then the game is over if and only if there is a winner
        else:
            return self.winner() is not None

    def applyTransformation(self, t: Transformation) -> None:
        """
        Applies the given Transformation to this Board.
        :param t: the Transformation to apply
        """
        newGrid = [Move.BLANK for i in range(self._size * self._size)]
        for row in range(self._size):
            for column in range(self._size):
                # we need to transform from row x column y to coordinate space;
                # for a 3x3 board, it's (column, 2 - row)
                x, y = t.transformedPoint((float(column), float(self._size - 1 - row)))
                # transfer from point space back to row/column space
                newRow, newColumn = round(self._size - 1 - y), round(x)
                newGrid[newRow + self._size * newColumn] = self._grid[row + self._size * column]
        self._grid = newGrid

    def transformationTo(self, other: Board) -> Transformation | None:
        """
        Determines the Transformation that would take this Board to the given Board, if one exists.
        :param other: the Board that we should get to
        :return: The Transformation that would take us to the Board, or None if no such transformation exists.
        """
        # with the bottom left at (0, 0) and the top right at (size - 1, size - 1), the center is just their midpoint
        center = ((self._size - 1) / 2, (self._size - 1) / 2)
        # these transformations are needed for the rotations and reflections
        translateToOrigin = Translation(-center[0], -center[1])
        translateBack = Translation(center[0], center[1])
        # check rotations for equivalence
        for i in range(4):
            duplicate = copy(self)
            pureRotation = Rotation((0, 0), 90 * i)
            combinedRotation = translateBack * pureRotation * translateToOrigin
            # check if the rotation would make the board states equivalent
            duplicate.applyTransformation(combinedRotation)
            if duplicate._grid == other._grid:
                return combinedRotation

        # check the reflections
        for i in range(4):
            duplicate = copy(self)
            # to reflect about the right line, we need to move the center to (0, 0), then flip, then move back
            reflection = Reflection(45 * i)
            # combine the transformations
            combinedTransformation = translateBack * reflection * translateToOrigin
            # apply the transformation
            duplicate.applyTransformation(combinedTransformation)
            # check to see if they're the same
            if duplicate._grid == other._grid:
                return combinedTransformation

        # if none of the transformations were equivalent, then no transformation exists
        return None

    def isEquivalentTo(self, other: Board) -> bool:
        """
        Determines if these boards are equivalent up to rotations and reflections, i.e. there exists a rotation or
        reflection to get from this board to the other.
        :param other: the Board to compare
        :return: True if the boards are equivalent up to symmetry, False otherwise
        """
        return self.transformationTo(other) is not None

    def __lt__(self, other: Board) -> bool:
        """
        Determines if this board has fewer symbols than the other
        :param other: the Board to compare against
        :return: True if this board has fewer symbols than the other, False otherwise
        """
        return self.sum() < other.sum()

    def __le__(self, other: Board) -> bool:
        """
        Determines if this board doesn't have more symbols than the other
        :param other: the Board to compare against
        :return: True if this board has fewer symbols or the same number of symbols as the other, False otherwise
        """
        return self.sum() <= other.sum()

    def __gt__(self, other: Board) -> bool:
        """
        Determines if this board has more symbols than the other
        :param other: the Board to compare against
        :return: True if this board has more symbols than the other, False otherwise
        """
        return not self <= other

    def __ge__(self, other: Board) -> bool:
        """
        Determines if this board has at least as many symbols as the other
        :param other: the Board to compare against
        :return: True if this board has at least as many symbols as the other, False otherwise
        """
        return not self < other

    def __eq__(self, other: Board) -> bool:
        """
        Compares the two boards to determine if they have the same number of symbols
        :param other: the Board to compare to this one
        :return: True if the boards have the same number of symbols, False otherwise
        """
        return self.sum() == other.sum()

    def __ne__(self, other: Board) -> bool:
        """
        Compares the two boards to determine if they're different in any way, including transformations
        :param other: the Board to compare against
        :return: True if there is any way the boards are different, False otherwise
        """
        return not self == other

    def __copy__(self) -> Board:
        """
        :return: An independent copy of the board
        """
        duplicate = Board(self._size)
        duplicate._grid = self._grid[:]
        return duplicate

    def __repr__(self) -> str:
        """
        :return: the string representation of this Board
        """
        result = []
        for row in range(self._size):
            # add each item in the row going across
            for column in range(self._size):
                result.append(self._grid[column + row * self._size])
            # make the next row on the next line
            result.append("\n")
        return "".join(result)


def printTransformationsOf(b: Board, verbose: bool = False) -> None:
    """
    Prints each of the 8 transformations of the given board to the console
    :param b: the Board to transform.
    :param verbose: If True, prints board states to the console
    """
    original = copy(b)
    b = copy(b)
    # to rotate about the correct point, we need to rotate about ((size - 1) / 2, (size - 1) / 2), since the points
    # go from (0, 0) to (size - 1, size - 1)
    center = ((b.size() - 1) / 2, (b.size() - 1) / 2)
    rotate90 = Rotation(center, 90)
    # check that each of the rotations work
    for i in range(4):
        b.applyTransformation(rotate90)
        assert b.isEquivalentTo(original)
        # print the board if the user asked for it
        if verbose:
            print(b)

    # check each of the reflections
    for i in range(4):
        # since we're reflecting about a line that doesn't go through the coordinates (0, 0), we need to translate
        translateToCenter = Translation(-center[0], -center[1])
        reflection = Reflection(45 * i)
        translateBack = Translation(center[0], center[1])
        totalTransformation = translateBack * reflection * translateToCenter

        b.applyTransformation(totalTransformation)
        assert b.isEquivalentTo(original)
        if verbose:
            print(b)
        # revert the transformation so we can do the next one
        b.applyTransformation(totalTransformation)


def testTransformations(size: int = 3, verbose: bool = False) -> None:
    """
    Tests each of the transformations on the board to ensure they work properly
    :param size: the size of board to test
    :param verbose: whether to print each board to the console for the user to check manually as well; defaults to False
    """
    # check that blank boards work
    b = Board(size)
    if verbose:
        print(b)
    printTransformationsOf(b, verbose)
    # make a second copy 1 move behind to see if it works
    b2 = copy(b)
    lastMove = None
    # fill each cell one at a time and make sure the transformations work
    for row in range(1, size + 1):
        for column in range(1, size + 1):
            pos = column + size * (row - 1)
            if pos % 2 == 0:
                symbol = Move.CROSS
            else:
                symbol = Move.NOUGHT
            m = Move(row, column, symbol)
            b.makeMove(m)
            # make whatever move we made last time on the other board so we can check that boards with a
            # different number of moves are not equivalent
            if lastMove is not None:
                b2.makeMove(lastMove)
            lastMove = m
            assert not b.isEquivalentTo(b2)
            # print the board and each of its transformations
            if verbose:
                print(b)
            printTransformationsOf(b, verbose)


def maximallyAsymmetricTest(size: int = 3, verbose: bool = False) -> None:
    """
    Tests that a board with format (A B C; D E F; G H I) is printed correctly and transformed correctly
    """
    b = Board(size)
    # populate the board with A B C; D E F; G H I for a 3x3
    for row in range(size):
        for column in range(size):
            b.makeMove(Move(row + 1, column + 1, chr(ord("A") + row + size * column)))
    # check each of its transformations
    if verbose:
        print(b)
    printTransformationsOf(b, verbose)


def testWinner(size: int = 3, verbose: bool = False):
    """
    Tests Board.winner to ensure it works properly
    :param size: the size of board to test
    :param verbose: whether to print each board to the console
    """
    # test that it can find a winner in any column
    for column in range(1, size + 1):
        b = Board(size)
        if verbose:
            print(b)
        for row in range(1, size + 1):
            assert not b.isOver()
            assert b.winner() is None
            b.makeMove(Move(row, column, Move.CROSS))
            if verbose:
                print(b)
        if verbose:
            print(b.winner())
        assert b.isOver()
        assert b.winner() == Move.CROSS

    # test that it can find a winner in any row
    for row in range(1, size + 1):
        b = Board(size)
        if verbose:
            print(b)
        for column in range(1, size + 1):
            assert not b.isOver()
            assert b.winner() is None
            b.makeMove(Move(row, column, Move.CROSS))
            if verbose:
                print(b)
        if verbose:
            print(b.winner())
        assert b.isOver()
        assert b.winner() == Move.CROSS

    # test that it can find a winner in any diagonal
    for i in range(2):
        top = ((1, 1), (1, size))[i]
        b = Board(size)
        if verbose:
            print(b)
        for offset in range(size):
            assert not b.isOver()
            assert b.winner() is None
            b.makeMove(Move(top[0] + offset, top[1] + offset * (-1) ** i, Move.CROSS))
            if verbose:
                print(b)
        if verbose:
            print(b.winner())
        assert b.isOver()
        assert b.winner() == Move.CROSS


def main():
    testWinner(5, True)


if __name__ == "__main__":
    main()
