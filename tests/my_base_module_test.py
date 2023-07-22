""" Test module included in the example repo. """
import ast
import os

import pycodestyle

from flake8_custom_import_rules.core.node_visitor import CustomImportRulesVisitor
from flake8_custom_import_rules.core.rules_checker import BaseCustomImportRulePlugin

file_name = "example_repos/my_base_module/my_base_module/package_a/module_a.py"
# file_name = "example_repos/my_base_module/my_base_module/package_c/module_c.py"
# file_name = "example_repos/my_base_module/my_base_module/module_y.py"
# file_name = "example_repos/my_base_module/my_base_module/module_z.py"
current_module = os.path.split(file_name)[-1].split(".")[0]
lines = pycodestyle.readlines(file_name)
tree = ast.parse("".join(lines))

plugin = BaseCustomImportRulePlugin(tree=tree, file_name=file_name)
plugin.get_run_list()

# data = "import sys; attrs = sys.modules['attrs']"
# tree = ast.parse(data)

visitor = CustomImportRulesVisitor(["my_base_module"], None)
visitor.visit(tree)
visitor.nodes
