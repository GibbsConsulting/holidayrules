def test_version():
    from holidayrules.version import __version__
    assert len(__version__) > 4
