import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import structlog

project_path = Path(".").absolute()

_log_pattern = (
    r"(?P<remote_addr>(\d+\.?){4})\s"
    r"(?P<remote_user>\S+)\s"
    r"\s-\s\[(?P<time_local>[^\]]+)\]\s"
    r"\"(?P<request_method>\w+)\s"
    r"(?P<request_uri>[^ ]+)\s"
    r"(?P<protocol>HTTP/\d\.\d)\"\s"
    r"(?P<status_code>[1-5][0-9][0-9])\s"
    r"(?P<size>\d+)\s"
    r"\"(?P<http_referer>.*?)\"\s"
    r"\"(?P<http_user_agent>.*?)\"\s"
    r"\"(?P<http_x_forwarded_for>.*?)\"\s"
    r"\"(?P<request_id>.*?)\"\s"
    r"\"(?P<host>.*?)\"\s"
    r"(?P<request_time>\d+\.\d+)"
)


def _create_dir_for_reports(path: Path | str) -> None:
    logger = get_logger(__name__)
    if not Path(path).exists():
        os.makedirs(path, exist_ok=True)
        logger.info("A directory has been created", path=path)


@dataclass
class Config:
    report_dir: Path | str = project_path.joinpath("reports")
    report_file_name_format: str = "report.log-{date}"  # Должен содержать `{date}`
    template_for_report_html: Path | str = project_path.joinpath("templates").joinpath("report.html")

    logs_path_dir: Path | str = project_path.joinpath("tests").joinpath("data")
    log_pattern: str = _log_pattern
    log_file_name_format: str = "nginx-access-ui\\.log-(?P<date>\\d{8})(?:\\.gz)?"  # Должен содержать `<date>`
    date_format_in_name: str = "%Y%m%d"
    encoding_for_log_file: str = "utf-8"
    max_unsuccessful_parsing_perc: float = 30

    stream_app_log: logging.Handler = logging.StreamHandler(sys.stdout)

    def __post_init__(self):
        self.report_dir = Path(self.report_dir)
        self.template_for_report_html = Path(self.template_for_report_html)
        self.logs_path_dir = Path(self.logs_path_dir)

        _create_dir_for_reports(self.report_dir)


def set_logging_settings():
    timestamper = structlog.processors.TimeStamper(fmt="iso")
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            timestamper,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(encoding="utf-8"),
            structlog.processors.CallsiteParameterAdder(
                {
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                }
            ),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
    )


def get_logger(name: str | None = None) -> Any:
    return structlog.get_logger(name)
