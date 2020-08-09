"""Library of common holiday rules"""


from .rules import HolidayRule
from .rules import (fixed_date_roll_forward,
                    fixed_date_roll_both,
                    christmas_day,
                    boxing_day,
                    easter_western,
                    good_friday_western,
                    )


_RULE_DESC = [
    ("NewYear", "New Year's day, rolling forward", fixed_date_roll_forward(1, 1)),
    ('Christmas', "Christmas day, rolling forward over Boxing day if needed", christmas_day),
    ('Boxing', 'Boxing day, rolling over observed Christmas day if needed', boxing_day),
    ('Easter', 'Easter Monday, western calendar', easter_western),
    ('GoodFriday', 'Good Friday, western calendar', good_friday_western),
    ('CanadaDay', 'Canada Day', fixed_date_roll_forward(7, 1)),
    ('USIndependence', 'Independence Day (USA)', fixed_date_roll_both(7, 4)),

]


RULES = {name: HolidayRule(name, description, rule) for name, description, rule in _RULE_DESC}
