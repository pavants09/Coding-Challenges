import sys
from collections import defaultdict
import heapq

class Node :
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq
    

def build_huffman_tree(freq):
    heap = []
    for char, count in freq.items():
        heapq.heappush(heap, Node(char, count))

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(heap, merged)

    return heap[0] if heap else None

def generate_codes(node, prefix="", code_map={}):
    if node is not None:
        if node.char is not None:
            code_map[node.char] = prefix
        generate_codes(node.left, prefix + "0", code_map)
        generate_codes(node.right, prefix + "1", code_map)
    return code_map



def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    freq = defaultdict(int)

    try :
        with open(filename,'r') as f:
            while True :
                chunk = f.read(1024)
                if not chunk:
                    break
                for ch in chunk:
                    freq[ch] += 1

            
    except:
        print("Error reading file")
        sys.exit(1)

    
    # print("Character frequencies Table :")
    # for char,count in sorted(freq.items()):
    #     if char == '\n':
    #         display_char = '\\n'
    #     elif char == '\t':
    #         display_char = '\\t'
    #     elif char == ' ':
    #         display_char = 'space'
    #     else:
    #         display_char = char
    #     print(f"'{display_char}': {count}") 

    
    # # Example checks
    # print("\nSample Checks:")
    # print(f"Occurrences of 'X': {freq.get('X', 0)}")
    # print(f"Occurrences of 't': {freq.get('t', 0)}")
    # return 0

    # Build Huffman Tree
    root = build_huffman_tree(freq)

    # Generate Huffman Codes
    codes = generate_codes(root)

    print("\nHuffman Codes:")
    for char, code in sorted(codes.items()):
        if char == '\n':
            display_char = '\\n'
        elif char == '\t':
            display_char = '\\t'
        elif char == ' ':
            display_char = 'space'
        else:
            display_char = char
        print(f"'{display_char}': {code}")

    # Example checks
    print("\nSample Checks:")
    print(f"Occurrences of 'X': {freq.get('X', 0)}")
    print(f"Occurrences of 't': {freq.get('t', 0)}")


if __name__ == "__main__":
    main()