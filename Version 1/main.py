#
# Gabe Byk
# CS481: Seminar
# 13 October 2022
#

from Game import Game
from MENACE import MENACE
from Human import Human
from Player import Player
from time import time


def menaceVsMenace(iterations, menace1File: str | None = None, menace2File: str | None = None, size: int = 3) -> None:
    try:
        m1 = MENACE.fromFile(menace1File)
    except FileNotFoundError:
        m1 = MENACE(menace1File[:-4])
    try:
        m2 = MENACE.fromFile(menace2File)
    except FileNotFoundError:
        m2 = MENACE(menace2File[:-4])
    g = Game(m1, m2, size)
    for i in range(iterations):
        winner = g.playGame(gameLogs)
        m1.learn(winner)
        m2.learn(winner)
    m1.save(menace1File)
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

def main():
    readLogs(gameLogs)
    size = 5
    # humanVsHuman()
    rounds = 50

    start = time()
    menaceVsMenace(rounds, "5x5 MENACE Test 1.txt", "5x5 MENACE Test 2.txt", size)
    end = time()
    # human = Human("Gabe")
    # menace = MENACE.fromFile("Menace 2.txt")
    # humanVsMenace(human, menace)
    print()
    readLogs(gameLogs)
    print()
    print(f"Finished {rounds} games in {end - start} seconds!")


if __name__ == "__main__":
    main()
