import sys

def print_data(data, delimiter):
    for line in data:
        print(delimiter.join(line))

def main():
    if len(sys.argv) < 3:
        print("Usage: python cuttool.py -f<fields> [-d<delimiter>] <file>")
        sys.exit(1)

    delimiter = '\t'   
    fields_arg = None
    filename = None

    # Parse arguments
    for arg in sys.argv[1:]:
        if arg.startswith('-f'):
            fields_arg = arg[2:]
        elif arg.startswith('-d'):
            delimiter = arg[2:]
        else:
            filename = arg

    if not fields_arg or not filename:
        print("Invalid arguments")
        sys.exit(1)

    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except:
        print("Error reading file")
        sys.exit(1)

    required_fields = [int(x) - 1 for x in fields_arg.split(',')]

    output_data = []

    for line in lines:
        data = line.rstrip('\n').split(delimiter)
        temp = []

        for idx in required_fields:
            if idx < len(data):
                temp.append(data[idx])
            else:
                temp.append("")  

        output_data.append(temp)

    print_data(output_data, delimiter)


if __name__ == "__main__":
    main()