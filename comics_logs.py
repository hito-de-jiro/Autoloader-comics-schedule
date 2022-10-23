import json

from pprint import pprint
from loader import all_files_date as comics_data
from loader import choice_folder as choice_folder


def create_log():
    """создать журнал загрузки комиксов. JSON файл - название комикса: дата последнего комикса"""

    comics_path = choice_folder()
    all_data_time = comics_data(comics_path)
    data_time = {k: v.isoformat() for k, v in all_data_time.items()}

    with open("info_comics.json", 'w', encoding='utf-8') as f:
        f.write(json.dumps(data_time, indent=4))


create_log()
