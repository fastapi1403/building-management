import pytest
from src.utils.validators import validate_national_id, validate_phone_number

def test_validate_national_id():
    assert validate_national_id("1234567890")
    assert not validate_national_id("123")

def test_validate_phone_number():
    assert validate_phone_number("+989123456789")
    assert not validate_phone_number("123")
