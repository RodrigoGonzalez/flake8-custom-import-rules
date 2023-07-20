""" Pytest configuration file for error code test cases. """
import ast
from functools import partial

import pytest

from flake8_custom_import_rules.flake8_linter import Linter


@pytest.fixture(scope="function", autouse=True)
def get_flake8_linter_results() -> partial:
    """Return a set of results."""

    def results(s: str, options: dict[str, list[str] | str] | None = None) -> set[str]:
        """Return a set of results."""
        if options is None:
            options = {}
        # for option_key in DEFAULT_CHECKER_SETTINGS.get_option_keys():
        #     option_value = getattr(options, option_key.lower())
        #     if option_value is not None:
        #         options[option_key] = option_value
        #
        # parsed_options: dict = {
        #     "checker_settings": Settings(**options),
        #     "test_env": False,
        # }

        linter = Linter(ast.parse(s), lines=s.split("; "))
        linter.update_checker_settings(options)
        return {"{}:{}: {}".format(*r) for r in linter.run()}

    return partial(results)
