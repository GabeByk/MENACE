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
    Base class for every class that interacts with the Game. Any subclass must override everything above __init__.
    """
    # The symbol this Player will play: one of Board.X or Board.O
    _symbol: str
    # The name assigned to this Player
    _name: str

    def makeMove(self, board: Board) -> None:
        raiseMethodUndefinedError(str(self), "makeMove")

    def clone(self) -> Player:
        raiseMethodUndefinedError(str(self), "clone")
        # PyCharm doesn't know that this code is unreachable, so it complained that clone doesn't return a Player
        return self.clone()

    def __init__(self, name: str, symbol: str = None):
        self._name = name
        self._symbol = symbol

    def _setSymbol(self, symbol: str):
        self._symbol = symbol

    def symbol(self) -> str:
        return self._symbol

    def name(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return f"{self.name()}: {self.symbol()}"
