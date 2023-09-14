""" Test flake8 defaults

To run this test file only:
poetry run python -m pytest -vvvrca tests/defaults_test.py
"""
import optparse
from collections import defaultdict

import pytest
from flake8.options.manager import OptionManager

from flake8_custom_import_rules.defaults import CUSTOM_IMPORT_RULES
from flake8_custom_import_rules.defaults import ERROR_CODES
from flake8_custom_import_rules.defaults import HELP_STRINGS
from flake8_custom_import_rules.defaults import POTENTIAL_DYNAMIC_IMPORTS
from flake8_custom_import_rules.defaults import STANDARD_PROJECT_LEVEL_RESTRICTION_KEYS
from flake8_custom_import_rules.defaults import STDIN_IDENTIFIERS
from flake8_custom_import_rules.defaults import Settings
from flake8_custom_import_rules.defaults import convert_to_dict
from flake8_custom_import_rules.defaults import convert_to_list
from flake8_custom_import_rules.defaults import register_opt
from flake8_custom_import_rules.defaults import register_options


@pytest.mark.parametrize(
    "test_case, expected",
    [
        (None, []),
        ("", []),
        ("test, example", ["test", "example"]),
        (["test, example"], ["test", "example"]),
        ("  test ,  example  ", ["test", "example"]),
        ("test,,example", ["test", "example"]),
        (["test,,example"], ["test", "example"]),
    ],
)
def test_convert_to_list(test_case, expected):
    actual = convert_to_list(test_case)
    assert actual == expected


@pytest.mark.parametrize(
    "delimiter",
    [
        None,
        ":",
        ";",
    ],
    ids=["empty", "colon", "semicolon"],
)
@pytest.mark.parametrize(
    ("test_case", "expected"),
    [
        ("", defaultdict(list)),
        (":", defaultdict(list)),
        (";", defaultdict(list)),
        (" ", defaultdict(list)),
        (None, defaultdict(list)),
    ],
)
def test_convert_to_dict__return_empty_dict(test_case, delimiter, expected):
    actual = convert_to_dict(test_case, delimiter)
    assert actual == expected


def get_default_dict(test_cases: list[tuple] | tuple) -> defaultdict[str, list]:
    """
    Return the default settings as a dictionary.

    Parameters
    ----------
    test_cases : list[tuple] | tuple, default=None
        The test cases to use.
    Returns
    -------
    defaultdict[str, list]
        The default settings as a dictionary.
    """
    if isinstance(test_cases, tuple):
        test_cases = [test_cases]
    modules: defaultdict[str, list] = defaultdict(list)
    for test_case in test_cases:
        module, *submodules = test_case
        modules[module].extend(submodules)
    return modules


@pytest.mark.parametrize(
    ("test_case", "delimiter", "expected"),
    [
        ("test:example", ":", get_default_dict(("test", "example"))),
        ("test:", ":", get_default_dict(("test",))),
        ("test", ":", get_default_dict(("test",))),
        ("test:a,b", ":", get_default_dict(("test", "a", "b"))),
        ("test:a,b,", ":", get_default_dict(("test", "a", "b"))),
        ("test:,a,b", ":", get_default_dict(("test", "a", "b"))),
        ("test:,a,b,", ":", get_default_dict(("test", "a", "b"))),
        ("test:,a,b,,", ":", get_default_dict(("test", "a", "b"))),
        ("test:a,b,c", ":", get_default_dict(("test", "a", "b", "c"))),
        ("test: a , b , c ", ":", get_default_dict(("test", "a", "b", "c"))),
        ("test;example", ";", get_default_dict(("test", "example"))),
        ("test;", ";", get_default_dict(("test",))),
        ("test", ";", get_default_dict(("test",))),
        ("test;a,b", ";", get_default_dict(("test", "a", "b"))),
        ("test;a,b,", ";", get_default_dict(("test", "a", "b"))),
        ("test;,a,b", ";", get_default_dict(("test", "a", "b"))),
        ("test;,a,b,", ";", get_default_dict(("test", "a", "b"))),
        ("test;,a,b,,", ";", get_default_dict(("test", "a", "b"))),
        ("test;a,b,c", ";", get_default_dict(("test", "a", "b", "c"))),
        ("test; a , b , c ", ";", get_default_dict(("test", "a", "b", "c"))),
    ],
)
def test_convert_to_dict(test_case, delimiter, expected):
    actual = convert_to_dict(test_case, delimiter)
    assert actual == expected


@pytest.mark.parametrize(
    ("constant", "expected_type"),
    [
        (POTENTIAL_DYNAMIC_IMPORTS, set),
        (STDIN_IDENTIFIERS, set),
        (STANDARD_PROJECT_LEVEL_RESTRICTION_KEYS, list),
        (CUSTOM_IMPORT_RULES, list),
        (HELP_STRINGS, dict),
        (ERROR_CODES, dict),
    ],
)
def test_constant_types(constant, expected_type):
    """Test constant types."""
    assert isinstance(constant, expected_type)


def test_key_not_present():
    """Test keys or string is present."""
    with pytest.raises(KeyError):
        settings = Settings()
        settings.get_settings_value("some_not_present_key")


@pytest.mark.parametrize(
    ("key", "option_default_value", "is_restriction"),
    [
        ("RESTRICT_RELATIVE_IMPORTS", 123, False),
        ("RESTRICT_RELATIVE_IMPORTS", [], False),
        ("CUSTOM_RESTRICTIONS", True, False),
        ("CUSTOM_RESTRICTIONS", 123, False),
        ("CUSTOM_RESTRICTIONS", [], False),
    ],
)
def test_register_options_raises_type_error(mocker, key, option_default_value, is_restriction):
    """
    Test that the `register_options` function raises a TypeError when given
    incorrect types for `option_default_value`.

    Parameters
    ----------
    mocker : pytest_mock.plugin.MockerFixture
        The mocker fixture for mocking objects.
    key : str
        The key representing the setting to be registered.
    option_default_value : Any
        The incorrect default value that should raise a TypeError.
    is_restriction : bool
        Flag to indicate whether the setting is a restriction or a rule.
    """
    mock_option_manager = mocker.Mock(spec=OptionManager)

    with pytest.raises(TypeError):
        register_options(
            mock_option_manager,
            item=key,
            option_default_value=option_default_value,
            is_restriction=is_restriction,
        )


def test_register_opt_for_flake8_3x(mocker):
    """Test register_opt for flake8 3.x registration."""
    mock_option_manager = mocker.Mock(spec=OptionManager)
    args = ("--example",)
    kwargs = {"action": "store_true"}

    register_opt(mock_option_manager, *args, **kwargs)

    # Check if the add_option method was called with the provided args and kwargs
    mock_option_manager.add_option.assert_called_once_with(*args, **kwargs)


def test_register_opt_for_flake8_2x(mocker):
    """
    Test that the `register_opt` function correctly handles optparse.OptionError.
    """
    # Create a mock instance of OptionManager
    mock_option_manager = mocker.Mock(spec=OptionManager)
    args = ("--example",)
    kwargs = {"action": "store_true"}

    # Make add_option raise optparse.OptionError when called
    mock_option_manager.add_option.side_effect = optparse.OptionError("some error", "some option")

    # Call register_opt
    with pytest.raises(Exception):
        register_opt(mock_option_manager, *args, **kwargs)

    # Assert that add_option was called twice: once for 3.x and once for 2.x
    assert mock_option_manager.add_option.call_count == 2
