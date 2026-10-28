import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from logic import get_recommendations, run_projection


def test_monthly_surplus_is_added_twelve_times_a_year():
    # 30k income, 20k expenses a month, 50k saved, no growth, no return
    assert run_projection(30000, 20000, 50000, 1, 0, 0, 0) == [170000.0]


def test_two_years_without_growth_is_linear():
    assert run_projection(30000, 20000, 0, 2, 0, 0, 0) == [120000.0, 240000.0]


def test_investment_return_compounds_on_the_year_end_balance():
    assert run_projection(0, 0, 1000, 2, 0, 0, 10) == [1100.0, 1210.0]


def test_income_growth_applies_before_saving():
    out = run_projection(10000, 10000, 0, 1, 10, 0, 0)  # income 11,000 vs expenses 10,000
    assert out == [12000.0]


def test_negative_surplus_reduces_savings():
    assert run_projection(10000, 12000, 50000, 1, 0, 0, 0) == [26000.0]


def test_recommendations():
    tips = get_recommendations(income=30000, expenses=29000, savings=1000)
    assert any("80%" in t for t in tips) and any("emergency fund" in t for t in tips)
    assert any("saving well" in t for t in get_recommendations(30000, 10000, 100000))
    assert any("exceed income" in t for t in get_recommendations(10000, 12000, 100000))
