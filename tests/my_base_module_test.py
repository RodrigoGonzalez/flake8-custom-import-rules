""" Test module included in the example repo. """
import ast
import os
from textwrap import dedent

import pycodestyle

from flake8_custom_import_rules.core.node_visitor import CustomImportRulesVisitor
from flake8_custom_import_rules.core.rules_checker import BaseCustomImportRulePlugin
from flake8_custom_import_rules.utils.node_utils import is_import_restricted

filename = "example_repos/my_base_module/my_base_module/package_a/module_a.py"
# filename = "example_repos/my_base_module/my_base_module/package_c/module_c.py"
# filename = "example_repos/my_base_module/my_base_module/module_y.py"
# filename = "example_repos/my_base_module/my_base_module/module_z.py"
filename = "example_repos/my_base_module/my_second_base_package/module_three.py"
file_identifier = os.path.split(filename)[-1].split(".")[0]
lines = pycodestyle.readlines(filename)
tree = ast.parse("".join(lines))

plugin = BaseCustomImportRulePlugin(tree=tree, filename=filename, lines=lines)
plugin.get_run_list()
plugin.get_import_nodes()
for _, _, node, _ in plugin.get_import_nodes():
    print(node)

# data = "import sys; attrs = sys.modules['attrs']"
# tree = ast.parse(data)

visitor = CustomImportRulesVisitor(["my_base_module"], None)
visitor.visit(tree)
visitor.nodes


COMPLEX_IMPORTS = dedent(
    """
    import my_second_base_package.module_one.file_one
    import my_second_base_package.module_one.file_two
    import my_second_base_package.module_one
    import my_second_base_package.module_two.file_one
    import my_second_base_package.module_two.file_two
    import my_second_base_package.module_two
    import my_second_base_package.file
    import my_second_base_package
    import base_package
    import my_third_base_package

    from my_second_base_package.module_one.file_one import A
    from my_second_base_package.module_one.file_two import B
    from my_second_base_package.module_one import file_one
    from my_second_base_package.module_one import file_two
    from my_second_base_package.module_one import C
    from my_second_base_package.module_two import file_one
    from my_second_base_package.module_two import file_two
    from my_second_base_package.module_two import D
    from my_second_base_package.file import C
    from my_second_base_package import module_one
    from my_second_base_package import module_two
    from my_second_base_package import file
    from my_second_base_package import E
    from base_package import F
    from my_third_base_package import G
    """
)

restricted_imports = [
    "my_second_base_package",
    "my_second_base_package.module_one",
    "my_second_base_package.module_one.file_one",
    "my_third_base_package",
]

current_modules = [
    "my_second_base_package.module_one.file_one",
    "my_second_base_package.module_one.file_two",
    "my_second_base_package.module_two.file_one",
    "my_second_base_package.module_two.file_two",
    "my_second_base_package.file",
]

current_module = "my_second_base_package.module_one.file_two"
# filename = "example_repos/my_second_base_package/module_one/file_two.py"
lines = COMPLEX_IMPORTS.split("\n")
tree = ast.parse(COMPLEX_IMPORTS)

plugin = BaseCustomImportRulePlugin(tree=tree, filename=filename, lines=lines)
plugin.get_run_list()
plugin.get_import_nodes()
parsed_imports = [parsed_import for _, _, parsed_import, _ in plugin.get_import_nodes()]
for current_module in current_modules:
    print(f"\n\nCurrent module: {current_module}")
    for parsed_import in parsed_imports:
        print(
            f"Is '{parsed_import.import_statement}' allowed in '{current_module}'? "
            f"{is_import_restricted(parsed_import, current_module, restricted_imports)}"
        )
