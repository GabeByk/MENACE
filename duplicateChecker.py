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
                for j in range(i + 1, len(lines)):
                    try:
                        assert lines[i][0:9] != lines[j][0:9]
                    except AssertionError:
                        print(f"line {i} of {fname}: {lines[i][0:9]}")
                        print(f"line {j} of {fname}: {lines[j][0:9]}")
        print(f"Finished checking {fname}")
    except FileNotFoundError:
        pass
