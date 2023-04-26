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
from MENACE import MENACE
from Human import Human
from Game import Game

class Button:
    """
    A simple button class
    """
    _border: Rectangle
    _label: Text

    def __init__(self, center: Point, width: float, height: float, label: str):
        topLeft = Point(center.x - width / 2, center.y - height / 2)
        bottomRight = Point(center.x + width / 2, center.y + height / 2)
        self._border = Rectangle(topLeft, bottomRight)
        self._label = Text(center, label)

    def isClicked(self, click: Point) -> bool:
        return self._border.p1.x <= click.x <= self._border.p2.x and self._border.p1.y <= click.y <= self._border.p2.y

    def draw(self, window: GraphWin) -> None:
        self._border.draw(window)
        self._label.draw(window)

    def undraw(self) -> None:
        self._border.undraw()
        self._label.undraw()

class BoardUI(Board):
    """
    A modified version of the Board that works with a GUI.
    """
    COLUMN_LABELS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ROW_LABELS = [i + 1 for i in range(len(COLUMN_LABELS))]

    _center: Point
    _width: int
    _cells: list[Text]
    _separators: list[Line]
    _labels: list[Text]

    def __init__(self, center: Point, width: int, size: int = 3):
        """
        Creates a Drawable Board with the given parameters
        :param center: where to put the center of the Board
        :param width: how wide and tall to make the board
        :param size: how many cells across the board is; default is 3 for a regular Tic-Tac-Toe board
        """
        self._center = center
        self._width = width
        self._cells = []
        self._separators = []
        self._labels = []
        super().__init__(size)
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
            # create the label for this row
            label = Text(Point(cellCenter.x - cellSpacing, cellCenter.y), BoardUI.ROW_LABELS[rowNumber])
            label.setSize(int(max(min(cellSpacing, 36) - 8, 5)))
            self._labels.append(label)
            # create the cells for this row
            for columnNumber in range(self._size):
                # create the column labels and separator lines for the first row
                if rowNumber == 0:
                    label = Text(Point(cellCenter.x, cellCenter.y - cellSpacing), BoardUI.COLUMN_LABELS[columnNumber])
                    label.setSize(int(max(min(cellSpacing, 36 - 8), 5)))
                    self._labels.append(label)
                    if columnNumber != 0:
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

    def reset(self) -> None:
        super().reset()
        for cell in self._cells:
            cell.setText("")


    def draw(self, win: GraphWin) -> None:
        for cell in self._cells:
            cell.draw(win)
        for separator in self._separators:
            separator.draw(win)
        for label in self._labels:
            label.draw(win)

    def undraw(self) -> None:
        for cell in self._cells:
            cell.undraw()
        for separator in self._separators:
            separator.undraw()
        for label in self._labels:
            label.undraw()

class HumanUI(Human):
    """
    A modified version of the Human class that works with a GUI.
    """
    _window: GraphWin
    _errorMessage: Text

    def __init__(self, window: GraphWin, errorMessage: Text = None, name: str = "", symbol: str = None):
        super().__init__(name, symbol)
        self._window = window
        self._errorMessage = errorMessage

    def _askForMove(self, board: BoardUI) -> Move:
        p = self._window.getMouse()
        self._errorMessage.setText("")
        m = board.moveFromClick(p, self.symbol())
        while m is None:
            p = self._window.getMouse()
            m = board.moveFromClick(p, self.symbol())
        return m

    def _reportIllegalMove(self) -> None:
        self._errorMessage.setText("That move was illegal. Please try again.")

class SwitchButton(Button):
    _labels: list[str]
    _labelIndex: int

    def __init__(self, center: Point, width: int, height: int, labels: list[str]):
        super().__init__(center, width, height, labels[0])
        self._labels = labels
        self._labelIndex = 0

    def processClick(self, click: Point) -> bool:
        clicked = self.isClicked(click)
        if clicked:
            self.advance()
        return clicked

    def getText(self) -> str:
        return self._label.getText()

    def advance(self) -> None:
        self._labelIndex += 1
        self._labelIndex %= len(self._labels)
        self._label.setText(self._labels[self._labelIndex])

class PlayerSelector:
    _name: Entry
    _type: SwitchButton
    _types: list[str] = ["Human", "MENACE"]

    def __init__(self, center: Point) -> None:
        self._name = Entry(Point(center.x - 100, center.y), 20)
        self._name.setText("")
        self._type = SwitchButton(Point(center.x + 100, center.y), 100, 25, PlayerSelector._types)
        self._name.setFill(color_rgb(225, 225, 225))

    def getPlayer(self) -> tuple[str, str]:
        return self._type.getText(), self._name.getText()

    def processClick(self, click: Point) -> None:
        self._type.processClick(click)

    def draw(self, window: GraphWin) -> None:
        self._name.draw(window)
        self._type.draw(window)

    def undraw(self) -> None:
        self._name.undraw()
        self._type.undraw()

class GameUI(Game):
    """
    A modified version of the Game that uses a GUI instead of text
    """
    _window: GraphWin
    _board: BoardUI
    _player1Selector: PlayerSelector
    _player2Selector: PlayerSelector
    _boardSizeEntry: Entry
    _submitButton: Button
    _quitButton: Button
    _playAgain: Button
    _returnToMenu: Button
    _train: SwitchButton

    def __init__(self):
        # call super's init here to make PyCharm happy; it will be called again from startGame
        super().__init__(Player(), Player(), 1)
        self._window = GraphWin("MENACE", 800, 600)
        self._player1Selector = PlayerSelector(Point(400, 250))
        self._player2Selector = PlayerSelector(Point(400, 300))
        self._boardSizeEntry = Entry(Point(400, 350), 5)
        self._boardSizeEntry.setText("3")
        self._boardSizeEntry.setFill(color_rgb(225, 225, 225))
        self._errorMessage = Text(Point(400, 462.5), "")
        self._errorMessage.draw(self._window)
        self._submitButton = Button(Point(400 - 75, 500), 125, 50, "Submit")
        self._quitButton = Button(Point(400 + 75, 500), 125, 50, "Quit")
        self._playAgain = Button(Point(400 - 75, 500), 125, 50, "Play Again")
        self._returnToMenu = Button(Point(400 + 75, 500), 125, 50, "Return to Setup")
        self._train = SwitchButton(Point(400, 550), 150, 25, ["Train", "Press ESC to Stop"])

    def winner(self) -> str:
        winner = self._board.winner()
        if winner == Move.CROSS:
            return f"{self._players[0].name()} won!"
        elif winner is None:
            return "Tie!"
        else:
            return f"{self._players[1].name()} won!"

    def train(self, logfile: str | None = "gameLogs.txt") -> None:
        key = self._window.checkKey()
        while key is None or key != "Escape":
            results = self.playGame(logfile)
            self._errorMessage.setText(self.winner())
            self._teachPlayers(results)
            key = self._window.checkKey()
        self._train.advance()

    def startGames(self, logfile: str | None = "gameLogs.txt"):
        # perform setup for the game
        self._setupGame()
        self._startGame()

        # play the game
        results = super().playGame(logfile)

        # ask if we should play again, train any MENACEs, or return to setup
        self._playAgain.draw(self._window)
        self._returnToMenu.draw(self._window)
        self._train.draw(self._window)
        self._errorMessage.setText(self.winner())
        p = self._window.getMouse()
        while True:
            if self._playAgain.isClicked(p):
                # if we're playing again, make any MENACEs learn from the results
                self._teachPlayers(results)
                # reset the GUI to before the game ended
                self._playAgain.undraw()
                self._returnToMenu.undraw()
                self._train.undraw()
                self._errorMessage.setText("")
                # play another game
                results = super().playGame(logfile)
                # reset the GUI for another game to be over
                self._errorMessage.setText(self.winner())
                self._playAgain.draw(self._window)
                self._returnToMenu.draw(self._window)
                self._train.draw(self._window)

            elif self._returnToMenu.isClicked(p):
                self._playAgain.undraw()
                self._returnToMenu.undraw()
                self._train.undraw()
                self._returnToSetup()
                break

            elif self._train.isClicked(p):
                self._train.processClick(p)
                self._playAgain.undraw()
                self._returnToMenu.undraw()
                self._errorMessage.setText("")
                self.train()
                self._errorMessage.setText(self.winner())
                self._playAgain.draw(self._window)
                self._returnToMenu.draw(self._window)
            p = self._window.getMouse()

        self._teachPlayers(results)
    def _returnToSetup(self) -> None:
        self._board.undraw()
        self._errorMessage.setText("")

    def _teachPlayers(self, results: str | None) -> None:
        if isinstance(self._players[0], MENACE):
            # i'm not sure how to convince PyCharm that players[0] is a MENACE
            player: MENACE = self._players[0]
            player.learn(results)
            player.save(player.name() + ".txt")
        if isinstance(self._players[1], MENACE):
            player: MENACE = self._players[1]
            player.learn(results)
            player.save(player.name() + ".txt")

    def _setupGame(self) -> None:
        """
        Waits for data from the user and ensures that it's valid, or quits the game
        """
        self._window.update()
        nameColumn = Text(Point(300, 200), "Player Name")
        nameColumn.draw(self._window)
        typeColumn = Text(Point(500, 200), "Player Type")
        typeColumn.draw(self._window)
        sizeLabel = Text(Point(300, 350), "Board Size (n by n):")
        sizeLabel.draw(self._window)
        self._player1Selector.draw(self._window)
        self._player2Selector.draw(self._window)
        self._boardSizeEntry.draw(self._window)
        self._submitButton.draw(self._window)
        self._quitButton.draw(self._window)

        while True:
            p = self._window.getMouse()
            while not self._submitButton.isClicked(p) and not self._quitButton.isClicked(p):
                self._player1Selector.processClick(p)
                self._player2Selector.processClick(p)
                p = self._window.getMouse()
            if self._quitButton.isClicked(p):
                self._window.close()
                exit()
            # check that the players' names aren't empty
            player1Name = self._player1Selector.getPlayer()[1]
            player2Name = self._player2Selector.getPlayer()[1]
            if player1Name != "" and player2Name != "":
                boardSize = self._boardSizeEntry.getText()
                # if int(boardSize) doesn't work, restart the loop and try again; otherwise break
                try:
                    if int(boardSize) <= 0:
                        self._errorMessage.setText("Please enter a positive board size.")
                    else:
                        break
                except ValueError:
                    self._errorMessage.setText("Please enter a positive integer board size.")
            elif player1Name == "":
                self._errorMessage.setText("Please enter a name for Player 1.")
            else:
                self._errorMessage.setText("Please enter a name for Player 2.")

        nameColumn.undraw()
        typeColumn.undraw()
        sizeLabel.undraw()
        self._player1Selector.undraw()
        self._player2Selector.undraw()
        self._boardSizeEntry.undraw()
        self._errorMessage.setText("")
        self._submitButton.undraw()
        self._quitButton.undraw()

    def _startGame(self) -> None:
        self._window.update()
        players: list[Player] = []
        for playerType, playerName in (self._player1Selector.getPlayer(), self._player2Selector.getPlayer()):
            if playerType.upper() == "HUMAN":
                players.append(HumanUI(self._window, self._errorMessage, playerName))
            elif playerType.upper() == "MENACE":
                players.append(MENACE.fromFile(playerName + ".txt"))


        boardSize = int(self._boardSizeEntry.getText())
        super().__init__(players[0], players[1], boardSize)
        boardX = self._window.getWidth() / 2
        boardY = self._window.getHeight() / 2
        self._board = BoardUI(Point(boardX, boardY), int(min(boardX, boardY)), boardSize)
        self._board.draw(self._window)
