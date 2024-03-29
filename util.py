#
# Gabe Byk
# CS481: Seminar
# 31 October 2022
#

from __future__ import annotations
from math import pi
# heavily referenced https://docs.python.org/3/library/typing.html and various sub-links to better understand
# type annotations for lists, tuples, and sequences
from typing import List, Sequence, TYPE_CHECKING
# learned this syntax from https://adamj.eu/tech/2021/05/13/python-type-hints-how-to-fix-circular-imports/
if TYPE_CHECKING:
    from Matchbox import Matchbox
    from Board import Board


def toRadians(degrees: float) -> float:
    """
    Converts the given angle from degrees to radians
    :param degrees: The angle measure, in degrees
    :return: The angle measure, in radians
    """
    return pi * degrees / 180


class MethodUndefinedError(Exception):
    pass


def raiseMethodUndefinedError(caller: str, method: str):
    """
    Raises a MethodUndefinedError with the following message:
    `Object {caller} tried to call {method}, but {method} is not defined!`
    :param caller: The object that called the undefined method
    :param method: The undefined method that was called
    """
    raise MethodUndefinedError(f"Object {caller} tried to call {method}, but {method} is not defined!")


class InvalidDimensionsError(Exception):
    pass


class IllegalMoveError(Exception):
    pass

class InvalidMoveError(Exception):
    pass

class BinarySearchTree:
    """
    A Binary Search Tree for MENACE to use with Matchboxes and Boards
    """
    # the items in the tree
    _items: List[Matchbox]
    # the sums of the items in the tree
    _sums: List[int]

    def __init__(self):
        self._items = []
        self._sums = []

    def append(self, item: Matchbox) -> None:
        """
        Add the given Matchbox to the tree
        :param item: the Matchbox to add
        """
        if len(self._items) == 0:
            self._items.append(item)
            self._sums.append(item.sum())
        else:
            # insert the item into the first spot where the list would be sorted
            for i in range(len(self._items)):
                if self._items[i] >= item:
                    self._items.insert(i, item)
                    self._sums.insert(i, item.sum())
                    return
            # if we're at this point, it must be larger than any item in the list; it belongs at the end
            self._items.append(item)
            self._sums.append(item.sum())

    def __iter__(self) -> Matchbox:
        for item in self._items:
            yield item

    def find(self, item: Board, symbol: str) -> Matchbox:
        """
        Find the Matchbox for the given Board, or create it if it doesn't exist
        :param item: the Board state to find
        :param symbol: the symbol to put on the box we create if we don't already have it
        :return: the Matchbox corresponding to this board state; automatically creates a new one and adds it if it
        isn't in here
        """
        box = self._recursiveFind(item, 0, len(self._items))
        if box is None:
            from Matchbox import Matchbox
            box = Matchbox(item, symbol)
            self.append(box)
        return box

    def _recursiveFind(self, item: Board, minPos: int, maxPos: int) -> Matchbox | None:
        """
        Tries to find the item in the subset of _items given by the bounds
        :param item: the item to search for
        :param minPos: the smallest bound that we should search
        :param maxPos: the smallest bound we shouldn't search
        :return: the Matchbox that matches Board, or None if no such matchbox exists.
        """
        # if we're trying to search a strip of length 0, it's not in here
        if minPos == maxPos:
            return None
        # if there's only one item, we can find it by hand
        elif minPos + 1 == maxPos:
            if self._items[minPos].holdsBoardState(item):
                return self._items[minPos]
            else:
                return None
        # guess that the item we're looking for is in the middle of the list
        guess = (minPos + maxPos) // 2
        # keep track of how many moves our guess made and how many moves the item made
        boxSum = self._sums[guess]
        boardSum = item.sum()
        # if item made fewer moves, it's somewhere before guess
        if boardSum < boxSum:
            return self._recursiveFind(item, minPos, guess)
        # if item made more moves, it's somewhere after guess
        elif boardSum > boxSum:
            return self._recursiveFind(item, guess, maxPos)
        # if they made the same number of moves, it's somewhere nearby
        else:
            # start from the middle of the section we're given and fan out
            for i in range(round((maxPos - minPos) / 2)):
                # check if we're still in bounds and if we need to look any further right or left
                largerStillEqual = guess + i < maxPos and self._sums[guess + i] == boardSum
                smallerStillEqual = guess - i >= minPos and self._sums[guess - i] == boardSum
                # if neither way is worth looking, we can exit
                if not largerStillEqual and not smallerStillEqual:
                    return None

                # use short circuit evaluation to skip evaluating states we know aren't equal from their sums
                # first pass looks right
                if largerStillEqual and self._items[guess + i].holdsBoardState(item):
                    return self._items[guess + i]

                # second pass looks left
                elif smallerStillEqual and self._items[guess - i].holdsBoardState(item):
                    return self._items[guess - i]


class Matrix:
    """
    A class for implementing Matrices, including addition, scalar multiplication, and matrix multiplication.
    """
    # the values in this matrix such that _matrix[i][j] is the item at row i, column j.
    _matrix = List[List]

    def __init__(self, m: int, n: int):
        """
        Creates an m by n matrix full of 0s.
        :param m: the width (number of columns) of the matrix
        :param n: the height (number of rows) of the matrix
        """
        self._matrix = [[0 for i in range(n)] for j in range(m)]

    def __len__(self) -> int:
        """
        :return: the number of rows in this matrix
        """
        return len(self._matrix)

    # referenced https://docs.python.org/3/reference/datamodel.html#object.__getitem__ for help understanding
    # how __getitem__ works
    def __getitem__(self, rowNumber: int) -> List[int | float]:
        """
        :param rowNumber: the row to retrieve
        :return: row rowNumber, with the first row being row 0
        """
        # make the index error we would get by indexing _matrix look nicer
        if rowNumber >= len(self._matrix):
            raise IndexError(f"Could not interpret {rowNumber} as a row number for matrix with "
                             f"{len(self._matrix)} rows.")
        else:
            return self._matrix[rowNumber]

    def setValue(self, i: int, j: int, value: int | float) -> None:
        """
        Sets the element at row i, column j to the given value
        :param i: the row to put this value
        :param j: the column to put this value
        :param value: the value to set
        """
        self._matrix[i][j] = value

    def setToIdentity(self) -> None:
        """
        Mutates this matrix so it is the identity matrix, if possible
        :raises InvalidDimensionsError: if this matrix is not square
        """
        if len(self) == len(self[0]):
            # the identity matrix of this size is the matrix with 1s along the main diagonal and 0s everywhere else
            for i in range(len(self)):
                for j in range(len(self)):
                    if i == j:
                        self[i][j] = 1
                    else:
                        self[i][j] = 0
        else:
            raise InvalidDimensionsError(f"Cannot set a matrix of size {len(self)} by {len(self[0])} to an identity")

    def getValue(self, i: int, j: int) -> int | float:
        """
        :param i: the row of the value to get
        :param j: the column of the value to get
        :return: the value at row i, column j
        """
        return self._matrix[i][j]

    def setValues(self, values: Sequence[Sequence[int | float]] | Matrix) -> None:
        """
        Sets the given values to this matrix.
        :raises InvalidDimensionsError: if values is not the same size as this Matrix.
        :param values: a 2d array of integers or floats to store in this Matrix
        """
        # set this matrix if they're the same dimensions
        if len(values) == len(self) and len(values[0]) == len(self[0]):
            for row in range(len(self)):
                for column in range(len(self[0])):
                    self[row][column] = values[row][column]
        # otherwise raise an InvalidDimensionsError
        else:
            raise InvalidDimensionsError(f"Cannot assign an array of size {len(values)} by {len(values[0])} to a "
                                         f"matrix of size {len(self)} by {len(self[0])}")

    def __add__(self, other: Matrix) -> Matrix:
        """
        Computes and returns the sum of self and the given matrix.
        :param other: The matrix to add to this one
        :raises InvalidDimensionsError: when self and other are not the same dimensions.
        :return: The sum of these matrices
        """
        # the sum of two matrices of different dimensions is undefined
        if len(other) != len(self) or len(other[0]) != len(self[0]):
            raise InvalidDimensionsError(f"Cannot add a matrix of size {len(other)} by {len(other[0])} to a matrix "
                                         f"of size {len(self)} by {len(other[0])}")
        else:
            # the sum of two matrices is just the sum of each component
            result = Matrix(len(self), len(self[0]))
            for row in range(len(self)):
                for column in range(len(self[0])):
                    result[row][column] = self[row][column] + other[row][column]
            return result

    def __mul__(self, other: int | float | Matrix) -> Matrix:
        """
        Computes and returns the product of this matrix and the given float or matrix. Performs scalar multiplication
        if other is an int or float and matrix multiplication if other is a Matrix.
        If a matrix product, computes self * other.
        :param other: the scalar or matrix to multiply this matrix by
        :raises InvalidDimensionsError: if self is an m by n matrix and other is not an n by r matrix; in other words,
        if the matrix product of the two matrices is undefined
        :return: the scalar or matrix product of self and other
        """
        # do scalar multiplication for ints and floats
        if isinstance(other, (int, float)):
            result = Matrix(len(self), len(self[0]))
            # the scalar product of a matrix and a scalar is each cell multiplied by the scalar
            for row in range(len(self)):
                for column in range(len(self[0])):
                    result[row][column] = self[row][column] * other
            return result
        # do matrix multiplication for matrices
        elif isinstance(other, Matrix):
            # check that multiplication is defined for these matrices
            if len(other) != len(self[0]):
                raise InvalidDimensionsError(f"Matrix multiplication is undefined for a matrix of size {len(self)} by "
                                             f"{len(self[0])} and a matrix of size {len(other)} by {len(other[0])}")
            else:
                # the matrix product C of A and B where C = A * B has the property that C_ij is the dot product of
                # row i in matrix A with column j in matrix B

                # if A is an m x n matrix and B is an n x r matrix, then C is an m x r matrix
                result = Matrix(len(self), len(other[0]))
                # iterate over the rows and columns in the result matrix
                for row in range(len(result)):
                    for column in range(len(result[0])):
                        # compute the dot product of the appropriate row and column
                        total = 0
                        for pos in range(len(self[0])):
                            total += self[row][pos] * other[pos][column]
                        # store the dot product in the appropriate cell
                        result[row][column] = total
                return result

    def __eq__(self, other: Matrix) -> bool:
        """
        :param other: The Matrix to compare to
        :return: True if the matrices are equal (up to floating point error), False otherwise
        """
        threshold = 10 ** -3
        if len(self) != len(other) or len(self[0]) != len(other[0]):
            return False
        else:
            equivalent = True
            for i in range(len(self)):
                for j in range(len(self[0])):
                    equivalent = equivalent and abs(self[i][j] - other[i][j]) < threshold
                    if not equivalent:
                        return False
        return True

    def __repr__(self) -> str:
        """
        :return: The string representation of a list of the rows of the matrix, with each row in brackets and separated
        by commas.
        """
        return str(self._matrix)

    def determinant(self) -> float | None:
        """
        Calculates and returns the determinant of this matrix
        NOTE: Currently only works for 2x2 and 3x3 matrices
        :return: The determinant of the matrix, or None if the determinant does not exist
        :raises InvalidDimensionsError: if the matrix is not 2x2 or 3x3
        """
        if len(self) == len(self[0]):
            if len(self) == 2:
                return self[0][0] * self[1][1] - self[1][0] * self[0][1]
            elif len(self) == 3:
                # referenced https://www.youtube.com/watch?v=v4MenooI1J0 (Khan Academy) for the shortcut method
                mainDiagonals = self[0][0] * self[1][1] * self[2][2] + \
                                self[0][1] * self[1][2] * self[2][0] + \
                                self[0][2] * self[1][0] * self[2][1]
                alternateDiagonals = self[0][0] * self[1][2] * self[2][1] + \
                                     self[0][1] * self[1][0] * self[2][2] + \
                                     self[0][2] * self[1][1] * self[2][0]
                return mainDiagonals - alternateDiagonals
            else:
                raise InvalidDimensionsError(f"Currently only the determinant of 2x2 and 3x3 matrices are supported")
        else:
            return None

    def transposed(self) -> Matrix:
        """
        Computes and returns the transpose of this matrix, i.e. the matrix with its rows and columns swapped compared
        to this one
        :return: The Transpose of this matrix
        """
        transpose = Matrix(len(self), len(self[0]))
        for i in range(len(self)):
            for j in range(len(self[0])):
                transpose[i][j] = self[j][i]
        return transpose

    def transpose(self) -> None:
        """
        Switches this matrix's rows and columns
        """
        self._matrix = self.transposed()._matrix


def testMatrices():
    v1 = ((1, 2, 3), (4, 5, 6))
    v2 = ((1, 2), (3, 4), (5, 6))
    m1 = Matrix(2, 3)
    m2 = Matrix(3, 2)
    m1.setValues(v1)
    m2.setValues(v2)
    print(m1)
    print(m2)
    print(m1 + m1)
    print(m2 + m2)
    print(m1 * m2)
    print(m2 * m1)
    print(m1 * 1)
    print(m1 * 2)
    print(m2 * 1)
    print(m2 * 2)


if __name__ == "__main__":
    testMatrices()
