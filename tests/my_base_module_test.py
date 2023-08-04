""" Test module included in the example repo. """
import ast

import pycodestyle

from tests.test_cases.conftest import BaseCustomImportRulePlugin

filename = "example_repos/my_base_module/my_base_module/package_a/module_a.py"


# filename = "example_repos/my_base_module/my_base_module/package_c/module_c.py"
# filename = "example_repos/my_base_module/my_base_module/module_y.py"
# filename = "example_repos/my_base_module/my_base_module/module_z.py"
# filename = "example_repos/my_base_module/my_second_base_package/module_three.py"
# file_identifier = os.path.split(filename)[-1].split(".")[0]
def print_import_nodes(filename: str) -> None:
    """
    Print the import nodes for a given file.

    Parameters
    ----------
    filename : str
        The filename to print the import nodes for.
    """
    lines = pycodestyle.readlines(filename)
    tree = ast.parse("".join(lines))

    plugin = BaseCustomImportRulePlugin(tree=tree, filename=filename, lines=lines)
    plugin.get_run_list()
    plugin.get_import_nodes()
    for _, _, node, _ in plugin.get_import_nodes():
        print(node)


# print_import_nodes(filename)

# data = "import sys; attrs = sys.modules['attrs']"
# tree = ast.parse(data)

# visitor = CustomImportRulesVisitor(["my_base_module"], None)
# visitor.visit(tree)
# visitor.nodes
