import aiden.mathlib

def test_add_up():
    assert aiden.mathlib.add_up(1, 2) == 3

def test_subtract():
    assert aiden.mathlib.subtract(3, 2) == 1

def test_calculate_area_circle():
    assert aiden.mathlib.calculate_area_circle(2) == round(12.566370614359172, 4)
