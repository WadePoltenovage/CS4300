import pytest
from task4 import calculate_discount

def test_calculate_discount_with_integers():
    assert calculate_discount(100, 10) == 90.0

def test_calculate_discount_with_floats():
    assert calculate_discount(250.75, 15.5) == pytest.approx(211.88375)

def test_calculate_discount_with_mixed_types():
    assert calculate_discount(75.50, 20) == pytest.approx(60.40)
    assert calculate_discount(200, 5.25) == 189.50

def test_calculate_discount_with_zero_discount():
    assert calculate_discount(500, 0) == 500.0

def test_calculate_discount_with_zero_price():
    assert calculate_discount(0, 25) == 0.0