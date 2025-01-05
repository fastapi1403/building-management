import pytest
from src.utils.validators import validate_email, validate_phone

def test_email_validator():
    assert validate_email("test@example.com")
    with pytest.raises(ValueError):
        validate_email("invalid-email")
