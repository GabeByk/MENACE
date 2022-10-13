#
# Gabe Byk
# CS481
# TransformableBoard.py
#
from __future__ import annotations
from Board import Board
from typing import Tuple
from copy import copy, deepcopy

class TransformableBoard(Board):

    def rotateOne(self) -> None:
        """
        Rotates the board 90 degrees clockwise
        """
        # rotate corners
        r0c0 = self._state[0][0]
        # R2C0 ends up in R0C0 after a rotation
        self._state[0][0] = self._state[2][0]
        # R2C2 ends up in R2C0
        self._state[2][0] = self._state[2][2]
        # R0C2 ends up in R2C2
        self._state[2][2] = self._state[0][2]
        # R0C0 ends up in R0C2
        self._state[0][2] = r0c0

        # rotate edges
        r0c1 = self._state[0][1]
        # R1C0 ends up in R0C1
        self._state[0][1] = self._state[1][0]
        # R2C1 ends up in R1C0
        self._state[1][0] = self._state[2][1]
        # R1C2 ends up in R2C1
        self._state[2][1] = self._state[1][2]
        # R0C1 ends up in R1C2
        self._state[1][2] = r0c1

        # center stays in place, so we're done

    def rotate(self, n: int = 1) -> None:
        """
        Rotates the board clockwise 90 * n degrees; negative numbers rotate counter-clockwise
        :param n: the number of times to rotate 90 degrees clockwise
            NOTE: rotate(i) and rotate(-i) cancel
        """
        for i in range(n % 4):
            self.rotateOne()

    def flipVertical(self) -> None:
        """
        Flips the board about the vertical axis
        """
        # swap the first and last columns, as requested
        for i in range(3):
            self._state[i][0], self._state[i][2] = self._state[i][2], self._state[i][0]

    def flip(self, n: int = 0) -> None:
        """
        Flips the board about the specified axis

        :param n: the number of times to rotate 45 degrees clockwise starting from vertical
            i.e. 0 is the vertical axis (|), 1 is the "positive" diagonal (/), 2 is horizontal (-),
            3 is the other diagonal (\). You can also think of n as the index of "|/-\".
            NOTE: flip(i) and flip(-i) don't always cancel; flip(1) is / and flip(-1) is \;
            they don't cancel. To cancel, flip(i) twice.
        """
        # i tried it with a prop; flipping about the vertical axis and then rotating 90 degrees clockwise n times
        # is the same as flipping about the desired axis
        self.flipVertical()
        self.rotate(n)

    def __eq__(self, other: TransformableBoard) -> bool:
        """
        Two TransformableBoards are considered equivalent if they are equivalent up to symmetry;
        for example, a board with a single O in any corner is considered equivalent to any other board with
        one O in any other corner.
        :param other: the TransformableBoard to compare against
        :return: True if the two TransformableBoards are equivalent up to symmetry, False otherwise
        """
        # compare self against the transformations of other
        equivalent = False
        for i in range(4):
            # test rotation of i
            other.rotate(i)
            equivalent = equivalent or self._state == other._state
            # restore other to its previous state
            other.rotate(-i)
            if equivalent:
                return True
            # test flip of i
            other.flip(i)
            equivalent = equivalent or self._state == other._state
            # return other to its previous state
            other.flip(i)
            if equivalent:
                return True

    def __copy__(self) -> TransformableBoard:
        b = TransformableBoard()
        b._state = deepcopy(self._state)
        return b

    def movesAreEquivalent(self, symbol: str, move1: Tuple[int, int], move2: Tuple[int, int]) -> bool:
        """
        Determines if the two given moves are equivalent up to symmetry
        :param symbol: the symbol to make the move with
        :param move1: the first (x, y) move to consider
        :param move2: the second (x, y) move to consider
        :return: True if the two moves are equivalent on this board, False otherwise
        """
        # make copies of the current board state so we don't change self
        b1 = copy(self)
        b2 = copy(self)
        # add the moves to the copies
        b1.addMove(symbol, move1)
        b2.addMove(symbol, move2)
        # check if the copies are equivalent up to symmetry
        return b1 == b2

    def exactlyEquals(self, other: TransformableBoard) -> bool:
        return self._state == other._state

    def matchesLabel(self, label: str) -> bool:
        other = TransformableBoard(label)
        return self == other

    def matchLabel(self, label: str) -> None:
        """
        Transforms the board to match the given label, if possible
        :param label: the compactStr of a Board
        """
        # create a board from the given board
        b = TransformableBoard(label)
        # if they're equivalent under symmetry, just take the new state
        if self == b:
            self._state = b._state


def rotate(b: TransformableBoard, n: int):
    b.rotate(n)
    print(b)
    print()

def flip(b: TransformableBoard, n: int):
    b.flip(n)
    print(b)
    print()

def main():
    b1 = TransformableBoard()
    b2 = TransformableBoard()
    b3 = TransformableBoard()
    # all empty boards are equivalent
    assert b1 == b2
    assert b2 == b1
    assert b3 == b1
    assert b1 == b3
    assert b2 == b3
    assert b3 == b1
    print(b1, b2, b3, sep="\n")
    for y in range(3):
        for x in range(3):
            # board should be 1 2 3 / 4 5 6 / 7 8 9
            num = 3 * y + x + 1
            # no matter what transformations we do, b1 and b2 are equal
            b1.addMove(f"{num}", (x, y))
            b2.addMove(f"{num}", (x, y))
            # since we moved the center, no transformation will make b1 or b2 equal b3
            b3.addMove(f"{num}", ((x + 1) % 3, (y + 1) % 3))

    # test rotations
    print("Now rotating!\n")
    rotate(b1, 0)

    for i in range(4):
        b1.rotateOne()
        print(b1)
        print()

    rotate(b1, -4)
    rotate(b1, -1)
    rotate(b1, 1)

    print("Now flipping!\n")

    b1.flipVertical()
    print(b1)
    print()

    b1.flipVertical()
    print(b1)
    print()

    for i in range(4):
        flip(b1, i)
        flip(b1, i)

    print("Testing equality!")
    for i in range(4):
        b2.rotateOne()
        b3.rotateOne()
        # test equality
        assert b1 == b2
        assert b2 == b1
        # test inequality
        assert b2 != b3
        assert b3 != b2
        assert b1 != b3
        assert b3 != b1
    for i in range(4):
        b2.flip(i)
        b3.flip(i)
        # test equality
        assert b1 == b2
        assert b2 == b1
        # test inequality
        assert b2 != b3
        assert b3 != b2
        assert b1 != b3
        assert b3 != b1
        b2.flip(i)
        b3.flip(i)


if __name__ == "__main__":
    main()
