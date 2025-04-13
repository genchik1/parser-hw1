import datetime
from dataclasses import dataclass
from pathlib import Path

from src.settings import get_logger

logger = get_logger(__name__)


@dataclass
class LogData:
    remote_addr: str
    remote_user: str
    time_local: str
    request_method: str
    request_uri: str
    protocol: str
    status_code: int
    size: str
    http_referer: str
    http_user_agent: str
    http_x_forwarded_for: str
    request_id: str
    host: str
    request_time: float

    def __post_init__(self) -> None:
        try:
            self.status_code = int(self.status_code)
        except ValueError as err:
            logger.error(str(err), status_code=self.status_code)
            raise err
        try:
            self.request_time = float(self.request_time)
        except ValueError as err:
            logger.error(str(err), request_time=self.request_time)
            raise err


@dataclass
class FileDTO:
    date: datetime.date
    path: Path
