# flake8-custom-import-rules
A Flake8 plugin that enforces custom import rules, allowing users to define and maintain clean and consistent import organization across their Python projects.

Restricted imports: Define a list of modules that are restricted from importing specific modules within your base module. For example, you might want to prevent module A from importing module B or any of its submodules.
Isolated imports: Specify a list of modules that cannot import from any other modules within your base module. This can be useful for ensuring that certain modules remain standalone and do not introduce unwanted dependencies.
Standard library only imports: Define a set of modules that can only import from the Python standard library. This rule helps to keep specific modules lightweight and free from third-party dependencies.
