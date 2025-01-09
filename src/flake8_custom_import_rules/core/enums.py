"""Enums used by the main package."""

from enum import Enum


class CustomImportRulesEnums(Enum):
    """Custom import rules."""

    PROJECT_ONLY = "PROJECT_ONLY"
    BASE_PACKAGE_ONLY = "BASE_PACKAGE_ONLY"
    FIRST_PARTY_ONLY = "FIRST_PARTY_ONLY"
    STANDALONE_MODULES = "STANDALONE_MODULES"
    STD_LIB_ONLY = "STD_LIB_ONLY"
    THIRD_PARTY_ONLY = "THIRD_PARTY_ONLY"
    RESTRICTED_PACKAGES = "RESTRICTED_PACKAGES"
    TOP_LEVEL_ONLY_IMPORTS = "TOP_LEVEL_ONLY_IMPORTS"
    CUSTOM_RESTRICTIONS = "CUSTOM_RESTRICTIONS"


class ProjectSpecialCasesEnums(Enum):
    """Project special cases."""

    INIT = "__init__"
    MAIN = "__main__"
    TESTS = "tests"
    CONTEST = "conftest"
    TEST_PREFIX = "test_"
    TEST_SUFFIX = "_test"
