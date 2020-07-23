"""Test ruleset"""


import datetime


from holidayrules.ruleset import RuleSet
from holidayrules.rules import (HolidayRule, fixed_date_function, adjust_weekend_to_monday,
                                wrap_adjustment_function,
                                fixed_date_roll_forward, fixed_date_roll_both,
                                new_year_roll_back,
                                )


def test_ruleset():
    """Check basic ruleset formation and operation"""
    rules = [HolidayRule('NewYears',
                         'New years day',
                         wrap_adjustment_function(fixed_date_function(1, 1),
                                                  adjust_weekend_to_monday)),
             HolidayRule("IndependenceDay",
                         "Independence day",
                         wrap_adjustment_function(fixed_date_function(7, 4),
                                                  adjust_weekend_to_monday)),
    ]

    hrs = RuleSet(rules)

    hfy2020 = hrs.dates_for_year(2020)
    assert len(hfy2020) == 2
    assert "20200101" in hfy2020
    assert "20200706" in hfy2020

    hfy2019 = hrs.dates_for_year(2019)
    assert len(hfy2019) == 2
    assert "20190101" in hfy2019
    assert "20190704" in hfy2019

    rs2 = hrs.dates_for_year(2020)
    assert rs2 == hfy2020

    dfy = hrs.dates_for_years([2020, 2021])
    assert len(dfy) == 4
    assert '20200101' in dfy
    assert '20200706' in dfy
    assert '20210101' in dfy
    assert '20210705' in dfy

    dmy_explicit = hrs.values_by_ymd(dfy)
    assert len(dmy_explicit) == len(dfy)
    assert dmy_explicit[0]['date_string'] == '20200101'
    assert dmy_explicit[0]['holiday'] == 'NewYears'
    assert dmy_explicit[0]['year'] == 2020
    assert dmy_explicit[0]['month'] == 1
    assert dmy_explicit[0]['day'] == 1
    assert dmy_explicit[3]['date_string'] == '20210705'
    assert dmy_explicit[3]['holiday'] == 'IndependenceDay [Observed]'
    assert dmy_explicit[3]['year'] == 2021
    assert dmy_explicit[3]['month'] == 7
    assert dmy_explicit[3]['day'] == 5


def test_no_holiday():
    """Check rule that returns None"""

    rules = [HolidayRule("New year, rolling back",
                         "New year rolling backwards if a Saturday",
                         new_year_roll_back),
             HolidayRule("New year, rolling forwards on sunday",
                         "NY2",
                         fixed_date_roll_both(1, 1)),
             HolidayRule("Canada Day",
                         "First of July",
                         fixed_date_roll_forward(7, 1)),
             ]
    hrs = RuleSet(rules)

    hfy19 = hrs.dates_for_year(2019)
    hfy20 = hrs.dates_for_year(2020)
    hfy21 = hrs.dates_for_year(2021)
    hfy22 = hrs.dates_for_year(2022)

    assert len(hfy19) == 2
    assert len(hfy20) == 2
    assert len(hfy21) == 3
    assert len(hfy22) == 1

    print(hfy21)

    assert hrs.is_good_day(datetime.date(2021, 12, 30))
    assert hrs.is_good_day(datetime.date(2021, 12, 24))
    assert hrs.is_good_day(datetime.date(2021, 2, 5))
    assert hrs.is_good_day(datetime.date(2021, 2, 8))

    assert not hrs.is_good_day(datetime.date(2021, 1, 1))
    assert not hrs.is_good_day(datetime.date(2021, 7, 1))
    assert not hrs.is_good_day(datetime.date(2021, 12, 31))
    assert not hrs.is_good_day(datetime.date(2021, 12, 25))
    assert not hrs.is_good_day(datetime.date(2021, 2, 6))
    assert not hrs.is_good_day(datetime.date(2021, 2, 7))


