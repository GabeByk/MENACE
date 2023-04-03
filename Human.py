from __future__ import annotations
from Player import Player
from Board import Board
from Move import Move


class Human(Player):
    """
    A usable Player that interacts with a Human via the Python Console.
    """
    def _askForMove(self, board: Board) -> Move:
        """
        Asks the Human for the move they want to make.
        :return: The Move the human wants to make
        """
        print(board)
        print("The top row is row 1 and the left-most column is column 1.")
        print(f"It's {self.name()}'s turn, and they're playing {self.symbol()}")
        while True:
            response = input("Enter your move in the format 'row, column': ")
            try:
                row, column = response.strip().split(",")
            except ValueError:
                print("Please make sure your numbers are separated by a comma.")
                # skip the rest of the loop since row and column didn't properly set
                continue
            try:
                row, column = int(row.strip()), int(column.strip())
            except ValueError:
                print("Please make sure you input numbers for the row and column.")
                # skip the rest of the loop since row and column are invalid
                continue
            if 1 <= row <= board.size() and 1 <= column <= board.size():
                # we have a valid board position; now create the move and return it
                # subtract 1 from the row and column numbers to be 0 indexed rather than 1 indexed
                return Move(row - 1, column - 1, self.symbol())
            else:
                print(f"Please make sure your input is between 1 and {board.size()}.")

    def _reportIllegalMove(self) -> None:
        """
        Informs the player that the Move they tried to make was illegal.
        """
        print("Sorry, the spot you wanted was taken. Here's the board again: ")

    def makeMove(self, board: Board) -> None:
        move = self._askForMove(board)
        while not board.legalMove(move):
            self._reportIllegalMove()
            move = self._askForMove(board)
        board.makeMove(move)

