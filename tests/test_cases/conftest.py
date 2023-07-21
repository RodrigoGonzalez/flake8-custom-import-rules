""" Pytest configuration file for error code test cases. """
import ast
from functools import partial
from textwrap import dedent

import pytest

from flake8_custom_import_rules.flake8_linter import Linter


@pytest.fixture(scope="function", autouse=True)
def get_flake8_linter_results() -> partial:
    """Return a set of results."""

    def results(
        s: str,
        options: dict[str, list[str] | str] | None = None,
        delimiter: str = "; ",
    ) -> set[str]:
        """Return a set of results."""
        if options is None:
            options = {}

        linter = Linter(ast.parse(s), lines=s.split(delimiter))
        linter.update_checker_settings(options)
        return {"{}:{}: {}".format(*r) for r in linter.run()}

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
