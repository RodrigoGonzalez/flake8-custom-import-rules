""" Test the flake8 plugin.

To run this test file only:
poetry run python -m pytest -vvvrca tests/flake8_plugin_test.py
"""

import ast
from contextlib import contextmanager
from functools import partial
from typing import Callable

import pycodestyle
import pytest
from flake8.main import options
from flake8.options import aggregator
from flake8.options import config
from flake8.options import manager

from flake8_custom_import_rules.flake8_plugin import Plugin


@contextmanager
def options_context(plugin_class: Plugin, context_dict: dict) -> None:
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


# @patch.dict(
#     "flake8_custom_import_rules.flake8_plugin.Plugin._options", {"test_env": True}, clear=False
# )
def test_parsing(get_plugin_with_parsed_options: Callable[..., type[Plugin]]):
    """Test parsing."""
    with options_context(Plugin, {"test_env": True}):
        plugin = get_plugin_with_parsed_options(plugin_argv=["--base-packages=my_base_module"])
        # assert plugin._options == {}
        assert plugin._options["checker_settings"].BASE_PACKAGES == ["my_base_module"]


# @patch.dict(
#     "flake8_custom_import_rules.flake8_plugin.Plugin._options", {"test_env": True}, clear=False
# )
def test_linter(get_plugin_with_parsed_options: Callable[..., type[Plugin]]):
    """Test linter."""
    with options_context(Plugin, {"test_env": True}):
        plugin = get_plugin_with_parsed_options(plugin_argv=["--base-packages=my_base_module"])
        data = "import ast\nimport flake8_import_order\nfrom __future__ import *"
        pycodestyle.stdin_get_value = lambda: data
        tree = ast.parse(data)

        checker = plugin(tree, lines=data.splitlines(True))
        results = {"{}:{}: {}".format(*r) for r in checker.run()}
        assert results == {"3:0: PIR107 Wildcard imports are disabled for this project."}
