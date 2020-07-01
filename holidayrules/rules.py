"""Holiday rules
"""


from dataclasses import dataclass
from datetime import date, timedelta
from functools import partial
from typing import Callable, List, Tuple

from dateutil.easter import easter, EASTER_ORTHODOX, EASTER_WESTERN
from dateutil.relativedelta import relativedelta


@dataclass(frozen=True)
class HolidayRule:
    """A single holiday rule"""

    name: str
    description: str
    rule: Callable[[int], Tuple[date, str]]  # Signature is year to (holday, optional extra desc)

    def fix_dates(self, years: List[int]) -> List[Tuple[date, str]]:
        """Return an array of holiday dates, one entry per year in the input vector.

        Each entry is a datetime.date instance, along with an optional second entry.
        If the second entry is not None, then its content describes how
        the date differs fron the normal holiday. The canonical use of this is to
        indicate an observed holiday.
        """
        return [self.rule(year) for year in years]


def new_year_no_obs(year: int) -> Tuple[date, str]:
    """New year, without any observation"""
    return date(year=year, month=1, day=1), None


def fixed_date_no_obs(year: int, month: int, day: int) -> Tuple[date, str]:
    """FIxed date, with no adjustment"""
    return date(year=year, month=month, day=day), None


def adjust_weekend_to_monday(idate, isadj):
    """Adjust weekend date forward to monday if need be"""
    wd = idate.weekday()

    if wd > 4:
        # Saturday or sunday
        return idate + timedelta(days=7 - wd), 'Observed'

    return idate, isadj


def adjust_weekend_both_ways(idate, isadj):
    """Adjust weekend date forward to monday from sunday, backward to friday if saturday"""
    wd = idate.weekday()

    if wd == 5:
        # Saturday or sunday
        return idate - timedelta(days=1), 'Observed'

    if wd == 6:
        return idate + timedelta(days=1), 'Observed'

    return idate, isadj


def wrap_adjustment_function(base, wrapper):
    """Wrap a function with an adjuster"""
    def wrapped_func(year):
        return wrapper(*base(year))
    return wrapped_func


def fixed_date_function(month, day):
    """A fixed day of the month, with no adjustment"""
    return partial(fixed_date_no_obs, month=month, day=day)


def fixed_date_no_roll(month, day):
    """Fixed day of the month, without rolling"""
    return fixed_date_function(month, day)


def fixed_date_roll_forward(month, day):
    """Fixed day of the month, rolling forward on weekends to observation date"""
    return wrap_adjustment_function(fixed_date_function(month, day),
                                    adjust_weekend_to_monday)


def fixed_date_roll_both(month, day):
    """Fixed day of the month, rolling forward on sunday, backwards on saturday, to observation date"""
    return wrap_adjustment_function(fixed_date_function(month, day),
                                    adjust_weekend_both_ways)


_NEW_YEAR_ROLL_BOTH = fixed_date_roll_both(1, 1)

def new_year_roll_back(year: int) -> Tuple[date, str]:
    """Special case of rolling backwards on a year end - second entry, rolled back"""
    following_year_date = _NEW_YEAR_ROLL_BOTH(year + 1)

    if following_year_date[0].year == year:
        # Rolled back
        return following_year_date

    return (None, None)


def easter_western(year: int) -> Tuple[date, str]:
    """Easter monday, western method"""
    return (easter(year, EASTER_WESTERN) + relativedelta(days=1), None)


def good_friday_western(year: int) -> Tuple[date, str]:
    """Good friday, western method"""
    return (easter(year, EASTER_WESTERN) - relativedelta(days=2), None)


def easter_orthodox(year: int) -> Tuple[date, str]:
    """Easter monday, orthodox method"""
    return (easter(year, EASTER_ORTHODOX) + relativedelta(days=1), None)
