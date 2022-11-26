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


class MENACE(Player):
    _matchboxes: list[Matchbox]
    _movesMade: list[(Move, Matchbox)]

    def __init__(self, name: str = "MENACE", symbol: str = Move.CROSS) -> None:
        """
        Creates a MENACE that knows nothing
        :param name: the name to give MENACE; defaults to MENACE
        :param symbol: the symbol MENACE will play; defaults to Move.CROSS
        """
        super().__init__(name, symbol)
        self._matchboxes = []
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
                    menace._matchboxes.append(matchbox)
        return menace

    def makeMove(self, board: Board) -> None:
        """
        Makes a move on the given Board
        :param board: the Board to make a move on
        """
        # find or create the matchbox for this board state
        correctMatchbox = None
        for matchbox in self._matchboxes:
            if matchbox.holdsBoardState(board):
                correctMatchbox = matchbox
                break
        if correctMatchbox is None:
            correctMatchbox = Matchbox(board, self.symbol())
            self._matchboxes.append(correctMatchbox)

        # make whichever move the matchbox gives us
        move = correctMatchbox.makeMove(board)
        # remember the move and matchbox so we can learn later
        self._movesMade.append((move, correctMatchbox))

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
            for matchbox in self._matchboxes:
                print(matchbox, file=outfile)
