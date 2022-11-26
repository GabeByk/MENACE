#
# Gabe Byk
# CS481: Seminar
# 13 October 2022
#

from Board import Board
from Player import Player
from Human import Human
from Move import Move
from typing import List


class Game:
    # the Board this game is played on
    _board: Board
    # list of players (list so alternating turns can be more efficient)
    _players: List[Player]

    def __init__(self, player1: Player, player2: Player):
        """
        Makes a new game with the two given players
        :param player1: The player that will go first; this player will be given X
        :param player2: The player that will go second; this player will be given O
        """
        self._board = Board()
        player1.setSymbol(Move.CROSS)
        player2.setSymbol(Move.NOUGHT)
        self._players = [player1, player2]

    def playGame(self) -> str | None:
        """
        Plays one game with the given players.
        :return: The symbol that won (one of Board.NOUGHT or Board.CROSS), or None if it was a draw
        """
        logs: list[str] = [f"{self._players[0]}; {self._players[1]}"]
        self._board.reset()
        turns = 0
        while not self._board.isOver():
            logs.append(str(self._board))
            self._players[turns % 2].makeMove(self._board)
            turns += 1
        logs.append(str(self._board))
        if isinstance(self._players[0], Human) or isinstance(self._players[1], Human):
            print(self._board)
        winner = self._board.winner()
        if winner is not None:
            print(f"{self._players[turns % 2 - 1].name()} won playing {winner} in {turns} turns!")
            logs.append(f"{self._players[turns % 2 - 1].name()} won playing {winner} in {turns} turns!")
        else:
            print(f"Draw in {turns} turns!")
            logs.append(f"Draw in {turns} turns!")
        with open("gameLogs.txt", "a") as outfile:
            print("\n".join(logs), file=outfile)
        return winner


class GameUI(Game):
    """
    An extension of the Game class that uses a GUI instead of the Python Console to run the game.
    """
