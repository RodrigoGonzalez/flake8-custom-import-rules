""" Pytest configuration file for error code test cases. """
import ast
import logging
import os
from functools import partial
from textwrap import dedent
from typing import Any
from typing import Generator

import pycodestyle
import pytest
from flake8.utils import normalize_path

from flake8_custom_import_rules.core.error_messages import ErrorMessage
from flake8_custom_import_rules.core.nodes import ParsedFromImport
from flake8_custom_import_rules.core.nodes import ParsedNode
from flake8_custom_import_rules.core.nodes import ParsedStraightImport
from flake8_custom_import_rules.core.rules_checker import CustomImportRulesChecker
from flake8_custom_import_rules.flake8_plugin import Plugin

logger = logging.getLogger(__name__)


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


class BaseCustomImportRulePlugin(CustomImportRulesChecker):
    _node_list: list
    _run_list: list
    _options: dict = {}
    _errors_set: set = set()

    def __init__(
        self,
        tree: ast.AST | None = None,
        filename: str | None = None,
        lines: list | None = None,
        options: dict | None = None,
    ) -> None:
        """Initialize the checker."""
        logger.info("Initializing the checker")
        self._tree = tree
        self._lines = lines
        self._filename = filename
        self._errors: list = []

        super().__init__(tree=tree, filename=filename, lines=lines)
        logger.info(f"Init options BaseCustomImportRulePlugin: {options}")
        self._options = options or {}
        self._options["test_env"] = True
        logger.info(f"Init options after setting: {options}")

    @property
    def errors(self) -> list[ErrorMessage]:
        """Return the errors."""
        logger.info("Getting the errors")
        return self._errors

    @property
    def errors_set(self) -> set:
        """Return the errors."""
        logger.info("Getting the errors")
        if not self._errors_set:
            self._errors_set = {
                f"{error.lineno}:{error.col_offset}: {error.code} {error.message}"
                for error in self._errors
            }
        return self._errors_set

    def run(self) -> Generator[Any, None, None]:
        """Run the plugin."""
        logger.info("Running the plugin")
        self._errors = list(self.check_custom_import_rules())
        for node in self.nodes:
            yield node.lineno, node.col_offset, node, type(self)

    def get_run_list(self, sort: bool = True) -> list:
        """Return the run list."""
        logger.info("Getting the run list")
        self._node_list = list(self.nodes) if self._nodes else []
        self._run_list = list(self.run())
        if sort:
            self._run_list.sort(key=lambda x: x[0])
        return self._run_list

    def get_import_nodes(self) -> list[ParsedNode]:
        """Return the import nodes."""
        logger.info("Getting the import nodes")
        return [
            node
            for node in self._run_list
            if isinstance(node[2], (ParsedStraightImport, ParsedFromImport))
        ]


@pytest.fixture(scope="function")
def get_base_plugin() -> partial:
    """Return a set of results."""

    def base_plugin(
        tree: ast.AST | None = None,
        filename: str | None = None,
        lines: list | None = None,
        options: dict[str, list[str] | str] | None = None,
    ) -> BaseCustomImportRulePlugin:
        """Return a set of results."""
        return BaseCustomImportRulePlugin(
            tree=tree, filename=filename, lines=lines, options=options
        )

    return partial(base_plugin)


@pytest.fixture(scope="module")
def custom_import_rules_fixture() -> str:
    """Custom import rules fixture."""
    return dedent(
        """
        import attrs
        import uuid

        import my_second_base_package.module_one.file_one
        import my_second_base_package.module_one.file_two
        import my_second_base_package.module_one
        import my_second_base_package.module_two.file_one
        import my_second_base_package.module_two.file_two
        import my_second_base_package.module_two
        import my_second_base_package.file
        import my_second_base_package
        import base_package
        import my_third_base_package

        from attrs import (
            define,
            field,
        )
        from uuid import UUID
        from uuid import uuid4

        from my_second_base_package.module_one.file_one import A
        from my_second_base_package.module_one.file_two import B
        from my_second_base_package.module_one import file_one
        from my_second_base_package.module_one import file_two
        from my_second_base_package.module_one import C
        from my_second_base_package.module_two import file_one
        from my_second_base_package.module_two import file_two
        from my_second_base_package.module_two import D
        from my_second_base_package.file import C
        from my_second_base_package import module_one
        from my_second_base_package import module_two
        from my_second_base_package import file
        from my_second_base_package import E
        from base_package import F
        from my_third_base_package import G
        """
    )
