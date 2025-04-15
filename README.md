### Запуск инструмента
```commandline
python cli.py
python cli.py --config config.ini
```
Либо, запустить все в докере
```commandline
make build
make run
make run_with_config   # для запуска с конфигами из файла config.ini
```
По дефолту запускается тестовый **урезанный** файл `tests/data/nginx-access-ui.log-20170630`. После удачного запуска в корне проекта будет создана директория `/reports` с отчетами.

### Разработка

1. Установить pre-commit и установить настройки git-hooks
```commandline
pip install pre-commit
pre-commit install
```
2. Запуск raff форматтера и линтеров
```commandline
make fmt
make lint
```
