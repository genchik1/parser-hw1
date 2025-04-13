import pytest

from src.calculate import DTOForCalc, DTOForReport, calc_time_perc, ROUND


def test_single_item():
    """Тест на один элемент в коллекции (должен вернуть 100%)."""
    input_data = [DTOForCalc(request_uri="/test", request_time=0.5)]
    expected = [DTOForReport(request_uri="/test", result=100.0)]
    assert calc_time_perc(input_data) == expected


def test_multiple_items_same_uri():
    """Тест на несколько элементов с одинаковым URI (должен вернуть 100%)."""
    input_data = [
        DTOForCalc(request_uri="/test", request_time=0.1),
        DTOForCalc(request_uri="/test", request_time=0.2),
        DTOForCalc(request_uri="/test", request_time=0.3),
    ]
    expected = [DTOForReport(request_uri="/test", result=100.0)]
    assert calc_time_perc(input_data) == expected


def test_multiple_items_different_uris():
    """Тест на несколько элементов с разными URI (проверка правильности расчета процентов)."""
    input_data = [
        DTOForCalc(request_uri="/test1", request_time=1.0),
        DTOForCalc(request_uri="/test2", request_time=2.0),
        DTOForCalc(request_uri="/test3", request_time=3.0),
    ]
    expected = [
        DTOForReport(request_uri="/test1", result=100 / 6),  # ~16.666...
        DTOForReport(request_uri="/test2", result=200 / 6),  # ~33.333...
        DTOForReport(request_uri="/test3", result=300 / 6),  # 50.0
    ]
    # Сортируем результаты для сравнения по URI
    result = sorted(calc_time_perc(input_data), key=lambda x: x.request_uri)
    expected_sorted = sorted(expected, key=lambda x: x.request_uri)

    # Проверяем соответствие URI и процентов с допуском float
    for res, exp in zip(result, expected_sorted):
        assert res.request_uri == exp.request_uri
        assert pytest.approx(res.result) == round(exp.result, ROUND)
