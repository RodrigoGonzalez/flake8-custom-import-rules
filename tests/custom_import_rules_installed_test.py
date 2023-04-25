"""Test that all custom import rules are installed."""
import pytest


@pytest.mark.parametrize("extension", ["E", "F", "W", "I", "C90", "CIR"])
@pytest.mark.usefixtures("list_flake8_extensions")
def test_all_extensions_installed(extension, list_flake8_extensions):
    """Test all extensions are installed."""
    assert extension in list_flake8_extensions
