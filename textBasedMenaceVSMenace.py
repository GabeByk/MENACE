from MENACE import MENACE
from TransformableBoard import TransformableBoard, Board

def main():
    # for now, if MENACE learns to forfeit, make a new one
    # TODO: Allow for forfeits
    try:
        m1 = MENACE(Board.naught, "menace1.txt")
    except ValueError:
        m1 = MENACE(Board.naught)
    try:
        m2 = MENACE(Board.cross, "menace2.txt")
    except ValueError:
        m2 = MENACE(Board.cross)
    b = TransformableBoard()
    print(b)
    print()
    moves = 0
    players = (Board.naught, Board.cross)
    while not b.isOver():
        # get the corresponding MENACE's move
        if moves % 2 == 0:
            move = m1.getMove(b)
        else:
            move = m2.getMove(b)
        # add the move, print the board
        crashed = False
        # TODO: Transforming moves from stored state to active state doesn't work properly, or else MENACE
        # TODO: is just straight up cheating somehow
        try:
            assert b.isLegal(move)
        except AssertionError:
            crashed = True
        b.addMove(players[moves % 2], move)
        moves += 1
        print(b)
        print()
        if crashed:
            raise AssertionError("The last move made was illegal!")
    assert moves <= 9

    winner = b.getWinner()
    if winner is not None:
        print(f"Player {winner} won in {moves} moves!")
    else:
        print(f"Tie after {moves} moves!")

    m1.gameOver(winner)
    m2.gameOver(winner)
    m1.save("menace1.txt")
    m2.save("menace2.txt")


if __name__ == "__main__":
    reps = 1000
    for i in range(reps):
        main()
