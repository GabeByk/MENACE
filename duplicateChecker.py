# reads the requested files and asserts that there aren't any duplicate matchboxes
from Board import Board
menacesFile = "../Menaces.txt"
with open(menacesFile, "r") as infile:
    fnames = infile.readlines()
for fname in fnames:
    fname = fname.strip()
    try:
        with open(fname, "r") as infile:
            lines = infile.readlines()
            for i in range(len(lines)):
                print(i)
                board1 = lines[i].split(";")[0]
                actualBoard1 = Board(int(len(board1) ** 0.5))
                actualBoard1._grid = [board1[i] for i in range(len(board1))]
                for j in range(i + 1, len(lines)):
                    board2 = lines[j].split(";")[0]
                    actualBoard2 = Board(int(len(board2) ** 0.5))
                    actualBoard2._grid = [board2[i] for i in range(len(board2))]
                    try:
                        assert board1 != board2
                    except AssertionError:
                        print(f"line {i} of {fname}: {board1}")
                        print(f"line {j} of {fname}: {board2}")
                    try:
                        assert not actualBoard1.isEquivalentTo(actualBoard2)
                    except AssertionError:
                        print(f"line {i} of {fname}: {board1}")
                        print(f"line {j} of {fname}: {board2}")
        print(f"Finished checking {fname}")
    except FileNotFoundError:
        pass
