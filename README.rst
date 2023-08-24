==========================
flake8-custom-import-rules
==========================
.. image:: https://images.squarespace-cdn.com/content/v1/5739206dc6fc0814566cf91d/1692854973337-STZOMBOTWFPEVZVQ4GRI/dependency-wheel.png?format=1000w
   :target: https://rodrigo-gonzalez.com/projects#/flake8-custom-import-rules/
   :alt: Project Dependency Wheel

.. image:: https://img.shields.io/pypi/v/flake8-custom-import-rules.svg?style=flat-square
    :target: https://pypi.org/project/flake8-custom-import-rules/
    :alt: PyPI Package latest release

.. image:: https://img.shields.io/pypi/pyversions/flake8-custom-import-rules.svg?style=flat-square
    :target: https://pypi.org/project/flake8-custom-import-rules/
    :alt: Supported versions

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. image:: https://codecov.io/gh/RodrigoGonzalez/flake8-custom-import-rules/graph/badge.svg?token=WIQPI6YRBL
    :target: https://codecov.io/gh/RodrigoGonzalez/flake8-custom-import-rules






A ``flake8`` plugin that enforces custom import rules, allowing
users to define and maintain clean and consistent import
organization across their Python projects.

This plugin takes advantage of ``flake8`` linting
capabilities and provides set of flags that enable you to
specify import restrictions, standalone packages and modules,
and additional custom and project-level import rules.
These flags can be used in conjunction
with each other to provide granular control over your import rules.
The use of these flags is highly dependent on the specific
needs and coding standards of your project. They provide
a means to enforce certain styles or practices, but may
not be necessary or beneficial in all cases. It's important
to consider the trade-offs and potential impacts before
deciding to use these restrictions.

There are two types of import rules that can be enforced by
this plugin:

-   Custom Import Rules (CIR) allow you to define and enforce
    import rules for specific package and modules within your
    project.
-   Project Import Rules (PIR) allow you to define and enforce
    import rules at a project level.


Detailed Documentation: https://rodrigogonzalez.github.io/flake8-custom-import-rules/


.. contents:: **Sections**
   :depth: 2


**Introduction**
----------------

This ``flake8`` plugin significantly enhances the organization
and consistency of imports in Python projects. By enabling
developers to set custom restrictions, define standalone
packages, and establish import rules, the plugin aids in
mitigating unwanted dependencies and maintaining clear separations
between packages. Specifically, it facilitates the management of
lightweight packages by limiting their imports to the Python
standard library or third-party libraries, thus preventing
unnecessary dependencies.

Beyond enhancing readability and maintainability, the plugin
promotes a modular architecture that is easier to comprehend,
test, and debug. Consequently, developers can smoothly adhere
to best practices, maintaining their projects in a clean,
organized, and collaborative-friendly state.

NOTE: While certain options might be considered niche and
are unlikely to be employed in everyday scenarios, their
inclusion is a deliberate design choice aimed at empowering
users with the utmost control and flexibility.


**Installation**
----------------

Install from ``pip`` with:

.. code-block:: sh

     pip install flake8-custom-import-rules


**Development**
---------------

Additional details on how to develop and contribute to this
plugin coming soon.


**Plugin Options: Required Flags & Options**
--------------------------------------------
The following flag is required to enable most of the
plugin functionality:

- base-packages


Base Packages Option
~~~~~~~~~~~~~~~~~~~~
The `--base-packages` flag serves as a foundational configuration
option within the tool, allowing users to explicitly define
the primary packages that constitute their project. These
identified packages are categorized as first-party,
signifying the core elements that are actively being developed
within the scope of the project itself.

By specifying the base packages, users create a clear
delineation between their main project components and external
dependencies. This distinction assists in various operations,
such as linting, dependency analysis, and code organization.

For instance, if a user is developing a library named
`my_library`, they would include `my_library` as a base
package by configuring this flag. This inclusion ensures
that the tool recognizes `my_library` a the reference
package for imposing many of the rules the user is
likely to define or enable, aligning its behavior with the
user's development practices. As seen below:

.. code-block:: ini

    [flake8]
    base-packages = my_library,my_other_library

It's important to note that if the base-packages flag is
not configured, the majority of functionality within the
tool will be limited or disabled. This flag is instrumental
in tailoring the plugin's behavior to the specific
structure and needs of the project.

That said, the project import rules (PIR) are not dependent
on the base-packages flag, and can be used independently,
therefore the base-packages flag is not set to as required
within the ``flake8`` framework.


**Plugin Options: Custom Import Rules (CIR)**
---------------------------------------------

Custom Import Rules (CIR) allow you to define and enforce
import rules for modules and packages within your project.

The following flags are available to restrict specific types
of imports:


=======================  =====================================================
 Custom Import Rules        Description
=======================  =====================================================
restricted-packages         This flag restricts the import of specified
                            packages into all other packages within your
                            project. It can be used to
                            prevent the use of packages known to cause
                            problems or that are undesired for specific
                            reasons. For instance, it can enforce a clear
                            separation between high-level and low-level
                            packages (e.g., the `app` package should not
                            be imported by `common`, `utils`, `core`, etc.).

std-lib-only                This flag ensures that only standard
                            library modules can be imported within the
                            specified package or module. It is useful in
                            scenarios where the target is intended to rely
                            solely on the standard library, without any
                            third-party or project dependencies. For
                            example, low-level packages that are used
                            across the rest of the project can be
                            restricted.

project-only                This flag enforces that only project
                            packages can be imported in the specified
                            modules and packages. This can be used
                            in a package where third-party dependencies
                            are intended to be minimized, and most of
                            the functionality is implemented within the
                            project itself. These are defined by the
                            base-packages flag.

base-package-only           This flag enforces that only the root
                            package of the project can be imported
                            into the specified packages or modules.
                            It ensures that only the root package is
                            solely relied on. Useful in a project where
                            a clear hierarchy and dependency flow is
                            required, and all functionality must be
                            accessed through the root package.

first-party-only            This flag enforces that only first-party
                            modules (i.e., developed as part of the
                            project) can be imported, including all
                            imports in base packages except for its
                            own root package. Useful in security-
                            sensitive environments, or to minimize
                            external dependencies, giving more control
                            over the codebase.

third-party-only            This flag enforces that only third-party
                            modules can be imported, restricting the
                            use of standard library or project-specific
                            modules. For example, in a plugin system
                            designed to extend functionality using
                            third-party libraries, this flag would
                            ensure that only those external libraries
                            are imported, excluding standard or
                            project-level modules. Unlike the
                            standalone-modules rule, third-party-only
                            does not allow imports from within the
                            specific module or package itself.

standalone-modules          This flag allows you to define a list of
                            packages that cannot import from any other
                            packages within your project, except for
                            modules and packages within the parent
                            package. This ensures that certain packages
                            remain standalone and do not introduce
                            unwanted dependencies.
                            For instance, you might have
                            a 'standalone_package' that performs a
                            specific task independently. To ensure it
                            remains decoupled from the rest of the
                            application, you can make this package
                            standalone. It promotes modular design,
                            aiding in maintainability and scalability.
                            (e.g., within your base package typically
                            have names like `common`, `utils`,
                            `helpers`, etc.)

custom-restrictions         This flag enables granular control over
                            the importing of specific packages or
                            modules within your project. It allows you
                            to specify a package or module, followed by
                            a colon, and then list the restricted imports,
                            separated by additional colons.
                            These restricted imports can include other
                            first-party packages, standard library
                            packages, or third-party imports. Particularly
                            useful in large projects, this flexibility
                            helps in managing complex dependencies.
                            Consider a scenario where `package_a` handles
                            raw data cleaning, and `package_b` processes
                            sensitive data. To prevent accidental leakage
                            of raw data into `package_b`, you could
                            restrict `package_a` from importing `package_b`
                            or its subpackages.

=======================  =====================================================


Each of these flags can be set according to the specific needs
and structure of the project, allowing for a high level of
customization of the import rules.

Restricted Packages Option
~~~~~~~~~~~~~~~~~~~~~~~~~~

The `--restricted-packages` flag allows you to specify high-level
packages that should not be imported into any other packages within
your project. This maintains the integrity of high-level packages,
ensuring that they are not tightly coupled with other parts of the
codebase.

For example, if you have a high-level package like 'app' responsible
for core functionality, you may want to prevent it from being
imported into lower-level packages such as 'common', 'utils', 'core',
etc. This can help avoid circular dependencies and preserve a clean
architectural hierarchy.

.. code-block:: ini

    [flake8]
    restricted_packages = app


Standard Library Only Imports Option
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `--std-lib-only` flag enables you to designate specific packages
within your project that are restricted to importing only from the
Python standard library. This maintains a lightweight footprint for
those packages, ensuring they remain easily portable and free from
third-party dependencies.

For example, you might be developing a 'lightweight_package' meant
to be used across various environments without the need for additional
dependencies. By restricting this package to import only from the
Python standard library, you can ensure its compatibility and ease of
use.

.. code-block:: ini

    [flake8]
    std_lib_only = lightweight_package


Project Only Imports Option
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `--project-only` flag restricts specified modules and packages
within your project to import solely from other packages developed
as part of the project and the standard library. This ensures that
the internal functionality is prioritized, and third-party
dependencies are minimized.

Consider a scenario where you want to maintain the integrity and
independence of your project's core functionality. By using the
`project-only` option, you can ensure that specific modules or
packages rely exclusively on the internally developed code, reducing
the risk of external dependencies and promoting a cohesive codebase.

For example, if you have a package 'package_a' and you want to restrict
it to only import from the local package and the project's top-level
package, you can specify:

.. code-block:: ini

    [flake8]
    project_only = package_a

In this configuration, 'package_a' is limited to importing only from
other packages defined within the project, fostering a controlled
and self-contained development environment.


Base Package Only Imports Option
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `--base-package-only` flag is a powerful tool for
enforcing a hierarchical structure within your project. By
specifying packages or modules with this flag, you ensure
that they can only import from the project's root package.
This centralizes the dependency flow and promotes a
well-structured project design.

Consider a complex project with multiple interdependent
packages. You might want to ensure that certain packages
rely solely on the root package to minimize potential
conflicts and promote maintainability. The
`base-package-only` option allows you to create this clear
and organized dependency structure.

For example, suppose you have a package named `package_h`
that you want to restrict to only import from the top-level
package of your project. You can specify this as follows:

.. code-block:: ini

    [flake8]
    base_package_only = my_base_package.package_h

In this configuration, 'package_h' can only import from
`my_base_package`. Any attempt to import from other
packages will be flagged by the linter. This ensures that
`my_base_package` remains the central point of interaction,
providing better control and clarity in the project's
architecture.

Now, let's consider another package, `my_second_package`.
Suppose you want to ensure that `my_second_package` does
not import any other packages specified in base-packages.
This might be useful if 'my_second_package' is designed to
be independent or if it contains functionality that should
not be influenced by other parts of the project. You can
specify this restriction as follows:

.. code-block:: ini

    [flake8]
    base_package_only = my_base_package.package_h, my_second_package

With this configuration, `my_second_package` is restricted
from importing any other packages specified in
base-packages. This ensures the independence of
`my_second_package`, allowing it to function without being
affected by changes in other parts of the project.


First-Party Only Imports Option
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `--first-party-only` flag ensures that only first-party modules,
i.e., those developed within the project, can be imported. This
restriction includes all imports defined within the base packages,
excluding the imports from its own root package.

This control over imports can be highly beneficial in security-
sensitive environments or in projects aiming to minimize external
dependencies. By limiting the imports to first-party modules, you
gain more control over the codebase and reduce potential risks
associated with third-party dependencies.

Consider a scenario where your project requires strict compliance
with certain regulations or standards. By enforcing a first-party
only import policy, you can ensure that all code is vetted and
maintained within your organization, reducing potential legal or
security concerns.

To implement this restriction, you can specify:

.. code-block:: ini

    [flake8]
    first_party_only = my_project.my_package

In this example, 'my_package' within 'my_project' will only be
allowed to import modules developed as part of the project. Any
attempt to import from outside the project will be flagged by
the linter, helping to maintain the integrity and security of
the codebase.


Third-Party Only Imports Option
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `--third-party-only` flag is designed to enforce the use of
only third-party modules in the specified packages or modules. This
restriction prohibits the import of both standard library modules
and project-specific modules, ensuring that only external libraries
are utilized.

Such a restriction can be particularly useful in scenarios where
a system is designed to extend its functionality exclusively through
third-party libraries. For instance, in a plugin system that relies
on external extensions, this flag guarantees that only those third-
party libraries are imported, excluding any standard or project-level
modules.

Unlike the `standalone-modules` rule, the `third-party-only` rule
prevents even the importation of modules from within the specified
package or module itself, further narrowing the scope of allowed
imports.

To apply this restriction, you can specify:

.. code-block:: ini

    [flake8]
    third_party_only = my_plugin_system.my_plugin

In this example, 'my_plugin' within 'my_plugin_system' will be
restricted to importing only third-party modules. Any attempt to
import from the standard library or from other modules within the
project will be flagged by the linter. This ensures a strict
adherence to the design principles of relying solely on third-party
extensions, maintaining the integrity of the plugin system.


Standalone Modules Option
~~~~~~~~~~~~~~~~~~~~~~~~~

The `--standalone-modules` flag is designed to allow specific
packages or modules to import only from the standard library,
the base package of the project, and third-party libraries,
excluding any other first-party or project-level imports.
This ensures that the specified standalone packages or modules
operate independently from other parts of the project, yet they
still have access to essential third-party libraries, the base
package, and standard libraries.

This option aids in maintainability and scalability, especially
in complex projects where clear boundaries and modular design
are essential. Standalone modules or packages can be used to
encapsulate specific functionalities that don't require
integration with the rest of the first-party code.

Here's an example of how you can configure this rule:

.. code-block:: ini

    [flake8]
    standalone_modules = my_base_package.standalone_module

In this example, 'standalone_module' within 'my_base_package'
is configured to import only from the standard library, the
base package itself, and third-party libraries. Any attempt to
import from other first-party packages or modules within the
project will be flagged by the linter.

It's worth noting the difference between the `standalone-modules`
rule and the `third-party-only` rule. While both restrict
project-specific imports, `standalone-modules` allows imports
from within the standalone package or module itself, whereas
`third-party-only` does not, further narrowing the scope of
allowed imports.

By employing the `standalone-modules` option, developers can
ensure that certain parts of the application remain decoupled
and self-contained, promoting a clean and organized code
structure that can be more easily managed and expanded.


Custom Restrictions Option
~~~~~~~~~~~~~~~~~~~~~~~~~~

The `--custom-restrictions` flag provides a powerful tool for
managing and limiting specific import capabilities within your
project. It enables you to precisely control the import behavior
of individual packages or modules, ensuring that certain imports
are restricted as per the project's requirements.

This control is achieved by specifying a package or module,
followed by a colon, and then listing the restricted imports,
separated by additional colons. These restricted imports can
range from other first-party packages within the project to
standard library packages, or even third-party imports.

Such granularity is particularly valuable in large or complex
projects where managing dependencies and maintaining a clear
structure can be challenging. For example, you may have
`package_a` responsible for raw data cleaning and `package_b`
for processing sensitive data. To avoid accidental leakage of
raw data into `package_b`, you could apply restrictions to
prevent `package_a` from importing `package_b` or any of its
subpackages.

The configuration might look like this:

.. code-block:: ini

    [flake8]
    custom-restrictions =
        # Restrict `package_a` from importing `package_b` and `os`
        my_base_package.package_a:my_base_package.package_b:os
        # Restrict `module_x` from importing `module_y` and `pandas`
        my_base_package.module_x:my_base_package.module_y:pandas

In the example above, specific restrictions are applied to
`package_a` and `module_x`, preventing them from importing
certain other packages or modules within the project, or even
from the standard library or third-party libraries. Again,
this is to provide a granular level of control over the
import behavior of individual packages or modules, restricting
imports from `pandas` or even `os` is not very likely within
your own project, but there may reasons make these restrictions.
This ensures that the intended separation and containment of
functionality are preserved, enhancing the maintainability
and security of the codebase.



Custom Import Rules: Import Rules and Import Types Table
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Remember to carefully assess your project's needs and structure
when applying these import rules, as they can significantly
impact your project's architecture and design.

+--------------------------+---------+----------------+-------------+-------------+-------------+
| RULE                     | STD LIB | BASE PACKAGE   | FIRST PARTY | THIRD PARTY | FUTURE [#]_ |
+==========================+=========+================+=============+=============+=============+
| std-lib-only             | X       |                |             |             | X           |
+--------------------------+---------+----------------+-------------+-------------+-------------+
| project-only             | X       | X              | X           |             | X           |
+--------------------------+---------+----------------+-------------+-------------+-------------+
| base-package-only [#]_   | X       | X              |             |             | X           |
+--------------------------+---------+----------------+-------------+-------------+-------------+
| first-party-only         | X       |                | X           |             | X           |
+--------------------------+---------+----------------+-------------+-------------+-------------+
| third-party-only         | X       |                |             | X           | X           |
+--------------------------+---------+----------------+-------------+-------------+-------------+
| standalone-modules [#]_  | X       | X              |             | X           | X           |
+--------------------------+---------+----------------+-------------+-------------+-------------+


.. [#] To restrict future imports, use the
    `--restrict-future-imports` flag.
.. [#] Technically base package imports are "First Party" imports,
    but in this case we want to make a distinction between
    the top-level package and the rest of the project.
.. [#] The difference between third-party only and standalone,
    is that standalone allows imports from within the standalone
    module/package, while third-party only does not.


**Plugin Options: Project Import Rules (PIR)**
----------------------------------------------

Project Import Rules (PIR) allow you to define and enforce
import rules at a project level.

There are also several flags available to restrict specific
types of imports. Project import restriction flags:

============================  ==============================================================
 Project Import Rule           Description
============================  ==============================================================
restrict-relative-imports       This flag prevents the usage of relative imports.
                                Relative imports allow for modules to be imported
                                relative to the current module's location. This can
                                sometimes lead to confusion or unintended behavior,
                                especially in larger code bases.
                                Enabled by default. This is a boolean option, and
                                can be set to True or False (e.g., flag = True).

restrict-local-scope-imports    This flag restricts local scope imports, preventing
                                the import of modules or specific functions within
                                a particular scope, such as inside a function or
                                method. It enforces that all imports occur at the
                                top-level of the file, promoting code clarity and
                                consistency.
                                Enabled by default. This is a boolean option, and
                                can be set to True or False (e.g., flag = True).


restrict-conditional-imports    This flag restricts the use of conditional imports.
                                Conditional imports are imports that occur within an
                                if statement or similar control structure. These can
                                potentially lead to inconsistent behavior, as
                                whether or not a module is imported may depend on
                                runtime conditions.
                                Disabled by default. This is a boolean option, and
                                can be set to True or False (e.g., flag = True).

restrict-dynamic-imports        This flag restricts the use of dynamic imports,
                                which are imports that occur within a function or
                                method. These can be hard to track and may cause
                                unexpected behavior, as the availability of a module
                                may depend on the specific execution path through
                                the code.
                                Enabled by default. This is a boolean option, and
                                can be set to True or False (e.g., flag = True).

restrict-private-imports        This flag restricts the import of private modules
                                (those that start with an underscore). Importing
                                these modules can lead to instability, as they're
                                intended for internal use within a package and may
                                change without warning. Although, there are no
                                truly private modules/functions/methods in Python,
                                this flag can be
                                Enabled by default. This is a boolean option, and
                                can be set to True or False (e.g., flag = True).

restrict-wildcard-imports       This flag restricts the use of wildcard imports
                                (e.g., `from module import *`). These imports can
                                lead to confusion, as it's unclear which names are
                                being imported, and they can potentially overwrite
                                existing names without warning.
                                Enabled by default. This is a boolean option, and
                                can be set to True or False (e.g., flag = True).

restrict-aliased-imports        This flag restricts the import of modules under an
                                alias (e.g., import numpy as np). While convenient,
                                this can sometimes lead to confusion, especially
                                for less common libraries or non-standard aliases.
                                Given the ubiquity of certain aliases (e.g., np for
                                numpy).
                                Disabled by default. This is a boolean option, and
                                can be set to True or False (e.g., flag = True).

restrict-future-imports         This flag restricts the use of `from __future__
                                import`. These imports are used to enable features
                                that will be standard in future versions of Python,
                                but their use can potentially cause confusion or
                                compatibility issues.
                                Disabled by default. This is a boolean option, and
                                can be set to True or False (e.g., flag = True).

restrict-init-imports           This flag restricts imports from `__init__.py` files.
                                Importing from these files can sometimes lead to
                                confusing circular dependencies or other unexpected
                                behavior.
                                Enabled by default. This is a boolean option, and
                                can be set to True or False (e.g., flag = True).

restrict-main-imports           This flag restricts imports from `__main__.py`
                                files. Importing from a `__main__.py` file
                                is generally not considered best practice in
                                Python development. The `__main__.py` file is
                                typically used to define the entry point for
                                a package when it's executed as a script.
                                It's designed to contain code that kicks off
                                the execution of the program, not to define
                                reusable functions or classes.
                                Enabled by default. This is a boolean option, and
                                can be set to True or False (e.g., flag = True).

restrict-test-imports           This flag restricts imports from test files and
                                the tests directory. This can be used to enforce
                                separation of testing and production code.
                                Enabled by default. This is a boolean option, and
                                can be set to True or False (e.g., flag = True).

restrict-conftest-imports       This flag restricts imports within pytest's
                                conftest.py files. These files are used to define
                                fixtures and other setup code for tests, and
                                imports within them can potentially lead to
                                unexpected behavior.
                                Enabled by default. This is a boolean option, and
                                can be set to True or False (e.g., flag = True).

top-level-only-imports          This flag would enforce that all import statements
                                only refer to top-level modules. This could be used
                                in a project where the structure is intended to be
                                flat, with all modules at the top level.
                                NOT IMPLEMENTED.
============================  ==============================================================


These flags help maintain clean and clear import structures
by preventing certain types of potentially problematic
imports. For example, you may want to prevent relative
imports, which can make code harder to understand, or
wildcard imports, which can pollute the namespace. Each of
these flags can be enabled or disabled independently,
allowing for fine-grained control over your project's import
structure.

Restrict Relative Imports
~~~~~~~~~~~~~~~~~~~~~~~~~

Relative imports in Python allow you to import modules or
specific objects from modules within the same package
hierarchy, using dots (`.`) to represent the relative path.

By default, the `--restrict-relative-imports` flag is
enabled, prohibiting the use of relative imports. Modules
must instead utilize absolute imports, specifying the full
path to the target module, starting from the top-level
package.

To enforce this restriction and disable relative imports
for your project, you can configure the following setting:

.. code-block:: cfg

    [flake8]
    restrict_relative_imports = True

With this configuration, any relative imports encountered
in your project will be flagged by the linter, guiding you
to use absolute imports instead.


Restrict Local Scope Imports
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Local scope imports refer to the practice of importing
modules or specific objects within a confined scope, such
as inside a function or method. While this can allow for
more granular control over imports, it may lead to code
that is less clear and consistent.

The `--restrict-local-scope-imports` flag is designed to
prevent such imports, enforcing that all imports occur at
the top-level of the file. By centralizing imports, it
promotes code clarity and consistency across the project.

This restriction is turned on by default, meaning that any
local scope imports will be flagged by the linter. If you
wish to adhere to this best practice, ensure that all
imports are declared at the top-level of your files, rather
than within specific functions or methods.

.. code-block:: cfg

    [flake8]
    restrict_local_scope_imports = True

With this configuration, the linter will guide you to
organize your imports at the top-level, fostering a more
readable and maintainable codebase.

Restrict Conditional Imports
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Conditional imports in Python refer to the practice of
importing modules or specific symbols based on certain
conditions or runtime logic. These imports can be found
inside control structures like `if` statements.

The `--restrict-conditional-imports` flag aims to limit
the use of these imports, as they can potentially lead to
inconsistent behavior. The importation of a module might
depend on varying runtime conditions, leading to unexpected
outcomes.

This restriction is turned off by default, allowing for
conditional imports. However, considering the potential
risks and complexities, you may choose to enable this flag:

.. code-block:: cfg

    [flake8]
    restrict_conditional_imports = True

By restricting conditional imports, you can foster a more
predictable and manageable codebase.

Restrict Dynamic Imports
~~~~~~~~~~~~~~~~~~~~~~~~

Dynamic imports in Python involve importing modules or
specific symbols within a function or method. Such imports
can be challenging to track and may result in unexpected
behavior, as the availability of a module may hinge on the
specific execution path.

The `--restrict-dynamic-imports` flag is designed to
prevent these imports, promoting a more stable and
transparent code structure. This restriction is turned on
by default, emphasizing the importance of predictability
in code execution.

.. code-block:: cfg

    [flake8]
    restrict_dynamic_imports = True

By enforcing this rule, you encourage a more coherent
and traceable import structure, enhancing code reliability.

Restrict Private Imports
~~~~~~~~~~~~~~~~~~~~~~~~

Private modules in Python are typically those that begin
with an underscore (`_`). These modules are meant for
internal use within a package, and importing them can lead
to instability, as they may change without notice.

The `--restrict-private-imports` flag limits the import of
private modules, preserving the stability of your code.
Although Python doesn't truly enforce private access,
this flag provides a layer of protection. It is turned on
by default, reflecting a best-practice approach.

.. code-block:: cfg

    [flake8]
    restrict_private_imports = True

By restricting the import of private modules, you align
with community conventions and safeguard your code from
potential instabilities related to internal package changes.


Restrict Wildcard Imports
~~~~~~~~~~~~~~~~~~~~~~~~~

Wildcard imports in Python, expressed as `from module
import *`, bring all symbols from a module into the
current namespace. While convenient, these imports can
lead to confusion, as it becomes unclear which names are
being imported. Furthermore, they may inadvertently
overwrite existing names.

The `--restrict-wildcard-imports` flag is designed to
prohibit these imports, fostering greater code clarity
and safety. This flag is turned on by default, reflecting
a standard practice in code organization.

.. code-block:: cfg

    [flake8]
    restrict_wildcard_imports = True

By restricting wildcard imports, you promote a more
transparent and manageable code structure, enhancing
maintainability.


Restrict Aliased Imports
~~~~~~~~~~~~~~~~~~~~~~~~

Aliased imports, such as `import numpy as np`, allow
modules or specific symbols to be imported under a
different name. While often convenient, especially for
widely recognized aliases, they can sometimes cause
confusion, particularly with non-standard or
unconventional aliases.

The `--restrict-aliased-imports` flag aims to limit this
practice, although it is turned off by default,
acknowledging the common usage of standard aliases.

.. code-block:: cfg

    [flake8]
    restrict_aliased_imports = False

While aliasing has its benefits, particularly with widely
accepted conventions, this flag provides an option for
those who prefer to maintain a stricter naming policy.


Restrict Future Imports
~~~~~~~~~~~~~~~~~~~~~~~

Future imports in Python, expressed as `from __future__
import`, enable features that will become standard in
upcoming versions of Python. While they facilitate
forward compatibility, their use might also introduce
confusion or compatibility challenges.

The `--restrict-future-imports` flag allows you to limit
the use of future imports, providing a layer of control.
This flag is turned off by default, allowing flexibility
in adopting future language features.

.. code-block:: cfg

    [flake8]
    restrict_future_imports = False

By offering this restriction, you can ensure that future
imports are used judiciously and aligned with your
project's needs and standards.


Restrict Imports From Init Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Importing from `__init__.py` files can sometimes lead to
confusing circular dependencies or unexpected behavior.
These files typically serve to initialize a package, and
importing from them may complicate the package structure.

The `--restrict-init-imports` flag is designed to prevent
these imports, promoting cleaner code organization. This
restriction is turned on by default.

.. code-block:: cfg

    [flake8]
    restrict_init_imports = True

By enforcing this rule, you can maintain a clear
separation between initialization and functional code,
enhancing code clarity and maintainability.


Restrict Import From Main Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Importing from ``__main__.py`` files is generally not
considered best practice in Python development, as
previously explained. The ``__main__.py`` file is meant to
define the entry point for package execution, not to house
reusable functions or classes.

The ``--restrict-main-imports`` flag restricts these
imports, aligning with best practices. This flag is turned
on by default.

.. code-block:: cfg

    [flake8]
    restrict_main_imports = True

By adhering to this restriction, you ensure that your
codebase follows a conventional structure, minimizing
potential confusion and maintenance challenges.


Restrict Test Imports
~~~~~~~~~~~~~~~~~~~~~

Test imports refer to imports from test files or the
tests directory. While these imports can be useful for
testing purposes, they may inadvertently create
dependencies between testing and production code. This
entanglement can complicate code maintenance and lead to
potential issues.

The ``--restrict-test-imports`` flag restricts these
imports, enforcing a separation between testing and
production code. This restriction is turned on by default.

.. code-block:: cfg

    [flake8]
    restrict_test_imports = True

By employing this flag, you ensure a clean demarcation
between testing and main code, enhancing the modularity
and maintainability of your codebase.


Restrict Conftest Imports
~~~~~~~~~~~~~~~~~~~~~~~~~

In the context of pytest, ``conftest.py`` files are utilized
to define fixtures and other setup code for tests.
Importing within these files can lead to unexpected
behavior, potentially affecting test outcomes.

The ``--restrict-conftest-imports`` flag restricts imports
within ``conftest.py`` files, mitigating the risk of
unintended side effects. This flag is turned on by default.

.. code-block:: cfg

    [flake8]
    restrict_conftest_imports = True

By restricting imports within ``conftest.py``, you promote
a more controlled and predictable testing environment.
This aligns with best practices for test setup and
minimizes potential complications.


Top-level Only Imports
~~~~~~~~~~~~~~~~~~~~~~

The `--top-level-only-imports` flag is currently not implemented.
Once available, it should allow you to restrict certain packages
or modules to only import from the top-level package.


**Example Configurations**
--------------------------

Define your configurations in either `.flake8`, `setup.cfg`,
or `tox.ini`.


NOTE: Each command-line option that you want to specify in
your config file can be named in either of two ways:

1. Using underscores (_) instead of hyphens (-)
2. Simply using hyphens (without the leading hyphens)


.. code-block:: ini

    [flake8]
    # Make sure to select the flake8-custom-import-rules validation codes
    select = E,W,F,N,CIR,PIR

    # Define the base packages for your project
    base-packages = my_base_package,my_other_base_package

    # Define import restrictions for your project
    custom-restrictions =
        # Restrict `package_a` from importing `package_b`
        my_base_package.package_a:my_base_package.package_b
        # Restrict `module_x` from importing `module_y`
        my_base_package.module_x:my_base_package.module_y

    restricted-packages = my_base_package.package_b

    # Make `package_c` a standalone package
    standalone-modules = my_base_package.package_c

    # Restrict `package_d` to import only from the standard library
    std-lib-only = my_base_package.package_d

    # Restrict `package_b` to import only from third-party libraries
    third-party-only = my_base_package.package_b

    # Restrict `package_f` to import only other packages within the project
    first-party-only = my_base_package.package_f

    # Restrict `package_g` to import only from the local package and submodules/packages
    project-only = my_base_package.package_g

    # Do not restrict relative imports
    restrict-relative-imports = False

    # Restrict local scope imports
    restrict-local-scope-imports = True

    # Restrict conditional imports
    restrict-conditional-imports = False

    # Allow dynamic imports
    restrict-dynamic-imports = False


**Custom Import Rule Violation Codes**
--------------------------------------

Custom Import Rule Violation Codes represent specific
errors related to the import rules defined within a
project. These codes are used to identify violations of
custom import restrictions, such as importing from
restricted packages or modules or violating import
standards defined by certain flags. Each code
corresponds to a different rule or condition, allowing
developers to quickly identify the source of the error and
take corrective action. The table below outlines the
various violation codes and their corresponding
descriptions.


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

  **CIR301**            This error signifies an import from a standalone
                        package, which is not allowed when the standalone
                        rule is enabled.

  **CIR302**            This error signifies a from import from an
                        standalone package, which is not allowed when the
                        standalone rule is enabled.

  **CIR303**            This error signifies an import from a standalone
                        module, which is not allowed when the standalone
                        rule is enabled.

  **CIR304**            This error signifies a from import from an
                        standalone module, which is not allowed when the
                        standalone rule is enabled.

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


**Project Import Rule Violation Codes**
---------------------------------------

Project Import Rule Violation Codes pertain to errors
thrown due to violations of project-specific import rules.
These rules are often defined to maintain a specific
structure or standard within the project, such as
restricting relative imports or wildcard imports. Violation
of these rules triggers specific error codes that help
developers identify the exact nature of the violation,
aiding in the debugging and maintenance of the codebase.
The following table provides a comprehensive list of these
violation codes, detailing their meanings and the conditions
under which they are triggered.


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

  **PIR103**            This error is thrown when a local scope import is
                        detected. This occurs when the
                        **--restrict-local-scope-imports** option is enabled.

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

**Plugin Limitations**
----------------------
-   This plugin is currently only compatible with Python 3.10+
    (support for 3.8 and 3.9 in the works).

-   Option custom-restrictions only supports restricting
    imports by package or module, not by class or function
    (i.e., `module_a.ClassA` or `module_a.function`).
    However, if you are trying to set import restrictions
    for a class or function, best practices would dictate
    that you should move that class or function to a
    separate module.

-   Files are not supported yet, use modules to set restrictions
    (e.g., `package/module/file.py` -> `package.module.file`).

-   Support for project level exceptions is not implemented yet.
    (e.g., you would like to restrict aliased imports but allow
    certain commonly aliased imports such as `numpy as np`).

-   Option top-level-only-imports has not been implemented yet.

-   Config checks have not been fully implemented yet, so
    it's possible to have invalid configurations that will
    not be caught by the plugin.
    (e.g., you designated a package or module as std-lib-only and
    third-party-only at the same time).

-   Private imports in tests are not supported yet. This
    means that if you have a test file that imports a private
    module, it will be flagged by the plugin. (An easy fix,
    including here in case I don't get to implementing it
    right away). Set the `--restrict-private-imports` flag
    to False in your config file if problematic.



**License**
-----------
This project is licensed under the terms of the `MIT License <LICENSE>`_.

**Acknowledgements**
--------------------

-   `flake8 <https://github.com/PyCQA/flake8>`_ - A wrapper around PyFlakes, pycodestyle and McCabe.
-   `flake8-import-order <https://github.com/PyCQA/flake8-import-order>`_ - ``flake8`` plugin that
    checks import order against various Python Style Guides. Used as a reference for this plugin.
-   `Writing Plugins for flake8 <https://flake8.pycqa.org/en/latest/plugin-development/index.html>`_ -
    ``flake8`` documentation on writing plugins.
-   `A flake8 plugin from scratch <https://www.youtube.com/watch?v=ot5Z4KQPBL8>`_ - YouTube video on
    writing a custom ``flake8`` plugin.
-   `flake8-bugbear <https://github.com/PyCQA/flake8-bugbear>`_ - ``flake8``
    plugin that finds likely bugs and design problems in your program.
