"""Test the option utils with a sample setting instance"""
from flake8_custom_import_rules.defaults import Settings
from flake8_custom_import_rules.utils.option_utils import check_conflicts


def test_check_conflicts():
    """Test the check_conflicts function."""
    sample_settings = Settings()
    sample_settings.THIRD_PARTY_ONLY = ["package1", "package2"]
    sample_settings.FIRST_PARTY_ONLY = ["package2", "package3"]
    sample_settings.STANDALONE_MODULES = ["module1"]
    sample_settings.IMPORT_RESTRICTIONS = {
        "module1": ["submoduleA", "submoduleB"],
        "module2": ["submoduleC"],
    }

    check_conflicts(sample_settings.dict)


def test_check_conflicts__for_none():
    """Test the check_conflicts function."""
    sample_settings = Settings()
    assert check_conflicts(sample_settings.dict) is None
