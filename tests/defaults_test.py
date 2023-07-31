""" Test flake8 defaults

To run this test file only:
poetry run python -m pytest -vvvrca tests/defaults_test.py
"""
from collections import defaultdict

import pytest

from flake8_custom_import_rules.defaults import convert_to_dict
from flake8_custom_import_rules.defaults import convert_to_list


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
