from __future__ import annotations

import pytest

from flake8_custom_import_rules.codes.error_codes import AllBlockedImportCodes
from flake8_custom_import_rules.codes.error_codes import AllCustomImportCodes
from flake8_custom_import_rules.codes.error_codes import AllErrorCodes
from flake8_custom_import_rules.codes.error_codes import ErrorCode
from flake8_custom_import_rules.codes.exceptions import ErrorCodeError
from flake8_custom_import_rules.codes.exceptions import ErrorCodeTypeError

BLOCKED_IMPORT_RULES = [
    "BIR101",
    "BIR102",
    "BIR103",
    "BIR104",
    "BIR105",
    "BIR106",
    "BIR107",
    "BIR108",
    "BIR201",
    "BIR202",
    "BIR203",
    "BIR204",
    "BIR205",
    "BIR206",
    "BIR207",
    "BIR208",
]

BLOCKED_IMPORT_RULES_ENUMS = [
    ErrorCode.BIR101,
    ErrorCode.BIR102,
    ErrorCode.BIR103,
    ErrorCode.BIR104,
    ErrorCode.BIR105,
    ErrorCode.BIR106,
    ErrorCode.BIR107,
    ErrorCode.BIR108,
    ErrorCode.BIR201,
    ErrorCode.BIR202,
    ErrorCode.BIR203,
    ErrorCode.BIR204,
    ErrorCode.BIR205,
    ErrorCode.BIR206,
    ErrorCode.BIR207,
    ErrorCode.BIR208,
]

CUSTOM_IMPORT_RULES = [
    "CIR101",
    "CIR102",
    "CIR103",
    "CIR104",
    "CIR105",
    "CIR106",
    "CIR107",
    "CIR201",
    "CIR202",
    "CIR203",
    "CIR204",
    "CIR301",
    "CIR302",
    "CIR303",
    "CIR304",
    "CIR401",
    "CIR402",
    "CIR403",
    "CIR404",
    "CIR501",
    "CIR502",
]

CUSTOM_IMPORT_RULES_ENUMS = [
    ErrorCode.CIR101,
    ErrorCode.CIR102,
    ErrorCode.CIR103,
    ErrorCode.CIR104,
    ErrorCode.CIR105,
    ErrorCode.CIR106,
    ErrorCode.CIR107,
    ErrorCode.CIR201,
    ErrorCode.CIR202,
    ErrorCode.CIR203,
    ErrorCode.CIR204,
    ErrorCode.CIR301,
    ErrorCode.CIR302,
    ErrorCode.CIR303,
    ErrorCode.CIR304,
    ErrorCode.CIR401,
    ErrorCode.CIR402,
    ErrorCode.CIR403,
    ErrorCode.CIR404,
    ErrorCode.CIR501,
    ErrorCode.CIR502,
]

ALL_ERROR_CODES = BLOCKED_IMPORT_RULES + CUSTOM_IMPORT_RULES

ALL_ERROR_CODES_ENUMS = BLOCKED_IMPORT_RULES_ENUMS + CUSTOM_IMPORT_RULES_ENUMS


@pytest.fixture(scope="module")
def error_codes():
    """Error codes."""
    return ALL_ERROR_CODES


@pytest.fixture(scope="module")
def error_code_enums():
    """Error codes."""
    return ALL_ERROR_CODES_ENUMS


@pytest.fixture(scope="module")
def enums_and_codes():
    """Error codes."""
    return error_code_enums + error_codes


@pytest.mark.usefixtures("error_codes")
def test_get_error_codes(error_codes):
    """Test get_error_codes."""
    msg = "ErrorCode changed, update tests."
    assert ErrorCode.get_all_error_codes() == error_codes, msg
    assert AllErrorCodes == error_codes, msg


def test_get_all_blocked_import_rule_codes():
    """Test get_all_blocked_import_rule_codes."""
    assert ErrorCode.get_all_blocked_import_rule_codes() == BLOCKED_IMPORT_RULES
    assert AllBlockedImportCodes == BLOCKED_IMPORT_RULES


def test_get_all_custom_import_rule_codes():
    """Test get_all_custom_import_rule_codes."""
    assert ErrorCode.get_all_custom_import_rule_codes() == CUSTOM_IMPORT_RULES
    assert AllCustomImportCodes == CUSTOM_IMPORT_RULES


@pytest.mark.parametrize("other_types", [1, 2.0, True, False, None, [], {}, (), set()])
def test_get_error_code__errors(other_types):
    """Test get_error_code does not work with other types."""
    with pytest.raises(NotImplementedError, match="Unsupported type"):
        assert ErrorCode.get_error_code(other_types) == other_types


@pytest.mark.parametrize("error_code", ALL_ERROR_CODES)
def test_get_error_code__str(error_code):
    """Test get_error_code."""
    assert ErrorCode.get_error_code(error_code) == error_code


@pytest.mark.parametrize("error_code", ["some_string", "", "BIR9999", "CIR9999"])
def test_get_error_code__str_error(error_code):
    """Test get_error_code does not work with strings that are not codes."""
    with pytest.raises(ValueError, match="Invalid error code"):
        assert ErrorCode.get_error_code(error_code) == error_code


@pytest.mark.parametrize("error_code_enum", ALL_ERROR_CODES_ENUMS)
def test_get_error_code__enum(error_code_enum):
    """Test get_error_code works with enums."""
    assert ErrorCode.get_error_code(error_code_enum) == error_code_enum.name


@pytest.mark.parametrize("other_types", [1, 2.0, True, False, None, [], {}, (), set()])
def test_get_error_message__errors(other_types):
    """Test get_error_message does not work with invalid types."""
    with pytest.raises(NotImplementedError, match="Unsupported type"):
        assert ErrorCode.get_error_message(other_types) == other_types


@pytest.mark.parametrize("error_code", ["some_string", "", "BIR9999", "CIR9999"])
def test_get_error_code_message__str_error(error_code):
    """Test get_error_message does not work with invalid strings."""
    with pytest.raises(ValueError, match="Invalid error code"):
        assert ErrorCode.get_error_message(error_code) == error_code


@pytest.mark.parametrize(
    ("error_code", "error_code_enum"), zip(ALL_ERROR_CODES, ALL_ERROR_CODES_ENUMS)
)
def test_get_error_code_message__str(error_code, error_code_enum):
    """Test get_error_message works with correct strings."""
    assert ErrorCode.get_error_message(error_code) == " ".join(error_code_enum.value.split(" ")[1:])


@pytest.mark.parametrize("error_code_enum", ALL_ERROR_CODES_ENUMS)
def test_get_error_code_message__enum(error_code_enum):
    """Test get_error_message works with correct enums."""
    assert isinstance(error_code_enum, ErrorCode)
    assert ErrorCode.get_error_message(error_code_enum) == " ".join(
        error_code_enum.value.split(" ")[1:]
    )


@pytest.mark.parametrize("error_code", ALL_ERROR_CODES)
def test_can_instantiate_using_error_code__str(error_code):
    """Test can instantiate using error code."""
    assert isinstance(ErrorCode(error_code), ErrorCode)


@pytest.mark.parametrize("wrong_string", ["some_string", "", "BIR9999", "CIR9999"])
def test_instantiate_using_error_code__error_wrong_code(wrong_string):
    """Test get_error_code."""
    with pytest.raises(ErrorCodeError, match="is not a valid ErrorCode"):
        assert isinstance(ErrorCode(wrong_string), ErrorCode)


@pytest.mark.parametrize("error_code", ALL_ERROR_CODES_ENUMS)
def test_can_instantiate_using_error_code__enum(error_code):
    """Test get_error_code."""
    assert isinstance(ErrorCode(error_code), ErrorCode)


@pytest.mark.parametrize("other_types", [1, 2.0, True, False, None, [], {}, (), set()])
def test_can_instantiate_using_error_code__error_wrong_type(other_types):
    """Test get_error_code."""
    with pytest.raises(ErrorCodeTypeError, match="is not a valid ErrorCode type"):
        assert isinstance(ErrorCode(other_types), ErrorCode)


##
@pytest.mark.parametrize("error_code", ALL_ERROR_CODES)
def test_membership__str(error_code):
    """Test can instantiate using error code."""
    assert error_code in ErrorCode


@pytest.mark.parametrize("wrong_string", ["some_string", "", "BIR9999", "CIR9999"])
def test_membership__error_wrong_code(wrong_string):
    """Test get_error_code."""
    assert wrong_string not in ErrorCode


@pytest.mark.parametrize("error_code_enum", ALL_ERROR_CODES_ENUMS)
def test_membership__enum(error_code_enum):
    """Test get_error_code."""
    assert error_code_enum in ErrorCode


@pytest.mark.parametrize("other_types", [1, 2.0, True, False, None, [], {}, (), set()])
def test_membership__error_wrong_type(other_types):
    """Test get_error_code."""
    assert other_types not in ErrorCode