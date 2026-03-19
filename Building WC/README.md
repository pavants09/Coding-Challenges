# Command Line Interface

`ccwc` is a simple Python utility that mimics basic behavior of the Unix `wc` command (word count). It can count lines, words, bytes, and characters in a file or from standard input.

## ✅ Features

- Count **lines** (`-l`)
- Count **words** (`-w`)
- Count **bytes** (`-c`)
- Count **characters** (`-m`)
- Default behavior (no option) prints: `lines words bytes <filename>`

## 🛠️ Setup

No compilation needed! Just ensure you have Python 3.6+ installed.

### Run directly

```bash
python ccwc.py <file>
```

Or make it executable:

```bash
chmod +x ccwc.py
./ccwc.py <file>
```

## ▶️ Usage

### Count lines, words, bytes, or chars for a file

```bash
python ccwc.py <file>
python ccwc.py -l <file>
python ccwc.py -w <file>
python ccwc.py -c <file>
python ccwc.py -m <file>
```

Example:

```bash
python ccwc.py -l test.txt
```

### Read from stdin (pipe)

```bash
cat test.txt | python ccwc.py -l
```

> Note: stdin mode only supports `-l`, `-w`, or `-c`.

## 📌 Exit Codes

- `0` - Success
- `1` - Usage error or failed to open file
