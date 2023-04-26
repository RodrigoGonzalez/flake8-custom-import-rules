# flake8-custom-import-rules
A Flake8 plugin that enforces custom import rules, allowing users to define and maintain clean and consistent import organization across their Python projects.

Restricted imports: Define a list of modules that are restricted from importing specific modules within your base module. For example, you might want to prevent module A from importing module B or any of its submodules.
Isolated imports: Specify a list of modules that cannot import from any other modules within your base module. This can be useful for ensuring that certain modules remain standalone and do not introduce unwanted dependencies.
Standard library only imports: Define a set of modules that can only import from the Python standard library. This rule helps to keep specific modules lightweight and free from third-party dependencies.

# Example Configuration

```toml
[flake8]
custom_import_rules.restricted_imports = [
    "my_base_module.module_A:my_base_module.module_B",
    "my_base_module.module_X:my_base_module.module_Y",
]
custom_import_rules.isolated_modules = ["my_base_module.module_C"]
custom_import_rules.standard_library_only = ["my_base_module.module_D"]
custom_import_rules.third_party_only = ["my_base_module.module_E"]
custom_import_rules.local_folder_only = ["my_base_module.module_F"]
```

```ini
[flake8]

[flake8.custom_import_rules]
restricted-imports =
    my_base_module.module_A:my_base_module.module_B
    my_base_module.module_X:my_base_module.module_Y
isolated-modules = my_base_module.module_C
standard-library_only = my_base_module.module_D
third-party-only = my_base_module.module_E
local-folder-only = my_base_module.module_F

```


## Acknowledgements
[Flake8](https://github.com/PyCQA/flake8) - A wrapper around PyFlakes, pycodestyle and McCabe.
[flake8-import-order](https://github.com/PyCQA/flake8-import-order) - Flake8 plugin that checks import order against various Python Style Guides. Used as a reference for this plugin.
[Writing Plugins for Flake8](https://flake8.pycqa.org/en/latest/plugin-development/index.html) - Flake8 documentation on writing plugins.
[A flake8 plugin from scratch](https://www.youtube.com/watch?v=ot5Z4KQPBL8) - YouTube video on writing a custom Flake8 plugin.
