""" Test the flake8 plugin.

To run this test file only:
poetry run python -m pytest -vvvrca tests/flake8_plugin_test.py
"""
import ast
from contextlib import contextmanager
from functools import partial
from typing import Callable
from unittest.mock import patch

import pycodestyle
import pytest
from attrs import define
from attrs import field
from flake8.main import options
from flake8.options import aggregator
from flake8.options import config
from flake8.options import manager

from flake8_custom_import_rules import __version__
from flake8_custom_import_rules import show_versions
from flake8_custom_import_rules.flake8_plugin import Plugin


@contextmanager
def options_context(plugin_class: type[Plugin], context_dict: dict) -> None:
    """Context manager to temporarily set _options."""
    original_options = plugin_class._options
    plugin_class._options = context_dict
    try:
        yield
    finally:
        plugin_class._options = original_options


@pytest.fixture(scope="function")
def get_plugin_with_parsed_options() -> partial:
    """Return a set of results."""

    def parsed_options(
        plugin_argv: list[str] | None = None,
        argv: list[str] | None = None,
    ) -> type[Plugin]:
        """Return a set of results."""
        # with options_context(Plugin, {"test_env": True}):
        if not argv:
            argv = ["example_repos/my_base_module/my_base_module/"]
        prelim_parser = options.stage1_arg_parser()
        args0, rest = prelim_parser.parse_known_args(argv)

        cfg, cfg_dir = config.load_config(
            config=args0.config,
            extra=args0.append_config,
            isolated=args0.isolated,
        )

        option_manager = manager.OptionManager(
            version="TestVersion: 1.0.0",
            plugin_versions=f"{Plugin.name}: {Plugin.version}",
            parents=[prelim_parser],
            formatter_names=[],
        )
        options.register_default_options(option_manager)
        # option_manager.register_plugins(plugins)
        opts = aggregator.aggregate_options(option_manager, cfg, cfg_dir, rest)

        Plugin.add_options(option_manager)
        if not plugin_argv:
            plugin_argv = ["--base_packages=my_base_module"]

        inner_parsed_options = option_manager.parse_args(plugin_argv, opts)
        Plugin.parse_options(option_manager, inner_parsed_options)

        return Plugin

    return partial(parsed_options)


@define(slots=True)
class ParserTestCase:
    """Parse test case."""

    test_case: str
    settings_key: str = field(init=False)
    expected: dict | list[str] | str

    def __attrs_post_init__(self):
        """Post init."""
        self.settings_key = self.test_case.split("=")[0].lstrip("-").replace("-", "_").upper()

    @property
    def test(self) -> tuple[str, str, list[str] | str]:
        """Test parsing."""
        return self.test_case, self.settings_key, self.expected


OPTIONS_TEST_CASES = [
    ParserTestCase("--base-packages=my_base_module", ["my_base_module"]),
    ParserTestCase(
        "--base-packages=my_base_module,second_base_module",
        ["my_base_module", "second_base_module"],
    ),
    ParserTestCase(
        (
            "--custom-restrictions=my_base_package.package_A:my_base_package.package_B,"
            "my_base_package/module_X.py:my_base_package/module_Y.py"
        ),
        {
            "my_base_package.package_A": ["my_base_package.package_B"],
            "my_base_package/module_X.py": ["my_base_package/module_Y.py"],
        },
    ),
    ParserTestCase(
        (
            "--custom-restrictions=my_base_package.package_A:my_base_package.package_B:"
            "my_base_package.package_C,"
            "my_base_package/module_X.py:my_base_package/module_Y.py"
        ),
        {
            "my_base_package.package_A": ["my_base_package.package_B", "my_base_package.package_C"],
            "my_base_package/module_X.py": ["my_base_package/module_Y.py"],
        },
    ),
    ParserTestCase(
        (
            "--custom-restrictions=my_base_package.package_A:my_base_package.package_B:"
            "my_base_package.package_C,"
            "my_base_package/module_X.py:my_base_package/module_Y.py:my_base_package/module_Z.py"
        ),
        {
            "my_base_package.package_A": ["my_base_package.package_B", "my_base_package.package_C"],
            "my_base_package/module_X.py": [
                "my_base_package/module_Y.py",
                "my_base_package/module_Z.py",
            ],
        },
    ),
    ParserTestCase(
        (
            "--custom-restrictions=my_base_package.package_A:my_base_package.package_B:"
            "my_base_package.package_C,"
            "my_base_package/module_X.py:my_base_package/module_Y.py,"
            "my_base_package.package_A:my_base_package.package_D"
        ),
        {
            "my_base_package.package_A": [
                "my_base_package.package_B",
                "my_base_package.package_C",
                "my_base_package.package_D",
            ],
            "my_base_package/module_X.py": ["my_base_package/module_Y.py"],
        },
    ),
]


@pytest.mark.parametrize(
    ("test_case", "settings_key", "expected"),
    [TEST_CASE.test for TEST_CASE in OPTIONS_TEST_CASES],
)
def test_parsing(
    test_case: str,
    settings_key: str,
    expected: dict | list,
    get_plugin_with_parsed_options: Callable[..., type[Plugin]],
):
    """Test parsing."""
    with options_context(Plugin, {"test_env": True}):
        plugin = get_plugin_with_parsed_options(plugin_argv=[test_case])
        checker_settings = plugin._options["checker_settings"]
        assert checker_settings.dict[settings_key] == expected


# @patch.dict(
#     "flake8_custom_import_rules.flake8_plugin.Plugin._options", {"test_env": True}, clear=False
# )
def test_linter(get_plugin_with_parsed_options: Callable[..., type[Plugin]]):
    """Test linter."""
    with options_context(Plugin, {"test_env": True}):
        plugin = get_plugin_with_parsed_options(plugin_argv=["--base-packages=my_base_module"])
        data = "import ast\nimport os\nfrom __future__ import *"
        pycodestyle.stdin_get_value = lambda: data
        tree = ast.parse(data)

        checker = plugin(tree, lines=data.splitlines(True))
        results = {"{}:{}: {}".format(*r) for r in checker.run()}
        assert results == {"3:0: PIR107 Wildcard Imports are disabled for this project."}


def test_linter__local_imports_enabled(get_plugin_with_parsed_options: Callable[..., type[Plugin]]):
    """Test linter."""
    with options_context(Plugin, {"test_env": True}):
        plugin = get_plugin_with_parsed_options(
            plugin_argv=[
                "--base-packages=my_base_module",
                "--restrict-relative-imports=False",
                "-vvvv",
            ]
        )
        data = "from .module_a_relative import ARelative"
        pycodestyle.stdin_get_value = lambda: data
        tree = ast.parse(data)

        checker = plugin(tree, lines=data.splitlines(True))
        results = {"{}:{}: {}".format(*r) for r in checker.run()}
        assert not results


def test_linter__local_imports_disabled(
    get_plugin_with_parsed_options: Callable[..., type[Plugin]]
):
    """Test linter."""
    with options_context(Plugin, {"test_env": True}):
        plugin = get_plugin_with_parsed_options(
            plugin_argv=["--base-packages=my_base_module", "--restrict-relative-imports=True"]
        )
        data = "from .module_a_relative import ARelative"
        pycodestyle.stdin_get_value = lambda: data
        tree = ast.parse(data)

        checker = plugin(tree, lines=data.splitlines(True))
        results = {"{}:{}: {}".format(*r) for r in checker.run()}
        assert results == {"1:0: PIR102 Relative Imports are disabled for this project."}


@patch("builtins.print")
def test_show_versions(mock_print):
    """Test show_versions from __init__.py file"""
    show_versions()
    mock_print.assert_called_once_with(__version__)
