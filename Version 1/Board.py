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
        self._grid = [Move.BLANK for i in range(size * size)]

    def size(self) -> int:
        """
        :return: The size of the board n, where the board is n by n.
        """
        return self._size

    def isLegal(self, move: Move) -> bool:
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
        if self.isLegal(move):
            row, column = move.position()
            self._grid[column - 1 + (row - 1) * self._size] = move.symbol()
        else:
            raise IllegalMoveError(f"Move {move} is illegal with game state {self}")

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
        Mutates this board to determine which transformation works, but returns to the original state before returning.
        :param other: the Board that we should get to
        :return: The Transformation that would take us to the Board, or None if no such transformation exists.
        """

        # with (0, 0) at one corner and (2, 2) at the other, the center to apply transformations about is given like so
        center = (self._size / 2 - 0.5, self._size / 2 - 0.5)
        # instead of returning immediately, keep track until we're back to the original state so we won't have changed
        # the board in the comparison
        desiredTransformation = None
        # check rotations for equivalence
        for i in range(4):
            rotation = Rotation(center, 90 * i)
            # the opposite of a rotation is a rotation by the opposite angle
            undo = Rotation(center, -90 * i)
            self.applyTransformation(rotation)
            if self == other:
                desiredTransformation = rotation
            self.applyTransformation(undo)
        # four 90 degree rotations returns us to the starting position, so now we can check if they're the same
        if desiredTransformation is not None:
            return desiredTransformation
        # check the reflections
        for i in range(4):
            # to reflect about the right line, we need to move the center to (0, 0), then flip, then move back
            translateToCenter = Translation(-center[0], -center[1])
            reflection = Reflection(45 * i)
            translateBack = Translation(center[0], center[1])
            # combine the transformations
            combinedTransformation = translateBack * reflection * translateToCenter
            # apply the transformation
            self.applyTransformation(combinedTransformation)
            # check to see if they're the same
            if self == other:
                desiredTransformation = combinedTransformation
            # reflections undo themselves, so we can just apply it again to get to the original state
            self.applyTransformation(combinedTransformation)
            # since we're back at the original state, we can return here
            if desiredTransformation is not None:
                return desiredTransformation
        # if none of the transformations were equivalent, then no transformation exists
        return None

    def isEquivalentTo(self, other: Board) -> bool:
        """
        Determines if these boards are equivalent up to rotations and reflections, i.e. there exists a rotation or
        reflection to get from this board to the other. Mutates this board throughout the method, but returns it to
        the original state before returning.
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

    def __repr__(self) -> str:
        """
        :return: the string representation of this Board
        """
        result = []
        for row in range(self._size):
            for column in range(self._size):
                result.append(self._grid[row + column * self._size])
            result.append("\n")
        return "".join(result)


def printTransformationsOf(b: Board) -> None:
    """
    Prints each of the 8 transformations of the given board to the console
    :param b: the Board to transform. will be mutated throughout, but returned to its original state before the function
    ends.
    """
    original = copy(b)
    # to rotate about the correct point, we need to rotate about ((size - 1) / 2, (size - 1) / 2), since the points
    # go from (0, 0) to (size - 1, size - 1)
    center = (b.size() / 2 - 0.5, b.size() / 2 - 0.5)
    rotate90 = Rotation(center, 90)
    for i in range(4):
        b.applyTransformation(rotate90)
        assert b.isEquivalentTo(original)
        print(b)

    for i in range(4):
        translateToCenter = Translation(-center[0], -center[1])
        reflection = Reflection(45 * i)
        translateBack = Translation(center[0], center[1])
        totalTransformation = translateBack * reflection * translateToCenter
        b.applyTransformation(totalTransformation)
        assert b.isEquivalentTo(original)
        print(b)
        b.applyTransformation(totalTransformation)


def maximallyAsymmetricTest(size: int = 3) -> None:
    """
    Tests that a board with format (0, 1, 2; 3, 4, 5; 6, 7, 8) is printed correctly and transformed correctly
    """
    b = Board(size)
    for row in range(size):
        for column in range(size):
            b.makeMove(Move(row + 1, column + 1, chr(ord("A") + row + size * column)))
    print(b)
    printTransformationsOf(b)


def main():
    size = 3
    b = Board(size)
    print(b)
    printTransformationsOf(b)
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
            print(b)
            printTransformationsOf(b)
    maximallyAsymmetricTest(size)


if __name__ == "__main__":
    main()
