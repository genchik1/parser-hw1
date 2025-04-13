from src.calculate import DTOForCalc, DTOForReport, calc_count


def test_single_item():
    """Тест на один элемент в коллекции."""
    input_data = [DTOForCalc(request_uri="/test", request_time=0.1)]
    expected = [DTOForReport(request_uri="/test", result=1)]
    assert calc_count(input_data) == expected


def test_multiple_items_same_uri():
    """Тест на несколько элементов с одинаковым URI."""
    input_data = [
        DTOForCalc(request_uri="/test", request_time=0.1),
        DTOForCalc(request_uri="/test", request_time=0.2),
    ]
    expected = [DTOForReport(request_uri="/test", result=2)]
    assert calc_count(input_data) == expected


def test_multiple_items_different_uris():
    """Тест на несколько элементов с разными URI."""
    input_data = [
        DTOForCalc(request_uri="/test1", request_time=0.1),
        DTOForCalc(request_uri="/test2", request_time=0.2),
        DTOForCalc(request_uri="/test1", request_time=0.3),
    ]
    expected = [
        DTOForReport(request_uri="/test1", result=2),
        DTOForReport(request_uri="/test2", result=1),
    ]
    # Сортируем результаты для сравнения, так как порядок не гарантирован
    assert sorted(calc_count(input_data), key=lambda x: x.request_uri) == sorted(expected, key=lambda x: x.request_uri)
