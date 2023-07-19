"""Error codes and messages."""
from enum import Enum
from enum import EnumMeta
from functools import singledispatch
from typing import Any

from flake8_custom_import_rules.codes.exceptions import ErrorCodeError
from flake8_custom_import_rules.codes.exceptions import ErrorCodeTypeError


class ErrorCodeMeta(EnumMeta):
    """Metaclass for error codes."""

    def __contains__(self, item: Any) -> bool:
        """Check if item is in the error code."""
        if isinstance(item, str):
            return item in (member.value.split(" ")[0] for member in self)  # type: ignore
        elif isinstance(item, Enum):
            return item.name in self._member_map_
        else:
            return False

    def __call__(  # type: ignore
        cls, input_value: Any, *args: Any, **kwargs: Any
    ) -> Enum | type[Enum]:
        """Check if input value is a valid error code."""
        if not isinstance(input_value, str):
            try:
                return super().__call__(input_value, *args, **kwargs)
            except ValueError as e:
                raise ErrorCodeTypeError(f"{input_value} is not a valid {cls.__name__} type") from e
        for member in cls:  # type: ignore
            if member.value.split(" ")[0] == input_value:
                return member
        raise ErrorCodeError(f"{input_value} is not a valid {cls.__name__}")


class ErrorCode(Enum, metaclass=ErrorCodeMeta):
    """Error codes for custom import rules."""

    # Custom Import Rules: Restricting imports
    CIR101 = "CIR101 Custom import rule conflicts"
    CIR102 = "CIR102 Restrict package import for specific package or module"
    CIR103 = "CIR103 Restrict package `from import` for specific package or module"
    CIR104 = "CIR104 Restrict module import for specific package or module"
    CIR105 = "CIR105 Restrict module `from import` for specific package or module"
    # Restricted package: For example the high level package can `app` is restricted
    CIR106 = "CIR106 Restricted package import, no one can import from this package"
    CIR107 = "CIR107 Restricted package `from import`, no one can import from this package"

    # Local only imports, packages and modules in your project:
    CIR201 = "CIR201 Non-local module import from a module or package outside your project"
    CIR202 = "CIR202 Non-local module `from import`"
    CIR203 = "CIR203 Non-local module import"
    CIR204 = "CIR204 Non-local module `from import`"

    # Isolated package: Package/module that can not import from any other package in your project.
    # Standalone package.
    CIR301 = "CIR301 Isolated package import from any other package in your project"
    CIR302 = "CIR302 Isolated package `from import` from any other package in your project"
    CIR303 = "CIR303 Isolated module import from any other package in your project"
    CIR304 = "CIR304 Isolated module `from import` from any other package in your project"

    # Standard library only imports:
    CIR401 = "CIR401 Non-standard library package import"
    CIR402 = "CIR402 Non-standard library package `from import`"
    CIR403 = "CIR403 Non-standard library module import"
    CIR404 = "CIR404 Non-standard library module `from import`"

    # Third party only imports:
    CIR501 = "CIR501 Non-third party package import"
    CIR502 = "CIR502 Non-third party package `from import`"

    # Project Import Rules
    PIR101 = "PIR101 Only top level imports are permitted in the project."
    PIR102 = "PIR102 Relative imports are blocked in the project."
    PIR103 = "PIR103 Conditional imports are blocked in the project."
    PIR104 = "PIR104 Local imports are blocked in the project."
    PIR105 = "PIR105 Functional imports are blocked in the project."
    PIR106 = "PIR106 Dynamic imports are blocked in the project."
    PIR107 = "PIR107 Star imports are blocked in the project."
    PIR108 = "PIR108 Aliased imports are blocked in the project."

    # Project Import Rules for Special Cases
    PIR201 = "PIR201 Block import test_*/*_test modules."
    PIR202 = "PIR202 Block imports from test_*.py/*_test.py modules."
    PIR203 = "PIR203 Block import `conftest`."
    PIR204 = "PIR204 Block import from `conftest.py` modules."
    PIR205 = "PIR205 Block import tests package or import tests subdirectories."
    PIR206 = "PIR206 Block import from tests package or subdirectories."
    PIR207 = "PIR207 Block import `__init__`."
    PIR208 = "PIR208 Block imports from `__init__.py files`."

    @staticmethod
    def get_error_code(error_code: Any) -> str:
        """Get error code."""
        return _get_error_code_dispatcher(error_code)

    @classmethod
    def get_error_message(cls, error_code: Any) -> str:
        """Get error message."""
        return _get_error_message_dispatcher(error_code)

    @classmethod
    def get_error_code_and_message(cls, error_code: str) -> tuple[str, str]:
        """Get error code and message."""
        return cls.get_error_code(error_code), cls.get_error_message(error_code)

    @classmethod
    def get_all_error_code_enums(cls) -> list["ErrorCode"]:
        """Get all error codes."""
        return list(cls)

    @classmethod
    def get_all_error_codes(cls) -> list[str]:
        """Get all error codes."""
        return [error_code.name for error_code in cls]

    @classmethod
    def get_all_blocked_import_rule_codes(cls) -> list[str]:
        """Get all blocked import rule codes."""
        return list(filter(lambda x: x.startswith("PIR"), cls.get_all_error_codes()))

    @classmethod
    def get_all_custom_import_rule_codes(cls) -> list[str]:
        """Get all custom import rule codes."""
        return list(filter(lambda x: x.startswith("CIR"), cls.get_all_error_codes()))


@singledispatch
def _get_error_code_dispatcher(error_code: Any) -> str:
    """Get error code dispatcher."""
    raise NotImplementedError(f"Unsupported type: {type(error_code)}")


@_get_error_code_dispatcher.register
def _(error_code: str) -> str:
    """Get error code."""
    if error_code.startswith("ErrorCode."):
        error_code = error_code.split(".")[1]
    if error_code.startswith("CIR") or error_code.startswith("PIR"):
        error_code = error_code.split(" ")[0]
    if error_code in ErrorCode.get_all_error_codes():
        return error_code
    raise ValueError(f"Invalid error code: {error_code}")


@_get_error_code_dispatcher.register
def _(error_code: ErrorCode) -> str:
    """Get error code."""
    return error_code.name


@singledispatch
def _get_error_message_dispatcher(error_code: Any) -> str:
    """Get error message dispatcher."""
    raise NotImplementedError(f"Unsupported type: {type(error_code)}")


@_get_error_message_dispatcher.register
def _(error_code: str) -> str:
    """Get error message."""
    if error_code in ErrorCode.get_all_error_codes():
        error_code = ErrorCode(error_code).value
    else:
        raise ValueError(f"Invalid error code: {error_code}")
    return " ".join(error_code.split(" ")[1:])


@_get_error_message_dispatcher.register
def _(error_code: ErrorCode) -> str:
    """Get error message."""
    return " ".join(error_code.value.split(" ")[1:])


AllErrorCodes = ErrorCode.get_all_error_codes()
AllBlockedImportCodes = ErrorCode.get_all_blocked_import_rule_codes()
AllCustomImportCodes = ErrorCode.get_all_custom_import_rule_codes()
