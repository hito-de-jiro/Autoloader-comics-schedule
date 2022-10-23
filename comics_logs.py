import datetime
import json



from pprint import pprint
from loader import all_files_date as comics_data
from loader import choice_folder as choice_folder

JSON_PATH = 'info_comics.json'


def create_log(path=JSON_PATH):
    """создать журнал загрузки комиксов. JSON файл - название комикса: дата последнего комикса"""

    comics_path = choice_folder()
    all_data_time = comics_data(comics_path)
    data_time = {k: v.isoformat() for k, v in all_data_time.items()}

    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data_time, indent=4))


def get_log_json(path=JSON_PATH) -> dict:
    """получает JSON и возвращает его словарем"""
    with open(path) as f:
        data = json.load(f)
    return data


create_log(path=JSON_PATH)
dates = get_log_json(path=JSON_PATH)
# for data in dates.values():
#     print(data)
y = datetime.datetime.now().isoformat()
x = {print(datetime.datetime.strptime(data, '%y-%m-%dT%H:%M:%S')) for data in dates.values()}

