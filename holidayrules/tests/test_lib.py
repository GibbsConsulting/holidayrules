"""Test library of rules"""


from holidayrules.lib import RULES

def test_rules_formed():

    assert len(RULES) > 6
    assert "NewYear" in RULES
