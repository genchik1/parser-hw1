from datetime import date
from pathlib import Path

import pytest

from src.settings import Config
from src.utils import search_last_file


@pytest.fixture
def tmp_dir(tmp_path: Path) -> Path:
    files = [
        "invalid.log",
        "nginx-access-ui.log-20250101",
        "nginx-access-ui.log-20250103",
        "nginx-access-ui.20250103-log.gz",
        "nginx-access-ui.log-20250102.gz",
    ]

    for f in files:
        (tmp_path / f).touch()  # type:ignore[operator]

    return tmp_path


def test_find_latest_valid_file(tmp_dir: Path, config: Config) -> None:
    result = search_last_file(
        file_dir=str(tmp_dir), file_name_pattern=config.log_file_name_format, date_format="%Y%m%d"
    )

    assert result is not None
    assert result.path.name == "nginx-access-ui.log-20250103"
    assert result.date == date(2025, 1, 3)


def test_no_matching_files(tmp_dir: Path) -> None:
    pattern = r"non-existent-pattern-(?P<date>\d{8})"
    result = search_last_file(file_dir=str(tmp_dir), file_name_pattern=pattern, date_format="%Y%m%d")

    assert result is None


def test_missing_date_group(tmp_dir: Path) -> None:
    pattern = r"nginx-access-ui\.log-\d{8}"
    with pytest.raises(KeyError):
        search_last_file(file_dir=str(tmp_dir), file_name_pattern=pattern, date_format="%Y%m%d")


def test_nonexistent_directory() -> None:
    with pytest.raises(Exception):
        search_last_file(file_dir="/nonexistent/path", file_name_pattern=".*", date_format="%Y%m%d")


def test_prefer_uncompressed_over_compressed(tmp_dir: Path, config: Config) -> None:
    (tmp_dir / "nginx-access-ui.log-20230104.gz").touch()
    result = search_last_file(
        file_dir=str(tmp_dir), file_name_pattern=config.log_file_name_format, date_format="%Y%m%d"
    )
    assert result is not None
    assert result.path.name in ["nginx-access-ui.log-20250103", "nginx-access-ui.log-20250104.gz"]
