# import pytest
# from flake8_import_order.checker import ImportVisitor
# from flake8_import_order.styles import ImportType
#
# from flake8_import_order import ImportVisitor
#
#
# @pytest.fixture(scope="module")
# def public_import_visitor():
#     """Return an instance of the public import visitor."""
#     return PublicImportVisitor(["application_module", "tests"], ["company_module"])
#
#
# @pytest.mark.usefixtures("public_import_visitor")
# def test_public_import_visitor__inherits_from_import_visitor(public_import_visitor):
#     """Test the public import visitor inherits from ImportVisitor."""
#     assert isinstance(public_import_visitor, ImportVisitor)
#
#
# @pytest.mark.usefixtures("public_import_visitor")
# def test_public_import_visitor__has_expected_attributes(public_import_visitor):
#     """Test the public import visitor has expected attributes."""
#     assert hasattr(public_import_visitor, "application_import_names")
#     assert hasattr(public_import_visitor, "application_package_names")
#     assert hasattr(public_import_visitor, "imports")
#
#
# @pytest.mark.parametrize(
#     ("module", "expected"),
#     [
#         ("__future__", ImportType.FUTURE),
#         ("os", ImportType.STDLIB),
#         ("pytest", ImportType.THIRD_PARTY),
#         ("application_module", ImportType.APPLICATION),
#         ("tests", ImportType.APPLICATION),
#         ("company_module", ImportType.APPLICATION_PACKAGE),
#     ],
# )
# @pytest.mark.usefixtures("public_import_visitor", "import_visitor")
# def test_public_import_visitor__consistent_with_import_visitor(
#     module, expected, public_import_visitor, import_visitor
# ):
#     """Test the public import visitor is consistent with the import visitor."""
#     assert (
#         public_import_visitor.classify_type(module)
#         == import_visitor._classify_type(module)
#         == expected
#     )
