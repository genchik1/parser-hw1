from statistics import median

from src.calculate import DTOForCalc, DTOForReport, calc_time_median


def test_single_item():
    """Тест на один элемент в коллекции (медиана = значению этого элемента)."""
    input_data = [DTOForCalc(request_uri="/test", request_time=0.5)]
    expected = [DTOForReport(request_uri="/test", result=0.5)]
    assert calc_time_median(input_data) == expected


def test_odd_number_of_items_same_uri():
    """Тест на нечетное количество элементов с одинаковым URI."""
    input_data = [
        DTOForCalc(request_uri="/test", request_time=0.1),
        DTOForCalc(request_uri="/test", request_time=0.5),
        DTOForCalc(request_uri="/test", request_time=0.3),
    ]
    expected_median = median([0.1, 0.3, 0.5])
    expected = [DTOForReport(request_uri="/test", result=expected_median)]
    result = calc_time_median(input_data)
    assert len(result) == 1
    assert result[0].request_uri == expected[0].request_uri
    assert result[0].result == expected[0].result


def test_multiple_uris_with_even_and_odd_counts():
    """Тест на несколько URI с четным и нечетным количеством элементов."""
    input_data = [
        DTOForCalc(request_uri="/odd", request_time=1.0),
        DTOForCalc(request_uri="/odd", request_time=3.0),
        DTOForCalc(request_uri="/odd", request_time=5.0),  # медиана 3.0
        DTOForCalc(request_uri="/even", request_time=2.0),
        DTOForCalc(request_uri="/even", request_time=4.0),
        DTOForCalc(request_uri="/even", request_time=6.0),
        DTOForCalc(request_uri="/even", request_time=8.0),  # медиана (4+6)/2 = 5.0
    ]
    expected = [
        DTOForReport(request_uri="/odd", result=3.0),
        DTOForReport(request_uri="/even", result=5.0),
    ]
    # Сортируем результаты для сравнения по URI
    result = sorted(calc_time_median(input_data), key=lambda x: x.request_uri)
    expected_sorted = sorted(expected, key=lambda x: x.request_uri)

    assert len(result) == len(expected_sorted)
    for res, exp in zip(result, expected_sorted):
        assert res.request_uri == exp.request_uri
        assert res.result == exp.result
