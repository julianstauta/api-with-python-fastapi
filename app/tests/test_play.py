import pytest

def func(x):
    return x + 1

def test_answer():
    assert func(3) == 4

def test_one():
    x = "this"
    assert "h" in x

def test_two():
    x = "hello"
    assert hasattr(x, "check") == False