import pytest

from src.log_analyzer import run


def test_file_not_found(config) -> None:
    config.logs_path_dir = "test"
    with pytest.raises(FileNotFoundError):
        run(config)


def test_get_parsed_logs_is_not_gotten(config) -> None:
    config.log_pattern = "test"
    with pytest.raises(ValueError):
        run(config)
