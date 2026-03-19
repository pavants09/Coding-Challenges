import sys

def extract_token(data):
    tokens = []
    i = 0

    while i < len(data):
        ch = data[i]

        if ch in ['{', '}', ':', ',', '[', ']']:
            tokens.append(ch)

        elif ch.isspace():
            pass

        elif ch == '"':
            i += 1
            start = i
            while i < len(data) and data[i] != '"':
                i += 1
            if i >= len(data):
                return None
            tokens.append(("STRING", data[start:i]))

        elif data[i:i+4] == "true":
            tokens.append(("BOOLEAN", True))
            i += 3

        elif data[i:i+5] == "false":
            tokens.append(("BOOLEAN", False))
            i += 4

        elif data[i:i+4] == "null":
            tokens.append(("NULL", None))
            i += 3

        elif ch.isdigit():
            start = i
            while i < len(data) and data[i].isdigit():
                i += 1
            tokens.append(("NUMBER", int(data[start:i])))
            i -= 1

        else:
            return None

        i += 1

    return tokens


def parse_value(tokens, i):
    tok = tokens[i]

    if isinstance(tok, tuple):
        return i + 1

    if tok == '{':
        return parse_object(tokens, i)

    if tok == '[':
        return parse_array(tokens, i)

    return None


def parse_object(tokens, i):
    if tokens[i] != '{':
        return None

    i += 1
    if tokens[i] == '}':
        return i + 1

    while True:
        if not isinstance(tokens[i], tuple) or tokens[i][0] != "STRING":
            return None
        i += 1

        if tokens[i] != ':':
            return None
        i += 1

        i = parse_value(tokens, i)
        if i is None:
            return None

        if tokens[i] == ',':
            i += 1
        elif tokens[i] == '}':
            return i + 1
        else:
            return None


def parse_array(tokens, i):
    if tokens[i] != '[':
        return None

    i += 1

    if tokens[i] == ']':
        return i + 1

    while True:
        i = parse_value(tokens, i)
        if i is None:
            return None

        if tokens[i] == ',':
            i += 1
        elif tokens[i] == ']':
            return i + 1
        else:
            return None


def parse_json(tokens):
    if not tokens:
        return False

    i = parse_object(tokens, 0)
    return i == len(tokens)


def main():
    if len(sys.argv) < 2:
        print("Usage: python step4jsonparser.py <file>")
        sys.exit(1)

    try:
        with open(sys.argv[1], 'r') as f:
            content = f.read()
    except:
        print("Error reading file")
        sys.exit(1)

    tokens = extract_token(content)

    if tokens is None:
        print("Invalid JSON")
        sys.exit(1)

    if parse_json(tokens):
        print("Valid JSON")
        sys.exit(0)
    else:
        print("Invalid JSON")
        sys.exit(1)


if __name__ == "__main__":
    main()