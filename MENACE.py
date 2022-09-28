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

    # the number of each move we should put in the box at first
    beads = 3

    def __init__(self, state: TransformableBoard, symbol: str, contents: str = None):
        """
        Initializes a Matchbox with the given state
        :param state: the TransformableBoard to act as the label for this Matchbox
        :param symbol: the symbol this matchbox's MENACE is playing as
        :param contents: Optional; if provided, initializes the matchbox with the given contents
        """
        self._state = state.compactStr()
        self._moves = dict()
        if contents is None:
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
                    distinct = distinct and not state.movesAreEquivalent(symbol, move1, move2)
                # if we haven't, add it
                if distinct:
                    self._moves[move1] = Matchbox.beads
        else:
            fields = contents.split(", (")
            for field in fields:
                key, value = field.split(": ")
                x, y = key.split(", ")
                key = (int(x.lstrip("(")), int(y.rstrip(")")))
                self._moves[key] = int(value)

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
            # remove a bead for the given move
            self._moves[move] += adjustment
            # if there are no beads left, remove the move from _moves
            if self._moves[move] <= 0:
                self._moves.pop(move)
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

def transformationsBetween(source: TransformableBoard, destination: TransformableBoard) -> str:
    # if no transformations are necessary, report so
    if source.exactlyEquals(destination):
        return "r0"
    source.rotateOne()
    # otherwise see if we need a rotation
    correct = False
    i = 0
    for i in range(1, 4):
        correct = correct or source.exactlyEquals(destination)
        if correct:
            break
    if correct:
        # undo our rotations and report back
        source.rotate(-i)
        return f"r{i}"
    i = 0
    correct = False
    for i in range(4):
        source.flip(i)
        correct = correct or source.exactlyEquals(destination)
        source.flip(i)
        if correct:
            break
    if correct:
        # report back
        return f"f{i}"
    return ""

def rotate(move: Tuple[int, int], n: int) -> Tuple[int, int]:
    for i in range(n):
        if move == (0, 0):
            move = (2, 0)
        elif move == (1, 0):
            move = (2, 1)
        elif move == (2, 0):
            move = (2, 2)

        elif move == (0, 1):
            move = (1, 0)
        elif move == (2, 1):
            move = (1, 2)

        elif move == (0, 2):
            move = (0, 0)
        elif move == (1, 2):
            move = (0, 1)
        elif move == (2, 2):
            move = (0, 2)
    return move

def fittedMove(move: Tuple[int, int], source: str, state: TransformableBoard) -> Tuple[int, int]:
    source = TransformableBoard(source)
    # we don't need to fix it if it's the center or we don't need a transformation
    if move == (1, 1) or source.exactlyEquals(state):
        return move
    # we need a transformation, so figure out what it is
    requiredTransformation = transformationsBetween(source, state)
    # transform the move, if possible
    if requiredTransformation == "":
        return -1, -1
    # if we're at a corner
    transformation = requiredTransformation[0]
    n = int(requiredTransformation[1])
    # if we need a rotation
    if transformation == "r":
        # rotate 90 degrees n times
        move = rotate(move, n)
    else:
        # we need a flip
        # as long as the x component isn't 1, a vertical flip is just adding 2 to the x component and taking mod 4
        if move[0] != 1:
            move = ((move[0] + 2) % 4, move[1])
        # if it is 1, then a vertical flip does nothing
        # now rotate n
        move = rotate(move, n)
    return move

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
                        # TODO: Crashes when MENACE learns to forfeit
                        matchboxLabel, matchboxContents = line.split("{")
                        self._matchboxes.append(Matchbox(TransformableBoard(matchboxLabel.rstrip(": ")), self._symbol,
                                                         matchboxContents))

    def getMove(self, state: TransformableBoard) -> Tuple[int, int]:
        # see if we have this state, recording the index of the state if we have it
        pos = 0
        haveThisState = False
        for i in range(len(self._matchboxes)):
            haveThisState = haveThisState or state.matchesLabel(self._matchboxes[i].label())
            if haveThisState:
                break
            pos += 1
        # if we don't have the state, make a matchbox for it
        if not haveThisState:
            matchbox = Matchbox(state, self._symbol)
            self._matchboxes.append(matchbox)
        # otherwise, get the one we have
        else:
            matchbox = self._matchboxes[pos]
        # get the move and record what to change later
        move = matchbox.getMove()
        self._moves[pos] = move
        # transform the move to the current board state
        return fittedMove(move, matchbox.label(), state)

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
