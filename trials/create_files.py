def main():

    f1 = open("files.txt", "r")

    for line in f1:
        f2 = open(line.rstrip(), "x")
        f2.write("~\n")
main()