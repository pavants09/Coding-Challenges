import sys

def extract_token(data):
    tokens = []
    if not data.strip():
        return None
    
    for ch in data:
        if ch == '{':
            tokens.append('{')
        elif ch == '}':
            tokens.append('}')
        elif ch.isspace():
            continue
        else:
            return None
    
    return tokens
    
def parse_json(token):
    if token[0] == "{" and token[-1] == "}":
        return True
    return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python jsonparser.py <file>")
        sys.exit(1)
    
    try :
        with open(sys.argv[1],'r') as f:
            content = f.read()
    except:
        print("Error reading file")
        sys.exit(1)
    
    
    token = extract_token(content)
    
    if token is None:
        print("Invalid JSON")
        sys.exit(1)     

    if parse_json(token):
        print("Valid JSON")
        sys.exit(0)
    else:
        print("Invalid JSON")   
        sys.exit(1)

if __name__ == "__main__":
    main()