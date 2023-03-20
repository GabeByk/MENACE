#
# Gabe Byk
# CS481: Seminar
# 13 October 2022
#

from __future__ import annotations
from Player import Player
from Board import Board
from Matchbox import Matchbox
from Move import Move
from util import BinarySearchTree


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
        try:
            with open(filename, "r") as infile:
                # the first line is 'name: symbol'
                name, symbol = infile.readline().split(": ")
                menace = MENACE(name, symbol)
                # the rest is one line per matchbox
                for line in infile:
                    if len(line) > 2:
                        matchbox = Matchbox.fromString(line)
                        menace._matchboxes[matchbox.label()] = matchbox
        except FileNotFoundError:
            menace = MENACE(filename[:-4])
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
