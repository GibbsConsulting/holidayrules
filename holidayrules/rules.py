"""Holiday rules
"""


from dataclasses import dataclass
from datetime import date
from functools import partial
from typing import Callable, List, Tuple


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
    return date(year=year, month=month, day=day), None


def fixed_date_function(month, day):
    return partial(fixed_date_no_obs, month=month, day=day)
