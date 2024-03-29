#
# Gabe Byk
# CS481: Seminar
# 13 October 2022
#

from Game import Game
from MENACE import MENACE
from Human import Human
from Player import Player
from Drawables import GameUI


def menaceVsMenace(iterations, menace1File: str | None = None, menace2File: str | None = None, size: int = 3) -> None:
    if menace1File is not None:
        try:
            m1 = MENACE.fromFile(menace1File)
        except FileNotFoundError:
            m1 = MENACE(menace1File[:-4])
    else:
        m1 = MENACE("Menace 1")
    if menace2File is not None:
        try:
            m2 = MENACE.fromFile(menace2File)
        except FileNotFoundError:
            m2 = MENACE(menace2File[:-4])
    else:
        m2 = MENACE("Menace 2")
    g = Game(m1, m2, size)
    for i in range(iterations):
        winner = g.playGame(gameLogs)
        m1.learn(winner)
        m2.learn(winner)
    if menace1File is not None:
        m1.save(menace1File)
    if menace2File is not None:
        m2.save(menace2File)


def humanVsHuman() -> None:
    h1 = Human("Gabe")
    h2 = Human("Gabe")
    g = Game(h1, h2)
    g.playGame(gameLogs)


def humanVsMenace(player1: Player, player2: Player) -> None:
    g = Game(player1, player2)
    g.playGame(gameLogs)
    if isinstance(player1, MENACE):
        player1.save("MENACE First vs Human.txt")
    if isinstance(player2, MENACE):
        player2.save("MENACE Second vs Human.txt")


def readLogs(filename: str = "gameLogs.txt"):
    with open(filename, "r") as infile:
        wins = dict()
        draws = 0
        for line in infile:
            if " won playing " in line and " turns!" in line:
                player = line.split(" won playing ")[0]
                if player in wins:
                    wins[player] += 1
                else:
                    wins[player] = 1
            elif "Draw in " in line and " turns!" in line:
                draws += 1
    for player in wins.keys():
        print(f"{player} won {wins[player]} times")
    print(f"There were {draws} draws")


gameLogs = "5x5 test.txt"


def trainMenace(file1: str = "Menace 1.txt", file2: str = "Menace 2.txt", size: int = 3, rounds: int = 500):
    menaceVsMenace(rounds, file1, file2, size)


def main():
    g = GameUI()
    # GameUI includes a quit button that will exit the program after each game if clicked
    while True:
        g.startGames()


if __name__ == "__main__":
    main()
