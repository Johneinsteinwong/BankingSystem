import pytest
from utils import convert_decimal
from decimal import Decimal

# Convert valid numbers
def test_convert_decimal_valid():
    res = convert_decimal('123.456')
    assert res == Decimal('123.456')

# Convert valid zero
def test_convert_decimal_zero():
    result = convert_decimal('0')
    assert result == Decimal('0')

# Non-number 'abc' should raise ValueError
def test_convert_decimal_non_numeric():
    with pytest.raises(ValueError, match="Invalid input, please input numbers only!"):
        convert_decimal('abc')

# We don't allow deposit/withdraw/transfer NaN or Infinity amount of money
# 'NaN' should raise ValueError
def test_convert_decimal_nan():
    with pytest.raises(ValueError, match="Invalid input, please input numbers only!"):
        convert_decimal("NaN")

# 'Infinity' should raise ValueError
def test_convert_decimal_infinity():
    with pytest.raises(ValueError, match="Invalid input, please input numbers only!"):
        convert_decimal("Infinity")