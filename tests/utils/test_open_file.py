import gzip

import pytest

from src.utils import open_log_file


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        list(open_log_file("non_existent_file.log"))


def test_is_a_directory(tmp_path):
    dir_path = tmp_path / "test"
    dir_path.mkdir()

    with pytest.raises(IsADirectoryError):
        list(open_log_file(str(dir_path)))


def test_permission_denied(tmp_path):
    test_content = "test"
    file_path = tmp_path / "protected.log"
    file_path.write_text(test_content, encoding="utf-8")

    file_path.chmod(0o000)

    try:
        with pytest.raises(PermissionError):
            list(open_log_file(str(file_path)))
    finally:
        file_path.chmod(0o644)


def test_invalid_gzip_file(tmp_path):
    file_path = tmp_path / "invalid.gz"
    file_path.write_text("Это не gzip!", encoding="utf-8")

    with pytest.raises(gzip.BadGzipFile):
        list(open_log_file(str(file_path)))
