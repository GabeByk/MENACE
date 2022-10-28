#
# Gabe Byk
# CS481: Seminar
# 27 October 2022
#

from __future__ import annotations
from typing import Tuple, Sequence
from math import sin, cos, pi
from Matrix import Matrix
# used only for testing purposes
from graphics import GraphWin, Point, Circle, color_rgb, Text

def toRadians(degrees: float) -> float:
    """
    Converts the given angle from degrees to radians
    :param degrees: The angle measure, in degrees
    :return: The angle measure, in radians
    """
    return pi * degrees / 180

class Transformation:
    """
    An interface used to contain all necessary information to tell an object how it should be transformed
    (rotation by x degrees, flip about some axis, etc). Not useful for applying transformations other than the identity.
    """
    # the matrix to use to apply the transformation
    _matrix: Matrix

    def __init__(self, matrix: Matrix = None):
        """
        :param matrix: The matrix to use with this transformation; if not provided, defaults to the identity.
        """
        self._matrix = Matrix(3, 3)

        if matrix is not None:
            self._matrix.setValues(matrix)
        else:
            self._matrix.setToIdentity()

    def transformationMatrix(self) -> Matrix:
        """
        :return: The 3x3 matrix that carries out this transformation
        """
        duplicate = Matrix(3, 3)
        duplicate.setValues(self._matrix)
        return duplicate

    def transformedPoint(self, position: Tuple[float, float]) -> Tuple[float, float]:
        """
        Applies the transformation to the given x, y values in the plane.
        :param position: the x, y value to transform
        :return: the transformed x, y values
        """
        # create a matrix for the given position
        point = Matrix(3, 1)
        point[0][0], point[1][0] = position
        point[2][0] = 1
        # transform the point to its image
        image = self._matrix * point
        # scale the image so its third value is 1
        image = image * (1 / image[2][0])
        # return the x, y values of the image
        return image[0][0], image[1][0]

    def __mul__(self, other: Transformation) -> Transformation:
        """
        Composes the two transformations in the given order and returns their result.
        :param other: The Transformation to apply before applying this one
        :return: The combined Transformation that results in both actions being applied
        """
        return Transformation(self._matrix * other._matrix)

    def __repr__(self) -> str:
        """
        :return: the string representation of this Transformation's matrix
        """
        return str(self.transformationMatrix())

class Translation(Transformation):

    def __init__(self, dx: float, dy: float):
        """
        Moves the plane by dx in the positive x direction and dy in the positive y direction.
        :param dx: The number of units to move right, with negative moving left
        :param dy: The number of units to move up, with negative moving down
        """
        super().__init__()
        self._matrix[0][2] = dx
        self._matrix[1][2] = dy

class Rotation(Transformation):

    def __init__(self, center: Tuple[float, float], degrees: float):
        """
        Rotates the plane about the point center by degrees.
        :param center: The point to rotate about
        :param degrees: The number of degrees to rotate clockwise
        """
        super().__init__()
        # compute the sin and cos of the given angle so we don't have to do it later
        s = sin(-toRadians(degrees))
        c = cos(-toRadians(degrees))

        # set up the matrix for rotating about (0, 0)
        pureRotation = Matrix(3, 3)
        pureRotation.setToIdentity()
        pureRotation[0][0] = c
        pureRotation[0][1] = -s
        pureRotation[1][0] = s
        pureRotation[1][1] = c

        # assign the proper transformation
        if center != (0, 0):
            # to rotate about center, we need three steps (matrix multiplication makes it so transformations are applied
            # in reverse order to how they're written):
            self._matrix = (
                    # Step 3: Move the center back to where it started
                    Translation(center[0], center[1]) *
                    # Step 2: Rotate about (0, 0)
                    Transformation(pureRotation) *
                    # Step 1: Move the center to (0, 0)
                    Translation(-center[0], -center[1])
                            ).transformationMatrix()
        else:
            # if the center is (0, 0), we can just rotate about it without translating
            self._matrix = pureRotation

class Scale(Transformation):

    def __init__(self, xScale: float, yScale: float):
        """
        Stretches the plane by a factor of xScale along the x-axis and a factor of yScale along the y-axis.
        :param xScale: The amount to scale by in the x direction, with negative flipping about the y-axis
        :param yScale: The amount to scale by in the y direction, with negative flipping about the x-axis
        """
        super().__init__()
        self._matrix[0][0] = xScale
        self._matrix[1][1] = yScale

class Reflection(Transformation):

    def __init__(self, degrees: float):
        """
        Reflects the plane about a line rotated the given number of degrees clockwise, starting from the y-axis.
        :param degrees: The amount in degrees to rotate the axis clockwise
        """
        super().__init__()
        # -degrees rotates to y-axis
        rotateToAxis = Rotation((0, 0), -degrees)
        # this scale flips about the y-axis
        flipAboutAxis = Scale(-1, 1)
        # +degrees rotates back to where it was
        rotateToStart = Rotation((0, 0), degrees)
        self._matrix = (rotateToStart * flipAboutAxis * rotateToAxis).transformationMatrix()

# code from here on out is to test the transformations

def drawPoints(points: Sequence[tuple[float | int, float | int]], transformation: Transformation, win: GraphWin)\
        -> list[Circle]:
    drawnPoints = []
    for x, y in points:
        transformedPoint = transformation.transformedPoint((x, y))
        p = Circle(Point(transformedPoint[0], transformedPoint[1]), 0.1)
        # going along the x-axis makes it redder and along the y-axis makes it bluer
        p.setFill(color_rgb(int((x + 2) * 255 / 5), 0, int((y + 2) * 255 / 5)))
        p.draw(win)
        drawnPoints.append(p)
        # draw text for the corners
        p = p.getCenter().clone()
        p.move(0, 0.3)
        t = None
        if x == -2:
            if y == -2:
                t = Text(p, "(0, 0)")
            elif y == 2:
                t = Text(p, "(0, 1)")
        elif x == 2:
            if y == -2:
                t = Text(p, "(1, 0)")
            elif y == 2:
                t = Text(p, "(1, 1)")
        if t is not None:
            t.draw(win)
            drawnPoints.append(t)

    return drawnPoints

def main():
    win = GraphWin("Transformation Testing", 600, 600)
    win.setCoords(-5, -5, 5, 5)
    # make points for a square of width 5 from (-2, -2) to (2, 2)
    points = []
    for x in range(-2, 3):
        for y in range(-2, 3):
            points.append((x, y))
    points = tuple(points)
    # test that doing nothing works
    print("identity:", Transformation())
    toUndraw = drawPoints(points, Transformation(), win)

    # transformations and text that describes what they should do
    transformations = (Translation(0, 0), Rotation((0, 0), 0), Scale(1, 1),
                       Translation(1, 0), Rotation((0, 0), 90), Scale(2, 1), Reflection(0),
                       Translation(0, 1), Rotation((1, 1), -90), Scale(1, -2), Reflection(45),
                       Rotation((0, 0), 180), Reflection(90), Reflection(135))
    labels = ("translate by 0", "rotate by 0", "scale by 1",

              "translate 1 right", "rotate 90 clockwise", "scale 2x wider", "flip about y axis",

              "translate 1 up", "rotate about (1, 1) 90 degrees counterclockwise", "flip about x and scale by 2",
              "reflect about diagonal with positive slope",

              "rotate 180 degrees", "reflect about x axis", "reflect about diagonal with negative slope")
    # apply each transformation and tell the user what it should do
    for i in range(len(transformations)):
        transformation = transformations[i]
        label = labels[i]
        win.getMouse()
        print(f"{label}: {transformation}")
        # undraw what we drew last time and draw the new points
        for point in toUndraw:
            point.undraw()
        toUndraw = drawPoints(points, transformation, win)

    win.getMouse()
    win.close()


if __name__ == "__main__":
    main()
