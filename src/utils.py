import gzip
import os
import re
from datetime import datetime, date
from functools import partial
from pathlib import Path
from typing import AnyStr, Generator, Iterator

from src.calculate import DTOForCalc
from src.settings import get_logger
from src.types import LogData, FileDTO

logger = get_logger(__name__)


def check_exists_path(path: str) -> None:
    if not Path(path).exists():
        logger.error("The specified folder does not exist.", path=path)
        raise FileNotFoundError("The specified folder does not exist.")


def search_for_a_match(text: str, pattern: str) -> dict[str, AnyStr] | None:
    match = re.match(pattern, text, re.VERBOSE)
    return match.groupdict() if match else None  # type: ignore[return-value]


def dict_to_log_data(log_dict: dict[str, AnyStr]) -> LogData | None:
    try:
        return LogData(**log_dict)  # type: ignore[arg-type]
    except ValueError as err:
        logger.error(str(err))
        return None


def file_parse(file, log_pattern: str) -> Generator[dict[str, AnyStr] | None, None, None]:
    for line in file:
        yield search_for_a_match(line, log_pattern)


def parse_compact_date(date_str: str, _format: str) -> date:
    try:
        return datetime.strptime(date_str, "%Y%m%d").date()
    except ValueError as err:
        logger.error(str(err))
        raise err


def search_last_file(file_dir: str, file_name_pattern: str, date_format: str) -> FileDTO | None:
    check_exists_path(file_dir)

    last_file = None
    for path in Path(file_dir).iterdir():
        file_name = path.name
        result = search_for_a_match(str(file_name), file_name_pattern)
        if result is not None:
            try:
                date_from_name = result["date"]
            except KeyError as err:
                logger.error(
                    "The `date` key is not specified in the file name template.", file_name_pattern=file_name_pattern
                )
                raise err
            parsed_date = parse_compact_date(date_from_name, date_format)
            if last_file is None or last_file.date < parsed_date:
                last_file = FileDTO(date=parsed_date, path=Path(file_dir).joinpath(file_name))
    return last_file


def transform_log_data_to_dto_for_calc(log_data: LogData) -> DTOForCalc:
    return DTOForCalc(request_uri=log_data.request_uri, request_time=log_data.request_time)


def open_log_file(filename: str, encoding: str = "utf-8") -> Iterator[str]:
    # Проверка существования файла
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")

    if not os.path.isfile(filename):
        raise IsADirectoryError(f"The path specified is a directory, not a file: {filename}")

    if not os.access(filename, os.R_OK):
        raise PermissionError(f"No permission to read file: {filename}")

    open_func = gzip.open if filename.endswith(".gz") else partial(open, encoding=encoding)  # type:ignore[assignment]

    try:
        with open_func(filename, "r") as file:
            for line in file:
                yield line.decode(encoding) if isinstance(line, bytes) else line
    except gzip.BadGzipFile as err:
        raise err
