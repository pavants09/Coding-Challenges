import sys

def extract_token(data):
    tokens = []
    i = 0

    while i < len(data):
        ch = data[i]

        if ch in ['{', '}', ':', ',']:
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

        # true
        elif data[i:i+4] == "true":
            tokens.append(("BOOLEAN", True))
            i += 3

        # false
        elif data[i:i+5] == "false":
            tokens.append(("BOOLEAN", False))
            i += 4

        # null
        elif data[i:i+4] == "null":
            tokens.append(("NULL", None))
            i += 3

        # invalid (case-sensitive)
        elif data[i:i+5] == "False":
            return None

        # number
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


def parse_json(tokens):
    if not tokens or tokens[0] != '{' or tokens[-1] != '}':
        return False
    
    i = 1

    while i < len(tokens) - 1:

        # key must be string
        if not isinstance(tokens[i], tuple) or tokens[i][0] != "STRING":
            return False
        i += 1

        # colon
        if tokens[i] != ':':
            return False
        i += 1

        # value types
        if not isinstance(tokens[i], tuple) or tokens[i][0] not in ["STRING", "NUMBER", "BOOLEAN", "NULL"]:
            return False
        i += 1

        # comma or end
        if tokens[i] == ',':
            i += 1
        elif tokens[i] == '}':
            return True
        else:
            return False

    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python step3jsonparser.py <file>")
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