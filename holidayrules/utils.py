"""Utilities for managing holiday rules
"""


_COMMON_RULES = dict()


def standard_ruleset():
    """Standard set of rules, available in code"""
    return _COMMON_RULES


def hr(name, description=None, long_description=None, ruleset=None):
    """Register a holiday rule, with optional additional information"""

    rs = ruleset if ruleset else standard_ruleset()
    if rs.get(name):
        print(f"Warning - repeated definition of rule {name}")
    def wrap(function):
        rs[name] = (function, description, long_description)
        return function

    return wrap
