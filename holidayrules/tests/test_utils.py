"""Test utility functions"""


from holidayrules.utils import hr, standard_ruleset


def test_hr_registration():

    sr = standard_ruleset()
    assert sr is not None

    num_prev = len(standard_ruleset())

    assert len(sr) > 4

    assert "DUMMY_RULE_1" not in standard_ruleset()
    assert "DUMMY_RULE_2" not in standard_ruleset()

    def dummy_func(year):
        """Never-a-holiday rule"""
        return (None, None)

    assert dummy_func(1234) == (None, None)

    hr("DUMMY_RULE_1")(dummy_func)
    assert len(sr) == num_prev + 1

    hr("DUMMY_RULE_2")(dummy_func)
    assert len(sr) == num_prev + 2

    hr("DUMMY_RULE_1")(dummy_func)
    assert len(sr) == num_prev + 2

    assert "DUMMY_RULE_3" not in standard_ruleset()
    assert "DUMMY_RULE_1" in standard_ruleset()
    assert "DUMMY_RULE_2" in standard_ruleset()

    @hr("DUMMY_RULE_3")
    def dummy_func_two(year):
        """Never-a-holiday rule"""
        return (None, None)

    assert len(sr) == num_prev + 3
    assert "DUMMY_RULE_3" in standard_ruleset()

    assert dummy_func_two(1234) == (None, None)

    assert "New Years Day" in standard_ruleset()
