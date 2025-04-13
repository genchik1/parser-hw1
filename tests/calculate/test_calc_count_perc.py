import pytest

from src.calculate import DTOForCalc, DTOForReport, calc_count_perc, ROUND


def test_single_item():
    """Тест на один элемент в коллекции (должен вернуть 100%)."""
    input_data = [DTOForCalc(request_uri="/test", request_time=0.1)]
    expected = [DTOForReport(request_uri="/test", result=100.0)]
    assert calc_count_perc(input_data) == expected


def test_two_items_same_uri():
    """Тест на два элемента с одинаковым URI (должен вернуть 100%)."""
    input_data = [
        DTOForCalc(request_uri="/test", request_time=0.1),
        DTOForCalc(request_uri="/test", request_time=0.2),
    ]
    expected = [DTOForReport(request_uri="/test", result=100.0)]
    assert calc_count_perc(input_data) == expected


def test_multiple_items_different_uris():
    """Тест на несколько элементов с разными URI (проверка правильности расчета процентов)."""
    input_data = [
        DTOForCalc(request_uri="/test1", request_time=0.1),
        DTOForCalc(request_uri="/test1", request_time=0.2),
        DTOForCalc(request_uri="/test2", request_time=0.3),
    ]
    expected = [
        DTOForReport(request_uri="/test1", result=200 / 3),  # ~66.666...
        DTOForReport(request_uri="/test2", result=100 / 3),  # ~33.333...
    ]
    result = sorted(calc_count_perc(input_data), key=lambda x: x.request_uri)
    expected_sorted = sorted(expected, key=lambda x: x.request_uri)

    # Сравниваем URI
    assert result[0].request_uri == expected_sorted[0].request_uri
    assert result[1].request_uri == expected_sorted[1].request_uri
    # Сравниваем значения result с допуском на погрешность float
    assert pytest.approx(result[0].result) == round(expected_sorted[0].result, ROUND)
    assert pytest.approx(result[1].result) == round(expected_sorted[1].result, ROUND)
