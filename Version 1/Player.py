#
# Gabe Byk
# CS481: Seminar
# 13 October 2022
#

from __future__ import annotations
from Board import Board

class MethodUndefinedError(Exception):
    pass

def raiseMethodUndefinedError(caller: str, method: str):
    """
    Raises a MethodUndefinedError with the following message:
    `Object {caller} tried to call {method}, but {method} is not defined!`
    :param caller: The object that called the undefined method
    :param method: The method that was undefined
    """
    raise MethodUndefinedError(f"Object {caller} tried to call {method}, but {method} is not defined!")

class Player:
    """
    An interface for interacting with a Tic-Tac-Toe game. To use, create a class that inherits from this, and implement
    makeMove. You may override any of the other methods to your liking, but you must override makeMove.
    """
    # The symbol this Player will play: one of Board.X or Board.O
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
