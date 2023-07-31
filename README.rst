==========================
flake8-custom-import-rules
==========================
A ``flake8`` plugin that enforces custom import rules, allowing users to define and
maintain clean and consistent import organization across their Python projects.


Introduction
------------

This ``flake8`` plugin significantly enhances the organization and consistency of
imports in Python projects. By enabling developers to set custom restrictions,
define isolated packages, and establish import rules, the plugin aids in
mitigating unwanted dependencies and maintaining clear separations between
packages. Specifically, it facilitates the management of lightweight packages
by limiting their imports to the Python standard library or third-party
libraries, thus preventing unnecessary dependencies. Beyond enhancing
readability and maintainability, the plugin promotes a modular architecture
that is easier to comprehend, test, and debug. Consequently, developers can
smoothly adhere to best practices, maintaining their projects in a clean,
organized, and collaborative-friendly state.

Installation
------------

Install from ``pip`` with:

.. code-block:: sh

     pip install flake8-custom-import-rules

Motivation
----------

This ``flake8`` plugin is extremely useful for enforcing custom import rules and
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


A ``flake8`` plugin that enforces custom import rules, allowing users to define
and maintain clean and consistent import organization across their Python
projects.

Restricted imports: Limit specific import capabilities for packages. Define a
list of packages that are restricted from importing certain packages or
modules within your base package. For example, you might want to prevent
package A from importing package B or any of its subpackages.

Restricted imports can be configured in two ways:

- By package: Restrict a package from importing another package, or subpackages
  or modules from another package.

  Example: Prevent 'package_a' from importing 'package_b' or any of its
  subpackages or modules.

- By module: Restrict a module from importing specific modules.
  Example: Prevent 'package_a.module_a' from importing 'package_b.module_b'.

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


Custom Import Rules
-------------------

+----------------------+-----------------------------------------------------------------------------------------------+
| Option               | Description                                                                                   |
+======================+===============================================================================================+
| --std-lib-only       | Restrict package to import only from the Python standard library.                             |
+----------------------+-----------------------------------------------------------------------------------------------+
| --project-only       | Restrict package to import only from the local package and the project's top-level package.   |
+----------------------+-----------------------------------------------------------------------------------------------+
| --base-package-only  | Restrict package to import only from the project's top-level package only.                    |
+----------------------+-----------------------------------------------------------------------------------------------+
| --first-party-only   | Restrict package to import only from the local packages only.                                 |
+----------------------+-----------------------------------------------------------------------------------------------+
| --third-party-only   | Restrict package to import only from third-party libraries.                                   |
+----------------------+-----------------------------------------------------------------------------------------------+
| --isolated           | Make a package isolated, so it cannot import from any other packages within the base package. |
+----------------------+-----------------------------------------------------------------------------------------------+
| --restricted         | Restrict a package from importing another package, or modules from another package.           |
+----------------------+-----------------------------------------------------------------------------------------------+

Custom Import Rules allowed import types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+-------------------+---------+--------------+-------------+-------------+--------+
| RULE              | STD LIB | PROJECT [#]_ | FIRST PARTY | THIRD PARTY | FUTURE |
+===================+=========+==============+=============+=============+========+
| std_lib_only      | X       |              |             |             | X      |
+-------------------+---------+--------------+-------------+-------------+--------+
| project_only      | X       | X            | X           |             | X      |
+-------------------+---------+--------------+-------------+-------------+--------+
| base_package_only | X       | X            |             |             | X      |
+-------------------+---------+--------------+-------------+-------------+--------+
| first_party_only  | X       |              | X           |             | X      |
+-------------------+---------+--------------+-------------+-------------+--------+
| third_party_only  | X       |              |             | X           | X      |
+-------------------+---------+--------------+-------------+-------------+--------+
| isolated          | X       |              |             | X           | X      |
+-------------------+---------+--------------+-------------+-------------+--------+



.. [#] Technically project imports are "First Party" imports, but in this case we want to make a distinction between the top-level package and the rest of the project.

Example Configurations
----------------------

**.toml file**

.. code-block:: toml

    [flake8]
    # Define the base packages for your project
    base_packages = ["my_base_package", "my_other_base_package"]
    import_restrictions = [
        "my_base_package.package_a:my_base_package.package_b",  # Restrict `package_a` from importing `package_b`
        "my_base_package.module_x:my_base_package.module_y",  # Restrict `module_x` from importing `module_y`
    ]
    # Make `package_c` an isolated package
    isolated_modules = ["my_base_package.package_c"]
    # Allow `package_d` to import only from the standard library
    std_lib_only = ["my_base_package.package_d"]
    # Allow `package_b` to import only from third-party libraries
    third_party_only = ["my_base_package.package_b"]
    # Allow `package_f` to import only from the local packages and the project's
    # top-level package. This will treat the first package defined in `base_packages` as the top-level package.
    first_party_only = ["my_base_package.package_f"]
    # Allow `package_g` to import only from the local package
    project_only = ["my_base_package.package_g"]


**.ini file**

.. code-block:: ini

    [flake8]
    base-packages = my_base_package,my_other_base_package
    import-restrictions =
        my_base_package.package_a:my_base_package.package_b
        my_base_package.module_x:my_base_package.module_y
    restricted-packages = my_base_package.package_b
    isolated-modules = my_base_package.package_c
    std-lib-only = my_base_package.package_d
    third-party-only = my_base_package.package_b
    first-party-only = my_base_package.package_f
    project-only = my_base_package.package_g


Rule Violations
---------------

=====================  ============================================================
 Rule Violation Code        Description
=====================  ============================================================
  **CIR101**            This error signifies a conflict with a custom import
                        rule. It is thrown when an import violates a custom
                        rule defined in your configuration.

  **CIR102**            This error is thrown when a specific package or
                        module is imported against the defined import restrictions.

  **CIR103**            This error is thrown when a from import statement
                        for a specific package or module violates the
                        defined import restrictions.

  **CIR104**            This error is thrown when a module import for a
                        specific package or module goes against the
                        defined import restrictions.

  **CIR105**            This error is thrown when a from import statement
                        for a specific module violates the defined import
                        restrictions.

  **CIR106**            This error is thrown when an import from a
                        restricted package is detected.

  **CIR107**            This error is thrown when an import from a
                        restricted module is detected.

  **CIR201**            This error signifies an import from a non-project
                        package, which is not allowed when the project_only
                        rule is enabled.

  **CIR202**            This error signifies an import from a non-project
                        module, which is not allowed when the project_only
                        rule is enabled.

  **CIR203**            This error signifies an import from a non-base
                        package, which is not allowed when the
                        **--base-package-only** rule is enabled.

  **CIR204**            This error signifies an import from a non-base
                        package module, which is not allowed when the
                        **--base-package-only** rule is enabled.

  **CIR205**            This error signifies an import from a non-first
                        party package, which is not allowed when the
                        **--first-party-only** rule is enabled.

  **CIR206**            This error signifies an import from a non-first
                        party module, which is not allowed when the
                        **--first-party-only** rule is enabled.

  **CIR301**            This error signifies an import from an isolated
                        package, which is not allowed when the isolated
                        rule is enabled.

  **CIR302**            This error signifies a from import from an
                        isolated package, which is not allowed when the
                        isolated rule is enabled.

  **CIR303**            This error signifies an import from an isolated
                        module, which is not allowed when the isolated
                        rule is enabled.

  **CIR304**            This error signifies a from import from an
                        isolated module, which is not allowed when the
                        isolated rule is enabled.

  **CIR401**            This error signifies an import from a non-standard
                        library package, which is not allowed when the
                        **--std-lib-only** rule is enabled.

  **CIR402**            This error signifies an import from a non-standard
                        library module, which is not allowed when the
                        **--std-lib-only** rule is enabled.

  **CIR501**            This error signifies an import from a non-third
                        party package, which is not allowed when the
                        **--third-party-only** rule is enabled.

  **CIR502**            This error signifies an import from a non-third
                        party module, which is not allowed when the
                        **--third-party-only** rule is enabled.

  **PIR101**            This error is thrown when an import is not at the
                        top level of a file. This occurs when the
                        **--top-level-only-imports** option is enabled.

  **PIR102**            This error is thrown when a relative import is
                        detected. This occurs when the
                        **--restrict-relative-imports** option is enabled.

  **PIR103**            This error is thrown when a local import is
                        detected. This occurs when the
                        **--restrict-local-imports** option is enabled.

  **PIR104**            This error is thrown when a conditional import is
                        detected. This occurs when the
                        **--restrict-conditional-imports** option is enabled.

  **PIR105**            This error is thrown when a dynamic import is
                        detected. This occurs when the
                        **--restrict-dynamic-imports** option is enabled.

  **PIR106**            This error is thrown when a private import is
                        detected. This occurs when the
                        **--restrict-private-imports** option is enabled.

  **PIR107**            This error is thrown when a wildcard import is
                        detected. This occurs when the
                        **--restrict-wildcard-imports** option is enabled.

  **PIR108**            This error is thrown when an aliased import is
                        detected. This occurs when the
                        **--restrict-aliased-imports** option is enabled.

  **PIR109**            This error is thrown when a **__future__** import
                        is detected. This occurs when the
                        **--restrict-future-imports** option is enabled.

  **PIR201**            This error is thrown when importing test modules
                        (**import test_<all>** or **import <all>_test**)
                        is detected. This occurs when the
                        **--restrict-test-imports** option is enabled.

  **PIR202**            This error is thrown when importing from
                        (**test_<all>.py** or **<all>_test.py**) modules
                        is detected. This occurs when the
                        **--restrict-test-imports** option is enabled.

  **PIR203**            This error is thrown when **import conftest**
                        is detected. This occurs when the
                        **--restrict-conftest-imports** option is enabled.

  **PIR204**            This error is thrown when importing from
                        **conftest.py** files is detected. This occurs when
                        the **--restrict-conftest-imports** option is
                        enabled.

  **PIR205**            This error is thrown when **import tests**
                        or **import tests.subdirectories** are detected.
                        This occurs when the
                        **--restrict-test-imports** option is enabled.

  **PIR206**            This error is thrown when importing from the
                        **tests** directory or its subdirectories is
                        detected. This occurs when the
                        **--restrict-test-imports** option is enabled.

  **PIR207**            This error is thrown when **import __init__**
                        is detected. This occurs when the
                        **--restrict-init-imports** option is enabled.

  **PIR208**            This error is thrown when importing from
                        **__init__.py** files is detected. This occurs when
                        the **--restrict-init-imports** option is enabled.

  **PIR209**            This error is thrown when **import __main__** is
                        detected. This occurs when the

                        **--restrict-main-imports** option is enabled.
  **PIR210**            This error is thrown when importing from
                        **__main__.py** files is detected. This occurs
                        when the **--restrict-main-imports** option is
                        enabled.

  **PIR301**            This error is thrown when a potential dynamic
                        import failed confirmation checks. This occurs
                        when the **--restrict-dynamic-imports** option
                        is enabled.

  **PIR302**            This error is thrown when an attempt to parse a
                        dynamic value string failed. This occurs when the
                        **--restrict-dynamic-imports** option is enabled.
=====================  ============================================================


Plugin Limitations
------------------
- This plugin is currently only compatible with Python 3.10+ (support for 3.8 and 3.9 in the works).
- Option import-restrictions only supports restricting imports by package or module, not by class
  or function. (i.e., module_a.ClassA or module_a.function)
- Files are not supported yet.
- Option top-level-only-imports has not been implemented yet.
- Dynamic string checks are not fully implemented yet. Currently they

License
-------
This project is licensed under the terms of the MIT license.

Acknowledgements
----------------

- `flake8 <https://github.com/PyCQA/flake8>`_ - A wrapper around PyFlakes, pycodestyle and McCabe.
- `flake8-import-order <https://github.com/PyCQA/flake8-import-order>`_ - ``flake8`` plugin that
checks import order against various Python Style Guides. Used as a reference for this plugin.
- `Writing Plugins for flake8 <https://flake8.pycqa.org/en/latest/plugin-development/index.html>`_ -
``flake8`` documentation on writing plugins.
- `A flake8 plugin from scratch <https://www.youtube.com/watch?v=ot5Z4KQPBL8>`_ - YouTube video on
writing a custom ``flake8`` plugin.
