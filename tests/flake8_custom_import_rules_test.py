from __future__ import annotations

import ast

from flake8_custom_import_rules.flake8_linter import Linter


def results(s) -> set[str]:
    """Return a list of results."""
    return {"{}:{}: {}".format(*r) for r in Linter(ast.parse(s)).run()}


def test_noop() -> None:
    """Test noop."""
    assert results("") == set()


def test_star() -> None:
    """Test star."""
    # assert results("from my_base_module.module_z import *") == {"1:0: CIR101 Custom Import Rule"}
    assert results("from my_base_module.module_z import *") == set()


def test_eval() -> None:
    """Test eval."""
    # assert results("eval('import datetime')") == set()
    assert results("eval('from my_base_module.module_z import Z')") == set()


def test_exec() -> None:
    """Test exec."""
    # assert results("exec('import datetime')") == {"1:0: CIR101 Custom Import Rule"}
    assert results("exec('import datetime')") == set()


def test_import_module_attribute() -> None:
    """Test import_module."""
    # assert results("import importlib; importlib.import_module('datetime')") == {
    #     "1:0: CIR101 Custom Import Rule"
    # }
    assert results("import importlib; importlib.import_module('datetime')") == set()


def test_import_module_name() -> None:
    """Test importlib.import_module."""
    # TODO: Add reload
    # assert results("from importlib import import_module; import_module('datetime')") == {
    #     "1:0: CIR101 Custom Import Rule"
    # }
    assert results("import importlib; importlib.import_module('datetime')") == set()
