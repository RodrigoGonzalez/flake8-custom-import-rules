"""Setuptools entry point for the project's Cython extension configuration.

Package metadata is defined in ``pyproject.toml``. This file exists only to
supply the programmable Cython extension configuration required by the
setuptools PEP 517 build backend.
"""

from __future__ import annotations

import sys
from pathlib import Path

from setuptools import setup

# setuptools executes this file as a string during PEP 517 isolation, so the
# project root is not guaranteed to be on ``sys.path``.
sys.path.insert(0, str(Path.cwd()))

from scripts.build import build


setup_kwargs: dict[str, object] = {}
build(setup_kwargs)
setup(**setup_kwargs)
