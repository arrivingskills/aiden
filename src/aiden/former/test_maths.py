import aiden.former.maths

def test_addup():
    assert aiden.former.maths.addup(1, 2) == 3

def test_subtract():
    assert aiden.former.maths.subtract(3, 2) == 1

def test_multiply():
    assert aiden.former.maths.multiply(2, 3) == 6

def test_divide():
    assert aiden.former.maths.divide(6, 3) == 2

def test_power():
    assert aiden.former.maths.power(2, 3) == 8

def test_square_root():
    assert aiden.former.maths.square_root(9) == 3
