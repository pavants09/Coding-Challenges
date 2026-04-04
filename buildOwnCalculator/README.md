# Build Your Own Calculator

A command-line calculator that parses mathematical expressions and evaluates them using the shunting yard algorithm and Reverse Polish Notation (RPN).

## Features

- Supports `+`, `-`, `*`, `/`, `^`
- Handles parentheses for precedence
- Supports unary `-` and unary `+`
- Supports `sin()`, `cos()`, and `tan()` functions
- Preserves integer output when the result is whole

## Run

```bash
python calc.py '2 * 3 + 4'
```

## Tests

```bash
pip install pytest
pytest
```
