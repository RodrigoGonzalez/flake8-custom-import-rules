"""Build configuration for Cython extension modules.

This module defines the Cython build configuration for the performance-sensitive
parts of ``flake8_custom_import_rules``.

The original implementation was added as a Poetry build hook. The project now
uses uv for dependency management, environment management, locking, command
execution, building, and publishing. Cython extension compilation is delegated
to an extension-capable PEP 517 build backend, such as ``setuptools.build_meta``.

The selected modules intentionally match the modules targeted by the original
Cython build implementation:

- ``core/error_messages.py``
- ``core/import_rules.py``
- ``core/node_visitor.py``
- ``core/nodes.py``
- ``core/restricted_import_visitor.py``
- ``core/rules_checker.py``

Cython documentation:
https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html

Setuptools integration:
https://cython.readthedocs.io/en/latest/src/userguide/compilation_setuptools.html

The historical implementation used a global ``CFLAGS=-O3`` environment
mutation. This implementation instead applies compiler-appropriate optimization
flags through ``build_ext`` so that GCC/Clang and MSVC builds can both be
supported without modifying the caller's environment.

The historical implementation also enabled Cython ``linetrace``. Cython
requires both the compiler directive and the ``CYTHON_TRACE`` C macro for line
tracing to be active, so both are configured here.

This module contains build configuration only. Package metadata remains in
``pyproject.toml``.
"""

from __future__ import annotations

from collections.abc import MutableMapping
from pathlib import Path
from typing import Final

from Cython.Build import cythonize
from setuptools import Extension
from setuptools.command.build_ext import build_ext


SOURCE_ROOT: Final[Path] = Path("src")

# Keep generated C/build intermediates out of the source package directories.
CYTHON_BUILD_DIR: Final[Path] = Path("build") / "cython"

# These are the performance-sensitive modules intentionally selected by the
# original Cython build implementation. Do not expand this list merely because
# additional Python modules exist; additions should be justified separately.
CYTHON_MODULES: Final[tuple[str, ...]] = (
    "flake8_custom_import_rules.core.error_messages",
    "flake8_custom_import_rules.core.import_rules",
    "flake8_custom_import_rules.core.node_visitor",
    "flake8_custom_import_rules.core.nodes",
    "flake8_custom_import_rules.core.restricted_import_visitor",
    "flake8_custom_import_rules.core.rules_checker",
)

# Cython line tracing requires the compiler directive plus this C macro.
CYTHON_TRACE_MACRO: Final[tuple[str, str]] = ("CYTHON_TRACE", "1")

# Preserve the original optimization intent without assuming every compiler
# understands GCC/Clang's ``-O3`` flag.
UNIX_OPTIMIZATION_FLAG: Final[str] = "-O3"
MSVC_OPTIMIZATION_FLAG: Final[str] = "/O2"


def _module_source(module_name: str) -> str:
    """Return the Python source path for a dotted extension-module name.

    Parameters
    ----------
    module_name : str
        Fully qualified Python module name beneath the project's ``src``
        directory.

    Returns
    -------
    str
        Relative path to the module's ``.py`` source file.

    Examples
    --------
    ``flake8_custom_import_rules.core.nodes`` becomes
    ``src/flake8_custom_import_rules/core/nodes.py``.
    """
    return str(SOURCE_ROOT.joinpath(*module_name.split(".")).with_suffix(".py"))


def _create_extensions() -> list[Extension]:
    """Create setuptools extension definitions for Cythonized modules.

    Returns
    -------
    list[Extension]
        Extension definitions for the explicitly selected Cython modules.

    Notes
    -----
    The extension names intentionally match the corresponding Python module
    names. The compiled extension therefore occupies the same import location
    as the Python implementation.

    ``CYTHON_TRACE`` is defined because ``linetrace=True`` alone is insufficient
    to enable Cython line tracing in generated extension modules.
    """
    return [
        Extension(
            name=module_name,
            sources=[_module_source(module_name)],
            define_macros=[CYTHON_TRACE_MACRO],
        )
        for module_name in CYTHON_MODULES
    ]


class OptimizedBuildExt(build_ext):
    """Build Cython extensions with compiler-appropriate optimization flags.

    The historical build script set ``CFLAGS=-O3`` globally. That approach
    overwrites caller configuration and is not portable to Microsoft's compiler.

    This command instead augments each extension's compile arguments after the
    active compiler has been initialized.

    GCC/Clang-style compilers receive ``-O3``. MSVC receives ``/O2``. Unknown
    compiler types are left unchanged rather than receiving an invalid flag.
    """

    def build_extensions(self) -> None:
        """Apply optimization flags and build all configured extensions.

        Returns
        -------
        None

        Notes
        -----
        Existing ``extra_compile_args`` are preserved. The optimization flag is
        appended only when it is not already present.

        Unknown compiler implementations are allowed to proceed without a
        project-imposed optimization flag. This is preferable to failing a
        supported platform because its compiler does not accept either the
        GCC/Clang or MSVC flag syntax.
        """
        compiler_type = getattr(self.compiler, "compiler_type", None)

        optimization_flag: str | None
        if compiler_type == "msvc":
            optimization_flag = MSVC_OPTIMIZATION_FLAG
        elif compiler_type in {"unix", "cygwin", "mingw32"}:
            optimization_flag = UNIX_OPTIMIZATION_FLAG
        else:
            optimization_flag = None

        if optimization_flag is not None:
            for extension in self.extensions:
                compile_args = list(extension.extra_compile_args or [])

                if optimization_flag not in compile_args:
                    compile_args.append(optimization_flag)

                extension.extra_compile_args = compile_args

        super().build_extensions()


def build_cython_extensions() -> list[Extension]:
    """Create the Cythonized extension modules used by the package build.

    Returns
    -------
    list[Extension]
        Cythonized setuptools extension definitions for the selected core
        modules.

    Notes
    -----
    Cythonization preserves the intent of the original build implementation:

    - Python 3 language semantics.
    - Line tracing support.
    - Compilation of the six explicitly selected core modules.
    - Optimized native compilation through ``OptimizedBuildExt``.
    - Disabled annotation typing so Cython 3 does not coerce existing
      function annotations into runtime C type checks. Several selected
      modules pass attrs ``field()`` objects into annotated helpers at
      class-body evaluation time, which is valid Python and must keep
      working after compilation.

    Generated C/build intermediates are placed under ``build/cython`` instead
    of being written into ``src/``.

    This function does not mutate package metadata. Metadata remains governed
    by ``pyproject.toml``.
    """
    return cythonize(
        _create_extensions(),
        build_dir=str(CYTHON_BUILD_DIR),
        compiler_directives={
            "language_level": 3,
            "linetrace": True,
            "annotation_typing": False,
        },
        annotate=False,
    )


def build(setup_kwargs: MutableMapping[str, object]) -> None:
    """Populate setuptools configuration with the Cython build definition.

    Parameters
    ----------
    setup_kwargs : MutableMapping[str, object]
        Mutable keyword-argument mapping that will be supplied to
        ``setuptools.setup``.

    Returns
    -------
    None
        The provided mapping is modified in place.

    Notes
    -----
    This function intentionally retains the public shape of the historical
    Poetry build hook:

    ``build(setup_kwargs)``

    Retaining that interface preserves the useful separation between package
    metadata and extension-build configuration while allowing the project to
    consume the function from a modern setuptools/PEP 517 build entry point.

    Unlike the historical implementation, Cython is expected to be declared as
    a build-system requirement. A missing Cython installation is therefore a
    build-environment defect and should fail explicitly rather than silently
    producing a different pure-Python distribution.
    """
    setup_kwargs.update(
        {
            "ext_modules": build_cython_extensions(),
            "cmdclass": {"build_ext": OptimizedBuildExt},
        }
    )
