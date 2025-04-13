import pytest

from src.calculate import DTOForCalc, DTOForReport, calc_time_avg


def test_single_item():
    """Тест на один элемент в коллекции (среднее = значению этого элемента)."""
    input_data = [DTOForCalc(request_uri="/test", request_time=0.5)]
    expected = [DTOForReport(request_uri="/test", result=0.5)]
    assert calc_time_avg(input_data) == expected


def test_multiple_items_same_uri():
    """Тест на несколько элементов с одинаковым URI (правильное усреднение)."""
    input_data = [
        DTOForCalc(request_uri="/test", request_time=0.1),
        DTOForCalc(request_uri="/test", request_time=0.3),
        DTOForCalc(request_uri="/test", request_time=0.5),
    ]
    expected = [DTOForReport(request_uri="/test", result=0.3)]  # (0.1+0.3+0.5)/3
    result = calc_time_avg(input_data)
    assert len(result) == 1
    assert result[0].request_uri == expected[0].request_uri
    assert pytest.approx(result[0].result) == expected[0].result


def test_multiple_items_different_uris():
    """Тест на несколько элементов с разными URI (раздельное усреднение по URI)."""
    input_data = [
        DTOForCalc(request_uri="/test1", request_time=1.0),
        DTOForCalc(request_uri="/test1", request_time=2.0),
        DTOForCalc(request_uri="/test2", request_time=5.0),
        DTOForCalc(request_uri="/test2", request_time=7.0),
        DTOForCalc(request_uri="/test2", request_time=9.0),
    ]
    expected = [
        DTOForReport(request_uri="/test1", result=1.5),  # (1.0+2.0)/2
        DTOForReport(request_uri="/test2", result=7.0),  # (5.0+7.0+9.0)/3
    ]
    # Сортируем результаты для сравнения по URI
    result = sorted(calc_time_avg(input_data), key=lambda x: x.request_uri)
    expected_sorted = sorted(expected, key=lambda x: x.request_uri)

    assert len(result) == len(expected_sorted)
    for res, exp in zip(result, expected_sorted):
        assert res.request_uri == exp.request_uri
        assert pytest.approx(res.result) == exp.result
