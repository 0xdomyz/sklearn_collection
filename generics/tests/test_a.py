def func(x):
    return x + 1


def test_answer():
    assert func(4) == 5


import pytest


def f():
    raise SystemExit(1)


def test_mytest():
    with pytest.raises(SystemExit):
        f()
