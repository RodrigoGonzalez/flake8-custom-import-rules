""" Import restriction test cases.

- CIR102
- CIR103
- CIR104
- CIR105

To run this test file only:
poetry run python -m pytest -vvvrca tests/test_cases/custom_import_rules/custom_restrictions_test.py
"""

import ast
import os
from collections import defaultdict
from functools import partial

import pycodestyle
import pytest
from flake8.utils import normalize_path

from flake8_custom_import_rules.codes.error_codes import ErrorCode
from flake8_custom_import_rules.core.error_messages import import_restriction_error
from flake8_custom_import_rules.core.import_rules import CustomImportRules
from flake8_custom_import_rules.core.nodes import HelperParsedImport
from flake8_custom_import_rules.defaults import Settings
from flake8_custom_import_rules.defaults import convert_to_dict
from flake8_custom_import_rules.utils.file_utils import get_module_name_from_filename
from flake8_custom_import_rules.utils.node_utils import root_package_name

HPI = partial(HelperParsedImport, col_offset=0)

CIR102 = partial(import_restriction_error, node=HPI, error_code=ErrorCode.CIR102)
CIR103 = partial(import_restriction_error, node=HPI, error_code=ErrorCode.CIR103)
CIR104 = partial(import_restriction_error, node=HPI, error_code=ErrorCode.CIR104)
CIR105 = partial(import_restriction_error, node=HPI, error_code=ErrorCode.CIR105)

BASE_EXPECTED_RESTRICTED_IDENTIFIERS = {
    "my_base_module",
    "my_base_module.file",
    "my_base_module.module_one",
    "my_base_module.module_one.file_one",
    "my_base_module.module_one.file_two",
    "my_base_module.module_two",
    "my_base_module.module_two.file_one",
    "my_base_module.module_two.file_two",
    "my_third_base_package",
    "my_third_base_package.file",
    "my_third_base_package.module_one",
    "my_third_base_package.module_one.file_one",
    "my_third_base_package.module_one.file_two",
    "my_third_base_package.module_two",
    "my_third_base_package.module_two.file_one",
    "my_third_base_package.module_two.file_two",
    "uuid",
}


@pytest.mark.parametrize(
    (
        "filename",
        "expected_current_module",
        "expected_restricted_identifiers",
        "expected",
        "expected_errors",
    ),
    [
        (
            "example_repos/my_base_module/my_second_base_package/module_one/file_one.py",
            "my_second_base_package.module_one.file_one",
            BASE_EXPECTED_RESTRICTED_IDENTIFIERS.union(
                {
                    "my_second_base_package.file",
                    "my_second_base_package.module_one.file_two",
                    "my_second_base_package.module_two",
                    "my_second_base_package.module_two.file_one",
                    "my_second_base_package.module_two.file_two",
                }
            ),
            18,
            [
                CIR104(
                    node=HPI(lineno=3, import_statement="import uuid"),
                    file_identifier="my_second_base_package.module_one.file_one",
                ),
                CIR102(
                    node=HPI(
                        lineno=6,
                        import_statement="import my_second_base_package.module_one.file_two",
                    ),
                    file_identifier="my_second_base_package.module_one.file_one",
                ),
                CIR102(
                    node=HPI(
                        lineno=8,
                        import_statement="import my_second_base_package.module_two.file_one",
                    ),
                    file_identifier="my_second_base_package.module_one.file_one",
                ),
                CIR102(
                    node=HPI(
                        lineno=9,
                        import_statement="import my_second_base_package.module_two.file_two",
                    ),
                    file_identifier="my_second_base_package.module_one.file_one",
                ),
                CIR102(
                    node=HPI(
                        lineno=10, import_statement="import my_second_base_package.module_two"
                    ),
                    file_identifier="my_second_base_package.module_one.file_one",
                ),
                CIR102(
                    node=HPI(lineno=11, import_statement="import my_second_base_package.file"),
                    file_identifier="my_second_base_package.module_one.file_one",
                ),
                CIR104(
                    node=HPI(lineno=14, import_statement="import my_third_base_package"),
                    file_identifier="my_second_base_package.module_one.file_one",
                ),
                CIR105(
                    node=HPI(lineno=20, import_statement="from uuid import UUID"),
                    file_identifier="my_second_base_package.module_one.file_one",
                ),
                CIR105(
                    node=HPI(lineno=21, import_statement="from uuid import uuid4"),
                    file_identifier="my_second_base_package.module_one.file_one",
                ),
                CIR103(
                    node=HPI(
                        lineno=24,
                        import_statement="from my_second_base_package.module_one.file_two import B",
                    ),
                    file_identifier="my_second_base_package.module_one.file_one",
                ),
                CIR103(
                    node=HPI(
                        lineno=26,
                        import_statement="from my_second_base_package.module_one import file_two",
                    ),
                    file_identifier="my_second_base_package.module_one.file_one",
                ),
                CIR103(
                    node=HPI(
                        lineno=28,
                        import_statement="from my_second_base_package.module_two import file_one",
                    ),
                    file_identifier="my_second_base_package.module_one.file_one",
                ),
                CIR103(
                    node=HPI(
                        lineno=29,
                        import_statement="from my_second_base_package.module_two import file_two",
                    ),
                    file_identifier="my_second_base_package.module_one.file_one",
                ),
                CIR103(
                    node=HPI(
                        lineno=30,
                        import_statement="from my_second_base_package.module_two import D",
                    ),
                    file_identifier="my_second_base_package.module_one.file_one",
                ),
                CIR103(
                    node=HPI(
                        lineno=31, import_statement="from my_second_base_package.file import C"
                    ),
                    file_identifier="my_second_base_package.module_one.file_one",
                ),
                CIR103(
                    node=HPI(
                        lineno=33, import_statement="from my_second_base_package import module_two"
                    ),
                    file_identifier="my_second_base_package.module_one.file_one",
                ),
                CIR103(
                    node=HPI(lineno=34, import_statement="from my_second_base_package import file"),
                    file_identifier="my_second_base_package.module_one.file_one",
                ),
                CIR105(
                    node=HPI(lineno=37, import_statement="from my_third_base_package import G"),
                    file_identifier="my_second_base_package.module_one.file_one",
                ),
            ],
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_one/file_two.py",
            "my_second_base_package.module_one.file_two",
            BASE_EXPECTED_RESTRICTED_IDENTIFIERS.union(
                {
                    "my_second_base_package.file",
                    "my_second_base_package.module_one.file_one",
                    "my_second_base_package.module_two",
                    "my_second_base_package.module_two.file_one",
                    "my_second_base_package.module_two.file_two",
                }
            ),
            18,
            [
                CIR104(
                    node=HPI(lineno=3, import_statement="import uuid"),
                    file_identifier="my_second_base_package.module_one.file_two",
                ),
                CIR102(
                    node=HPI(
                        lineno=5,
                        import_statement="import my_second_base_package.module_one.file_one",
                    ),
                    file_identifier="my_second_base_package.module_one.file_two",
                ),
                CIR102(
                    node=HPI(
                        lineno=8,
                        import_statement="import my_second_base_package.module_two.file_one",
                    ),
                    file_identifier="my_second_base_package.module_one.file_two",
                ),
                CIR102(
                    node=HPI(
                        lineno=9,
                        import_statement="import my_second_base_package.module_two.file_two",
                    ),
                    file_identifier="my_second_base_package.module_one.file_two",
                ),
                CIR102(
                    node=HPI(
                        lineno=10, import_statement="import my_second_base_package.module_two"
                    ),
                    file_identifier="my_second_base_package.module_one.file_two",
                ),
                CIR102(
                    node=HPI(lineno=11, import_statement="import my_second_base_package.file"),
                    file_identifier="my_second_base_package.module_one.file_two",
                ),
                CIR104(
                    node=HPI(lineno=14, import_statement="import my_third_base_package"),
                    file_identifier="my_second_base_package.module_one.file_two",
                ),
                CIR105(
                    node=HPI(lineno=20, import_statement="from uuid import UUID"),
                    file_identifier="my_second_base_package.module_one.file_two",
                ),
                CIR105(
                    node=HPI(lineno=21, import_statement="from uuid import uuid4"),
                    file_identifier="my_second_base_package.module_one.file_two",
                ),
                CIR103(
                    node=HPI(
                        lineno=23,
                        import_statement="from my_second_base_package.module_one.file_one import A",
                    ),
                    file_identifier="my_second_base_package.module_one.file_two",
                ),
                CIR103(
                    node=HPI(
                        lineno=25,
                        import_statement="from my_second_base_package.module_one import file_one",
                    ),
                    file_identifier="my_second_base_package.module_one.file_two",
                ),
                CIR103(
                    node=HPI(
                        lineno=28,
                        import_statement="from my_second_base_package.module_two import file_one",
                    ),
                    file_identifier="my_second_base_package.module_one.file_two",
                ),
                CIR103(
                    node=HPI(
                        lineno=29,
                        import_statement="from my_second_base_package.module_two import file_two",
                    ),
                    file_identifier="my_second_base_package.module_one.file_two",
                ),
                CIR103(
                    node=HPI(
                        lineno=30,
                        import_statement="from my_second_base_package.module_two import D",
                    ),
                    file_identifier="my_second_base_package.module_one.file_two",
                ),
                CIR103(
                    node=HPI(
                        lineno=31, import_statement="from my_second_base_package.file import C"
                    ),
                    file_identifier="my_second_base_package.module_one.file_two",
                ),
                CIR103(
                    node=HPI(
                        lineno=33, import_statement="from my_second_base_package import module_two"
                    ),
                    file_identifier="my_second_base_package.module_one.file_two",
                ),
                CIR103(
                    node=HPI(lineno=34, import_statement="from my_second_base_package import file"),
                    file_identifier="my_second_base_package.module_one.file_two",
                ),
                CIR105(
                    node=HPI(lineno=37, import_statement="from my_third_base_package import G"),
                    file_identifier="my_second_base_package.module_one.file_two",
                ),
            ],
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_two/file_one.py",
            "my_second_base_package.module_two.file_one",
            BASE_EXPECTED_RESTRICTED_IDENTIFIERS.union(
                {
                    "my_second_base_package.file",
                    "my_second_base_package.module_one",
                    "my_second_base_package.module_one.file_one",
                    "my_second_base_package.module_one.file_two",
                    "my_second_base_package.module_two.file_two",
                }
            ),
            19,
            [
                CIR104(
                    node=HPI(lineno=3, import_statement="import uuid"),
                    file_identifier="my_second_base_package.module_two.file_one",
                ),
                CIR102(
                    node=HPI(
                        lineno=5,
                        import_statement="import my_second_base_package.module_one.file_one",
                    ),
                    file_identifier="my_second_base_package.module_two.file_one",
                ),
                CIR102(
                    node=HPI(
                        lineno=6,
                        import_statement="import my_second_base_package.module_one.file_two",
                    ),
                    file_identifier="my_second_base_package.module_two.file_one",
                ),
                CIR102(
                    node=HPI(lineno=7, import_statement="import my_second_base_package.module_one"),
                    file_identifier="my_second_base_package.module_two.file_one",
                ),
                CIR102(
                    node=HPI(
                        lineno=9,
                        import_statement="import my_second_base_package.module_two.file_two",
                    ),
                    file_identifier="my_second_base_package.module_two.file_one",
                ),
                CIR102(
                    node=HPI(lineno=11, import_statement="import my_second_base_package.file"),
                    file_identifier="my_second_base_package.module_two.file_one",
                ),
                CIR104(
                    node=HPI(lineno=14, import_statement="import my_third_base_package"),
                    file_identifier="my_second_base_package.module_two.file_one",
                ),
                CIR105(
                    node=HPI(lineno=20, import_statement="from uuid import UUID"),
                    file_identifier="my_second_base_package.module_two.file_one",
                ),
                CIR105(
                    node=HPI(lineno=21, import_statement="from uuid import uuid4"),
                    file_identifier="my_second_base_package.module_two.file_one",
                ),
                CIR103(
                    node=HPI(
                        lineno=23,
                        import_statement="from my_second_base_package.module_one.file_one import A",
                    ),
                    file_identifier="my_second_base_package.module_two.file_one",
                ),
                CIR103(
                    node=HPI(
                        lineno=24,
                        import_statement="from my_second_base_package.module_one.file_two import B",
                    ),
                    file_identifier="my_second_base_package.module_two.file_one",
                ),
                CIR103(
                    node=HPI(
                        lineno=25,
                        import_statement="from my_second_base_package.module_one import file_one",
                    ),
                    file_identifier="my_second_base_package.module_two.file_one",
                ),
                CIR103(
                    node=HPI(
                        lineno=26,
                        import_statement="from my_second_base_package.module_one import file_two",
                    ),
                    file_identifier="my_second_base_package.module_two.file_one",
                ),
                CIR103(
                    node=HPI(
                        lineno=27,
                        import_statement="from my_second_base_package.module_one import C",
                    ),
                    file_identifier="my_second_base_package.module_two.file_one",
                ),
                CIR103(
                    node=HPI(
                        lineno=29,
                        import_statement="from my_second_base_package.module_two import file_two",
                    ),
                    file_identifier="my_second_base_package.module_two.file_one",
                ),
                CIR103(
                    node=HPI(
                        lineno=31, import_statement="from my_second_base_package.file import C"
                    ),
                    file_identifier="my_second_base_package.module_two.file_one",
                ),
                CIR103(
                    node=HPI(
                        lineno=32, import_statement="from my_second_base_package import module_one"
                    ),
                    file_identifier="my_second_base_package.module_two.file_one",
                ),
                CIR103(
                    node=HPI(lineno=34, import_statement="from my_second_base_package import file"),
                    file_identifier="my_second_base_package.module_two.file_one",
                ),
                CIR105(
                    node=HPI(lineno=37, import_statement="from my_third_base_package import G"),
                    file_identifier="my_second_base_package.module_two.file_one",
                ),
            ],
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_two/file_two.py",
            "my_second_base_package.module_two.file_two",
            BASE_EXPECTED_RESTRICTED_IDENTIFIERS.union(
                {
                    "my_second_base_package.file",
                    "my_second_base_package.module_one",
                    "my_second_base_package.module_one.file_one",
                    "my_second_base_package.module_one.file_two",
                    "my_second_base_package.module_two.file_one",
                }
            ),
            19,
            [
                CIR104(
                    node=HPI(lineno=3, import_statement="import uuid"),
                    file_identifier="my_second_base_package.module_two.file_two",
                ),
                CIR102(
                    node=HPI(
                        lineno=5,
                        import_statement="import my_second_base_package.module_one.file_one",
                    ),
                    file_identifier="my_second_base_package.module_two.file_two",
                ),
                CIR102(
                    node=HPI(
                        lineno=6,
                        import_statement="import my_second_base_package.module_one.file_two",
                    ),
                    file_identifier="my_second_base_package.module_two.file_two",
                ),
                CIR102(
                    node=HPI(lineno=7, import_statement="import my_second_base_package.module_one"),
                    file_identifier="my_second_base_package.module_two.file_two",
                ),
                CIR102(
                    node=HPI(
                        lineno=8,
                        import_statement="import my_second_base_package.module_two.file_one",
                    ),
                    file_identifier="my_second_base_package.module_two.file_two",
                ),
                CIR102(
                    node=HPI(lineno=11, import_statement="import my_second_base_package.file"),
                    file_identifier="my_second_base_package.module_two.file_two",
                ),
                CIR104(
                    node=HPI(lineno=14, import_statement="import my_third_base_package"),
                    file_identifier="my_second_base_package.module_two.file_two",
                ),
                CIR105(
                    node=HPI(lineno=20, import_statement="from uuid import UUID"),
                    file_identifier="my_second_base_package.module_two.file_two",
                ),
                CIR105(
                    node=HPI(lineno=21, import_statement="from uuid import uuid4"),
                    file_identifier="my_second_base_package.module_two.file_two",
                ),
                CIR103(
                    node=HPI(
                        lineno=23,
                        import_statement="from my_second_base_package.module_one.file_one import A",
                    ),
                    file_identifier="my_second_base_package.module_two.file_two",
                ),
                CIR103(
                    node=HPI(
                        lineno=24,
                        import_statement="from my_second_base_package.module_one.file_two import B",
                    ),
                    file_identifier="my_second_base_package.module_two.file_two",
                ),
                CIR103(
                    node=HPI(
                        lineno=25,
                        import_statement="from my_second_base_package.module_one import file_one",
                    ),
                    file_identifier="my_second_base_package.module_two.file_two",
                ),
                CIR103(
                    node=HPI(
                        lineno=26,
                        import_statement="from my_second_base_package.module_one import file_two",
                    ),
                    file_identifier="my_second_base_package.module_two.file_two",
                ),
                CIR103(
                    node=HPI(
                        lineno=27,
                        import_statement="from my_second_base_package.module_one import C",
                    ),
                    file_identifier="my_second_base_package.module_two.file_two",
                ),
                CIR103(
                    node=HPI(
                        lineno=28,
                        import_statement="from my_second_base_package.module_two import file_one",
                    ),
                    file_identifier="my_second_base_package.module_two.file_two",
                ),
                CIR103(
                    node=HPI(
                        lineno=31, import_statement="from my_second_base_package.file import C"
                    ),
                    file_identifier="my_second_base_package.module_two.file_two",
                ),
                CIR103(
                    node=HPI(
                        lineno=32, import_statement="from my_second_base_package import module_one"
                    ),
                    file_identifier="my_second_base_package.module_two.file_two",
                ),
                CIR103(
                    node=HPI(lineno=34, import_statement="from my_second_base_package import file"),
                    file_identifier="my_second_base_package.module_two.file_two",
                ),
                CIR105(
                    node=HPI(lineno=37, import_statement="from my_third_base_package import G"),
                    file_identifier="my_second_base_package.module_two.file_two",
                ),
            ],
        ),
        (
            "example_repos/my_base_module/my_second_base_package/file.py",
            "my_second_base_package.file",
            BASE_EXPECTED_RESTRICTED_IDENTIFIERS.union(
                {
                    "my_second_base_package.module_one",
                    "my_second_base_package.module_one.file_one",
                    "my_second_base_package.module_one.file_two",
                    "my_second_base_package.module_two",
                    "my_second_base_package.module_two.file_one",
                    "my_second_base_package.module_two.file_two",
                }
            ),
            21,
            [
                CIR104(
                    node=HPI(lineno=3, import_statement="import uuid"),
                    file_identifier="my_second_base_package.file",
                ),
                CIR102(
                    node=HPI(
                        lineno=5,
                        import_statement="import my_second_base_package.module_one.file_one",
                    ),
                    file_identifier="my_second_base_package.file",
                ),
                CIR102(
                    node=HPI(
                        lineno=6,
                        import_statement="import my_second_base_package.module_one.file_two",
                    ),
                    file_identifier="my_second_base_package.file",
                ),
                CIR102(
                    node=HPI(lineno=7, import_statement="import my_second_base_package.module_one"),
                    file_identifier="my_second_base_package.file",
                ),
                CIR102(
                    node=HPI(
                        lineno=8,
                        import_statement="import my_second_base_package.module_two.file_one",
                    ),
                    file_identifier="my_second_base_package.file",
                ),
                CIR102(
                    node=HPI(
                        lineno=9,
                        import_statement="import my_second_base_package.module_two.file_two",
                    ),
                    file_identifier="my_second_base_package.file",
                ),
                CIR102(
                    node=HPI(
                        lineno=10, import_statement="import my_second_base_package.module_two"
                    ),
                    file_identifier="my_second_base_package.file",
                ),
                CIR104(
                    node=HPI(lineno=14, import_statement="import my_third_base_package"),
                    file_identifier="my_second_base_package.file",
                ),
                CIR105(
                    node=HPI(lineno=20, import_statement="from uuid import UUID"),
                    file_identifier="my_second_base_package.file",
                ),
                CIR105(
                    node=HPI(lineno=21, import_statement="from uuid import uuid4"),
                    file_identifier="my_second_base_package.file",
                ),
                CIR103(
                    node=HPI(
                        lineno=23,
                        import_statement="from my_second_base_package.module_one.file_one import A",
                    ),
                    file_identifier="my_second_base_package.file",
                ),
                CIR103(
                    node=HPI(
                        lineno=24,
                        import_statement="from my_second_base_package.module_one.file_two import B",
                    ),
                    file_identifier="my_second_base_package.file",
                ),
                CIR103(
                    node=HPI(
                        lineno=25,
                        import_statement="from my_second_base_package.module_one import file_one",
                    ),
                    file_identifier="my_second_base_package.file",
                ),
                CIR103(
                    node=HPI(
                        lineno=26,
                        import_statement="from my_second_base_package.module_one import file_two",
                    ),
                    file_identifier="my_second_base_package.file",
                ),
                CIR103(
                    node=HPI(
                        lineno=27,
                        import_statement="from my_second_base_package.module_one import C",
                    ),
                    file_identifier="my_second_base_package.file",
                ),
                CIR103(
                    node=HPI(
                        lineno=28,
                        import_statement="from my_second_base_package.module_two import file_one",
                    ),
                    file_identifier="my_second_base_package.file",
                ),
                CIR103(
                    node=HPI(
                        lineno=29,
                        import_statement="from my_second_base_package.module_two import file_two",
                    ),
                    file_identifier="my_second_base_package.file",
                ),
                CIR103(
                    node=HPI(
                        lineno=30,
                        import_statement="from my_second_base_package.module_two import D",
                    ),
                    file_identifier="my_second_base_package.file",
                ),
                CIR103(
                    node=HPI(
                        lineno=32, import_statement="from my_second_base_package import module_one"
                    ),
                    file_identifier="my_second_base_package.file",
                ),
                CIR103(
                    node=HPI(
                        lineno=33, import_statement="from my_second_base_package import module_two"
                    ),
                    file_identifier="my_second_base_package.file",
                ),
                CIR105(
                    node=HPI(lineno=37, import_statement="from my_third_base_package import G"),
                    file_identifier="my_second_base_package.file",
                ),
            ],
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_three.py",
            "my_second_base_package.module_three",
            BASE_EXPECTED_RESTRICTED_IDENTIFIERS,
            5,
            [
                CIR104(
                    node=HPI(lineno=3, import_statement="import uuid"),
                    file_identifier="my_second_base_package.module_three",
                ),
                CIR104(
                    node=HPI(lineno=14, import_statement="import my_third_base_package"),
                    file_identifier="my_second_base_package.module_three",
                ),
                CIR105(
                    node=HPI(lineno=20, import_statement="from uuid import UUID"),
                    file_identifier="my_second_base_package.module_three",
                ),
                CIR105(
                    node=HPI(lineno=21, import_statement="from uuid import uuid4"),
                    file_identifier="my_second_base_package.module_three",
                ),
                CIR105(
                    node=HPI(lineno=37, import_statement="from my_third_base_package import G"),
                    file_identifier="my_second_base_package.module_three",
                ),
            ],
        ),
    ],
)
def test_complex_imports(
    filename: str,
    expected_current_module: str,
    expected_restricted_identifiers: set,
    expected: int,
    expected_errors: list[str],
    get_base_plugin: callable,
    custom_import_rules_fixture: str,
    package_10: list[str],
) -> None:
    """Test restricted imports."""
    lines = custom_import_rules_fixture.split("\n")
    tree = ast.parse(custom_import_rules_fixture)
    options = {
        "base_packages": ["my_second_base_package"],
        "custom_restrictions": convert_to_dict(package_10),
        "checker_settings": Settings(
            **{
                "CUSTOM_RESTRICTIONS": convert_to_dict(package_10),
                "RESTRICT_DYNAMIC_IMPORTS": False,
                "RESTRICT_LOCAL_SCOPE_IMPORTS": False,
                "RESTRICT_RELATIVE_IMPORTS": False,
            }
        ),
    }
    plugin = get_base_plugin(tree=tree, filename=filename, lines=lines, options=options)

    import_rules = plugin.import_rules
    assert isinstance(import_rules, CustomImportRules)
    plugin.get_run_list()

    restricted_identifiers = plugin.restricted_identifiers
    assert isinstance(restricted_identifiers, defaultdict)
    assert plugin.import_rules.restricted_identifiers == restricted_identifiers

    assert set(restricted_identifiers.keys()) == expected_restricted_identifiers

    errors = plugin.errors
    assert isinstance(errors, list)
    assert len(errors) == expected
    assert plugin.errors_set == {str(error) for error in expected_errors}, sorted(plugin.errors_set)


@pytest.mark.parametrize(
    ("test_case", "expected"),
    [
        (
            "example_repos/my_base_module/my_second_base_package/module_one/file_one.py",
            [
                CIR105(
                    node=HPI(lineno=3, import_statement="from uuid import UUID"),
                    file_identifier="my_second_base_package.module_one.file_one",
                ),
                CIR105(
                    node=HPI(lineno=4, import_statement="from uuid import uuid4"),
                    file_identifier="my_second_base_package.module_one.file_one",
                ),
            ],
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_one/file_two.py",
            [
                CIR105(
                    node=HPI(lineno=3, import_statement="from uuid import UUID"),
                    file_identifier="my_second_base_package.module_one.file_two",
                ),
                CIR105(
                    node=HPI(lineno=4, import_statement="from uuid import uuid4"),
                    file_identifier="my_second_base_package.module_one.file_two",
                ),
            ],
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_two/file_one.py",
            [
                CIR104(
                    node=HPI(lineno=2, import_statement="import uuid"),
                    file_identifier="my_second_base_package.module_two.file_one",
                ),
                CIR103(
                    node=HPI(
                        lineno=10,
                        import_statement="from my_second_base_package.module_one.file_two import "
                        "ModuleTwo",
                    ),
                    file_identifier="my_second_base_package.module_two.file_one",
                ),
                CIR103(
                    node=HPI(
                        lineno=11,
                        import_statement="from my_second_base_package.module_two.file_two "
                        "import ModuleTwoFileTwo",
                    ),
                    file_identifier="my_second_base_package.module_two.file_one",
                ),
            ],
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_two/file_two.py",
            [
                CIR105(
                    node=HPI(lineno=3, import_statement="from uuid import UUID"),
                    file_identifier="my_second_base_package.module_two.file_two",
                ),
                CIR105(
                    node=HPI(lineno=4, import_statement="from uuid import uuid4"),
                    file_identifier="my_second_base_package.module_two.file_two",
                ),
            ],
        ),
        (
            "example_repos/my_base_module/my_second_base_package/module_three.py",
            [
                CIR104(
                    node=HPI(lineno=9, import_statement="import my_base_module.module_y"),
                    file_identifier="my_second_base_package.module_three",
                ),
                CIR105(
                    node=HPI(lineno=11, import_statement="from my_base_module.module_x import X"),
                    file_identifier="my_second_base_package.module_three",
                ),
                CIR105(
                    node=HPI(lineno=3, import_statement="from uuid import UUID"),
                    file_identifier="my_second_base_package.module_three",
                ),
                CIR105(
                    node=HPI(lineno=4, import_statement="from uuid import uuid4"),
                    file_identifier="my_second_base_package.module_three",
                ),
            ],
        ),
    ],
)
def test_custom_restrictions(
    test_case: str,
    expected: set,
    get_flake8_linter_results: callable,
    package_10: list[str],
) -> None:
    """Test restricted imports."""
    filename = normalize_path(test_case)
    assert os.path.exists(filename)
    lines = pycodestyle.readlines(filename)
    identifier = get_module_name_from_filename(filename)
    root_package_name(identifier)
    options = {
        "base_packages": ["base_package", "my_second_base_package"],
        "custom_restrictions": convert_to_dict(package_10),
        "checker_settings": Settings(
            **{
                "CUSTOM_RESTRICTIONS": convert_to_dict(package_10),
                "RESTRICT_DYNAMIC_IMPORTS": False,
                "RESTRICT_LOCAL_SCOPE_IMPORTS": False,
                "RESTRICT_RELATIVE_IMPORTS": False,
            }
        ),
    }
    actual = get_flake8_linter_results(
        s="".join(lines), options=options, delimiter="\n", filename=filename
    )
    assert set(actual) == {str(error) for error in expected}, sorted(actual)


def test_custom_restrictions_import_settings_do_not_error(
    valid_custom_import_rules_imports: str,
    get_flake8_linter_results: callable,
) -> None:
    """Test restricted imports do not have an effect on regular import methods."""
    options = {
        "checker_settings": Settings(**{"CUSTOM_RESTRICTIONS": {}}),
        "custom_restrictions": {},
    }
    actual = get_flake8_linter_results(
        s=valid_custom_import_rules_imports, options=options, delimiter="\n"
    )
    assert actual == set()
