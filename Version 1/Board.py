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
        duplicate = copy(self)
        # with the bottom left at (0, 0) and the top right at (size - 1, size - 1), the center is just their midpoint
        center = ((self._size - 1) / 2, (self._size - 1) / 2)
        # check rotations for equivalence
        for i in range(4):
            rotation = Rotation(center, 90 * i)
            # while the Transformation class has a method for getting the inverse, using it is kind of expensive,
            # so it's better to keep track of it manually where we can
            inverseRotation = Rotation(center, -90 * i)
            # check if the rotation would make the board states equivalent
            duplicate.applyTransformation(rotation)
            if duplicate == other:
                return rotation
            # undo the rotation so we can check the next one
            duplicate.applyTransformation(inverseRotation)

        # check the reflections
        for i in range(4):
            # to reflect about the right line, we need to move the center to (0, 0), then flip, then move back
            translateToCenter = Translation(-center[0], -center[1])
            reflection = Reflection(45 * i)
            translateBack = Translation(center[0], center[1])
            # combine the transformations
            combinedTransformation = translateBack * reflection * translateToCenter
            # apply the transformation
            duplicate.applyTransformation(combinedTransformation)
            # check to see if they're the same
            if duplicate == other:
                return combinedTransformation
            # reflections undo themselves, so we can just apply it again to get to the original state
            duplicate.applyTransformation(combinedTransformation)

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

    def __eq__(self, other: Board) -> bool:
        """
        Compares the two boards to determine if they're exactly the same board state, including rotations and
        reflections
        :param other: the Board to compare to this one
        :return: True if the boards are exactly the same, False otherwise
        """
        return self._grid == other._grid

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

    def winner(self) -> str | None:
        """
        Determines if there is a winner of the game
        :return: Which symbol won (one of Move.NOUGHT or Move.CROSS), or None if there is no winner or there's a draw
        """
        # check for a winner in the rows
        for row in range(self._size):
            winner = self._grid[row]
            won = True
            if winner != Move.BLANK:
                for column in range(1, self._size):
                    won = won and self._grid[row + self._size * column] == winner
                if won:
                    return winner
        # check for a winner in the columns
        for column in range(self._size):
            winner = self._grid[column * self._size]
            won = True
            if winner != Move.BLANK:
                for row in range(1, self._size):
                    won = won and self._grid[row + self._size * column] == winner
                if won:
                    return winner
        # check for a winner in the diagonals
        mainDiagonalWinner = self._grid[0]
        alternateDiagonalWinner = self._grid[2 * self._size]
        mainDiagonalWon = mainDiagonalWinner != Move.BLANK
        alternateDiagonalWon = alternateDiagonalWinner != Move.BLANK
        for i in range(1, self._size):
            mainDiagonalWon = mainDiagonalWon and self._grid[i * (self._size + 1)] == mainDiagonalWinner
            alternateDiagonalWon = alternateDiagonalWon and \
                                   self._grid[2 * self._size - i * (self._size - 1)] == alternateDiagonalWinner
        if mainDiagonalWon:
            return mainDiagonalWinner
        elif alternateDiagonalWon:
            return alternateDiagonalWinner
        # if there was no winner anywhere, there is no winner
        return None

    def isOver(self) -> bool:
        # a drawn game is over
        if Move.BLANK not in self._grid:
            return True
        # if the game isn't drawn, then the game is over if and only if there is a winner
        else:
            return self.winner() is not None

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
    center = (b.size() / 2 - 0.5, b.size() / 2 - 0.5)
    rotate90 = Rotation(center, 90)
    for i in range(4):
        b.applyTransformation(rotate90)
        assert b.isEquivalentTo(original)
        if verbose:
            print(b)

    for i in range(4):
        translateToCenter = Translation(-center[0], -center[1])
        reflection = Reflection(45 * i)
        translateBack = Translation(center[0], center[1])
        totalTransformation = translateBack * reflection * translateToCenter
        b.applyTransformation(totalTransformation)
        assert b.isEquivalentTo(original)
        if verbose:
            print(b)
        b.applyTransformation(totalTransformation)


def testTransformations(size: int = 3, verbose: bool = False):
    b = Board(size)
    if verbose:
        print(b)
    printTransformationsOf(b, verbose)
    b2 = copy(b)
    lastMove = None
    for row in range(1, size + 1):
        for column in range(1, size + 1):
            pos = column + size * (row - 1)
            if pos % 2 == 0:
                symbol = Move.CROSS
            else:
                symbol = Move.NOUGHT
            m = Move(row, column, symbol)
            b.makeMove(m)
            if lastMove is not None:
                b2.makeMove(lastMove)
            lastMove = m
            assert not b.isEquivalentTo(b2)
            if verbose:
                print(b)
            printTransformationsOf(b, verbose)


def maximallyAsymmetricTest(size: int = 3, verbose: bool = False) -> None:
    """
    Tests that a board with format (0, 1, 2; 3, 4, 5; 6, 7, 8) is printed correctly and transformed correctly
    """
    b = Board(size)
    for row in range(size):
        for column in range(size):
            b.makeMove(Move(row + 1, column + 1, chr(ord("A") + row + size * column)))
    if verbose:
        print(b)
    printTransformationsOf(b, verbose)


def testWinner(size: int = 3, verbose: bool = False):
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
    for top in ((1, 1), (1, 3)):
        b = Board(size)
        if verbose:
            print(b)
        for offset in range(3):
            assert not b.isOver()
            assert b.winner() is None
            b.makeMove(Move(top[0] + offset, top[1] + offset * (-1) ** (top[1] // 2), Move.CROSS))
            if verbose:
                print(b)
        if verbose:
            print(b.winner())
        assert b.isOver()
        assert b.winner() == Move.CROSS


def main():
    size = 3
    b = Board(size)
    b.makeMove(Move(3, 1, "X"))
    print(b)
    # testWinner(size, True)


if __name__ == "__main__":
    main()
