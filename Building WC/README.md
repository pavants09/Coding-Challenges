# Command Line Interface

`ccwc` is a small, single-file C++ utility that mimics basic behavior of the Unix `wc` command (word count). It can count lines, words, bytes, and characters in a file or from standard input.

## ✅ Features

- Count **lines** (`-l`)
- Count **words** (`-w`)
- Count **bytes** (`-c`)
- Count **characters** (`-m`)
- Default behavior (no option) prints: `lines words bytes <filename>`

## 🛠️ Build

From the project folder, compile with `g++`:

```sh
g++ ccwc.cpp -o ccwc
```

## ▶️ Usage

### Count lines, words, bytes, or chars for a file

```sh
./ccwc <file>
./ccwc -l <file>
./ccwc -w <file>
./ccwc -c <file>
./ccwc -m <file>
```

Example:

```sh
./ccwc -l test.txt
```

### Read from stdin (pipe)

```sh
cat test.txt | ./ccwc -l
```

> Note: stdin mode only supports `-l`, `-w`, or `-c`.

## 📌 Exit Codes

- `0` - Success
- `1` - Usage error or failed to open file
