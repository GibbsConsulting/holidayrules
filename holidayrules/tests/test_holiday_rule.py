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

    new_year_uk = wrap_adjustment_function(fixed_date_function(1, 1),
                                           adjust_weekend_to_monday)
    assert new_year_uk is not None
    assert new_year_uk(2020) == (datetime.date(2020, 1, 1), None)
    assert new_year_uk(2015) == (datetime.date(2015, 1, 1), None)
    assert new_year_uk(2018) == (datetime.date(2018, 1, 1), None)
    assert new_year_uk(2016) == (datetime.date(2016, 1, 1), None)
    assert new_year_uk(2017) == (datetime.date(2017, 1, 2), 'Observed')
    assert new_year_uk(2022) == (datetime.date(2022, 1, 3), 'Observed')
    assert new_year_uk(2023) == (datetime.date(2023, 1, 2), 'Observed')
