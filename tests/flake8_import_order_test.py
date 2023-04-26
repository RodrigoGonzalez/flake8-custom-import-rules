"""flake8-import-order compatibility test module."""
import pytest
from flake8_import_order.checker import ImportVisitor
from flake8_import_order.styles import ImportType


@pytest.mark.parametrize(
    ("module", "expected"),
    [
        ("__future__", ImportType.FUTURE),
        ("os", ImportType.STDLIB),
        ("pytest", ImportType.THIRD_PARTY),
        ("application_module", ImportType.APPLICATION),
        ("tests", ImportType.APPLICATION),
        ("company_module", ImportType.APPLICATION_PACKAGE),
    ],
)
@pytest.mark.usefixtures("import_visitor")
def test_import_visitor__classify_type_method(module, expected, import_visitor):
    """Test the `_classify_type` method returns expected values"""
    assert import_visitor._classify_type(module) == expected


@pytest.mark.usefixtures("import_visitor")
def test_import_visitor__inherits_from_ast_node_visitor(import_visitor):
    """Test the public import visitor inherits from ast.NodeVisitor."""
    assert isinstance(import_visitor, ImportVisitor)


@pytest.mark.usefixtures("import_visitor")
def test_import_visitor__has_expected_attributes(import_visitor):
    """Test the public import visitor has expected attributes."""
    assert hasattr(import_visitor, "application_import_names")
    assert hasattr(import_visitor, "application_package_names")
    assert hasattr(import_visitor, "imports")


@pytest.mark.parametrize(
    "expected_attributes",
    [
        "FUTURE",
        "STDLIB",
        "THIRD_PARTY",
        "APPLICATION_PACKAGE",
        "APPLICATION",
        "APPLICATION_RELATIVE",
        "MIXED",
    ],
)
def test_import_type__has_expected_attributes(expected_attributes):
    """Test the import type has expected attributes."""
    msg = (
        f"ImportType does not have attribute {expected_attributes}, "
        f"check flask8_import_order version"
    )
    assert hasattr(ImportType, expected_attributes), msg
