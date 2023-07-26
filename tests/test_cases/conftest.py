""" Pytest configuration file for error code test cases. """
import ast
import os
from functools import partial
from textwrap import dedent

import pycodestyle
import pytest
from flake8.utils import normalize_path

from flake8_custom_import_rules.flake8_plugin import Plugin


@pytest.fixture(scope="function")
def get_flake8_linter_results() -> partial:
    """Return a set of results."""

    def results(
        s: str,
        options: dict[str, list[str] | str] | None = None,
        delimiter: str = "; ",
        filename: str | None = None,
    ) -> set[str]:
        """Return a set of results."""
        if options is None:
            options = {}

        linter = Plugin(ast.parse(s), lines=s.split(delimiter), filename=filename)
        linter.update_checker_settings(options)
        return {"{}:{}: {}".format(*r) for r in linter.run()}

    return partial(results)


@pytest.fixture(scope="function", autouse=True)
def generate_ast_from_file() -> partial:
    """Generate an AST from a file."""

    def results(filename: str) -> tuple[ast.AST, list[str]]:
        """Generate an AST from a file name."""
        filename = normalize_path(filename)
        if not os.path.isfile(filename):
            raise FileNotFoundError(filename)

        lines = pycodestyle.readlines(filename)
        tree = ast.parse("".join(lines))

        return tree, lines

    return partial(results)


@pytest.fixture(scope="session", autouse=True)
def valid_custom_import_rules_imports() -> str:
    """These imports are valid and should not be reported."""
    return dedent(
        """
        import os
        from os import path
        import sys
        from sys import argv
        import math
        from math import sqrt
        import math.pi
        import json
        from json import JSONEncoder
        import datetime
        from datetime import datetime, timedelta
        import collections
        from collections import defaultdict, namedtuple
        import itertools
        from itertools import cycle
        import functools
        from functools import lru_cache
        import random
        from random import randint
        import re
        from re import match
        import typing
        from typing import TYPE_CHECKING
        """
    )
