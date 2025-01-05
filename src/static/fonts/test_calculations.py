import pytest
from decimal import Decimal
from src.utils.calculations import calculate_total_area, calculate_monthly_charge

def test_calculate_total_area():
    areas = [Decimal("100.5"), Decimal("150.75"), Decimal("200.25")]
    assert calculate_total_area(areas) == Decimal("451.50")

def test_calculate_monthly_charge():
    area = Decimal("100.5")
    rate = Decimal("10000")
    assert calculate_monthly_charge(area, rate) == Decimal("1005000")
