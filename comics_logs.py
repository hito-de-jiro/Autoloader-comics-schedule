import datetime
import json

from pprint import pprint
from loader import all_files_date as comics_data
from loader import choice_folder as choice_folder
from loader import check_new_comics

JSON_PATH = 'info_comics.json'


def create_log(comic_name: str, last_date):
    """создать журнал загрузки комиксов. JSON файл - название комикса: дата последнего комикса"""

    comics_path = choice_folder()
    all_data_time = comics_data(comics_path)
    new_comics_date = check_new_comics(comics_path)
    print(new_comics_date)
    data_log = {comic_name: last_date.isoformat()}

    data_time = {k: v.isoformat() for k, v in all_data_time.items()}

    create_log_json(data_log)


def create_log_json(data_time: dict, path=JSON_PATH):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data_time, indent=4))


def get_log_json(path=JSON_PATH) -> dict:
    """получает JSON и возвращает его словарем"""
    with open(path) as f:
        log_data = json.load(f)
    return log_data


create_log(JSON_PATH)

dates = get_log_json(path=JSON_PATH)
# for data in dates.values():
#     print(datetime.datetime.strptime(data, '%Y-%m-%dT%H:%M:%S.%f'))
# now_time = datetime.datetime.now()
# y = now_time.isoformat()  # <-- str
# print(y)
# print(type(y))
# x = datetime.datetime.strptime(y, '%Y-%m-%dT%H:%M:%S.%f')  # <-- datetime
# print(x)
# print(type(x))
# a = {print(datetime.datetime.strptime(data, '%Y-%m-%dT%H:%M:%S.%f')) for data in dates.values()}
# print(a)
