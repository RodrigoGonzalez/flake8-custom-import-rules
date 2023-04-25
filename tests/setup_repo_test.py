import pytest


@pytest.mark.parametrize("initial, expected", [(1, 2), (2, 3)])
def test_increment(initial, expected):
    """Test incrementing a number (remove after setting project up.)"""
    initial += 1
    assert initial == expected
