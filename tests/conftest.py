from src.settings import Config
import pytest


@pytest.fixture
def config():
    return Config()
