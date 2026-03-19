import sys

# Count bytes
def count_bytes(f):
    f.seek(0, 2) 
    return f.tell()

# Count lines
def count_lines(f):
    count = 0
    for _ in f:
        count += 1
    return count

# Count words
def count_words(f):
    count = 0
    for line in f:
        count += len(line.split())
    return count

# Count characters
def count_chars(f):
    count = 0
    while True:
        chunk = f.read(1024)
        if not chunk:
            break
        count += len(chunk)
    return count


def main():
    args = sys.argv

    option = ""
    filename = ""

    if len(args) == 2:
        filename = args[1]

    elif len(args) == 3:
        option = args[1]
        filename = args[2]

    elif len(args) == 2 and args[1].startswith("-"):
        option = args[1]

    elif len(args) > 3:
        print("Usage:")
        print("  ccwc -c|-l|-w|-m <file>")
        print("  ccwc <file>")
        return

    if filename == "":
        data = sys.stdin.read()

        if option == "-l":
            print(data.count("\n"))
        elif option == "-w":
            print(len(data.split()))
        elif option == "-c":
            print(len(data.encode()))
        elif option == "-m":
            print(len(data))
        else:
            print("Invalid usage with stdin")
        return

    try:
        if option == "-c":
            with open(filename, "rb") as f:
                print(len(f.read()), filename)

        elif option == "-l":
            with open(filename, "r", encoding="utf-8") as f:
                print(count_lines(f), filename)

        elif option == "-w":
            with open(filename, "r", encoding="utf-8") as f:
                print(count_words(f), filename)

        elif option == "-m":
            with open(filename, "r", encoding="utf-8") as f:
                print(count_chars(f), filename)

        # default (no option)
        elif option == "":
            with open(filename, "r", encoding="utf-8") as f:
                lines = count_lines(f)

            with open(filename, "r", encoding="utf-8") as f:
                words = count_words(f)

            with open(filename, "rb") as f:
                bytes_count = len(f.read())

            print(lines, words, bytes_count, filename)

        else:
            print("Unsupported option")

    except FileNotFoundError:
        print("Error opening file")


if __name__ == "__main__":
    main()