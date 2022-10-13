from MENACE import MENACE
from TransformableBoard import TransformableBoard, Board

TRAIN = True
def main():
    # for now, if MENACE learns to forfeit, make a new one
    m1 = MENACE(Board.naught, "menace1.txt")
    m2 = MENACE(Board.cross, "menace2.txt")
    b = TransformableBoard()
    if not TRAIN:
        print(b)
        print()
    moves = 0
    players = (Board.naught, Board.cross)
    while not b.isOver():
        # get the corresponding MENACE's move
        if moves % 2 == 0:
            m1.makeMove(b)
        else:
            m2.makeMove(b)
        moves += 1
        if not TRAIN:
            print(b)
            print()
    assert moves <= 9

    winner = b.getWinner()
    if not TRAIN:
        if winner is not None:
            print(f"Player {winner} won in {moves} moves!")
        else:
            print(f"Tie after {moves} moves!")

    if TRAIN:
        m1.gameOver(winner)
        m2.gameOver(winner)
        m1.save("menace1.txt")
        m2.save("menace2.txt")


if __name__ == "__main__":
    reps = 1000
    for i in range(reps):
        main()
