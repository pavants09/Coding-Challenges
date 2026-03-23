# Huffman Compression Tool

A simple Python implementation of Huffman coding for text compression. This tool analyzes a given text file, calculates character frequencies, builds a Huffman tree, and generates Huffman codes for each character.

## Features

- Reads any text file and computes character frequency distribution
- Builds a Huffman tree based on character frequencies
- Generates optimal prefix codes (Huffman codes) for compression
- Displays the Huffman codes for each character
- Includes sample checks for specific characters ('X' and 't')

## Requirements

- Python 3.x
- No external dependencies (uses only standard library modules: `sys`, `collections`, `heapq`)

## Usage

Run the script from the command line with a text file as an argument:

```bash
python main.py <filename>
```

Replace `<filename>` with the path to your text file.

### Example

```bash
python main.py test.txt
```

This will output the Huffman codes for each character in `test.txt`, along with sample occurrence counts for 'X' and 't'.

## Output

The tool prints:
- Huffman codes for each character (sorted alphabetically)
- Sample checks showing occurrences of 'X' and 't' in the file

Special characters are displayed as:
- Newline: `\n`
- Tab: `\t`
- Space: `space`

## How It Works

1. **Frequency Calculation**: Reads the input file in chunks and counts the frequency of each character.
2. **Tree Building**: Uses a priority queue (heap) to build the Huffman tree by repeatedly combining the two nodes with the lowest frequencies.
3. **Code Generation**: Traverses the tree to assign binary codes (0 for left, 1 for right) to each character.

## Limitations

- Currently only generates and displays Huffman codes; does not perform actual compression/decompression.
- Assumes UTF-8 encoding for text files.
- Does not handle binary files.

## Contributing

Feel free to extend the functionality, such as adding compression and decompression features.

## License

This project is open-source. Use at your own discretion.