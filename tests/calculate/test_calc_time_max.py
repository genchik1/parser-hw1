from src.calculate import DTOForCalc, DTOForReport, calc_time_max


def test_single_item():
    """Тест на один элемент в коллекции (максимум = значению этого элемента)."""
    input_data = [DTOForCalc(request_uri="/test", request_time=0.5)]
    expected = [DTOForReport(request_uri="/test", result=0.5)]
    assert calc_time_max(input_data) == expected


def test_multiple_items_same_uri():
    """Тест на несколько элементов с одинаковым URI (нахождение максимума)."""
    input_data = [
        DTOForCalc(request_uri="/test", request_time=0.1),
        DTOForCalc(request_uri="/test", request_time=0.5),
        DTOForCalc(request_uri="/test", request_time=0.3),
    ]
    expected = [DTOForReport(request_uri="/test", result=0.5)]
    assert calc_time_max(input_data) == expected


def test_multiple_items_different_uris():
    """Тест на несколько элементов с разными URI (раздельный поиск максимума по URI)."""
    input_data = [
        DTOForCalc(request_uri="/test1", request_time=1.0),
        DTOForCalc(request_uri="/test1", request_time=2.0),
        DTOForCalc(request_uri="/test2", request_time=5.0),
        DTOForCalc(request_uri="/test2", request_time=3.0),
        DTOForCalc(request_uri="/test2", request_time=7.0),
    ]
    expected = [
        DTOForReport(request_uri="/test1", result=2.0),
        DTOForReport(request_uri="/test2", result=7.0),
    ]
    # Сортируем результаты для сравнения по URI
    result = sorted(calc_time_max(input_data), key=lambda x: x.request_uri)
    expected_sorted = sorted(expected, key=lambda x: x.request_uri)

    assert result == expected_sorted
