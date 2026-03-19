import sys

def extract_token(data):
    token = []
    
    i = 0

    while i < len(data):
        ch = data[i].strip()

        if ch in ['{', '}', ':',','] :
            token.append(ch)
        
        elif ch.isspace():
            pass
        
        elif ch == '"':
            i += 1
            starting = i

            while i < len(data) and data[i] != '"':
                i += 1
            
            if i >= len(data):
                return None
            
            token.append(data[starting:i])
        
        i += 1
    return token


def parse_json(token):
    if not token or token[0] != '{' or token[-1] != '}':
        return False
    
    i = 1

    while i < len(token) - 1:
        if not isinstance(token[i],str) or token[i] in ['{', '}', ':',',']:
            return False
        i += 1

        if token[i] != ':':
            return False
        i += 1

        if not isinstance(token[i],str) or token[i] in ['{', '}', ':',',']:
            return False
        i += 1

        if token[i] == ',' :
            i += 1
        elif token[i] == '}':
            i += 1
        else:
            return False
    return True

def main():
    if len(sys.argv) < 2 :
        print("Usage: python ccwc.py <file>")
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

if __name__ == "__main__" :
    main()