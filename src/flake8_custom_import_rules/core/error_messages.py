""" Error messages for custom import rules. """

from attrs import define

from flake8_custom_import_rules.codes.error_codes import ErrorCode
from flake8_custom_import_rules.core.nodes import ParsedNode


@define(slots=True)
class ErrorMessage:
    """Error message

    Attributes
    ----------
    lineno : int
        The line number of the error.
    col_offset : int
        The column offset of the error.
    code : str
        The error code.
    message : str
        The error message to show to the user.
    custom_explanation : str | None
        Custom explanation to add to the error message.
    """

    lineno: int
    col_offset: int
    code: str
    message: str
    custom_explanation: str | None = None

    def __attrs_post_init__(self) -> None:
        """Post init."""
        self.custom_explanation = self.custom_explanation or ""
        self.message = f"{self.message} {self.custom_explanation}".strip()

    def __str__(self) -> str:
        """Return the error message."""
        return f"{self.lineno}:{self.col_offset}: {self.code} {self.message}"


def standard_error_message(
    node: ParsedNode,
    error_code: ErrorCode,
    custom_explanation: str | None = None,
) -> ErrorMessage:
    """
    Generate error message from node.

    Parameters
    ----------
    node : ParsedNode
        The node that caused the error.
    error_code : ErrorCode
        The error code.
    custom_explanation : str | None
        Custom explanation to add to the error message.

    Returns
    -------
    ErrorMessage
    """
    return ErrorMessage(
        lineno=node.lineno,
        col_offset=node.col_offset,
        code=error_code.code,
        message=error_code.message,
        custom_explanation=custom_explanation,
    )


def standalone_imports_error(
    node: ParsedNode,
    error_code: ErrorCode,
    file_identifier: str,
) -> ErrorMessage:
    """Generate error message for standalone imports."""
    custom_explanation = (
        f"Using '{node.import_statement}'. Standalone module '{file_identifier}' "
        f"cannot import from project packages."
    )
    return standard_error_message(node, error_code, custom_explanation)


def std_lib_only_error(
    node: ParsedNode,
    error_code: ErrorCode,
) -> ErrorMessage:
    """
    Generate error message for std lib only.

    Parameters
    ----------
    node : ParsedNode
        The node that caused the error.
    error_code : ErrorCode
        The error code.

    Returns
    -------
    ErrorMessage
    """
    custom_explanation = (
        f"Using '{node.import_statement}'."
        # f"which is not a Python standard library."
    )
    return standard_error_message(node, error_code, custom_explanation)


def third_party_only_error(
    node: ParsedNode,
    error_code: ErrorCode,
) -> ErrorMessage:
    """
    Generate error message for third-party only.

    Parameters
    ----------
    node : ParsedNode
        The node that caused the error.
    error_code : ErrorCode
        The error code.

    Returns
    -------
    ErrorMessage
    """
    custom_explanation = (
        f"Using '{node.import_statement}'."
        # f"which is not a third-party library."
    )
    return standard_error_message(node, error_code, custom_explanation)


def first_party_only_error(
    node: ParsedNode,
    error_code: ErrorCode,
) -> ErrorMessage:
    """Generate error message for first-party only.

    Parameters
    ----------
    node : ParsedNode
        The node that caused the error.
    error_code : ErrorCode
        The error code.

    Returns
    -------
    ErrorMessage
    """
    custom_explanation = (
        f"Using '{node.import_statement}'."
        # f"which is not a first-party library."
    )
    return standard_error_message(node, error_code, custom_explanation)


def restricted_package_error(
    node: ParsedNode,
    error_code: ErrorCode,
    file_identifier: str,
) -> ErrorMessage:
    """Generate error message for restricted imports.

    Parameters
    ----------
    node : ParsedNode
        The node that caused the error.
    error_code : ErrorCode
        The error code.
    file_identifier : str
        The file identifier.

    Returns
    -------
    ErrorMessage
    """
    custom_explanation = (
        f"Using '{node.import_statement}'. Restricted package "
        f"cannot be imported into module '{file_identifier}'."
    )
    return standard_error_message(node, error_code, custom_explanation)


def import_restriction_error(
    node: ParsedNode,
    error_code: ErrorCode,
    file_identifier: str,
) -> ErrorMessage:
    """Generate error message for import restriction.

    Parameters
    ----------
    node : ParsedNode
        The node that caused the error.
    error_code : ErrorCode
        The error code.
    file_identifier : str
        The file identifier.

    Returns
    -------
    ErrorMessage
    """
    custom_explanation = (
        f"Using '{node.import_statement}'. Restricted package/module "
        f"cannot be imported into module '{file_identifier}'."
    )
    return standard_error_message(node, error_code, custom_explanation)
