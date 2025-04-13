from src.settings import Config
from src.types import LogData
from src.utils import search_for_a_match, dict_to_log_data


def test_search_for_a_math_success_v1(config: Config) -> None:
    test_line = """1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/banner/25019354 HTTP/1.1" 200 927 "-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-2190034393-4708-9752759" "dc7161be3" 0.390"""

    valid_data = {
        "remote_addr": "1.196.116.32",
        "remote_user": "-",
        "time_local": "29/Jun/2017:03:50:22 +0300",
        "request_method": "GET",
        "request_uri": "/api/v2/banner/25019354",
        "protocol": "HTTP/1.1",
        "status_code": "200",
        "size": "927",
        "http_referer": "-",
        "http_user_agent": "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5",
        "http_x_forwarded_for": "-",
        "request_id": "1498697422-2190034393-4708-9752759",
        "host": "dc7161be3",
        "request_time": "0.390",
    }

    assert search_for_a_match(test_line, config.log_pattern) == valid_data


def test_search_for_a_math_success_v2(config: Config) -> None:
    test_line = """1.200.76.128 f032b48fb33e1e692  - [29/Jun/2017:03:50:23 +0300] "GET /api/1/banners/?campaign=7789704 HTTP/1.1" 200 604049 "-" "-" "-" "1498697421-4102637017-4708-9752733" "-" 2.577"""

    valid_data = {
        "remote_addr": "1.200.76.128",
        "remote_user": "f032b48fb33e1e692",
        "time_local": "29/Jun/2017:03:50:23 +0300",
        "request_method": "GET",
        "request_uri": "/api/1/banners/?campaign=7789704",
        "protocol": "HTTP/1.1",
        "status_code": "200",
        "size": "604049",
        "http_referer": "-",
        "http_user_agent": "-",
        "http_x_forwarded_for": "-",
        "request_id": "1498697421-4102637017-4708-9752733",
        "host": "-",
        "request_time": "2.577",
    }

    assert search_for_a_match(test_line, config.log_pattern) == valid_data


def test_search_for_a_math_success_v3(config: Config) -> None:
    test_line = """1.162.124.208 -  - [29/Jun/2017:03:50:27 +0300] "POST /accounts/login/ HTTP/1.1" 302 30 "-" "r/curl/jeroen" "-" "1498697427-2383406390-4708-9752885" "-" 0.256"""

    valid_data = {
        "remote_addr": "1.162.124.208",
        "remote_user": "-",
        "time_local": "29/Jun/2017:03:50:27 +0300",
        "request_method": "POST",
        "request_uri": "/accounts/login/",
        "protocol": "HTTP/1.1",
        "status_code": "302",
        "size": "30",
        "http_referer": "-",
        "http_user_agent": "r/curl/jeroen",
        "http_x_forwarded_for": "-",
        "request_id": "1498697427-2383406390-4708-9752885",
        "host": "-",
        "request_time": "0.256",
    }

    assert search_for_a_match(test_line, config.log_pattern) == valid_data


def test_search_for_a_math_non_success(config: Config) -> None:
    test_line = """1.162.124.208"""
    assert search_for_a_match(test_line, config.log_pattern) is None


def test_dict_to_log_data(config: Config) -> None:
    valid_data = {
        "remote_addr": "1.162.124.208",
        "remote_user": "-",
        "time_local": "29/Jun/2017:03:50:27 +0300",
        "request_method": "POST",
        "request_uri": "/accounts/login/",
        "protocol": "HTTP/1.1",
        "status_code": "302",
        "size": "30",
        "http_referer": "-",
        "http_user_agent": "r/curl/jeroen",
        "http_x_forwarded_for": "-",
        "request_id": "1498697427-2383406390-4708-9752885",
        "host": "-",
        "request_time": "0.256",
    }

    log_data = LogData(
        remote_addr="1.162.124.208",
        remote_user="-",
        time_local="29/Jun/2017:03:50:27 +0300",
        request_method="POST",
        request_uri="/accounts/login/",
        protocol="HTTP/1.1",
        status_code=302,
        size="30",
        http_referer="-",
        http_user_agent="r/curl/jeroen",
        http_x_forwarded_for="-",
        request_id="1498697427-2383406390-4708-9752885",
        host="-",
        request_time=0.256,
    )

    assert dict_to_log_data(valid_data) == log_data
