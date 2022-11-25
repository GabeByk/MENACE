from __future__ import annotations
from Player import Player
from Board import Board
from Move import Move


class Human(Player):
    """
    A usable Player that interacts with a Human via the Python Console.
    """
    def _askForMove(self) -> Move:
        """
        Asks the Human for the move they want to make.
        :return: The Move the human wants to make
        """
        pass

    def _reportIllegalMove(self) -> None:
        """
        Informs the player that the Move they tried to make was illegal.
        """
        pass

    def makeMove(self, board: Board) -> None:
        move = self._askForMove()
        while not board.isLegal(move):
            self._reportIllegalMove()
            move = self._askForMove()
        board.makeMove(move)


class HumanUI(Human):
    """
    A modified version of the Human class that works with a GUI.
    """
    pass
