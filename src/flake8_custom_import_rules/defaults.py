"""The default settings for the flake8_custom_import_rules plugin."""
import sys

if sys.version_info < (3, 8):
    from typing_extensions import TypedDict
else:
    from typing import TypedDict


class Settings(TypedDict, total=False):
    base_package: str
    # version: Optional[str]
    # version_files: List[str]
    # version_provider: Optional[str]
    # tag_format: Optional[str]
    # bump_message: Optional[str]
    # allow_abort: bool
    # changelog_file: str
    # changelog_incremental: bool
    # changelog_start_rev: Optional[str]
    # changelog_merge_prerelease: bool
    # update_changelog_on_bump: bool
    # use_shortcuts: bool
    # style: Optional[List[Tuple[str, str]]]
    # customize: CzSettings
    # major_version_zero: bool
    # pre_bump_hooks: Optional[List[str]]
    # post_bump_hooks: Optional[List[str]]
    # prerelease_offset: int
    # version_type: Optional[str]


DEFAULT_SETTINGS: Settings = {
    "base_package": "",
}
