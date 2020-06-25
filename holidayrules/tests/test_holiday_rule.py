"""Check holiday rule structure"""


import datetime
from holidayrules.rules import (HolidayRule, new_year_no_obs, fixed_date_function,
                                adjust_weekend_to_monday, adjust_weekend_both_ways,
                                wrap_adjustment_function,
                                )


def test_simple_rule():
    "Check basic operation of a single simple rule."

    hr = HolidayRule("NYD", "New Year No Obs", new_year_no_obs)

    assert hr.name == 'NYD'
    assert hr.description == 'New Year No Obs'

    assert hr.fix_dates([2020]) == [(datetime.date(2020, 1, 1), None), ]


def test_function_formation():
    fdf = fixed_date_function(3, 4)
    assert fdf(2020) == (datetime.date(2020, 3, 4), None)

    independence_day = wrap_adjustment_function(fixed_date_function(7, 4),
                                                adjust_weekend_both_ways)
    assert independence_day is not None
    assert independence_day(2020) == (datetime.date(2020, 7, 3), 'Observed')
    assert independence_day(2021) == (datetime.date(2021, 7, 5), 'Observed')
    assert independence_day(2022) == (datetime.date(2022, 7, 4), None)
