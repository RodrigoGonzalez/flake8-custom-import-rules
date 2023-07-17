""" Pytest configuration file. """
import configparser

import pytest
from flake8_import_order.checker import ImportVisitor


def load_config(path: str) -> configparser.RawConfigParser:
    """Load the config file at the given path."""
    cfg = configparser.RawConfigParser()
    cfg.read(path, encoding="UTF-8")
    return cfg


# while True:
# 	for candidate in ("setup.cfg", "tox.ini", ".flake8"):
# 		cfg = configparser.RawConfigParser()
# 		cfg_path = os.path.join(path, candidate)
# 		try:
# 			cfg.read(cfg_path, encoding="UTF-8")
# 		except (UnicodeDecodeError, configparser.ParsingError) as e:
# 			LOG.warning("ignoring not parseable config %s: %s", cfg_path, e)
# 		else:
# 			# only consider it a config if it contains flake8 sections
# 			if "flake8" in cfg or "flake8:local-plugins" in cfg:
# 				return cfg_path


@pytest.fixture(scope="session")
def import_visitor():
    """Return an instance of the public import visitor."""
    return ImportVisitor(["application_module", "tests"], ["company_module"])


@pytest.fixture(scope="session")
def list_flake8_extensions():
    """List all installed flake8 extensions."""
    from pkg_resources import iter_entry_points

    extensions = []
    for entry_point in iter_entry_points(group="flake8.extension"):
        extensions.append(entry_point.name)

    print(extensions)
    return extensions


def pytest_configure(config):
    """Register markers for pytest."""
    config.addinivalue_line("markers", "flake8: mark test to run flake8 checks.")
    config.addinivalue_line("markers", "pylama: mark test to run pylama checks.")