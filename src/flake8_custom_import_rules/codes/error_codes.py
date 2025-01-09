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
        """Determine if the given item is present in the error code enumeration."""
        if isinstance(item, str):
            return item in (member.value.split(" ")[0] for member in self)  # type: ignore
        elif isinstance(item, Enum):
            return item.name in self._member_map_
        else:
            return False

    def __call__(  # type: ignore
        cls, input_value: Any, *args: Any, **kwargs: Any
    ) -> Enum | type[Enum]:
        """Validate if the input value corresponds to a defined error code."""
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
    """Error codes for custom import rules.

    Error codes are used to identify the error and to provide a short
    description of the error.
    """

    # Custom Import Rules: Restricting imports
    CIR101 = "CIR101 Custom import rule conflicts."
    CIR102 = "CIR102 Import Restriction Violation. Restricted project import."
    CIR103 = "CIR103 Import Restriction Violation. Restricted project `from import`"
    CIR104 = "CIR104 Import Restriction Violation. Restricted non-project import."
    CIR105 = "CIR105 Import Restriction Violation. Restricted non-project `from import`."
    # Restricted package: For example the high level package can `app` is restricted
    CIR106 = "CIR106 Restricted Package Violation. Restricted project import."
    CIR107 = "CIR107 Restricted Package Violation. Restricted project `from import`."

    # Project only imports. No packages and modules from outside your project
    # (i.e. No Third Party Imports)
    CIR201 = "CIR201 Non-project package import."
    CIR202 = "CIR202 Non-project module import."
    CIR203 = "CIR203 Non-base package package import."
    CIR204 = "CIR204 Non-base package module import."
    CIR205 = "CIR205 Non-first party package import."
    CIR206 = "CIR206 Non-first party module import."

    # Standalone package: Package/module that can not import from any other package in your project.
    # Standalone package.
    CIR301 = "CIR301 Standalone package, imports from project disabled."
    CIR302 = "CIR302 Standalone package, from imports from project disabled."
    CIR303 = "CIR303 Standalone module, imports from project disabled."
    CIR304 = "CIR304 Standalone module, from imports from project disabled."

    # Standard library only import in specified packages or modules
    CIR401 = "CIR401 Non-standard library package import."
    CIR402 = "CIR402 Non-standard library module import."

    # Third party only imports:
    CIR501 = "CIR501 Non-third party package import."
    CIR502 = "CIR502 Non-third party module import."

    # Project Level Import Rules and Restrictions
    PIR101 = "PIR101 Only top level imports are permitted in the project."
    PIR102 = "PIR102 Relative Imports are disabled for this project."
    PIR103 = "PIR103 Local Imports are disabled for this project."
    PIR104 = "PIR104 Conditional Imports are disabled for this project."
    PIR105 = "PIR105 Dynamic Imports are disabled for this project."
    PIR106 = "PIR106 Private Imports are disabled for this project."
    PIR107 = "PIR107 Wildcard Imports are disabled for this project."
    PIR108 = "PIR108 Aliased Imports are disabled for this project."
    PIR109 = "PIR109 Future Imports are disabled for this project."

    # Project Level Import Rules for Special Cases
    PIR201 = "PIR201 Importing test_*/*_test modules is restricted."
    PIR202 = "PIR202 Importing from test_*.py/*_test.py modules is restricted."
    PIR203 = "PIR203 Importing 'conftest' is restricted."
    PIR204 = "PIR204 Importing from `conftest.py` modules is restricted."
    PIR205 = "PIR205 Importing tests directory or tests subdirectories is restricted."
    PIR206 = "PIR206 Importing from tests directory or its subdirectories is restricted."
    PIR207 = "PIR207 Importing `__init__` is restricted."
    PIR208 = "PIR208 Importing from `__init__.py` files is restricted."
    PIR209 = "PIR209 Importing `__main__` is restricted."
    PIR210 = "PIR210 Importing from `__main__.py` files is restricted."

    # Dynamic Imports Rules and Special Cases
    PIR301 = "PIR301 Potential dynamic import failed confirmation checks."
    PIR302 = "PIR302 Attempt to parse dynamic value string failed"

    # conditions = {
    #     CIR101: lambda node: "__init__" in node.module,
    #     CIR102: lambda node: "restricted_package" in node.module,
    #     # ... other conditions ...
    # }
    #
    # @classmethod
    # def check_condition(cls, error_code, node):
    #     if condition := cls.conditions.get(error_code):
    #         return condition(node)
    #     return False

    @property
    def code(self) -> str:
        """Get error code."""
        return self.name

    @property
    def message(self) -> str:
        """Get error code."""
        return self.value.split(f"{self.name} ")[1]

    @property
    def full_message(self) -> str:
        """Get error code."""
        return self.value

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
    def get_all_project_import_rule_codes(cls) -> list[str]:
        """Get all blocked import rule codes."""
        return [code for code in cls.get_all_error_codes() if code.startswith("PIR")]

    @classmethod
    def get_all_custom_import_rule_codes(cls) -> list[str]:
        """Get all custom import rule codes."""
        return [code for code in cls.get_all_error_codes() if code.startswith("CIR")]


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
AllProjectImportCodes = ErrorCode.get_all_project_import_rule_codes()
AllCustomImportCodes = ErrorCode.get_all_custom_import_rule_codes()
