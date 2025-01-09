"""Test the option utils with a sample setting instance"""

import pytest

from flake8_custom_import_rules.defaults import Settings
from flake8_custom_import_rules.utils.option_utils import check_conflicts
from flake8_custom_import_rules.utils.option_utils import get_bool_value


def test_check_conflicts():
    """Test the check_conflicts function."""
    sample_settings = Settings()
    sample_settings.THIRD_PARTY_ONLY = ["package1", "package2"]
    sample_settings.FIRST_PARTY_ONLY = ["package2", "package3"]
    sample_settings.STANDALONE_MODULES = ["module1"]
    sample_settings.CUSTOM_RESTRICTIONS = {
        "module1": ["submoduleA", "submoduleB"],
        "module2": ["submoduleC"],
    }

    check_conflicts(sample_settings.dict)


def test_check_conflicts__for_none():
    """Test the check_conflicts function."""
    sample_settings = Settings()
    assert check_conflicts(sample_settings.dict) is None


@pytest.mark.parametrize(
    "value, expected_result",
    [
        # Test with boolean inputs
        (True, True),
        (False, False),
        # Test with integer inputs
        (0, False),
        (1, True),
        # Test with string inputs
        ("true", True),
        ("false", False),
        ("yes", True),
        ("no", False),
        ("y", True),
        ("n", False),
        ("1", True),
        ("0", False),
        ("", False),
    ],
)
def test_get_bool_value_valid_inputs(value, expected_result):
    assert get_bool_value(value) == expected_result


@pytest.mark.parametrize(
    "value",
    [
        "invalid_string",
        2,
        -1,
        None,
        [],
        {},
    ],
)
def test_get_bool_value_invalid_inputs(value):
    with pytest.raises(ValueError) as e:
        get_bool_value(value)
    assert f'Cannot interpret value "{value}" as boolean' in str(e.value)
