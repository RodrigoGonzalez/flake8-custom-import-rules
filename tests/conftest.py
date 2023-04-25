"""Pytest configuration file."""
import pytest


@pytest.fixture(scope="session")
def list_flake8_extensions():
    """List all installed flake8 extensions."""
    from pkg_resources import iter_entry_points

    extensions = []
    for entry_point in iter_entry_points(group="flake8.extension"):
        extensions.append(entry_point.name)

    print(extensions)
    return extensions
