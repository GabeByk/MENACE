#
# Gabe Byk
# CS481
# main.py
#
from Board import Board
def main():
    b = Board()
    print(b)
    moves = 0
    players = (Board.naught, Board.cross)
    while not b.isOver():
        print("Top left is 0, 0 and bottom right is 2, 2.")
        given = input("Where would you like to move? enter an x, y value: ")
        move = given.split(", ")
        move = (int(move[0]), int(move[1]))
        b.addMove(players[moves % 2], move)
        moves += 1
        print(b)
    print(f"Player {players[moves % 2 - 1]} won in {moves} moves!")



if __name__ == '__main__':
    main()
