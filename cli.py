import argparse
from pathlib import Path
import configparser
from typing import Any

from src import log_analyzer
from src.utils import check_exists_path
from src.settings import Config, get_logger, set_logging_settings

logger = get_logger(__name__)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--config", type=Path)
    args = parser.parse_args()

    config: dict[str, Any] = {}

    if args.config:
        check_exists_path(args.config)
        config_from_file = configparser.ConfigParser()
        config_from_file.read(args.config)
        config = config_from_file["DEFAULTS"] if "DEFAULTS" in config_from_file else config  # type:ignore[assignment]

    set_logging_settings()

    config_dto = Config(**config)

    try:
        log_analyzer.run(config_dto)
    except Exception as err:
        logger.error("An unexpected error has occurred", err=str(err))
