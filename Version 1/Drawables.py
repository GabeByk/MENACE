#
# Gabe Byk
# Drawables.py
# 21 February 2023
#

from __future__ import annotations
from graphics import *
from Move import Move
from Board import Board
from Player import Player
from Human import Human
from Game import Game

class BoardUI(Board):
    """
    A modified version of the Board that works with a GUI.
    """
    _center: Point
    _width: int
    _cells: list[Text]
    _separators: list[Line]

    def __init__(self, center: Point, width: int, size: int = 3):
        """
        Creates a Drawable Board with the given parameters
        :param center: where to put the center of the Board
        :param width: how wide and tall to make the board
        :param size: how many cells across the board is; default is 3 for a regular Tic-Tac-Toe board
        """
        super().__init__(size)
        self._center = center
        self._width = width
        self._cells = []
        self._separators = []
        self._generateUI()

    def _generateUI(self) -> None:
        # how much space is between cells
        cellSpacing = self._width / self._size
        # where the center of the top left cell is
        initialCenter = (self._center.x - self._width / 2 + cellSpacing / 2,
                         self._center.y - self._width / 2 + cellSpacing / 2)
        # the center of the next cell to create
        cellCenter = Point(initialCenter[0], initialCenter[1])
        # create the cells
        for rowNumber in range(self._size):
            for columnNumber in range(self._size):
                # create the vertical separator line during the first row
                if columnNumber != 0 and rowNumber == 0:
                    separator = Line(Point(cellCenter.x - cellSpacing / 2, self._center.y - self._width / 2),
                                     Point(cellCenter.x - cellSpacing / 2, self._center.y + self._width / 2))
                    self._separators.append(separator)
                # create the symbol
                symbol = self._grid[columnNumber + self._size * rowNumber]
                if symbol == "_":
                    symbol = ""
                cell = Text(cellCenter, symbol)
                # make sure the text is a reasonable size on the screen
                cell.setSize(int(max(min(cellSpacing, 36), 5)))
                self._cells.append(cell)
                cellCenter.move(cellSpacing, 0)
            # create the horizontal separator line
            if rowNumber != 0:
                separator = Line(Point(self._center.x - self._width / 2, cellCenter.y - cellSpacing / 2),
                                 Point(self._center.x + self._width / 2, cellCenter.y - cellSpacing / 2))
                self._separators.append(separator)
            cellCenter.move(-self._size * cellSpacing, cellSpacing)

    def makeMove(self, move: Move) -> None:
        super().makeMove(move)
        row, column = move.position()
        self._cells[column + self._size * row].setText(move.symbol())

    def _swap(self, pos1: int, pos2: int) -> None:
        super()._swap(pos1, pos2)
        self._cells[pos1], self._cells[pos2] = self._cells[pos2], self._cells[pos1]


    def moveFromClick(self, click: Point, symbol: str) -> Move | None:
        # how much space is between cells
        cellSpacing = self._width / self._size
        # the corner of the board with minimal x and y coordinates
        topLeft = self._center.clone()
        topLeft.move(-self._width / 2, -self._width / 2)
        # how many cells over from the left we are
        column = (click.getX() - topLeft.getX()) // cellSpacing
        # how many cells down from the top we are
        row = (click.getY() - topLeft.getY()) // cellSpacing
        # if the move is on the board, return it
        if 0 <= row < self._size and 0 <= column < self._size:
            return Move(int(row), int(column), symbol)
        # otherwise, there is no move in that position
        else:
            return None


    def draw(self, win: GraphWin) -> None:
        for separator in self._separators:
            separator.draw(win)
        for cell in self._cells:
            cell.draw(win)

    def undraw(self) -> None:
        for separator in self._separators:
            separator.undraw()
        for cell in self._cells:
            cell.undraw()

class HumanUI(Human):
    """
    A modified version of the Human class that works with a GUI.
    """
    _window: GraphWin

    def __init__(self, window: GraphWin, name: str = "", symbol: str = None):
        super().__init__(name, symbol)
        self._window = window

    def _askForMove(self, board: BoardUI) -> Move:
        p = self._window.getMouse()
        m = board.moveFromClick(p, self.symbol())
        while m is None:
            print("Please click on the board.")
            p = self._window.getMouse()
            m = board.moveFromClick(p, self.symbol())
        print(m)
        return m

    def _reportIllegalMove(self) -> None:
        print("Sorry, that move was illegal. Try somewhere else.")

class GameUI(Game):
    """
    A modified version of the Game that uses a GUI instead of text
    """
    _window: GraphWin
    _board: BoardUI

    def __init__(self, player1: Player, player2: Player, window: GraphWin, boardSize: int = 3):
        super().__init__(player1, player2, boardSize)
        self._window = window
        boardX = window.getWidth() / 2
        boardY = window.getHeight() / 2
        self._board = BoardUI(Point(boardX, boardY), int(min(boardX, boardY)), boardSize)
        self._board.draw(window)

def main():
    win = GraphWin("board test", 800, 600)
    print("creating game")
    p1 = HumanUI(win, "Gabe 1")
    p2 = HumanUI(win, "Gabe 2")
    game = GameUI(p1, p2, win, 3)
    print("making move")
    game.playGame(logfile=None)
    win.getMouse()
    win.close()


if __name__ == "__main__":
    main()
