from attr import define

from flake8_custom_import_rules.codes.error_codes import ErrorCode
from flake8_custom_import_rules.core.nodes import ParsedNode


@define(slots=True)
class ErrorMessage:
    """Error message"""

    lineno: int
    col_offset: int
    code: str
    message: str
    custom_explanation: str | None = None

    def __attrs_post_init__(self) -> None:
        """Post init."""
        self.custom_explanation = self.custom_explanation or ""
        self.message = f"{self.message} {self.custom_explanation}".strip()


def standard_error_message(
    node: ParsedNode,
    error_code: ErrorCode,
    custom_explanation: str | None = None,
) -> ErrorMessage:
    """Generate error message from node."""
    return ErrorMessage(
        lineno=node.lineno,
        col_offset=node.col_offset,
        code=error_code.code,
        message=error_code.message,
        custom_explanation=custom_explanation,
    )


def std_lib_only_error(
    node: ParsedNode,
    error_code: ErrorCode,
) -> ErrorMessage:
    """Generate error message for std lib only."""
    custom_explanation = (
        f"Using '{node.import_node}'."
        # f"which is not a Python standard library."
    )
    return standard_error_message(node, error_code, custom_explanation)


def third_party_only_error(
    node: ParsedNode,
    error_code: ErrorCode,
) -> ErrorMessage:
    """Generate error message for third-party only."""
    custom_explanation = (
        f"Using '{node.import_node}'."
        # f"which is not a third-party library."
    )
    return standard_error_message(node, error_code, custom_explanation)
