#
# Gabe Byk
# CS481: Seminar
# 13 October 2022
#

from Board import Board
from Player import Player
from Move import Move
from typing import List


class Game:
    # the Board this game is played on
    _board: Board
    # the players of the game
    _players = List[Player]

    def __init__(self, player1: Player, player2: Player):
        """
        Makes a new game with the two given players
        :param player1: The player that will go first; this player will be given X
        :param player2: The player that will go second; this player will be given O
        """
        self._board = Board()
        player1.setSymbol(Move.CROSS)
        player2.setSymbol(Move.NOUGHT)
        self._players = []

    def playGame(self):
        """
        Plays one game with the given players.
        """

    def run(self):
        """
        Enters the run loop of the game; exits when the user doesn't want to play anymore.
        """
        self.playGame()
        while True:
            # TODO: let the human involved choose to play another game or to quit
            self.playGame()


class GameUI(Game):
    """
    An extension of the Game class that uses a GUI instead of the Python Console to run the game.
    """
