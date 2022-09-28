from MENACE import MENACE
from Board import Board

def main():
    m = MENACE(Board.cross)
    m1 = MENACE(Board.naught)
    m2 = MENACE(Board.cross)
    m.save("menace.txt")
    m1.save("menace1.txt")
    m2.save("menace2.txt")


if __name__ == "__main__":
    main()
