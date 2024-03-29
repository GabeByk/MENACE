#
# Gabe Byk
# CS481: Seminar
# 13 October 2022
#

from __future__ import annotations
from Board import Board
# found random.choice here: https://www.geeksforgeeks.org/how-to-get-weighted-random-choice-in-python/
from random import choices
from util import InvalidMoveError
from copy import copy
from Move import Move

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
            row = position // board.size()
            column = position % board.size()
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

    def makeMove(self, board: Board) -> Move:
        """
        Makes a random move on the given board, with the weights of each option dictated by the beads for each move
        :param board: the Board to make a move on
        """
        # get a random move
        move = choices(tuple(self._moves.keys()), tuple(self._moves.values()))[0]

        # make the move
        # transform the given board so the move is legal
        transformation = board.transformationTo(self._board)
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
                move = Move(row, column, self._symbol)
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


def main():
    b1 = Board()
    b2 = Board()
    for i in range(9):
        move = Move(i // 3, i % 3, str(i))
        if i % 2 == 0:
            b1.makeMove(move)
        else:
            b2.makeMove(move)
    for board in (b1, b2):
        matchboxToReconstruct = Matchbox(board, "X")
        reconstructableString = str(matchboxToReconstruct)
        box = Matchbox.fromString(reconstructableString)
        print(matchboxToReconstruct)
        print(box)
        assert box == matchboxToReconstruct


if __name__ == "__main__":
    main()

