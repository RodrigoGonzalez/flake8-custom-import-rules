""" Test flake8 defaults

To run this test file only:
poetry run python -m pytest -vvvrca tests/defaults_test.py
"""
from collections import defaultdict

import pytest

from flake8_custom_import_rules.defaults import convert_to_dict
from flake8_custom_import_rules.defaults import convert_to_list
from flake8_custom_import_rules.defaults import register_opt


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


def test_register_opt_for_flake8_3x(mocker):
    """Test register_opt for flake8 3.x registration."""
    mock_option_manager = mocker.Mock()
    args = ("--example",)
    kwargs = {"action": "store_true"}

    register_opt(mock_option_manager, *args, **kwargs)

    # Check if the add_option method was called with the provided args and kwargs
    mock_option_manager.add_option.assert_called_once_with(*args, **kwargs)


# Fix later

# def test_register_opt_for_flake8_2x(mocker):
#     """Test register_opt for flake8 2.x registration."""
#     mock_option_manager = mocker.Mock()
#     args = ("--example",)
#     kwargs = {
#         "action": "store_true",
#         "parse_from_config": True,
#         "comma_separated_list": True,
#         "normalize_paths": True,
#     }
#
#     # Define a side effect function to simulate exceptions
#     def side_effect(*args, **kwargs):
#         # Raise optparse.OptionError first, then TypeError
#         raise optparse.OptionError("error", "--example")
#         raise TypeError
#
#     # Use an iterator to ensure that the exceptions are raised in sequence
#     mock_option_manager.add_option.side_effect = iter(side_effect, None)
#
#     register_opt(mock_option_manager, *args, **kwargs)
#
#     # Check if the add_option method was called without the specific kwargs
#     reduced_kwargs = {"action": "store_true"}
#     mock_option_manager.add_option.assert_called_with(*args, **reduced_kwargs)
#     assert args[-1].lstrip("-") in mock_option_manager.config_options
