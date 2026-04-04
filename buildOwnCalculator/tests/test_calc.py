import pytest

from calc import evaluate_expression


def test_simple_addition():
    assert evaluate_expression('1 + 2') == 3


def test_simple_subtraction():
    assert evaluate_expression('2 - 1') == 1


def test_simple_multiplication():
    assert evaluate_expression('2 * 3') == 6


def test_simple_division():
    assert evaluate_expression('3 / 2') == 1.5


def test_mixed_precedence():
    assert evaluate_expression('1 + 1 * 5') == 6


def test_parentheses_precedence():
    assert evaluate_expression('(1 + 1) * 5') == 10


def test_division_with_parentheses():
    assert evaluate_expression('10 / (6 - 1)') == 2


def test_unary_minus():
    assert evaluate_expression('-3 + 5') == 2


def test_functions():
    assert pytest.approx(evaluate_expression('sin(0)'), rel=1e-9) == 0
    assert pytest.approx(evaluate_expression('cos(0)'), rel=1e-9) == 1
    assert pytest.approx(evaluate_expression('tan(0)'), rel=1e-9) == 0


def test_nested_expression():
    assert evaluate_expression('2 * (3 + 4) - 5') == 9
