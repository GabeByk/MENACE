#
# Gabe Byk
# CS481: Seminar
# 7 February 2023
#

from __future__ import annotations
from random import randrange
from copy import copy
from typing import List, Tuple


class Move:
    # class variables that determine the character to be used for O, X, and nothing
    NOUGHT = "O"
    CROSS = "X"
    BLANK = "_"
    # this Move is made in row _row, column _column of a Board
    _row: int
    _column: int
    # the symbol of the move to make: one of Board.X or Board.O
    _symbol: str

    def __init__(self, row: int, column: int, symbol: str):
        """
        Creates a Move
        :param row: the row number of the move, with the top being row 1 and increasing by 1 for each row down
        :param column: the column of the move, with the left being column 1 and increasing by 1 for each column right
        :param symbol: the symbol of the player that made this move; should be one of Move.NOUGHT or Move.CROSS
        """
        self._row = row
        self._column = column
        self._symbol = symbol

    def position(self) -> Tuple[int, int]:
        """
        :return: the row and column of where the move is on the board
        """
        return self._row, self._column

    def symbol(self) -> str:
        """
        :return: the symbol for this move
        """
        return self._symbol

    def __repr__(self) -> str:
        """
        :return: A string of the format '(row, column): symbol'
        """
        return f"{self.position()}: {self.symbol()}"

class Player:
    """
    An interface for interacting with a Tic-Tac-Toe game. To use, create a class that inherits from this, and implement
    makeMove. You may override any of the other methods to your liking, but you must override makeMove.
    """
    # The symbol this Player will play: one of Board.CROSS or Board.NOUGHT
    _symbol: str
    # The name assigned to this Player
    _name: str

    def makeMove(self, board: Board) -> None:
        """
        Determines the Move this Player wants to make, then makes it on the given Board.
        :raises MethodUndefinedError: if not overridden by a subclass
        :param board: the Board to make a move on
        """
        raiseMethodUndefinedError(str(self), "makeMove")

    def __init__(self, name: str = "", symbol: str = None):
        """
        :param name: The name to give this Player. Defaults to "" if not provided.
        :param symbol: The symbol this Player will play with, usually one of Move.NOUGHT or Move.CROSS. If not provided,
        one can be set later using setSymbol.
        """
        self._name = name
        self._symbol = symbol

    def setSymbol(self, symbol: str):
        """
        Mutates this Player so it will use the given symbol.
        :param symbol:
        """
        self._symbol = symbol

    def symbol(self) -> str:
        """
        :return: The symbol this player uses
        """
        return self._symbol

    def name(self) -> str:
        """
        :return: This Player's name
        """
        return self._name

    def __repr__(self) -> str:
        """
        If this player has a name, then this method returns the name, followed by a : and a space, then the symbol
        this player plays as. Otherwise, just returns the symbol this player plays as.
        :return: The string representation of this Player, as described above.
        """
        if len(self.name()) > 0:
            return f"{self.name()}: {self.symbol()}"
        else:
            return self.symbol()

def menaceVsMenace(iterations, menace1File: str | None = None, menace2File: str | None = None, size: int = 3) -> None:
    if menace1File is not None:
        try:
            m1 = MENACE.fromFile(menace1File)
        except FileNotFoundError:
            m1 = MENACE(menace1File[:-4])
    else:
        m1 = MENACE("Menace 1")
    if menace2File is not None:
        try:
            m2 = MENACE.fromFile(menace2File)
        except FileNotFoundError:
            m2 = MENACE(menace2File[:-4])
    else:
        m2 = MENACE("Menace 2")
    g = Game(m1, m2, size)
    for i in range(iterations):
        winner = g.playGame(gameLogs)
        m1.learn(winner)
        m2.learn(winner)
    if menace1File is not None:
        m1.save(menace1File)
    if menace2File is not None:
        m2.save(menace2File)


def humanVsHuman() -> None:
    h1 = Human("Gabe")
    h2 = Human("Gabe")
    g = Game(h1, h2)
    g.playGame(gameLogs)


def humanVsMenace(player1: Player, player2: Player) -> None:
    g = Game(player1, player2)
    g.playGame(gameLogs)
    if isinstance(player1, MENACE):
        player1.save("MENACE First vs Human.txt")
    if isinstance(player2, MENACE):
        player2.save("MENACE Second vs Human.txt")


def readLogs(filename: str = "gameLogs.txt"):
    with open(filename, "r") as infile:
        wins = dict()
        draws = 0
        for line in infile:
            if " won playing " in line and " turns!" in line:
                player = line.split(" won playing ")[0]
                if player in wins:
                    wins[player] += 1
                else:
                    wins[player] = 1
            elif "Draw in " in line and " turns!" in line:
                draws += 1
    for player in wins.keys():
        print(f"{player} won {wins[player]} times")
    print(f"There were {draws} draws")


gameLogs = "5x5 test.txt"

def main():
    # readLogs(gameLogs)
    size = 3
    # humanVsHuman()
    rounds = 500

    menaceVsMenace(rounds, f"Menace 1.txt", f"Menace 2.txt", size)
    # menaceVsMenace(rounds, size=size)
    # human = Human("Gabe")
    # menace = MENACE.fromFile("Menace 2.txt")
    # humanVsMenace(human, menace)
    # readLogs(gameLogs)

class Matchbox:
    """
    A helper class for MENACE that contains a Board state and the Moves that could be made on that Board.
    """
    # Class variable: the number of beads each legal move gets to start with
    BEADS: int = 3
    # Class variable: the number of beads to add on a win
    winAdjustment: int = 3
    # Class variable: the number of beads to add on a draw
    drawAdjustment: int = 1
    # Class variable: the number of beads to add on a loss (negative to remove beads rather than add them)
    lossAdjustment: int = -1

    # the state that this matchbox represents
    _board: Board
    # the symbol this matchbox will play; one of Move.NOUGHT or Move.CROSS
    _symbol: str
    # each legal move and the beads remaining
    _moves: dict[Move: int]

    def __init__(self, board: Board, symbol: str, generateMoves: bool = True):
        """
        Creates a matchbox for the given board
        :param board: The Board to put on this matchbox
        :param symbol: The move MENACE will make on this board; one of Move.NOUGHT or Move.CROSS
        :param generateMoves: Whether to initialize the legal moves that can be made on this board; defaults to True
                              Only set to False if you're going to initialize it manually
        """
        self._board = copy(board)
        self._symbol = symbol
        self._moves = dict()
        if generateMoves:
            self._generateLegalMoves()

    # referenced https://realpython.com/python-multiple-constructors for this syntax
    @classmethod
    def fromString(cls, representation: str) -> Matchbox:
        """
        Constructs and returns a Matchbox from a string formatted as the result of str()
        :param representation: a string of the same format as str(Matchbox)
        :return: the Matchbox that is created
        """
        boardString, symbol, movesString = representation.strip().split("; ")
        # set up the board correctly
        board = Board(int(len(boardString) ** 0.5))
        for position in range(len(boardString)):
            moveSymbol = boardString[position]
            row = position // board.size() + 1
            column = position % board.size() + 1
            board.makeMove(Move(row, column, moveSymbol))
        # at this point we have enough information to make the matchbox
        box = cls(board, symbol, generateMoves=False)
        # reconstruct _moves
        # remove the outer curly brackets
        movesString = movesString.lstrip("{").rstrip("}")
        # split each entry of the dictionary
        moves = movesString.split(", (")
        # get rid of the first ( so they're uniform
        moves[0] = moves[0].lstrip("(")
        for i in range(len(moves)):
            # each entry at this point is formatted row, column): symbol: beads
            # splitting on : separates into move, symbol, beads
            moveString, moveSymbol, beads = moves[i].split(": ")
            # get rid of the ) so we can extract the row and column
            moveString = moveString.rstrip(")")
            # split up the row and column, and convert to an integer
            row, column = moveString.split(", ")
            row, column = int(row), int(column)
            # create the move and add it to _moves
            move = Move(row, column, moveSymbol)
            box._moves[move] = int(beads)
        # since this is a class method, we need to return the box we constructed
        return box

    @profile
    def makeMove(self, board: Board) -> Move:
        """
        Makes a random move on the given board, with the weights of each option dictated by the beads for each move
        :param board: the Board to make a move on
        """
        # create a list of moves where moves with multiple beads are included multiple times
        weightedMoves = []
        for move in self._moves.keys():
            # add a copy of the move for each of its beads
            for i in range(self._moves[move]):
                weightedMoves.append(move)

        # choose a random move
        movePosition = randrange(len(weightedMoves))
        move = weightedMoves[movePosition]

        # make the move
        # transform the given board so the move is legal
        transformation = board.transformationTo(self._board)
        loops = 0
        while transformation is None:
            if loops == 0:
                print("Bug happened; trying again")
            transformation = board.transformationTo(self._board)
            loops += 1
            if loops == 100:
                print("What?? 100 times in a row??")
                break
        if loops > 0 and transformation is not None:
            print(f"Fixed after {loops} attempt(s).")
        board.applyTransformation(transformation)
        board.makeMove(move)
        # undo the transformation so it looks like it did before
        board.applyTransformation(transformation.getInverse())
        # report the move we made so we can learn from it later
        return move

    def sum(self) -> int:
        """
        :return: The number of symbols on the matchbox
        """
        return self._board.sum()

    def learnFromWin(self, move: Move) -> None:
        """
        Adjusts the Matchbox to reflect that we won, making the given move more likely to be chosen in the future
        :param move: the move this Matchbox made
        :raises InvalidMoveError: if this matchbox can't make that move (i.e. the move is illegal on the board state
        this matchbox represents)
        """
        self._adjust(move, Matchbox.winAdjustment)

    def learnFromDraw(self, move: Move) -> None:
        """
        Adjusts the Matchbox to reflect that we drew the game, making the given move slightly more likely to be chosen
        in the future
        :param move: the move this Matchbox made
        :raises InvalidMoveError: if this matchbox can't make that move (i.e. the move is illegal on the board state
        this matchbox represents)
        """
        self._adjust(move, Matchbox.drawAdjustment)

    def learnFromLoss(self, move: Move) -> None:
        """
        Adjusts the Matchbox to reflect that we lost the game, making the given move slightly less likely to be chosen
        in the future
        :param move: the move this Matchbox made
        :raises InvalidMoveError: if this matchbox can't make that move (i.e. the move is illegal on the board state
        this matchbox represents)
        """
        self._adjust(move, Matchbox.lossAdjustment)

    def holdsBoardState(self, board: Board) -> bool:
        """
        Determines if the board state this Matchbox holds is equivalent under symmetry to the given Board
        :param board: the board to compare
        :return: True if the boards are equivalent up to symmetry, False otherwise
        """
        return board.isEquivalentTo(self._board)

    def _adjust(self, move: Move, adjustment: int) -> None:
        """
        Adds or removes beads corresponding to the given move to the matchbox
        :param move: the move to add or remove beads for
        :param adjustment: the number of beads to add; negative values remove beads
        :return:
        """
        try:
            self._moves[move] += adjustment
            # if this bead has no moves left, remove it
            if self._moves[move] <= 0:
                self._moves.pop(move)
            # if there are no moves left at all, reset the matchbox
            if len(self._moves) == 0:
                self._generateLegalMoves()
        except KeyError:
            raise InvalidMoveError(f"Move {move} is illegal on board state \n{self._board}!") from None

    def label(self) -> str:
        """
        :return: the string version of the board state for this Matchbox; matches str(Board)
        """
        return str(self._board)

    def labels(self) -> tuple[str]:
        """
        :return: all labels for boards equivalent to this board's state
        """
        labels = []
        for board in self._board.equivalentBoards():
            labels.append(str(board))
        return tuple(labels)
    def _generateLegalMoves(self) -> None:
        """
        Populates self._moves with every legal move
        """
        board = self._board
        # add an entry in _moves for each legal move
        # keep track of which possible moves are legal
        legalMoves = []
        for row in range(board.size()):
            for column in range(board.size()):
                # check that the move is legal
                move = Move(row + 1, column + 1, self._symbol)
                if board.legalMove(move):
                    legalMoves.append(move)

        # check that each move we add is distinct
        # keep track of which moves we've added so we can only add distinct moves
        addedMoves = []
        for move in legalMoves:
            distinct = True
            # make the move we're checking
            currentBoard = copy(board)
            currentBoard.makeMove(move)
            # make each move we've added and see if the boards are equivalent;
            # if the boards are equivalent, so are the moves
            for addedMove in addedMoves:
                addedBoard = copy(board)
                addedBoard.makeMove(addedMove)
                distinct = distinct and not currentBoard.isEquivalentTo(addedBoard)
                if not distinct:
                    break
            # if the legal move is distinct, add it
            if distinct:
                self._moves[move] = Matchbox.BEADS
                addedMoves.append(move)

    def __repr__(self) -> str:
        """
        :return: a string with enough information to reconstruct the matchbox
        """
        board = str(self._board)
        board = "".join(board.split("\n"))
        return f"{board}; {self._symbol}; {self._moves}"

    def __eq__(self, other: Matchbox) -> bool:
        """
        Determines if the two matchboxes are for the same turn
        :param other: the Matchbox to compare to this one
        :return: True if the Matchboxes' states have the same number of symbols, False otherwise
        """
        return self._board == other._board

    def __gt__(self, other: Matchbox) -> bool:
        """
        Determines if this matchbox is later in the game than the other
        :param other: The matchbox to compare against
        :return: True if this matchbox has more symbols than the other, False otherwise
        """
        return self._board > other._board

    def __ge__(self, other: Matchbox) -> bool:
        """
        Determines if this matchbox is on at least the same turn as the other
        :param other: the matchbox to compare against
        :return: True if this matchbox is at least as far into the game as the other, False otherwise
        """
        return self._board >= other._board

    def __lt__(self, other: Matchbox) -> bool:
        """
        Determines if this matchbox is on an earlier turn than the other
        :param other: the matchbox to compare against
        :return: True if this matchbox has fewer symbols than the other, False otherwise
        """
        return self._board < other._board

    def __le__(self, other: Matchbox) -> bool:
        """
        Determines if this matchbox is at most on the same turn as the other
        :param other: the matchbox to compare against
        :return: True if this matchbox has at most as many symbols as the other, False otherwise
        """
        return self._board <= other._board

    def __ne__(self, other: Matchbox) -> bool:
        """
        Determines if the matchboxes are not on the same turn
        :param other: the matchbox to compare against
        :return: True if this matchbox is on a different turn than the other, False otherwise
        """
        return self._board != other._board

#
# Gabe Byk
# CS481: Seminar
# 13 October 2022
#

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
        self._grid = [Move.BLANK for _ in range(self._size * self._size)]

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
        newGrid = [Move.BLANK for _ in range(self._size * self._size)]
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
            if duplicate == other:
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
            if duplicate == other:
                return combinedTransformation

        # if none of the transformations were equivalent, then no transformation exists
        return None

    def equivalentBoards(self) -> tuple[Board]:
        """
        :return: a tuple of all boards equivalent to this one
        """
        boards: list[Board] = []

        # with the bottom left at (0, 0) and the top right at (size - 1, size - 1), the center is just their midpoint
        center = ((self._size - 1) / 2, (self._size - 1) / 2)
        # these transformations are needed for the rotations and reflections
        translateToOrigin = Translation(-center[0], -center[1])
        translateBack = Translation(center[0], center[1])
        # calculate the total 90 degree rotation
        pureRotation = Rotation((0, 0), 90)
        combinedRotation = translateBack * pureRotation * translateToOrigin
        # check rotations for equivalence
        for i in range(4):
            # check if the rotation would make the board states equivalent
            self.applyTransformation(combinedRotation)
            if self not in boards:
                boards.append(copy(self))

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
            if duplicate not in boards:
                boards.append(copy(duplicate))
        return tuple(boards)

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
        Compares the two boards to determine if they match exactly
        :param other: the Board to compare to this one
        :return: True if the boards are exactly the same; False otherwise
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

#
# Gabe Byk
# CS481: Seminar
# 13 October 2022
#

class MENACE(Player):
    _matchboxes: dict[str: Matchbox]
    _movesMade: list[tuple[Move, Matchbox]]

    def __init__(self, name: str = "MENACE", symbol: str = Move.CROSS) -> None:
        """
        Creates a MENACE that knows nothing
        :param name: the name to give MENACE; defaults to MENACE
        :param symbol: the symbol MENACE will play; defaults to Move.CROSS
        """
        super().__init__(name, symbol)
        self._matchboxes = dict()
        self._movesMade = []

    @classmethod
    def fromFile(cls, filename: str) -> MENACE:
        with open(filename, "r") as infile:
            # the first line is 'name: symbol'
            name, symbol = infile.readline().split(": ")
            menace = MENACE(name, symbol)
            # the rest is one line per matchbox
            for line in infile:
                if len(line) > 2:
                    matchbox = Matchbox.fromString(line)
                    menace._matchboxes[matchbox.label()] = matchbox
        return menace

    def makeMove(self, board: Board) -> None:
        """
        Makes a move on the given Board
        :param board: the Board to make a move on
        """
        # find or create the matchbox for this board state
        correctMatchbox = self._matchboxFor(board)

        # make whichever move the matchbox gives us
        move = correctMatchbox.makeMove(board)
        # remember the move and matchbox so we can learn later
        self._movesMade.append((move, correctMatchbox))

    @profile
    def _matchboxFor(self, board: Board) -> Matchbox:
        """
        Finds or creates the matchbox for this board state
        :param board: the board state to find
        :return: the existing matchbox in _matchboxes, or creates and adds one if there isn't one
        """
        # see if we have an equivalent board already
        for equivalentBoard in board.equivalentBoards():
            try:
                # if the lookup succeeds, we've found the correct board
                return self._matchboxes[str(equivalentBoard)]
            except KeyError:
                # if the lookup fails, try the next board
                pass
        # if we get to this point, we don't; create one
        box = Matchbox(board, self._symbol)
        self._matchboxes[box.label()] = box
        return box

    def learn(self, winner: str | None) -> None:
        """
        Updates each matchbox to hold more or less beads depending on if we won, drew, or lost
        :param winner: the winner of the game; one of Move.NOUGHT, Move.CROSS, or None if there was no winner
        """
        if winner is None:
            for move, matchbox in self._movesMade:
                matchbox.learnFromDraw(move)
        elif winner == self.symbol():
            for move, matchbox in self._movesMade:
                matchbox.learnFromWin(move)
        else:
            for move, matchbox in self._movesMade:
                matchbox.learnFromLoss(move)
        # prepare for a new game
        self._movesMade = []

    def save(self, filename: str) -> None:
        """
        Saves MENACE's progress to the given file
        :param filename: The directory to the file to write to
        """
        with open(filename, "w") as outfile:
            print(self, file=outfile)
            for matchbox in self._matchboxes.values():
                print(matchbox, file=outfile)


class Game:
    # the Board this game is played on
    _board: Board
    # the two players; tuple so alternating turns can be more efficient
    _players: tuple[Player, Player]

    def __init__(self, player1: Player, player2: Player, size: int = 3):
        """
        Makes a new game with the two given players
        :param player1: The player that will go first; this player will be given X
        :param player2: The player that will go second; this player will be given O
        :param size: The size of Tic-Tac-Toe board to play on, where the board is a size by size grid; defaults to 3.
        """
        self._board = Board(size)
        player1.setSymbol(Move.CROSS)
        player2.setSymbol(Move.NOUGHT)
        self._players = (player1, player2)

    def playGame(self, logfile: str | None = "gameLogs.txt") -> str | None:
        """
        Plays one game with the given players.
        :param logfile: the text file to print logs to; defaults to gameLogs.txt. if None is provided, no logs will be
        printed.
        :return: The symbol that won (one of Board.NOUGHT or Board.CROSS), or None if it was a draw
        """
        logs: list[str] = [f"{self._players[0]}; {self._players[1]}"]
        self._board.reset()
        turns = 0
        while not self._board.isOver():
            logs.append(str(self._board))
            self._players[turns % 2].makeMove(self._board)
            turns += 1
        logs.append(str(self._board))
        if isinstance(self._players[0], Human) or isinstance(self._players[1], Human):
            print(self._board)
        winner = self._board.winner()
        if winner is not None:
            print(f"{self._players[turns % 2 - 1].name()} won playing {winner} in {turns} turns!")
            logs.append(f"{self._players[turns % 2 - 1].name()} won playing {winner} in {turns} turns!")
        else:
            print(f"Draw in {turns} turns!")
            logs.append(f"Draw in {turns} turns!")
        if logfile is not None:
            with open(logfile, "a") as outfile:
                print("\n".join(logs), file=outfile)
        return winner


class GameUI(Game):
    """
    An extension of the Game class that uses a GUI instead of the Python Console to run the game.
    """


class Human(Player):
    """
    A usable Player that interacts with a Human via the Python Console.
    """
    def _askForMove(self, board: Board) -> Move:
        """
        Asks the Human for the move they want to make.
        :return: The Move the human wants to make
        """
        print(board)
        print("The top row is row 1 and the left-most column is column 1.")
        print(f"It's {self.name()}'s turn, and they're playing {self.symbol()}")
        while True:
            response = input("Enter your move in the format 'row, column': ")
            try:
                row, column = response.strip().split(",")
            except ValueError:
                print("Please make sure your numbers are separated by a comma.")
                # skip the rest of the loop since row and column didn't properly set
                continue
            try:
                row, column = int(row.strip()), int(column.strip())
            except ValueError:
                print("Please make sure you input numbers for the row and column.")
                # skip the rest of the loop since row and column are invalid
                continue
            if 1 <= row <= board.size() and 1 <= column <= board.size():
                # we have a valid board position; now create the move and return it
                return Move(row, column, self.symbol())
            else:
                print(f"Please make sure your input is between 1 and {board.size()}.")

    def _reportIllegalMove(self) -> None:
        """
        Informs the player that the Move they tried to make was illegal.
        """
        print("Sorry, the spot you wanted was taken. Here's the board again: ")

    def makeMove(self, board: Board) -> None:
        move = self._askForMove(board)
        while not board.legalMove(move):
            self._reportIllegalMove()
            move = self._askForMove(board)
        board.makeMove(move)


class HumanUI(Human):
    """
    A modified version of the Human class that works with a GUI.
    """
    pass


from typing import Sequence
from math import sin, cos
# used only for testing purposes
from graphics import GraphWin, Point, Circle, color_rgb, Text


class Transformation:
    """
    An interface used to contain all necessary information to tell an object how it should be transformed
    (rotation by x degrees, flip about some axis, etc). Not useful for applying transformations other than the identity.
    """
    # the matrix to use to apply the transformation
    _matrix: Matrix
    # the matrix used to keep track of the inverse
    _inverse: Matrix

    def __init__(self, matrix: Matrix = None):
        """
        :param matrix: The matrix to use with this transformation; if not provided, defaults to the identity.
        """
        self._matrix = Matrix(3, 3)
        self._inverse = Matrix(3, 3)

        if matrix is not None:
            self._matrix.setValues(matrix)
        else:
            self._matrix.setToIdentity()
            self._inverse.setToIdentity()

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
        # if we're asked to do self * other, perform self * other
        result = Transformation(self._matrix * other._matrix)
        # the inverse of self * other is other' * self'
        result._inverse = other._inverse * self._inverse
        return result

    def __repr__(self) -> str:
        """
        :return: the string representation of this Transformation's matrix
        """
        return str(self._matrix)

    def getInverse(self) -> Transformation:
        """
        Calculates and provides the transformation that undoes this one
        :return: A new Transformation that completely undoes this one
        """
        inverse = Transformation(self._inverse)
        inverse._inverse.setValues(self._matrix)
        return inverse

    def __eq__(self, other: Transformation) -> bool:
        """
        :param other: the Transformation to compare against
        :return: True if the transformations are the same up to floating point error, False otherwise
        """
        return self._matrix == other._matrix

    def __ne__(self, other: Transformation) -> bool:
        """
        :param other: the Transformation to compare against
        :return: True if the transformations are significantly different, False otherwise
        """
        return not self == other


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
        self._inverse[0][2] = -dx
        self._inverse[1][2] = -dy


class Rotation(Transformation):

    def __init__(self, center: Tuple[float, float], degrees: float):
        """
        Rotates the plane about the point center by degrees.
        :param center: The point to rotate about
        :param degrees: The number of degrees to rotate clockwise
        """
        super().__init__()
        # compute the sin and cos of the given angle so we don't have to do it later
        s = sin(toRadians(degrees))
        c = cos(toRadians(degrees))

        # set up the matrix for rotating about (0, 0)
        rotationMatrix = Matrix(3, 3)
        rotationMatrix.setToIdentity()
        # rotation matrix to rotate clockwise by theta should look like this:
        # cos(theta) | sin(theta) | 0
        # -sin(theta)| cos(theta) | 0
        #      0     |      0     | 1
        rotationMatrix[0][0] = c
        rotationMatrix[0][1] = s
        rotationMatrix[1][0] = -s
        rotationMatrix[1][1] = c

        # the inverse of a rotation is a rotation by -degrees
        # since cos is even and sin is odd, we can just negate sin and keep cos
        inverseMatrix = Matrix(3, 3)
        inverseMatrix.setToIdentity()
        inverseMatrix[0][0] = c
        inverseMatrix[0][1] = -s
        inverseMatrix[1][0] = s
        inverseMatrix[1][1] = c

        pureRotation = Transformation(rotationMatrix)
        pureRotation._inverse.setValues(inverseMatrix)

        # assign the proper transformation
        if center != (0, 0):
            # to rotate about the center, we need to move the center to (0, 0), rotate about (0, 0), then move it back
            # transformations are applied right to left, since the point is on the right during multiplication
            completeTransformation = Translation(center[0], center[1]) *\
                                     pureRotation *\
                                     Translation(-center[0], -center[1])
            # now we can just set our instance variables and it works
            self._matrix = completeTransformation._matrix
            self._inverse = completeTransformation._inverse
        else:
            # if the center is (0, 0), we can just rotate about it without translating
            self._matrix = pureRotation._matrix
            self._inverse = pureRotation._inverse


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
        self._inverse[0][0] = 1 / xScale
        self._inverse[1][1] = 1 / yScale


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

        # compute the total transformation and extract the values we need
        total: Transformation = rotateToStart * flipAboutAxis * rotateToAxis
        self._matrix = total._matrix
        self._inverse = total._inverse


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

from math import pi

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
        self._matrix = [[0 for _ in range(n)] for _ in range(m)]

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
    main()
