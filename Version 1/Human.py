from __future__ import annotations
from Player import Player, raiseMethodUndefinedError
from Board import Board
from Move import Move

class BaseHuman(Player):
    def _askForMove(self) -> Move:
        raiseMethodUndefinedError(str(self), "_askForMove")
        return self._askForMove()

    def _reportIllegalMove(self):
        raiseMethodUndefinedError(str(self), "_reportIllegalMove")

    def makeMove(self, board: Board) -> None:
        move = self._askForMove()
        while not board.isLegal(move):
            self._reportIllegalMove()
            move = self._askForMove()
        board.makeMove(move)

