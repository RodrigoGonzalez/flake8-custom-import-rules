==========================
flake8-custom-import-rules
==========================
A ``flake8`` plugin that enforces custom import rules, allowing users to define and
maintain clean and consistent import organization across their Python projects.


.. contents:: README Sections
   :depth: 2


Introduction
------------

This ``flake8`` plugin significantly enhances the organization and consistency of
imports in Python projects. By enabling developers to set custom restrictions,
define isolated packages, and establish import rules, the plugin aids in
mitigating unwanted dependencies and maintaining clear separations between
packages. Specifically, it facilitates the management of lightweight packages
by limiting their imports to the Python standard library or third-party
libraries, thus preventing unnecessary dependencies.

Beyond enhancing readability and maintainability, the plugin promotes a
modular architecture that is easier to comprehend, test, and debug.
Consequently, developers can smoothly adhere to best practices,
maintaining their projects in a clean,
organized, and collaborative-friendly state.



Installation
------------

Install from ``pip`` with:

.. code-block:: sh

     pip install flake8-custom-import-rules

Plugin Options
--------------

Custom Import Rules (CIR) allow you to define and enforce import rules for
packages within your project. This plugin provides a set of flags that enable
you to specify import restrictions, isolated packages, and import rules. These
flags can be used in conjunction with each other to provide granular control
over your import rules.

Project Import Rules (PIR) allow you to define and enforce import rules at a project level.

**Restricted Imports**
~~~~~~~~~~~~~~~~~~~~~~

Use the `--import-restrictions` flag to limit
specific import capabilities for packages. This
feature allows you to define a list of packages
that are restricted from importing certain
packages or modules within your base package.

Consider a scenario where you're building a data processing application
where 'package_a' handles raw data cleaning and 'package_b' carries
out sensitive data processing. To avoid accidentally leaking raw
data into 'package_b', you might want to prevent 'package_a' from
importing 'package_b' or any of its subpackages.

**Restricted Packages**
~~~~~~~~~~~~~~~~~~~~~~~

The `--restricted-packages` flag allows you to specify a list of packages that are not permitted to be imported or used by other packages or modules within your base package. This helps maintain a clear separation between high-level and low-level packages.

For example, if you have a 'lower_level_package' that
contains utility functions and a 'higher_level_package'
that handles business logic, you might want to restrict
importing 'lower_level_package' into
'higher_level_package' to avoid circular dependencies.

**Isolated Packages**
~~~~~~~~~~~~~~~~~~~~~

The `--isolated-modules` flag allows you to define a list of packages that cannot import from any other packages within your base package. This ensures that certain packages remain standalone and do not introduce unwanted dependencies.

For instance, you might have a 'standalone_package' that performs a specific task independently. To ensure it remains decoupled from the rest of the application, you can make this package isolated.

**Standard Library Only Imports**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `--std-lib-only` flag allows you to specify a set of packages that can only import from the Python standard library. This rule helps to keep specific packages lightweight and free from third-party dependencies.

Suppose you're building a 'lightweight_package' that needs to be easily portable and free from external dependencies. In this case, you might restrict this package to import only from Python standard library modules.

More flags are available to provide granular control over your import rules. For instance, `--third-party-only`, `--first-party-only`, `--project-only`, and `--base-package-only` allow you to restrict imports to third-party libraries, local packages, the local package and the project's top-level package, and the project's top-level package respectively. Additionally, various flags are available to restrict relative, local, conditional, dynamic, private, wildcard, aliased, future, init, main, test, and conftest imports. Review the flake8-custom-import-rules documentation for more details and examples on how to use these flags.

For example, if you want to restrict a package to only import from the local package and the project's top-level package, you can use the `--project-only` flag:

.. code-block:: toml

    [flake8]
    project_only = ["my_base_package.package_g"]


In this example, 'package_g' is only allowed to import from 'my_base_package' and the project's top-level package. Any attempt to import from other packages will be flagged by the linter.

Remember to carefully assess your project's needs and structure when applying these import rules, as they can significantly impact your project's architecture and design.


**Base Package Only Imports**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `--base-package-only` flag allows you to restrict a package to import only from the project's top-level package. This can help maintain a clear hierarchy within your project's package structure.

For example, if you have a package named 'package_h' and you want it to only import from the top-level package of your project, you can specify:

.. code-block:: toml

    [flake8]
    base_package_only = ["my_base_package.package_h"]


In this case, any attempt by 'package_h' to import from other packages will be flagged by the linter.

**Top-level Only Imports**
~~~~~~~~~~~~~~~~~~~~~~~~~~

The `--top-level-only-imports` flag is currently not implemented. Once available, it should allow you to restrict certain packages or modules to only import from the top-level package.

**Import Restriction Flags**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are also several flags available to restrict specific types of imports. These include:

* `--restrict-relative-imports`
* `--restrict-local-imports`
* `--restrict-conditional-imports`
* `--restrict-dynamic-imports`
* `--restrict-private-imports`
* `--restrict-wildcard-imports`
* `--restrict-aliased-imports`
* `--restrict-future-imports`
* `--restrict-init-imports`
* `--restrict-main-imports`
* `--restrict-test-imports`
* `--restrict-conftest-imports`.

These flags help maintain clean and clear import structures by preventing certain types of potentially problematic imports. For example, you may want to prevent relative imports, which can make code harder to understand, or wildcard imports, which can pollute the namespace. Each of these flags can be enabled or disabled independently, allowing for fine-grained control over your project's import structure.

For instance, to disable relative imports for your project, you can set:

.. code-block:: toml

    [flake8]
    restrict_relative_imports = True


With this setting, any relative imports in your project will be flagged by the linter.

These rules and flags allow you to enforce a clean and understandable structure for your project's imports, making your code more maintainable and less prone to bugs or design issues. Remember to review each flag and its implications carefully, and choose the ones that best suit your project's needs and design.


**CustomImportRules class**

The `CustomImportRules` class is designed to enforce custom import rules in a Python project. It is especially useful in large projects where managing the structure and dependencies of the project can become difficult. This class uses `flake8`, a Python tool for enforcing coding style, to enforce these custom rules. It inspects each import statement in the codebase and checks whether it violates any of the defined rules.

**Import Restriction Flags**

The import restriction flags are defined as fields in the `CustomImportRules` class. Each flag corresponds to a specific rule that can be enforced in the codebase. These are the flags and their use cases:

1. `top_level_only_imports` (not implemented): This flag would enforce that all import statements only refer to top-level modules. This could be used in a project where the structure is intended to be flat, with all modules at the top level.

2. `project_only`: This flag enforces that only project-level modules can be imported. This could be used in a project where third-party dependencies are intended to be minimized, and most of the functionality is implemented within the project itself.

3. `base_package_only`: This flag enforces that only the base package of the project can be imported. This could be used in a project with a specific structure where all functionality is accessed through the base package.

4. `first_party_only`: This flag enforces that only first-party modules (i.e., those developed as part of the project) can be imported. This could be used in a project where third-party dependencies are intended to be minimized.

5. `isolated_module`: This flag enforces that only modules that are marked as 'isolated' can be imported. This could be used in a project where certain modules are intended to be used independently of the rest of the project.

6. `isolated_package`: This flag enforces that only packages that are marked as 'isolated' can be imported. This could be used in a project where certain packages are intended to be used independently of the rest of the project.

7. `std_lib_only`: This flag enforces that only standard library modules can be imported. This could be used in a project where it is intended to rely solely on the standard library, without any third-party dependencies.

8. `third_party_only`: This flag enforces that only third-party modules can be imported. This could be used in a project where it is intended to rely heavily on third-party libraries, and not on the standard library or project-specific modules.

9. `restricted_packages`: This flag enforces that certain specified packages cannot be imported. This could be used in a project where certain packages are known to cause issues or are not desired for some other reason.

10. `file_in_restricted_packages`: This flag enforces that files within certain specified packages cannot be imported. This could be used in a project where certain packages are allowed, but specific files within those packages are not.

Each of these flags can be set according to the specific needs and structure of the project, allowing for a high level of customization of the import rules.


Project import restriction flags:

--restrict-relative-imports: This flag prevents the usage of relative imports. Relative imports allow for modules to be imported relative to the current module's location. This can sometimes lead to confusion or unintended behavior, especially in larger code bases.

--restrict-local-imports: This flag restricts the import of modules that are local to the project. This could be useful to enforce dependencies only on external libraries and not on project-specific modules.

--restrict-conditional-imports: This flag restricts the use of conditional imports. Conditional imports are imports that occur within an if statement or similar control structure. These can potentially lead to inconsistent behavior, as whether or not a module is imported may depend on runtime conditions.

--restrict-dynamic-imports: This flag restricts the use of dynamic imports, which are imports that occur within a function or method. These can be hard to track and may cause unexpected behavior, as the availability of a module may depend on the specific execution path through the code.

--restrict-private-imports: This flag restricts the import of private modules (those that start with an underscore). Importing these modules can lead to instability, as they're intended for internal use within a package and may change without warning.

--restrict-wildcard-imports: This flag restricts the use of wildcard imports (e.g., from module import *). These imports can lead to confusion, as it's unclear which names are being imported, and they can potentially overwrite existing names without warning.

--restrict-aliased-imports: This flag restricts the import of modules under an alias (e.g., import numpy as np). While convenient, this can sometimes lead to confusion, especially for less common libraries or non-standard aliases.

--restrict-future-imports: This flag restricts the use of from __future__ import. These imports are used to enable features that will be standard in future versions of Python, but their use can potentially cause confusion or compatibility issues.

--restrict-init-imports: This flag restricts imports from __init__.py files. Importing from these files can sometimes lead to confusing circular dependencies or other unexpected behavior.

--restrict-main-imports: This flag restricts imports within the if __name__ == "__main__" block. These imports will only run when the script is run directly, which can sometimes lead to inconsistent behavior.

--restrict-test-imports: This flag restricts imports within test files. This can be used to enforce separation of testing and production code.

--restrict-conftest-imports: This flag restricts imports within pytest's conftest.py files. These files are used to define fixtures and other setup code for tests, and imports within them can potentially lead to unexpected behavior.

The use of these flags is highly dependent on the specific needs and coding standards of your project. They provide a means to enforce certain styles or practices, but may not be necessary or beneficial in all cases. It's important to consider the trade-offs and potential impacts before deciding to use these restrictions.


Old Option Section
------------------

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


Custom Import Rules (CIR)
-------------------------

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

Custom Import Rules Allowed Import Types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+-------------------+---------+--------------+-------------+-------------+-------------+
| RULE              | STD LIB | PROJECT [#]_ | FIRST PARTY | THIRD PARTY | FUTURE [#]_ |
+===================+=========+==============+=============+=============+=============+
| std_lib_only      | X       |              |             |             | X           |
+-------------------+---------+--------------+-------------+-------------+-------------+
| project_only      | X       | X            | X           |             | X           |
+-------------------+---------+--------------+-------------+-------------+-------------+
| base_package_only | X       | X            |             |             | X           |
+-------------------+---------+--------------+-------------+-------------+-------------+
| first_party_only  | X       |              | X           |             | X           |
+-------------------+---------+--------------+-------------+-------------+-------------+
| third_party_only  | X       |              |             | X           | X           |
+-------------------+---------+--------------+-------------+-------------+-------------+
| isolated          | X       |              |             | X           | X           |
+-------------------+---------+--------------+-------------+-------------+-------------+


.. [#] Technically project imports are "First Party" imports, but in this case we
    want to make a distinction between the top-level package and the rest of the project.
.. [#] To restrict future imports, use the `--restrict-future-imports` flag.

Example Configurations
----------------------

**.toml file**
~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~

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


Custom Import Rule Violation Codes
----------------------------------

=====================  ============================================================
 Rule Violation Code    Description
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
=====================  ============================================================


Project Import Rule Violation Codes
-----------------------------------

=====================  ============================================================
 Rule Violation Code        Description
=====================  ============================================================
  **PIR101**            This error is thrown when an import is not at the
                        top level of a file. This occurs when the
                        **--top-level-only-imports** option is enabled.
                        **NOT IMPLEMENTED**

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
                        is enabled. **NOT IMPLEMENTED**

  **PIR302**            This error is thrown when an attempt to parse a
                        dynamic value string failed. This occurs when the
                        **--restrict-dynamic-imports** option is enabled.
                        **NOT IMPLEMENTED**
=====================  ============================================================

Plugin Limitations
------------------
-   This plugin is currently only compatible with Python 3.10+ (support
    for 3.8 and 3.9 in the works).
-   Option import-restrictions only supports restricting imports by
    package or module, not by class or function
    (i.e., module_a.ClassA or module_a.function). However, if you
    are trying to set import restrictions for a class or function,
    you should probably move that class or function to a separate
    module.
-   Files are not supported yet, use modules to set restrictions
    (e.g., package/module/file.py -> package.module.file).
-   Support for project level exceptions is not implemented yet.
    (e.g., restrict aliased imports but allow import of numpy as np).
-   Option top-level-only-imports has not been implemented yet.

License
-------
This project is licensed under the terms of the MIT license.

Acknowledgements
----------------

-   `flake8 <https://github.com/PyCQA/flake8>`_ - A wrapper around PyFlakes, pycodestyle and McCabe.
-   `flake8-import-order <https://github.com/PyCQA/flake8-import-order>`_ - ``flake8`` plugin that
    checks import order against various Python Style Guides. Used as a reference for this plugin.
-   `Writing Plugins for flake8 <https://flake8.pycqa.org/en/latest/plugin-development/index.html>`_ -
    ``flake8`` documentation on writing plugins.
-   `A flake8 plugin from scratch <https://www.youtube.com/watch?v=ot5Z4KQPBL8>`_ - YouTube video on
    writing a custom ``flake8`` plugin.
-   `flake8-bugbear <https://github.com/PyCQA/flake8-bugbear>`_ - ``flake8``
    plugin that finds likely bugs and design problems in your program.
