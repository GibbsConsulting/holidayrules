"""Check holiday rule structure"""


import datetime
from holidayrules.rules import HolidayRule, new_year_no_obs, fixed_date_function


def test_simple_rule():
    "Check basic operation of a single simple rule."

    hr = HolidayRule("NYD", "New Year No Obs", new_year_no_obs)

    assert hr.name == 'NYD'
    assert hr.description == 'New Year No Obs'

    assert hr.fix_dates([2020]) == [(datetime.date(2020, 1, 1), None), ]


def test_function_formation():
    fdf = fixed_date_function(3, 4)
    assert fdf(2020) == (datetime.date(2020, 3, 4), None)
