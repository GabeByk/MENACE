#
# Gabe Byk
# CS481
# TransformableBoard.py
#
from Board import Board

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
        """
        # i tried it with a prop; flipping about the vertical axis and then rotating 90 degrees clockwise n times
        # is the same as flipping about the desired axis
        self.flipVertical()
        self.rotate(n)

def rotate(b: TransformableBoard, n: int):
    b.rotate(n)
    print(b)
    print()

def flip(b: TransformableBoard, n: int):
    b.flip(n)
    print(b)
    print()

def main():
    b = TransformableBoard()
    for y in range(3):
        for x in range(3):
            # board should be 1 2 3 / 4 5 6 / 7 8 9
            b.addMove(f"{3 * y + x + 1}", (x, y))
    rotate(b, 0)

    for i in range(4):
        b.rotateOne()
        print(b)
        print()

    rotate(b, -4)
    rotate(b, -1)
    rotate(b, 1)

    print("Now flipping!\n")

    b.flipVertical()
    print(b)
    print()

    b.flipVertical()
    print(b)
    print()

    for i in range(4):
        flip(b, i)
        flip(b, i)


if __name__ == "__main__":
    main()
