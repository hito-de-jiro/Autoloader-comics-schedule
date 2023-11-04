import json
import os

from loader import get_last_date as last_data
from loader import check_new_comics

DESKTOP_PATH = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
JSON_PATH = 'info_comics.json'


def create_log(comic_name: str, last_date=last_data):
    """Create a comic download magazine. JSON file - the name of the comic: the date of the last comic"""
    comics_path = os.path.join((os.getcwd()), 'comics_folder')
    # all_data_time = comics_data(comics_path)
    new_comics_date = check_new_comics(comics_path)
    print(new_comics_date)
    data_log = {comic_name: last_date.isoformat()}

    # data_time = {k: v.isoformat() for k, v in all_data_time.items()}

    create_log_json(data_log)


def create_log_json(data_time: dict, path=JSON_PATH):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data_time, indent=4))


def get_log_json(path=JSON_PATH) -> dict:
    """receives JSON and returns it as a dictionary"""
    with open(path) as f:
        log_data = json.load(f)
    return log_data


create_log(JSON_PATH)

dates = get_log_json(path=JSON_PATH)
