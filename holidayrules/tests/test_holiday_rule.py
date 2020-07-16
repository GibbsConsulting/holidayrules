"""Check holiday rule structure"""


import datetime
from holidayrules.rules import (HolidayRule, new_year_no_obs, fixed_date_function,
                                adjust_weekend_to_monday, adjust_weekend_both_ways,
                                wrap_adjustment_function,
                                exclude_years_wrapper,
                                fixed_date_roll_forward, fixed_date_roll_both,
                                fixed_date_no_roll, new_year_roll_back,
                                easter_western, easter_orthodox,
                                good_friday_western,
                                christmas_day, boxing_day,
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

    assert independence_day(2020) == (datetime.date(2020, 7, 3), 'Observed')
    assert independence_day(2021) == (datetime.date(2021, 7, 5), 'Observed')
    assert independence_day(2022) == (datetime.date(2022, 7, 4), None)

    indep_ex_none = exclude_years_wrapper(independence_day)
    indep_ex_2021 = exclude_years_wrapper(independence_day, [2021])
    indep_ex_202x = exclude_years_wrapper(independence_day, [2020, 2022])
    indep_ny_ex21 = exclude_years_wrapper(new_year_uk, [2021])

    assert indep_ex_none(2020) == (datetime.date(2020, 7, 3), 'Observed')
    assert indep_ex_none(2021) == (datetime.date(2021, 7, 5), 'Observed')
    assert indep_ex_none(2022) == (datetime.date(2022, 7, 4), None)

    assert indep_ex_2021(2020) == (datetime.date(2020, 7, 3), 'Observed')
    assert indep_ex_2021(2021) == (None, None)
    assert indep_ex_2021(2022) == (datetime.date(2022, 7, 4), None)

    assert indep_ex_202x(2020) == (None, None)
    assert indep_ex_202x(2021) == (datetime.date(2021, 7, 5), 'Observed')
    assert indep_ex_202x(2022) == (None, None)

    assert indep_ny_ex21(2020) == (datetime.date(2020, 1, 1), None)
    assert indep_ny_ex21(2021) == (None, None)
    assert indep_ny_ex21(2022) == (datetime.date(2022, 1, 3), 'Observed')


def test_fixed_date_functions():
    """Test fix date functions"""
    ny_fwd = fixed_date_roll_forward(1, 1)
    ny_both = fixed_date_roll_both(1, 1)
    ny_none = fixed_date_no_roll(1, 1)

    assert ny_fwd(2016) == (datetime.date(2016, 1, 1), None)
    assert ny_fwd(2021) == (datetime.date(2021, 1, 1), None)
    assert ny_fwd(2017) == (datetime.date(2017, 1, 2), 'Observed')
    assert ny_fwd(2022) == (datetime.date(2022, 1, 3), 'Observed')
    assert ny_fwd(2023) == (datetime.date(2023, 1, 2), 'Observed')

    assert ny_both(2016) == (datetime.date(2016, 1, 1), None)
    assert ny_both(2021) == (datetime.date(2021, 1, 1), None)
    assert ny_both(2017) == (datetime.date(2017, 1, 2), 'Observed')
    assert ny_both(2022) == (datetime.date(2021, 12, 31), 'Observed')
    assert ny_both(2023) == (datetime.date(2023, 1, 2), 'Observed')

    assert ny_none(2016) == (datetime.date(2016, 1, 1), None)
    assert ny_none(2017) == (datetime.date(2017, 1, 1), None)
    assert ny_none(2021) == (datetime.date(2021, 1, 1), None)
    assert ny_none(2022) == (datetime.date(2022, 1, 1), None)
    assert ny_none(2023) == (datetime.date(2023, 1, 1), None)

    assert new_year_roll_back(2016) == (None, None)
    assert new_year_roll_back(2017) == (None, None)
    assert new_year_roll_back(2022) == (None, None)
    assert new_year_roll_back(2021) == (datetime.date(2021, 12, 31), 'Observed')


def test_easter():
    """Test Easter rules: monday and good friday"""

    assert easter_western(2020) == (datetime.date(2020, 4, 13), None)
    assert good_friday_western(2020) == (datetime.date(2020, 4, 10), None)
    assert easter_orthodox(2020) == (datetime.date(2020, 4, 20), None)


def test_xmas():
    """Check Christmas and Boxing day rules"""

    assert christmas_day(2019) == (datetime.date(2019, 12, 25), None)
    assert christmas_day(2020) == (datetime.date(2020, 12, 25), None)
    assert christmas_day(2021) == (datetime.date(2021, 12, 27), 'Observed') # Sat to Mon
    assert christmas_day(2022) == (datetime.date(2022, 12, 27), 'Observed') # Sun to Tue, skip over boxing on Mon
    assert christmas_day(2023) == (datetime.date(2023, 12, 25), None)

    assert boxing_day(2019) == (datetime.date(2019, 12, 26), None)
    assert boxing_day(2020) == (datetime.date(2020, 12, 28), 'Observed') # Sat to Mon
    assert boxing_day(2021) == (datetime.date(2021, 12, 28), 'Observed') # Sun to Tue, skip over Xmas on Mon
    assert boxing_day(2022) == (datetime.date(2022, 12, 26), None)
    assert boxing_day(2023) == (datetime.date(2023, 12, 26), None)


def test_exclude_years():
    """Check exclusion of years"""

    exclude2122 = exclude_years_wrapper(christmas_day, [2021, 2022])

    assert exclude2122(2020) == (datetime.date(2020, 12, 25), None)
    assert exclude2122(2019) == (datetime.date(2019, 12, 25), None)
    assert exclude2122(2023) == (datetime.date(2023, 12, 25), None)

    assert exclude2122(2021) == (None, None)
    assert exclude2122(2022) == (None, None)
