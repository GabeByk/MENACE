#
# Gabe Byk
# CS481: Seminar
# 13 October 2022
#

from Board import Board
from Player import Player
from Human import Human
from Move import Move

class Game:
    # the Board this game is played on
    _board: Board
    # the two players; tuple so alternating turns can be more efficient
    _players: tuple[Player, Player]

    def __init__(self, player1: Player, player2: Player, size: int = 3):
        """
        Makes a new game with the two given players
        :param player1: The player that will go first; this player will be given X
        :param player2: The player that will go second; this player will be given O
        :param size: The size of Tic-Tac-Toe board to play on, where the board is a size by size grid; defaults to 3.
        """
        self._board = Board(size)
        player1.setSymbol(Move.CROSS)
        player2.setSymbol(Move.NOUGHT)
        self._players = (player1, player2)

    def playGame(self, logfile: str | None = "gameLogs.txt") -> str | None:
        """
        Plays one game with the given players.
        :param logfile: the text file to print logs to; defaults to gameLogs.txt. if None is provided, no logs will be
        printed.
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
        # if isinstance(self._players[0], Human) or isinstance(self._players[1], Human):
        #     print(self._board)
        winner = self._board.winner()
        if winner is not None:
            # print(f"{self._players[turns % 2 - 1].name()} won playing {winner} in {turns} turns!")
            logs.append(f"{self._players[turns % 2 - 1].name()} won playing {winner} in {turns} turns!")
        else:
            # print(f"Draw in {turns} turns!")
            logs.append(f"Draw in {turns} turns!")
        if logfile is not None:
            with open(logfile, "a") as outfile:
                print("\n".join(logs), file=outfile)
        # else:
            # print(logs)
        return winner
