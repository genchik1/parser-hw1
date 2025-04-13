from dataclasses import dataclass
from typing import Any, Callable
from statistics import median

from collections import defaultdict

ReportResultType = Any

ROUND: int = 3


@dataclass
class DTOForCalc:
    request_uri: str
    request_time: float


@dataclass
class DTOForReport:
    request_uri: str
    result: ReportResultType = 0


def _calc_count_requests_per_uri(collection: list[DTOForCalc]) -> dict[str, int]:
    result: dict[str, int] = {}
    for obj in collection:
        result[obj.request_uri] = result.get(obj.request_uri, 0) + 1
    return result


def calc_count(collection: list[DTOForCalc]) -> list[DTOForReport]:
    if not collection:
        return []

    result: list[DTOForReport] = []
    for uri, count in _calc_count_requests_per_uri(collection).items():
        result.append(DTOForReport(request_uri=uri, result=count))

    return result


def calc_count_perc(collection: list[DTOForCalc]) -> list[DTOForReport]:
    if not collection:
        return []

    count_per_url = _calc_count_requests_per_uri(collection)

    total_count = sum(count_per_url.values())
    result: list[DTOForReport] = []
    for uri, count in count_per_url.items():
        result.append(DTOForReport(request_uri=uri, result=round(count / total_count * 100, ROUND)))

    return result


def _calc_sum_request_time_per_uri(collection: list[DTOForCalc]) -> dict[str, float]:
    result: dict[str, float] = {}
    for obj in collection:
        result[obj.request_uri] = result.get(obj.request_uri, 0) + obj.request_time
    return result


def calc_time_sum(collection: list[DTOForCalc]) -> list[DTOForReport]:
    time_sum: list[DTOForReport] = []
    for uri, request_time in _calc_sum_request_time_per_uri(collection).items():
        time_sum.append(DTOForReport(request_uri=uri, result=round(request_time, ROUND)))

    return time_sum


def calc_time_perc(collection: list[DTOForCalc]) -> list[DTOForReport]:
    request_time_per_uri = _calc_sum_request_time_per_uri(collection)

    total_request_tim = sum(request_time_per_uri.values())
    time_perc: list[DTOForReport] = []
    for uri, request_time in request_time_per_uri.items():
        time_perc.append(DTOForReport(request_uri=uri, result=round(request_time / total_request_tim * 100, ROUND)))

    return time_perc


def calc_time_avg(collection: list[DTOForCalc]) -> list[DTOForReport]:
    request_time_per_uri = _calc_sum_request_time_per_uri(collection)
    count_per_url = _calc_count_requests_per_uri(collection)

    time_avg: list[DTOForReport] = []

    for uri in count_per_url:
        time_avg.append(
            DTOForReport(request_uri=uri, result=round(request_time_per_uri[uri] / count_per_url[uri], ROUND))
        )

    return time_avg


def calc_time_max(collection: list[DTOForCalc]) -> list[DTOForReport]:
    result: dict[str, float] = {}
    for obj in collection:
        result[obj.request_uri] = max(result.get(obj.request_uri, 0), obj.request_time)

    time_max: list[DTOForReport] = [
        DTOForReport(request_uri=uri, result=round(max_time, ROUND)) for uri, max_time in result.items()
    ]

    return time_max


def calc_time_median(collection: list[DTOForCalc]) -> list[DTOForReport]:
    result: dict[str, list[float]] = defaultdict(list)
    for obj in collection:
        result[obj.request_uri].append(obj.request_time)

    time_median: list[DTOForReport] = [
        DTOForReport(request_uri=uri, result=round(median(list_time), ROUND)) for uri, list_time in result.items()
    ]

    return time_median


CALCULATE_STATISTICS_BUS: dict[str, Callable[[list[DTOForCalc]], list[DTOForReport]]] = {
    "count": calc_count,
    "count_perc": calc_count_perc,
    "time_sum": calc_time_sum,
    "time_perc": calc_time_perc,
    "time_avg": calc_time_avg,
    "time_max": calc_time_max,
    "time_med": calc_time_median,
}


def calculate_report_pipeline(collection: list[DTOForCalc]) -> list[dict[str, Any]]:
    _report: dict[str, dict[str, Any]] = defaultdict(dict)
    for calc_name, calc_func in CALCULATE_STATISTICS_BUS.items():
        for dto_for_report in calc_func(collection):
            _report[dto_for_report.request_uri][calc_name] = dto_for_report.result
    report = [{"url": url, **values} for url, values in _report.items()]
    return sorted(report, key=lambda x: x["time_sum"], reverse=True)
