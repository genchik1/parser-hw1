from src.settings import Config
import pytest


@pytest.fixture
def config(tmp_path):
    yield Config(report_dir=tmp_path)
