import json
from pathlib import Path
from typing import Any

from src.calculate import DTOForCalc, calculate_report_pipeline
from src.settings import Config, get_logger
from src.utils import (
    search_last_file,
    dict_to_log_data,
    search_for_a_match,
    transform_log_data_to_dto_for_calc,
    open_log_file,
)

logger = get_logger(__name__)


def get_parsed_logs(
    path: Path, log_pattern: str, max_unsuccessful_parsing_perc: float, encoding: str
) -> list[DTOForCalc]:
    unsuccessful_parsing_counter: int = 0
    successful_parsing_counter: int = 0

    collection: list[DTOForCalc] = []
    for line in open_log_file(str(path), encoding=encoding):
        parsed_log = search_for_a_match(line, log_pattern)
        if parsed_log is None:
            unsuccessful_parsing_counter += 1
            logger.error("Unsuccessful attempt to parse the log.", line=line)
            continue
        successful_parsing_counter += 1
        log_data = dict_to_log_data(parsed_log)
        if log_data is None:
            logger.error("Error when creating the LogData object.", parsed_log=parsed_log)
            continue
        collection.append(transform_log_data_to_dto_for_calc(log_data))

    if successful_parsing_counter > 0:
        error_perc = unsuccessful_parsing_counter / successful_parsing_counter * 100
        if error_perc > max_unsuccessful_parsing_perc:
            logger.error(
                "The acceptable threshold for unsuccessful attempts at parsing logs has been exceeded.",
                error_perc=error_perc,
            )
    else:
        if unsuccessful_parsing_counter > 0:
            logger.error("Failed file parsing attempt.", paht=path)
            raise
        logger.info("The log file is empty.", paht=path)

    return collection


def run(config: Config) -> None:
    last_file = search_last_file(str(config.logs_path_dir), config.log_file_name_format, config.date_format_in_name)
    if last_file is None:
        logger.error("File not found.")
        raise

    path_to_report_file = Path(config.report_dir).joinpath(f"report-{last_file.date:%Y.%m.%d}.html")
    if path_to_report_file.exists():
        logger.info("The file with the reports for the current date already exists.", path=path_to_report_file)
        return None

    collection = get_parsed_logs(
        last_file.path, config.log_pattern, config.max_unsuccessful_parsing_perc, encoding=config.encoding_for_log_file
    )

    if not collection:
        return None

    report = calculate_report_pipeline(collection)
    save_report(
        report,
        template=config.template_for_report_html,
        save_path=path_to_report_file,
    )


def save_report(data: list[dict[str, Any]], template: Path | str, save_path: Path | str) -> None:
    json_table = json.dumps(data)

    with open(template, "r") as file:
        template_report = "".join(file.readlines())

    template_report_with_table = template_report.replace("$table_json", json_table)

    with open(str(save_path), "w") as file:
        file.write(template_report_with_table)

    logger.info("The report was saved successfully", path=save_path)
