"""Holiday rules
"""

from abc import abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass(frozen=True)
class HolidayRule:
    """A single holiday rule"""

    name : str
    description : str
    rule: Any  # Signature is year to (holday, optional extra desc)

    def fix_dates(self, years):
        """Return an array of holiday dates, one entry per year

        Each entry is a datetime.date instance, along with an optional second entry.
        If the second entry is present, and not None, then its content describes how
        the date differs fron the normal holiday. The canonical use of this is to
        indicate an observed holiday.
        """
        return [self.rule(year) for year in years]

def new_year_no_obs(year):
    """New year, without any observation"""
    return date(year=year, month=1, day=1), None
