"""Test noop when there is an empty string."""


def test_noop(get_flake8_linter_results) -> None:
    """Test noop."""
    assert get_flake8_linter_results("") == set()
