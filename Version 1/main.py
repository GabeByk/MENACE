#
# Gabe Byk
# CS481: Seminar
# 13 October 2022
#

from Game import Game
from MENACE import MENACE
from Human import Human


def main():
    m = MENACE("MENACE")
    h = Human("Human")
    g = Game(m, h)
    g.run()


if __name__ == "__main__":
    main()
