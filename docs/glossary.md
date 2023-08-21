# Glossary and Terminology

Welcome to the "Glossary," a comprehensive guide to
understanding key concepts and terminology in the
`flake8-custom-import-rules` package.

## Important Terms Used in This Package

- [Aliased Imports](#aliased-imports)
- [Conditional Imports](#conditional-imports)
- [Dynamic Imports](#dynamic-imports)
- [Future Imports (\_\_future__)](#future-imports-__future__)
- [Importing a Package Locally](#importing-a-package-locally)
- [Local Scope Import](#local-scope-import)
- [Main Script Imports (\_\_main__)](#main-script-imports-__main__)
- [Private Imports](#private-imports)
- [Python Modules](#python-modules)
- [Python Packages](#python-packages)
- [Relative Imports](#relative-imports)
- [Root Package](#root-package)
- [Wildcard Imports](#wildcard-imports)



## Aliased Imports

Aliased imports in Python refer to the practice of
importing a module or specific symbols from a module
under a different name, typically to make the code
more concise or to avoid naming conflicts. This is
done using the `as` keyword, allowing you to assign a
different name (alias) to the imported module or
symbol.

Here's an example of an aliased import:

```python
import numpy as np
```

In this example, the numpy module is imported under
the alias np, so you can refer to it as np in your
code instead of numpy. This is a common convention in
the scientific and data analysis community.

Here's another example, where a specific symbol is
aliased:

```python
from matplotlib import pyplot as plt
```

Here, the `pyplot` module from the `matplotlib` package
is imported under the alias `plt`.

### **Advantages of Aliased Imports:**

1.  **Conciseness**: Aliasing can make the code more
    concise, especially when dealing with modules or
    symbols with long or cumbersome names.

2.  **Avoiding Naming Conflicts**: If you have symbols
    with the same name in different modules, you can use
    aliasing to avoid conflicts.

3.  **Community Conventions**: Certain aliases are widely
    recognized and used in specific communities, such as
    `np` for `numpy` or `pd` for `pandas`.

### **Disadvantages and Considerations:**

1.  **Potential Confusion**: Non-standard or
    unconventional aliases might lead to confusion,
    especially for readers who are not familiar with the
    specific aliasing choices.
2.  **Loss of Clarity**: Overuse of aliasing or using
    overly short or cryptic aliases can reduce the
    readability of the code.

### **Best Practices and Recommendations:**

-   **Use Standard Aliases**: Where possible, stick to
    widely recognized and accepted aliases, such as `np`
    for `numpy`.
-   **Be Clear and Consistent**: If you choose to use
    aliases, make sure they are clear, descriptive, and
    used consistently throughout your codebase.
-   **Consider Readability**: Use aliasing judiciously and
    consider the trade-off between conciseness and
    readability.

In summary, aliased imports are a useful tool in Python,
allowing for more concise code and the ability to handle
naming conflicts. However, they should be used
thoughtfully and in line with community standards and best
practices to maintain code clarity and readability.

## Conditional Imports

Conditional imports in Python refer to the practice of
importing a module or specific symbols from a module based
on certain conditions or runtime logic. This means that the
import statement is executed only if a particular condition
is met, typically determined by an `if` statement or
similar control structure.

Here's an example that illustrates the concept of
conditional imports:

```python
import sys

if sys.version_info[0] == 3:
    import urllib.request as urllib_request
else:
    import urllib2 as urllib_request
```

In this example, the code checks the major version of
Python being used and imports the appropriate module
accordingly. This can be useful for maintaining
compatibility across different versions of Python or
other varying environments.

### **Advantages of Conditional Imports:**

1.  **Compatibility**: As shown above, conditional
    imports can be used to handle differences between
    Python versions, platforms, or other varying
    environments, helping to maintain compatibility.

2.  **Optimization**: By importing modules only when
    necessary, you might optimize the loading time or
    resource utilization of your program, especially when
    dealing with large or resource-heavy modules.

### **Disadvantages and Risks of Conditional Imports:**

1.  **Code Complexity**: Conditional imports can increase
    the complexity of the code, making it harder to read,
    understand, and maintain.

2.  **Potential Inconsistency**: The behavior of the code
    might become inconsistent or harder to predict, as the
    availability of a module or specific symbols may
    depend on runtime conditions.

### **Best Practices and Recommendations:**

-   **Clear Documentation**: If you use conditional
    imports, make sure to document the conditions and the
    reasoning behind them to help others (and yourself)
    understand the code.
-   **Testing**: Thoroughly test the code under different
    conditions to ensure that the conditional imports work
    as intended and do not introduce unexpected behavior or
    bugs.
-   **Avoid Overuse**: Consider whether conditional
    imports are truly necessary for your use case, and
    avoid overusing them, as they can lead to more complex
    and challenging-to-maintain code.

Conditional imports are a tool best suited for specific
scenarios, such as handling differences between Python
versions or platforms. In general code, it's usually
preferable to stick with straightforward and consistent
import statements.


## Dynamic Imports

Dynamic imports in Python refer to the practice of
importing modules or specific symbols from modules at
runtime, based on conditions or logic within the code.
Unlike standard imports, which are resolved at the time the
code is compiled, dynamic imports are resolved when the
code is executed. This is achieved using functions like
`importlib.import_module` or the built-in `__import__`
function.

Here's an example that illustrates the concept of dynamic
imports:

```python
import importlib

module_name = "os" if some_condition else "sys"
module = importlib.import_module(module_name)
```

In this example, the code dynamically imports either the
`os` or `sys` module, depending on the value of `some_condition`.

### **Advantages of Dynamic Imports:**

1.  **Flexibility**: Dynamic imports allow you to load modules
    based on runtime conditions, giving you more control and
    adaptability in your code.

2.  **Optimization**: By importing modules only when needed, you
    can potentially reduce the initial loading time or resource
    utilization of your application.

### **Disadvantages and Risks of Dynamic Imports:**

1.  **Code Complexity**: Dynamic imports can add complexity to
    the code, making it more challenging to read, understand, and
    maintain.

2.  **Potential Errors**: Errors related to dynamic imports might
    only manifest at runtime, making them harder to catch and
    debug.

### **Best Practices and Recommendations:**

-   **Use Standard Libraries**: Utilize the `importlib` standard
    library for dynamic imports rather than relying on the
    lower-level `__import__` function.

-   **Testing**: Ensure thorough testing of the code paths that
    involve dynamic imports to catch potential issues.

-   **Documentation**: Clearly document the reasoning and usage of
    dynamic imports in the code to aid understanding.

### **Limitations and Considerations:**

-   **Static Analysis Limitations**: Tools that perform static
    analysis on the code might have difficulty handling dynamic
    imports, as the imported modules are determined at runtime.

In summary, dynamic imports are a powerful but complex feature in
Python, allowing for more adaptable and potentially optimized
code. Care must be taken in their use to ensure clarity,
maintainability, and robustness.

## Future Imports ( \_\_future__ )

Future imports in Python are a special mechanism that
allows you to enable features that will become standard in
future versions of the language. By using future imports,
you can ensure compatibility with newer Python versions
and make your code more forward-compatible.

The `__future__` module in Python provides these future
import statements. When you import a feature from
`__future__`, it changes the compiler's behavior to
include that feature, even if it's not the default
behavior in the current version of Python.


Here's an example of a future import:

```python
from __future__ import division
```

This import changes the division operator `/` to always
perform true division, returning a floating-point result
even when dividing two integers. This behavior became the
default in Python 3, but the above import allows you to
use it in Python 2 as well.

### Common Uses of Future Imports:**

1.  **Division Behavior**: As shown above, changing the
    behavior of the division operator to be consistent
    with Python 3.

2.  **Print Function**: Enabling the use of the `print`
    function instead of the `print` statement in Python 2,
    making the code compatible with Python 3.

3.  **Unicode Literals**: Enabling the use of Unicode
    literals in Python 2, consistent with the behavior in
    Python 3.

### **Advantages of Future Imports:**

1.  **Forward Compatibility**: Future imports help prepare
    your code for future versions of Python, making the
    transition smoother when you decide to upgrade.

2.  **Consistency**: If you're working in an environment
    with different versions of Python, future imports can
    help ensure consistent behavior across those versions.

### **Considerations and Best Practices:**

1.  **Explicitness**: Future imports should be used
    explicitly in each module where the future behavior is
    needed.

2.  **Placement**: Future imports must appear at the top
    of the file, before any other imports or code, to affect
    the entire module.

3.  **Documentation**: If you're using future imports, it
    may be helpful to document why, especially if the reason
    might not be immediately obvious to others reading the
    code.

In summary, future imports are a valuable tool for ensuring
forward compatibility and consistency across different Python
versions. By understanding and using them appropriately, you
can write code that's more robust and maintainable as the
Python language evolves.


## Importing a Package Locally

This typically refers to importing a package that resides
within the local file system or project directory. It may
be a package or module developed specifically for the
project or a third-party package that has been downloaded
and stored locally. It's accessed directly from the local
path rather than from a globally installed location or
package repository.

**Example:**

```python
import my_local_package
from .local_module import local_function
```

In this context, "local" refers to the physical location of
the package on the system.

While the terms local scope import and import a package locally
may sound similar, they refer to different
aspects of the import process. The first is concerned with
where the package or module is located on the file system,
while the second deals with where in the code the import
statement is placed and the scope of the imported elements.


## Local Scope Import
A local import often refers to an import statement that
is specific to a particular scope within the code. It
may mean importing a module or function within a specific
function or method, rather than at the top level of a
file. This type of import is often used to minimize
the scope of the imported element, ensuring that it's
only available where it's needed.

**Example:**

```python
def my_function():
    """A function that imports a module locally."""
    import requests  # third-party local import
    response = requests.get('https://example.com')
    return response.text
```

Here, "local" refers to the scope and context of the
import, not the physical location of the imported module.


### **Advantages of Local Scope Imports:****

1.  **Reduced Initial Loading Time**: If a module is
    imported inside a function and that function is never
    called, the module won't be imported, potentially
    reducing the initial loading time of the script.

2.  **Avoiding Circular Dependencies**: Sometimes, local
    imports can help in avoiding circular dependencies
    between different modules.

3.  **Selective Importing**: Importing only in the scope
   where it is needed can help in keeping the global
   namespace clean.

### **Disadvantages of Local Scope Imports:****

1.  **Potential Performance Overhead**: If a function with a
    local import is called many times, the import statement
    will be executed each time the function is called,
    which might introduce a small performance overhead.

2.  **Code Clarity**: Local imports can make the code harder
    to follow, especially if overused, as it may become
    unclear where exactly different modules and functions
    are being imported.

### **When to Use Local Scope Imports:****

Local scope imports are not common in every project, and
their usage often depends on specific needs, coding
guidelines, and design considerations. They might be used
to solve particular problems like circular dependencies
or to optimize the loading of large and infrequently used
modules.

Typically, code style guides recommend importing at the
top level of the file for clarity and consistency, but
local scope imports can be a valuable tool in certain
situations.


## Main Script Imports (\_\_main__)

Importing from the `__main__` module or a `__main__.py`
file is generally not considered best practice in Python
development.

### **Importing from the `__main__` Module**

The `__main__` module is the entry point of a program, and
it's the context in which the top-level script is run.
Importing from this module is relatively uncommon and can
lead to code that is difficult to understand or maintain.
Here are some reasons why:

-   **Uncommon Practice**: The `__main__` module is
    typically associated with script execution, not with
    defining reusable components.

-   **Potential Confusion**: It might be unclear what is
    being imported from `__main__`, especially if the main
    script is large or complex.

-   **Code Organization Issues**: Needing to import from
    `__main__` may indicate that the code could benefit
    from reorganization.

-   **Testing Challenges**: Code that relies on imports
    from `__main__` may be more difficult to test in
    isolation.

### **Importing from a `__main__.py` File**

The `__main__.py` file is used to define the entry point
for a package when it's executed as a script. Here's why
importing from `__main__.py` can be problematic:

-   **Lack of Clarity**: Like the `__main__` module,
    `__main__.py` is usually associated with script
    execution, not with defining reusable components.

-   **Potential Circular Dependencies**: You can easily end
    up with circular dependencies that are difficult to
    resolve.

-   **Maintenance Challenges**: Serving dual purposes can
    become a maintenance burden.

-   **Incompatibility with Certain Tools**: Some tools
    might treat `__main__.py` specially, leading to
    unexpected behavior.

### **Recommended Structure**

Instead of putting reusable code in the `__main__` module
or `__main__.py` file, it's generally a better practice to
define functions, classes, and other reusable components in
separate modules within your package. Here's an example
structure:

```plaintext
mypackage/
├── __main__.py         # Entry point for script execution
├── utilities.py        # Reusable functions and classes
└── other_module.py     # Other reusable components
```
In `__main__.py`, you can import from `utilities.py` and
other_module.py as needed for script execution. This keeps
your codebase organized and clear and avoids the potential
problems mentioned above.

In summary, while importing from the `__main__` module or a
`__main__.py` file is technically possible, it's generally
not a common or recommended practice. Organizing code into
separate modules enhances clarity, maintainability, and
avoids potential issues.


## Private Imports

Private imports in Python refer to the practice of
importing symbols (such as functions, classes, or variables)
that are intended for internal use within a module or
package and are not part of the public API. These symbols
are often prefixed with an underscore (`_`), which by
convention signals that they are considered "private" or
"internal" and should not be accessed directly by external
code.

Here's an example to illustrate private imports:

Suppose you have a module `my_module.py`:

```python
# my_module.py

def public_function():
    """A public function that can be accessed externally."""
    return _private_helper_function()

def _private_helper_function():
    return "This is a private function!"
```

You might import and use the `_private_helper_function` within
the same package, but it is not intended to be accessed
directly by external code.

### **Why Use Private Imports?**

1.  **Encapsulation**: By marking certain symbols as private,
    you can define a clear and stable public API while keeping
    the flexibility to change, remove, or refactor the internal
    implementation without affecting external code.

2.  **Code Organization**: Private imports help organize code by
    clearly separating the public interface from the internal
    implementation details.

### **Best Practices and Recommendations:**

-   **Naming Convention**: Use a single leading underscore to
    mark symbols as private. This does not prevent access to the
    symbols but serves as a gentle warning to other developers
    that the symbol is considered internal.

-   **Documentation**: Clearly document which parts of your module
    or package are considered public and which are private.

-   **Respect the Convention**: As a consumer of other modules or
    packages, respect the private nature of symbols with leading
    underscores and avoid using them directly.

### **Limitations and Considerations:**

-   **No Strict Enforcement**: Python does not provide a strict
    mechanism to enforce private access. The leading underscore is
    a convention, not a hard restriction, so external code can still
    import and use private symbols. However, doing so is generally
    considered bad practice and may lead to compatibility issues if
    the internal symbols change in future versions of the module
    or package.

-   **Not to be Confused with Name Mangling**: Double leading
    underscores (e.g., `__private_var`) trigger name mangling in
    Python, which alters the name to avoid clashes in subclasses.
    This is a separate mechanism and not the same as marking a
    symbol as private.

In summary, private imports are a valuable tool in designing
clean and maintainable code by defining a clear boundary between
public interfaces and internal implementation. They rely on
community conventions and developer discipline rather than strict
language enforcement.


## Python Modules

**Definition**: A module is a single file containing Python
code. It can contain functions, variables, classes, and
runnable code. Essentially, any Python file with a `.py`
extension is a module.

**Purpose**: Modules are used to organize code into reusable
and manageable chunks. By putting related functions and
variables into a module, you can import them into other
Python files.

**Example:**

A file named `mymodule.py` containing functions
and classes related to mathematical operations.

## Python Packages

**Definition**: A package is a directory that contains
multiple module files and a special `__init__.py` file.
The presence of `__init__.py` (which can be empty) tells
Python that the directory should be considered a package.

**Purpose**: Packages are used to organize multiple modules
into a hierarchical namespace. This allows for structuring
your code in a way that groups related modules together,
making it more maintainable and scalable.

**Example:**

A directory named mypackage containing several
module files related to different aspects of data
processing, and an `__init__.py` file to signify it as a
package.

## Relative Imports

Relative imports in Python allow you to import modules or
specific objects from modules that are located relative to
the current module or package. They make use of dots (`.`)
to indicate the relative path to the desired module within
the same package hierarchy.

Here's a breakdown of how relative imports work:

-   A single dot (`.`) refers to the current package or
    directory.
-   Two dots (`..`) refer to the parent package or
    directory.
-   Additional dots (`...`, `....`, etc.) refer to
    higher-level parent packages or directories.

**Example:**

Consider the following directory structure:

```plaintext
my_package/
├── subpackage_a/
│   ├── module_a.py
│   └── __init__.py
├── subpackage_b/
│   ├── module_b.py
│   └── __init__.py
└── __init__.py
```

If you want to import `module_a.py` from `module_b.py`,
you can use a relative import like this (inside
`module_b.py`):

```python
from ..subpackage_a import module_a
```

### **Advantages of Relative Imports**

1.  **Portability**: Relative imports make the code more
   portable, as they don't rely on the absolute path of
   the module. If you move the package to a different
   location, the relative imports will still work.

2.  **Readability**: In a well-structured project, relative
   imports can make the code more concise and clear by
   showing the relationship between modules.

### **Potential Issues**

1.  **Ambiguity**: Without clear context, relative imports
   might be less intuitive to understand, especially in a
   complex project.

2.  **Compatibility**: Relative imports require the file to
   be part of a package (i.e., there must be an
   `__init__.py` file), and they are not meant to be used
   in standalone scripts.

### **Best Practices**

While relative imports can be useful, it's essential to
use them thoughtfully and consistently. Many projects
prefer to use absolute imports for clarity, especially if
the package structure is not overly complex. Mixing
relative and absolute imports without clear guidelines can
lead to confusing code.

In Python 3, all imports that start with a dot are
considered relative, and attempting to perform a relative
import from a script that is not part of a package will
result in an ImportError. Therefore, understanding the
package structure and following consistent practices is key
to using relative imports effectively.


## Root Package

A root package, also referred to as the top-level package,
is the main or primary package in a project that serves as
the entry point for accessing other modules and packages
within the project hierarchy. It is often the package that
represents the project's main functionality or encapsulates
the entire codebase. The root package can be considered the
"base" or "parent" of all other packages and modules within
the project.

**Definition:**

The root package is the highest-level package in a project's
hierarchy. It often contains the main entry points, key
functionalities, or core components of the project. Other
packages and modules within the project are typically
organized under the root package, either directly or
through nested subpackages.

**Example:**

Consider a project called `MyApp` that has the following
directory structure:

```
MyApp/
├── my_root_package/
│   ├── __init__.py
│   ├── subpackage_a/
│   │   ├── __init__.py
│   │   └── module_a.py
│   ├── subpackage_b/
│   │   ├── __init__.py
│   │   └── module_b.py
│   └── main_module.py
└── setup.py
```

In this example, `my_root_package` is the root package of
the project. It serves as the top-level package containing
all the other subpackages (`subpackage_a`, `subpackage_b`)
and modules (`main_module.py`) within the project. The root
package often plays a central role in the project's
architecture and dependency management. Accessing
functionalities within the project would typically involve
importing from this root package.


## Wildcard Imports

Wildcard imports in Python refer to the practice of
importing all symbols (functions, classes, variables, etc.)
from a module into the current namespace using the asterisk
(`*`) symbol. This can make all the names defined in the
imported module available in the current scope without
needing to prefix them with the module name.

Here's an example of a wildcard import:

```python
from math import *
```

After this import, you can directly use functions like
`sqrt`, `sin`, `cos`, etc., from the `math` module
without prefixing them with `math.`.

### **Advantages of Wildcard Imports**

1.  **Conciseness**: Wildcard imports can make the code
   more concise, as you don't need to prefix every call
   with the module name or list all the specific names
   you want to import.

### **Disadvantages and Risks of Wildcard Imports**

1.  **Namespace Clashes**: If different modules define
   symbols with the same name, wildcard imports can lead
   to name clashes, potentially overwriting existing names
   in the current namespace.

2.  **Readability and Maintainability**: Wildcard imports
   can make the code less readable, as it becomes unclear
   where a specific symbol comes from. This can make code
   maintenance and debugging more challenging.

3.  **Lack of Control**: By importing everything, you may
   bring into scope symbols that you don't need or intend
   to use, cluttering the namespace.

4.  **Potential Inefficiency**: Importing everything from
   a large module might consume more memory or slow down
   the loading time, even if you only need a small subset
   of the functions or classes.

### **Best Practices and Recommendations**

Wildcard imports are generally discouraged in production
code due to the risks and disadvantages mentioned above.
Many style guides, such as PEP 8, recommend avoiding
wildcard imports and instead explicitly listing the names
you want to import. This promotes clarity, maintainability,
and reduces the risk of unexpected behavior.

If you need to use many symbols from a module, you can
import the module itself and then use the module prefix to
access its symbols:

```python
import math

result = math.sqrt(16)
```

Or, you can explicitly list the symbols you want to
import:

```python
from math import sqrt, sin, cos
```

Both of these approaches provide more control and clarity
compared to wildcard imports.
