# reads the requested files and asserts that there aren't any duplicate matchboxes
menacesFile = "../Menaces.txt"
with open(menacesFile, "r") as infile:
    fnames = infile.readlines()
for fname in fnames:
    fname = fname.strip()
    try:
        with open(fname, "r") as infile:
            lines = infile.readlines()
            for i in range(len(lines)):
                board1 = lines[i].split(";")[0]
                for j in range(i + 1, len(lines)):
                    board2 = lines[j].split(";")[0]
                    try:
                        assert board1 != board2
                    except AssertionError:
                        print(f"line {i} of {fname}: {board1}")
                        print(f"line {j} of {fname}: {board2}")
        print(f"Finished checking {fname}")
    except FileNotFoundError:
        pass
