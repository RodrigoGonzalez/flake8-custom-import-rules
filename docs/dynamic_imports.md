# Dynamic Imports Explained

Dynamic importing is a method where modules are loaded when they are
needed, or at runtime. Python provides several built-in functions
and packages that support dynamic imports. Here are a few examples:

###  1. **`importlib`**

This is a built-in Python library that offers functions for importing
modules programmatically. The `import_module()` function is commonly
used for dynamic imports. Here’s an example:


```python
"""Dynamic Imports importlib Example"""
import importlib

module = importlib.import_module('math')
print(module.sqrt(4))  # Outputs: 2.0
```


### 2. **`__import__()`**
This is a built-in Python function that can be used for dynamic
imports. However, it’s generally recommended to use
`importlib.import_module()` instead, as `__import__()` is more
complex and not intended for direct use. Here’s an example:

```python
"""Dynamic Imports importlib Example"""
module_name = "math"
module = __import__(module_name)
print(module.sqrt(4))
# Outputs: 2.0
```

### 3. **`exec() and eval()`**

This is a built-in Python function that can execute Python code
dynamically. It can be used for dynamic imports, but it’s
generally not recommended because it can pose security risks if used
with untrusted input. Here’s an example:

```python
"""Dynamic Imports Execute Example"""
module_name = "math"
exec(f"import {module_name}")
print(math.sqrt(4))
# Outputs: 2.0
```

### 4. **`globals()` and `locals()`**

These are built-in Python functions that return the current global
and local symbol table, respectively. They can be used in
conjunction with `exec()` or `__import__()` to dynamically import
modules into the current namespace.

Here’s an example of using `globals()` with `__import__()` to
dynamically import a module into the current namespace:

```python
"""Dynamic Imports Globals Example"""
module_name = "math"
globals()[module_name] = __import__("math")

# Now you can use the 'math' module directly
print(math.sqrt(4))
# Outputs: 2.0
```

And here’s an example of using `locals()` with `exec()` to
dynamically import a module into the current namespace:

```python
"""Dynamic Imports Example"""
module_name = "math"
exec(f"{module_name} = __import__('{module_name}')")

# Now you can use the 'math' module directly
print(math.sqrt(4))
# Outputs: 2.0
```

In this example,
```exec(f"{module_name} = __import__('{module_name}')")```
executes a string of Python code that imports the `math` module
and adds it to the local symbol table. This allows you to use the
`math` module directly in your code, just like if you had imported
it with `import math`.

The `exec()` function should be used with caution, as it can pose
security risks if used with untrusted input.

### 5. **`pkgutil`**:

```python
import pkgutil

# Load the 'os' module
module = pkgutil.get_loader('os').load_module('os')
```

### 6. **`pkgutil.get_loader`**:

```python
from pkgutil import get_loader

# Load the 'os' module
module = get_loader('os').load_module('os')
```

### 7. **`pkgutil.iter_modules`**:

```python
import pkgutil

# List all the modules in the 'os' package
for module_info in pkgutil.iter_modules(['os']):
    print(module_info)
```

### 8. **`zipimport`**:

```python
import zipimport

# Import a module from a zip archive
zipimporter = zipimport.zipimporter('my_module.zip')
module = zipimporter.load_module('my_module')
```

### 9. **`zipimport.zipimporter`**:

```python
from zipimport import zipimporter

# Import a module from a zip archive
zipimporter = zipimporter('my_module.zip')
module = zipimporter.load_module('my_module')
```


NOTE: Remember, dynamic imports can make code harder to
understand and debug, and they can pose security risks
if used improperly. Therefore, they should be used sparingly
and with caution.
