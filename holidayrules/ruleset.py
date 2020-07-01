"""Collection of rules
"""


class RuleSet:
    """Set of rules"""

    def __init__(self, rules, day_mask=None):
        day_mask = day_mask if day_mask else [5, 6]
        self._rules = rules
        self._day_mask = day_mask
        self._cached_years = {}

    @staticmethod
    def ymd_str(date):
        """Convert date to an ordereed string."""
        ed = "0" if date.day < 10 else ""
        em = "0" if date.month < 10 else ""
        return f"{date.year}{em}{date.month}{ed}{date.day}"

    def dates_for_year(self, year):
        """Work out what dates are holidays in a particular year"""
        if year in self._cached_years:
            return self._cached_years[year]

        holidays = {}
        for r in self._rules:
            hday, msg = r.rule(year)
            if hday is not None and hday.year == year:
                if msg:
                    holidays[self.ymd_str(hday)] = f"{r.name} [{msg}]"
                else:
                    holidays[self.ymd_str(hday)] = f"{r.name}"

                self._cached_years[year] = holidays

        return holidays

    def _is_good_date(self, date):
        wd = date.weekday()
        if wd in self._day_mask:
            return False

        dfy = self.dates_for_year(date.year)

        if self.ymd_str(date) in dfy:
            return False
        return True

    def is_good_day(self, date):
        """Return True if a good day"""
        return self._is_good_date(date)
