""" Pytest configuration file. """
import configparser
import itertools
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def main_directory() -> Path:
    """Return the main directory of the project."""
    return Path(__file__).parent.parent


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


def pytest_configure(config):
    """Register markers for pytest."""
    config.addinivalue_line("markers", "flake8: mark test to run flake8 checks.")
    config.addinivalue_line("markers", "pylama: mark test to run pylama checks.")


@pytest.fixture(scope="module")
def package_7() -> list:
    """Test get_restricted_identifiers."""
    package_7 = []
    first_list = [
        "my_second_base_package",
        "my_base_module",
        "my_third_base_package",
    ]
    second_list = ["", "module_one", "module_two", "file"]
    third_list = ["", "file_one", "file_two"]
    for first, second in itertools.product(first_list, second_list):
        if second in [""]:
            package_7.append(first)
            continue
        if f"{second}" in ["file"]:
            package_7.append(f"{first}.{second}")
            continue
        for third in third_list:
            if f"{second}.{third}" in [".", "file.file_one", "file.file_two"]:
                package_7.append(f"{first}.{second}")
                continue
            package_7.append(f"{first}.{second}.{third}".strip("."))
    return package_7


@pytest.fixture(scope="module")
def package_8(package_7) -> list:
    """Test get_restricted_identifiers."""
    package_8 = []
    for restricted_package in package_7:
        temp = [package for package in package_7 if not package.startswith(restricted_package)]
        package_8.append(f"{restricted_package}:{','.join(temp)}")
    return package_8
