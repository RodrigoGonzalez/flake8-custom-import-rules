# flake8-custom-import-rules
A Flake8 plugin that enforces custom import rules, allowing users to define and
maintain clean and consistent import organization across their Python projects.


## Motivation
This Flake8 plugin is extremely useful for enforcing custom import rules and
maintaining a consistent import organization across Python projects. By
allowing users to define specific restrictions, isolated packages, and import
rules, this plugin helps to prevent unwanted dependencies and ensures a clear
separation between high-level and low-level packages. Furthermore, it aids in
managing lightweight packages by restricting them to import only from the
Python standard library or third-party libraries, keeping them free
from unnecessary dependencies.

This plugin not only enhances code readability and maintainability but also
encourages a modular architecture that is easier to understand, test, and debug.
As a result, developers can effortlessly adhere to best practices, ensuring
their projects remain clean, well-organized, and optimized for efficient
collaboration.

In today's digital age, with the prolific production of code at many
organizations and the increasing number of contributors to various projects,
one of the significant challenges we face is the maintainability and
comprehensibility of code. Ensuring consistent and clean code is not merely
an aesthetic or pedantic pursuit; it directly impacts the efficiency of
onboarding new team members and the associated costs. Misunderstandings and
inconsistencies in code can lead to miscommunication, errors, and increased
time spent onboarding and training new staff. By enforcing custom import
rules and maintaining a consistent import organization across Python projects,
we can significantly mitigate these issues, streamlining the process of
integrating new team members and maintaining the high quality and readability
of our codebase.

### Rewrite this paragraph
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
  Example: Prevent 'package_A.module_A' from importing 'package_B.module_B'.

Restricted packages: Specify a list of packages that are not permitted to be
imported or used by other packages or modules within your base package. This
helps maintain a clear separation between high-level and low-level packages.

Example: Restrict importing 'lower_level_package' into 'higher_level_package'.

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


## Custom Import Rules

| Rule              | Description                                                                                   |
|-------------------|-----------------------------------------------------------------------------------------------|
| std_lib_only      | Restrict package to import only from the Python standard library.                             |
| project_only      | Restrict package to import only from the local package and the project's top-level package.   |
| base_package_only | Restrict package to import only from the project's top-level package only.                    |
| first_party_only  | Restrict package to import only from the local packages only.                                 |
| third_party_only  | Restrict package to import only from third-party libraries.                                   |
| isolated          | Make a package isolated, so it cannot import from any other packages within the base package. |
| restricted        | Restrict a package from importing another package, or modules from another package.           |


| RULE              | STD LIB | PROJECT* | FIRST PARTY | THIRD PARTY | FUTURE |
|-------------------|---------|----------|-------------|-------------|--------|
| std_lib_only      | X       |          |             |             | X      |
| project_only      | X       | X        | X           |             | X      |
| base_package_only | X       | X        |             |             | X      |
| first_party_only  | X       |          | X           |             | X      |
| third_party_only  | X       |          |             | X           | X      |
| isolated          | X       |          |             | X           | X      |


*Technically project imports are "First Party" imports, but in this case we want to make a distinction between the top-level package and the rest of the project.

# Example Configuration

```toml
[flake8]
# Define the base packages for your project
base_packages = ["my_base_package", "my_other_base_package"]
import_restrictions = [
    "my_base_package.package_A:my_base_package.package_B",  # Restrict `package_A` from importing `package_B`
    "my_base_package.module_X.py:my_base_package.module_Y.py",  # Restrict `module_X.py` from importing `module_Y.py`
]
# Make `package_C` an isolated package
isolated_modules = ["my_base_package.package_C"]
# Allow `package_D` to import only from the standard library
std_lib_only = ["my_base_package.package_D"]
# Allow `package_E` to import only from third-party libraries
third_party_only = ["my_base_package.package_E"]
# Allow `package_F` to import only from the local packages and the project's
# top-level package. This will treat the first package defined in `base_packages` as the top-level package.
first_party_only = ["my_base_package.package_F"]
# Allow `package_G` to import only from the local package
project_only = ["my_base_package.package_G"]
```

```ini
[flake8]
base-packages = my_base_package,my_other_base_package
import-restrictions =
    my_base_package.package_A:my_base_package.package_B
    my_base_package.module_X.py:my_base_package.module_Y.py
restricted-packages = my_base_package.package_B
isolated-modules = my_base_package.package_C
std-lib-only = my_base_package.package_D
third-party-only = my_base_package.package_E
first-party-only = my_base_package.package_F
project-only = my_base_package.package_G
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
This plugin is currently only compatible with Python 3.8+.

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
