import pytest

from src.calculate import DTOForCalc, DTOForReport, calc_time_sum


def test_single_item():
    """Тест на один элемент в коллекции."""
    input_data = [DTOForCalc(request_uri="/test", request_time=0.5)]
    expected = [DTOForReport(request_uri="/test", result=0.5)]
    assert calc_time_sum(input_data) == expected


def test_multiple_items_same_uri():
    """Тест на несколько элементов с одинаковым URI (суммирование времени)."""
    input_data = [
        DTOForCalc(request_uri="/test", request_time=0.1),
        DTOForCalc(request_uri="/test", request_time=0.2),
        DTOForCalc(request_uri="/test", request_time=0.3),
    ]
    expected = [DTOForReport(request_uri="/test", result=0.6)]
    result = sorted(calc_time_sum(input_data), key=lambda x: x.request_uri)
    result = [DTOForReport(request_uri=data.request_uri, result=pytest.approx(data.result)) for data in result]
    assert result == sorted(expected, key=lambda x: x.request_uri)


def test_multiple_items_different_uris():
    """Тест на несколько элементов с разными URI (раздельное суммирование по URI)."""
    input_data = [
        DTOForCalc(request_uri="/test1", request_time=0.1),
        DTOForCalc(request_uri="/test2", request_time=0.2),
        DTOForCalc(request_uri="/test1", request_time=0.3),
        DTOForCalc(request_uri="/test2", request_time=0.4),
    ]
    expected = [
        DTOForReport(request_uri="/test1", result=0.4),
        DTOForReport(request_uri="/test2", result=0.6),
    ]
    # Сортируем результаты для сравнения, так как порядок не гарантирован

    result = sorted(calc_time_sum(input_data), key=lambda x: x.request_uri)
    result = [DTOForReport(request_uri=data.request_uri, result=pytest.approx(data.result)) for data in result]
    assert result == sorted(expected, key=lambda x: x.request_uri)
