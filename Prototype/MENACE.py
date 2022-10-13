#
# Gabe Byk
# CS481
# MENACE.py
#
from TransformableBoard import TransformableBoard
from typing import Dict, Tuple, List
from random import randrange

class InvalidMENACEException(Exception):
    pass

class Matchbox:
    # the board this matchbox is labeled with
    _state: str
    # the moves this matchbox can make
    _moves: Dict
    # the player to move in this board state
    _symbol: str

    # the number of each move we should put in the box at first
    beads = 3
    # the value used to signify a forfeit
    forfeit = "Forfeit"

    def __init__(self, state: TransformableBoard, symbol: str, contents: str = None):
        """
        Initializes a Matchbox with the given state
        :param state: the TransformableBoard to act as the label for this Matchbox
        :param symbol: the symbol this matchbox's MENACE is playing as
        :param contents: Optional; if provided, initializes the matchbox with the given contents
        """
        self._state = state.compactStr()
        self._symbol = symbol
        self._moves = dict()
        if contents is None:
            self.reset()
        else:
            fields = contents.split(", (")
            for field in fields:
                key, value = field.split(": ")
                key = key.strip("'")
                if key != Matchbox.forfeit:
                    x, y = key.split(", ")
                    key = (int(x.lstrip("(")), int(y.rstrip(")")))
                self._moves[key] = int(value)

    def reset(self) -> None:
        # get the state
        state = TransformableBoard(self._state)
        # get all the legal moves
        legalMoves = []
        for y in range(3):
            for x in range(3):
                if state.isLegal((x, y)):
                    legalMoves.append((x, y))
        # add all distinct moves to self._moves
        for move1 in legalMoves:
            # see if we've added a move equivalent to move1
            distinct = True
            for move2 in self._moves.keys():
                distinct = distinct and not state.movesAreEquivalent(self._symbol, move1, move2)
            # if we haven't, add it
            if distinct:
                self._moves[move1] = Matchbox.beads

    def getMove(self) -> Tuple[int, int]:
        """
        :return: a random move, weighted according to the beads in the matchbox
        """
        weightedMoves = []
        for move in self._moves.keys():
            for i in range(self._moves[move]):
                weightedMoves.append(move)
        return weightedMoves[randrange(len(weightedMoves))]

    def adjust(self, move: Tuple[int, int], adjustment: int) -> None:
        """
        Adjusts the number of matching beads in the Matchbox by adjustment
        :param move: the move to add or remove beads from
        :param adjustment: the number of beads to add or remove
        """
        try:
            # adjust the given move
            self._moves[move] += adjustment
            # if there are no beads left, remove the move from _moves
            if self._moves[move] <= 0:
                self._moves.pop(move)
            # if the box is completely empty, reset
            if len(self._moves) == 0:
                self.reset()
        # if move isn't in _moves, just do nothing
        except KeyError:
            pass

    def label(self) -> str:
        return self._state

    def __repr__(self) -> str:
        """
        :return: the string representation of this matchbox
        """
        return f"{self._state}: {self._moves}"

class MENACE:
    # the matchboxes involved in this MENACE
    _matchboxes: List[Matchbox]
    # the symbol this MENACE is playing as
    _symbol: str
    # the moves this MENACE has made
    _moves: Dict
    # the number of wins, ties, and losses this MENACE has had, in that order
    _games: List[int]

    # the amount to adjust each move by on a win
    winAdjustment = 3
    # the amount to adjust each move by on a tie
    tieAdjustment = 1
    # the amount to adjust each move by on a loss
    lossAdjustment = -1

    def __init__(self, symbol: str = None, filename: str = None):
        if symbol is None and filename is None:
            raise InvalidMENACEException("MENACE needs either a symbol or filename to work with, but got None for both")
        self._matchboxes = []
        self._symbol = symbol
        self._moves = dict()
        self._games = [0, 0, 0]
        if filename is not None:
            with open(filename, "r") as infile:
                # find where this MENACE starts
                for line in infile:
                    if line == "BEGIN MENACE\n":
                        break
                # continue where we left off
                self._symbol = ""
                self._games = [-1, -1, -1]
                for line in infile:
                    # if MENACE is over, don't change anything
                    if line == "END MENACE\n":
                        break
                    # extract the symbol if we haven't already
                    elif self._symbol == "":
                        self._symbol = line[0]
                    # extract the games we've played if we haven't already
                    elif self._games[0] == -1:
                        line = line.lstrip("[")
                        line = line.rstrip("]\n")
                        wins, ties, losses = line.split(", ")
                        self._games = [int(wins), int(ties), int(losses)]
                    # otherwise, this is a board
                    else:
                        # remove the newline and end bracket, then split on the start bracket
                        line = line.strip()
                        line = line.rstrip("}")
                        matchboxLabel, matchboxContents = line.split("{")
                        self._matchboxes.append(Matchbox(TransformableBoard(matchboxLabel.rstrip(": ")), self._symbol,
                                                         matchboxContents))

    def makeMove(self, board: TransformableBoard) -> None:
        """
        Makes a move on the given board
        :param board: the board to make a move on
        """
        # see if we have this state, recording the index of the state if we have it
        pos = 0
        haveThisState = False
        for i in range(len(self._matchboxes)):
            haveThisState = haveThisState or board.matchesLabel(self._matchboxes[i].label())
            if haveThisState:
                break
            pos += 1
        # if we don't have the state, make a matchbox for it
        if not haveThisState:
            matchbox = Matchbox(board, self._symbol)
            self._matchboxes.append(matchbox)
        # otherwise, get the one we have
        else:
            matchbox = self._matchboxes[pos]
        # get the move and record what to change later
        move = matchbox.getMove()
        self._moves[pos] = move
        label = matchbox.label()
        # if the given state doesn't match the box's label, transform the board so it does
        oldBoard = board.compactStr()
        if oldBoard != label:
            # change the board to match the matchbox
            board.matchLabel(label)
            # add the move
            board.addMove(self._symbol, move)
            # change the board back
            for i in range(9):
                newBoard = list(oldBoard)
                newBoard[i] = self._symbol
                board.matchLabel("".join(newBoard))
        else:
            board.addMove(self._symbol, move)

    def gameOver(self, winner: str | None) -> None:
        """
        Report to MENACE if it won, lost, or tied; MENACE will learn from its experience
        """
        # record whether we won, tied, or lost
        if winner == self._symbol:
            adjustment = MENACE.winAdjustment
            self._games[0] += 1
        elif winner is None:
            adjustment = MENACE.tieAdjustment
            self._games[1] += 1
        else:
            adjustment = MENACE.lossAdjustment
            self._games[2] += 1

        for pos in self._moves.keys():
            move = self._moves[pos]
            matchbox = self._matchboxes[pos]
            matchbox.adjust(move, adjustment)

    def save(self, filename: str) -> None:
        """
        Saves this MENACE to the given file
        :param filename: the file to write to
        """
        with open(filename, "w") as outfile:
            print("BEGIN MENACE", file=outfile)
            print(self._symbol, file=outfile)
            print(self._games, file=outfile)
            for matchbox in self._matchboxes:
                print(matchbox, file=outfile)
            print("END MENACE", file=outfile)
