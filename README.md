# flake8-custom-import-rules
A Flake8 plugin that enforces custom import rules, allowing users to define
and maintain clean and consistent import organization across their Python
projects.

## Motivation
Developers will find this Flake8 plugin extremely useful for enforcing custom
import rules and maintaining a consistent import organization across their
Python projects. By allowing users to define specific restrictions, isolated
packages, and import rules, this plugin helps to prevent unwanted dependencies
and ensures a clear separation between high-level and low-level packages.
Furthermore, it aids in managing lightweight packages by restricting them to
import only from the Python standard library or third-party libraries,
keeping them free from unnecessary dependencies. This plugin not only enhances
code readability and maintainability but also encourages a modular
architecture that is easier to understand, test, and debug. As a result,
developers can effortlessly adhere to best practices, ensuring their projects
remain clean, well-organized, and optimized for efficient collaboration.


A Flake8 plugin that enforces custom import rules, allowing users to define
and maintain clean and consistent import organization across their Python
projects.

Restricted imports: Limit specific import capabilities for packages. Define a
list of packages that are restricted from importing certain packages or
modules within your base package. For example, you might want to prevent
package A from importing package B or any of its subpackages.

Restricted imports can be configured in two ways:
- By package: Restrict a package from importing another package, or subpackages
  or modules from another package.
  Example: Prevent 'package_A' from importing 'package_B' or any of its
  subpackages or modules.
- By module: Restrict a module from importing specific modules.
  Example: Prevent 'module_A' from importing 'module_B'.

Restricted packages: Specify a list of packages that are not permitted to be
imported or used by other packages or modules within your base package. This
helps maintain a clear separation between high-level and low-level packages.

Example: Disallow importing 'low_level_package' into 'high_level_package'.

Isolated packages: Define a list of packages that cannot import from any other
packages within your base package. This ensures that certain packages remain
standalone and do not introduce unwanted dependencies.

Example: Make 'standalone_package' isolated, so it cannot import from any
other packages within the base package.

Standard library only imports: Specify a set of packages that can only import
from the Python standard library. This rule helps to keep specific packages
lightweight and free from third-party dependencies.

Example: Allow 'lightweight_package' to import only from Python standard
library modules.

# Example Configuration

```toml
[flake8]
restricted_imports = [
    "my_base_package.package_A:my_base_package.package_B",
    "my_base_package.module_X.py:my_base_package.module_Y.py",
]
isolated_packages = ["my_base_package.package_C"]
standard_library_only = ["my_base_package.package_D"]
third_party_only = ["my_base_package.package_E"]
local_only = ["my_base_package.package_F"]
```

```ini
[flake8]
restricted-imports =
    my_base_package.package_A:my_base_package.package_B
    my_base_package.module_X.py:my_base_package.module_Y.py
isolated-imports = my_base_package.package_C
standard-library-only = my_base_package.package_D
third-party-only = my_base_package.package_E
local-only = my_base_package.package_F

```

Restricted imports:
RMI1: Restricted module import
RMI2: Restricted package import
RFI1: Restricted module 'from import'
RFI2: Restricted package 'from import'
Restricted packages:
RPI1: Restricted package import
RFI3: Restricted package 'from import'

Isolated packages:
IPI1: Isolated package import
IFI1: Isolated package 'from import'

Local only imports:
LPI1: Non-local module import
LFI1: Non-local module 'from import'

Standard library only imports:
SLI1: Non-standard library module import
SFI1: Non-standard library module 'from import'

Third party only imports:
TPI1: Non-third party module import
TFI1: Non-third party module 'from import'



## Error Codes
| Error Code | Description |
| ---------- | ----------- |


## Limitations
This plugin is currently only compatible with Python 3.7+.

The plugin does not currently support the following import types:
- `from . import module`
- imports that use `__import__` or `importlib`
- imports in string literals
- dynamic imports (e.g. `__import__("module_name")`)
- imports using eval (e.g. `eval("import module_name")`)

## License
This project is licensed under the terms of the MIT license.

## Acknowledgements
[Flake8](https://github.com/PyCQA/flake8) - A wrapper around PyFlakes,
pycodestyle and McCabe.
[flake8-import-order](https://github.com/PyCQA/flake8-import-order) - Flake8
plugin that checks import order against various Python Style Guides. Used as
a reference for this plugin.
[Writing Plugins for Flake8](https://flake8.pycqa.org/en/latest/plugin-development/index.html) - Flake8
documentation on writing plugins.
[A flake8 plugin from scratch](https://www.youtube.com/watch?v=ot5Z4KQPBL8) - YouTube
video on writing a custom Flake8 plugin.
