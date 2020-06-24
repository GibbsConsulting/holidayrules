"""Simple tests of basic structure"""


import datetime


def test_version():
    "Test version string is importable and non-trivial"
    from holidayrules.version import __version__
    assert len(__version__) > 4


def test_simple_rule():
    from holidayrules.rules import new_year_no_obs

    assert new_year_no_obs(2020) == (datetime.date(2020, 1, 1), None)
