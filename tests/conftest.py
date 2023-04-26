from __future__ import annotations

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
# 			LOG.warning("ignoring unparseable config %s: %s", cfg_path, e)
# 		else:
# 			# only consider it a config if it contains flake8 sections
# 			if "flake8" in cfg or "flake8:local-plugins" in cfg:
# 				return cfg_path


@pytest.fixture(scope="session")
def import_visitor():
    """Return an instance of the public import visitor."""
    return ImportVisitor(["application_module", "tests"], ["company_module"])
