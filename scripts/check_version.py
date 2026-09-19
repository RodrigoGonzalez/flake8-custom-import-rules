#!/usr/bin/env python3
"""Compare version authorities without importing the package.

This script is stdlib-only and must remain runnable when ``uv.lock`` is
stale or the project is not installed. Python 3.10 does not provide
``tomllib``, so parsing is narrowly scoped to the known project files.

The compared authorities are:

- ``pyproject.toml`` ``[project].version``
- ``uv.lock`` root project package version
- ``src/flake8_custom_import_rules/__init__.py`` ``__version__``
- top release heading in ``CHANGELOG.md``
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROJECT_NAME = "flake8-custom-import-rules"


def normalize_project_name(name: str) -> str:
    """Normalize a distribution name for identity comparison.

    Parameters
    ----------
    name : str
        A project or package name that may mix hyphen, underscore,
        dot, and case.

    Returns
    -------
    str
        The name in lowercase with hyphen, underscore, and dot
        collapsed to hyphen.
    """
    collapsed = re.sub(r"[-_.]+", "-", name.strip())
    return collapsed.lower()


def parse_pyproject_version(path: Path) -> str:
    """Read ``[project].version`` from ``pyproject.toml``.

    Parameters
    ----------
    path : Path
        Path to ``pyproject.toml``.

    Returns
    -------
    str
        The project version string.

    Raises
    ------
    ValueError
        If the ``[project]`` table or ``version`` field is missing.
    """
    text = path.read_text(encoding="utf-8")
    in_project = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("[") and line.endswith("]"):
            in_project = line == "[project]"
            continue
        if in_project:
            match = re.fullmatch(r'version\s*=\s*["\']([^"\']+)["\']', line)
            if match:
                return match.group(1)
    raise ValueError(f"could not parse [project].version from {path}")


def parse_uv_lock_version(path: Path, project_name: str) -> str:
    """Read the root project version from ``uv.lock``.

    Parameters
    ----------
    path : Path
        Path to ``uv.lock``.
    project_name : str
        Canonical project name used for identity matching.

    Returns
    -------
    str
        The locked root package version.

    Raises
    ------
    ValueError
        If no matching root package entry is found.
    """
    text = path.read_text(encoding="utf-8")
    expected = normalize_project_name(project_name)
    current_name: str | None = None
    current_version: str | None = None
    is_root = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line == "[[package]]":
            if (
                current_name is not None
                and normalize_project_name(current_name) == expected
                and is_root
                and current_version is not None
            ):
                return current_version
            current_name = None
            current_version = None
            is_root = False
            continue
        name_match = re.fullmatch(r'name\s*=\s*"([^"]+)"', line)
        if name_match:
            current_name = name_match.group(1)
            continue
        version_match = re.fullmatch(r'version\s*=\s*"([^"]+)"', line)
        if version_match and current_version is None:
            current_version = version_match.group(1)
            continue
        if "source = { editable = \".\" }" in line or line == 'source = { editable = "." }':
            is_root = True
    if (
        current_name is not None
        and normalize_project_name(current_name) == expected
        and is_root
        and current_version is not None
    ):
        return current_version
    raise ValueError(f"could not parse root package version from {path}")


def parse_init_version(path: Path) -> str:
    """Read ``__version__`` from the package ``__init__.py``.

    Parameters
    ----------
    path : Path
        Path to ``src/flake8_custom_import_rules/__init__.py``.

    Returns
    -------
    str
        The source version string.

    Raises
    ------
    ValueError
        If ``__version__`` is not found.
    """
    text = path.read_text(encoding="utf-8")
    match = re.search(r'^__version__\s*=\s*["\']([^"\']+)["\']', text, re.M)
    if match:
        return match.group(1)
    raise ValueError(f"could not parse __version__ from {path}")


def parse_changelog_version(path: Path) -> str:
    """Read the top stable release version from ``CHANGELOG.md``.

    Parameters
    ----------
    path : Path
        Path to ``CHANGELOG.md``.

    Returns
    -------
    str
        The first ``vMAJOR.MINOR.PATCH`` heading version.

    Raises
    ------
    ValueError
        If no matching release heading is found.
    """
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^##\s+v(\d+\.\d+\.\d+)\b", text, re.M)
    if match:
        return match.group(1)
    raise ValueError(f"could not parse top changelog version from {path}")


def main() -> int:
    """Compare version authorities and report mismatches.

    Returns
    -------
    int
        ``0`` when all versions agree, otherwise ``1``.
    """
    sources = {
        "pyproject.toml": PROJECT_ROOT / "pyproject.toml",
        "uv.lock": PROJECT_ROOT / "uv.lock",
        "src/flake8_custom_import_rules/__init__.py": (
            PROJECT_ROOT / "src" / "flake8_custom_import_rules" / "__init__.py"
        ),
        "CHANGELOG.md": PROJECT_ROOT / "CHANGELOG.md",
    }
    observed: dict[str, str] = {}
    errors: list[str] = []
    parsers = {
        "pyproject.toml": lambda: parse_pyproject_version(sources["pyproject.toml"]),
        "uv.lock": lambda: parse_uv_lock_version(sources["uv.lock"], PROJECT_NAME),
        "src/flake8_custom_import_rules/__init__.py": lambda: parse_init_version(
            sources["src/flake8_custom_import_rules/__init__.py"]
        ),
        "CHANGELOG.md": lambda: parse_changelog_version(sources["CHANGELOG.md"]),
    }
    for label, parser in parsers.items():
        try:
            observed[label] = parser()
        except (OSError, ValueError) as exc:
            observed[label] = f"<unreadable: {exc}>"
            errors.append(str(exc))

    versions = [value for value in observed.values() if not value.startswith("<unreadable:")]
    unique = set(versions)
    mismatch = len(unique) != 1 or bool(errors)

    print("Observed versions:")
    for label, value in observed.items():
        print(f"  {label}: {value}")

    if mismatch:
        print("Version mismatch.")
        return 1
    print("Versions are consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
