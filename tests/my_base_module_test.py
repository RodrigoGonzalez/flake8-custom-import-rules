""" Test module included in the example repo. """
import ast
import os

import pycodestyle

from flake8_custom_import_rules.core.node_visitor import CustomImportRulesVisitor
from flake8_custom_import_rules.core.rules_checker import BaseCustomImportRulePlugin

filename = "example_repos/my_base_module/my_base_module/package_a/module_a.py"
# filename = "example_repos/my_base_module/my_base_module/package_c/module_c.py"
# filename = "example_repos/my_base_module/my_base_module/module_y.py"
# filename = "example_repos/my_base_module/my_base_module/module_z.py"
current_module = os.path.split(filename)[-1].split(".")[0]
lines = pycodestyle.readlines(filename)
tree = ast.parse("".join(lines))

plugin = BaseCustomImportRulePlugin(tree=tree, filename=filename)
plugin.get_run_list()

# data = "from .module_a_relative import ARelative"
# tree = ast.parse(data)

visitor = CustomImportRulesVisitor(["my_base_module"], [])
visitor.visit(tree)
visitor.nodes
