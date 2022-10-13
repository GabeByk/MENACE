from MENACE import MENACE
from TransformableBoard import TransformableBoard, Board

TRAIN = False
PlayerFirst = False
def main():
    if PlayerFirst:
        n = 0
    else:
        n = 1
    menace = f"menace{2 - n}.txt"
    m = MENACE(Board.cross, menace)
    b = TransformableBoard()
    print(b)
    print()
    moves = 0
    players = (Board.naught, Board.cross)
    while not b.isOver():
        prompts = [
            "Top left is 0, 0 and bottom right is 2, 2.",
            f"Where would player {players[moves % 2]} like to move? enter an x, y value: ",
            "Sorry, the value should be two integers separated by a comma and a space. Please re-enter your move.",
            "Sorry, either that spot is taken or that spot's not on the board. Please re-enter your move."
        ]
        # if it's the human's turn, get the human's move
        if moves % 2 == n:
            print(prompts[0])
            # keep trying to get a move until we get one that's legal
            while True:
                # get a prompt from the user
                given = input(prompts[1])
                print()
                # prepare to extract the coordinates
                move = given.split(", ")
                # if there aren't two coordinates, they entered it wrong
                if len(move) != 2:
                    print(prompts[2])
                # extract the two coordinates
                else:
                    try:
                        # int method raises a ValueError if it can't convert to an integer
                        move = (int(move[0]), int(move[1]))
                        # check to see if the move is legal while we have it
                        if b.isLegal(move):
                            b.addMove(players[n], move)
                            break
                        else:
                            print(prompts[3])
                            print(prompts[0])
                    except ValueError:
                        print(prompts[2])
        # otherwise, get MENACE's move
        else:
            m.makeMove(b)
        # add the move, print the board
        moves += 1
        print(b)
        print()

    winner = b.getWinner()
    if winner is not None:
        print(f"Player {winner} won in {moves} moves!")
    else:
        print(f"Tie after {moves} moves!")
    if TRAIN:
        m.gameOver(winner)
        m.save(menace)


if __name__ == "__main__":
    main()
