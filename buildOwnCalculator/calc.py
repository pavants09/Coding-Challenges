import math
import re
import sys
from typing import List

OPERATORS = {
    '+': {'precedence': 2, 'associativity': 'left', 'arity': 2},
    '-': {'precedence': 2, 'associativity': 'left', 'arity': 2},
    '*': {'precedence': 3, 'associativity': 'left', 'arity': 2},
    '/': {'precedence': 3, 'associativity': 'left', 'arity': 2},
    '^': {'precedence': 4, 'associativity': 'right', 'arity': 2},
    'u+': {'precedence': 5, 'associativity': 'right', 'arity': 1},
    'u-': {'precedence': 5, 'associativity': 'right', 'arity': 1},
}

FUNCTIONS = {'sin', 'cos', 'tan'}
TOKEN_REGEX = re.compile(r"\s*(?:(\d+(?:\.\d+)?)|([A-Za-z_][A-Za-z0-9_]*)|(.))")


def tokenize(expression: str) -> List[str]:
    tokens: List[str] = []
    position = 0

    while position < len(expression):
        match = TOKEN_REGEX.match(expression, position)
        if not match:
            raise ValueError(f"Invalid expression at position {position}: {expression[position:]}")

        number, word, other = match.groups()
        position = match.end()

        if number:
            tokens.append(number)
            continue

        if word:
            lower = word.lower()
            if lower in FUNCTIONS:
                tokens.append(lower)
                continue
            raise ValueError(f"Unknown function or token: {word}")

        if other in '+-*/^(),':
            tokens.append(other)
            continue

        if other and other.isspace():
            continue

        raise ValueError(f"Unknown token: {other}")

    return tokens


def infix_to_postfix(tokens: List[str]) -> List[str]:
    output_queue: List[str] = []
    operator_stack: List[str] = []
    previous_token = None

    for token in tokens:
        if re.fullmatch(r"\d+(?:\.\d+)?", token):
            output_queue.append(token)
            previous_token = 'number'
            continue

        if token in FUNCTIONS:
            operator_stack.append(token)
            previous_token = 'function'
            continue

        if token == ',':
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            if not operator_stack:
                raise ValueError('Misplaced comma or mismatched parentheses')
            continue

        if token in OPERATORS:
            if previous_token in (None, 'operator', 'left_paren', 'function'):
                if token == '+':
                    token = 'u+'
                elif token == '-':
                    token = 'u-'

            while operator_stack:
                top = operator_stack[-1]
                if top == '(':
                    break

                if top in OPERATORS:
                    top_info = OPERATORS[top]
                    tok_info = OPERATORS[token]
                    if (tok_info['associativity'] == 'left' and tok_info['precedence'] <= top_info['precedence']) or (
                        tok_info['associativity'] == 'right' and tok_info['precedence'] < top_info['precedence']
                    ):
                        output_queue.append(operator_stack.pop())
                        continue
                if top in FUNCTIONS:
                    output_queue.append(operator_stack.pop())
                    continue
                break

            operator_stack.append(token)
            previous_token = 'operator'
            continue

        if token == '(':
            operator_stack.append(token)
            previous_token = 'left_paren'
            continue

        if token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            if not operator_stack:
                raise ValueError('Mismatched parentheses')
            operator_stack.pop()
            if operator_stack and operator_stack[-1] in FUNCTIONS:
                output_queue.append(operator_stack.pop())
            previous_token = 'right_paren'
            continue

        raise ValueError(f"Invalid token in expression: {token}")

    while operator_stack:
        top = operator_stack.pop()
        if top in ('(', ')'):
            raise ValueError('Mismatched parentheses')
        output_queue.append(top)

    return output_queue


def evaluate_rpn(tokens: List[str]) -> float:
    stack: List[float] = []

    for token in tokens:
        if re.fullmatch(r"\d+(?:\.\d+)?", token):
            stack.append(float(token))
            continue

        if token in OPERATORS:
            op_info = OPERATORS[token]
            arity = op_info['arity']
            if len(stack) < arity:
                raise ValueError('Malformed expression')

            if arity == 1:
                value = stack.pop()
                if token == 'u-':
                    stack.append(-value)
                else:
                    stack.append(value)
                continue

            right = stack.pop()
            left = stack.pop()

            if token == '+':
                stack.append(left + right)
            elif token == '-':
                stack.append(left - right)
            elif token == '*':
                stack.append(left * right)
            elif token == '/':
                if right == 0:
                    raise ValueError('Division by zero')
                stack.append(left / right)
            elif token == '^':
                stack.append(left ** right)
            else:
                raise ValueError(f'Unknown operator: {token}')
            continue

        if token in FUNCTIONS:
            if not stack:
                raise ValueError('Malformed expression')
            value = stack.pop()
            if token == 'sin':
                stack.append(math.sin(value))
            elif token == 'cos':
                stack.append(math.cos(value))
            elif token == 'tan':
                stack.append(math.tan(value))
            else:
                raise ValueError(f'Unknown function: {token}')
            continue

        raise ValueError(f"Unknown RPN token: {token}")

    if len(stack) != 1:
        raise ValueError('Malformed expression')

    return stack[0]


def evaluate_expression(expression: str) -> float:
    tokens = tokenize(expression)
    postfix = infix_to_postfix(tokens)
    return evaluate_rpn(postfix)


def format_result(value: float) -> str:
    if value.is_integer():
        return str(int(value))
    return str(value)


def main() -> None:
    if len(sys.argv) < 2:
        print('Usage: python calc.py "<expression>"')
        sys.exit(1)

    expression = ' '.join(sys.argv[1:])
    try:
        result = evaluate_expression(expression)
        print(format_result(result))
    except ValueError as exc:
        print(f'Error: {exc}')
        sys.exit(1)


if __name__ == '__main__':
    main()
