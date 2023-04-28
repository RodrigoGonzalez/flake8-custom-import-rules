"Error codes and messages."
from __future__ import annotations

from enum import Enum


class CustomImportRulesErrorCodes(Enum):
    """Error codes for custom import rules."""

    # Blocked Imports Rules
    BIR101 = "BIR101 Only top level imports are permitted in the project."
    BIR102 = "BIR102 Relative imports are blocked in the project."
    BIR103 = "BIR103 Conditional imports are blocked in the project."
    BIR104 = "BIR104 Local imports are blocked in the project."
    BIR105 = "BIR105 Functional imports are blocked in the project."
    BIR106 = "BIR106 Dynamic imports are blocked in the project."
    BIR107 = "BIR107 Star imports are blocked in the project."
    BIR108 = "BIR108 Aliased imports are blocked in the project."

    # Blocked Imports Rules for Special Cases
    BIR201 = "BIR201 Block import test_*/*_test modules."
    BIR202 = "BIR202 Block imports from test_*.py/*_test.py modules."
    BIR203 = "BIR203 Block import `conftest`."
    BIR204 = "BIR204 Block import from `conftest.py` modules."
    BIR205 = "BIR205 Block import tests package or import tests subdirectories."
    BIR206 = "BIR206 Block import from tests package or subdirectories."
    BIR207 = "BIR207 Block import `__init__`."
    BIR208 = "BIR208 Block imports from `__init__.py files`."

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
