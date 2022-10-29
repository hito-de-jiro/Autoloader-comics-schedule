#!python3
import argparse
import datetime
import os
import subprocess
import sys

from os.path import getctime
from dateutil.parser import parse as parse_date

DESKTOP_PATH = r'E:\Domix\Desktop'
NEW_COMICS_INFO_PATH = os.path.join(DESKTOP_PATH, 'new_comics_info.txt')
DEFAULT_PATH = r'E:\GitHub\Autoloader-comics-schedule\comics_folder'
START_TIME = datetime.datetime.now()
DEFAULT_DATE = (START_TIME - datetime.timedelta(days=30)).strftime("%Y-%m-%d")


def run_parsers():
    """Run main loop of program"""
    params = parse_params()
    date = params.date_limit

    comics_path = params.outdir
    os.makedirs(comics_path, exist_ok=True)

    comix_parsers = {
        "buttersafe": "buttersafe.py",  # <--comic_name, base_folder
        "chickens": "chickens.py",
        "exocomics": "exocomics.py",
        "left_handed": "left_handed.py",
        "lunarbaboon": "lunarbaboon.py",
        "wonderella": "wonderella.py",
    }

    # Run parsers
    for name, comix_parser in comix_parsers.items():
        path = os.path.join(comics_path, name)
        if date is None:
            comic_dates = get_last_date()
            for comic_date in comic_dates.values():
                date_limit = comic_date
                subprocess.run(
                    [sys.executable, comix_parser, '--outdir', path, '--date_limit', date_limit])  # date_limit - str
                break
        else:
            date_limit = datetime.datetime.strftime(date, '%Y-%m-%d')
            subprocess.run(
                [sys.executable, comix_parser, '--outdir', path, '--date_limit', date_limit])  # date_limit - str

    # Check new comics
    new_comics = check_new_comics(comics_path)
    if not new_comics:
        print('Not found new comics')
        return

    # Notify user about new comics
    notify_user(new_comics)


def get_last_date(path_folder=DEFAULT_PATH) -> dict:
    """Get the latest first download date of comics and create a dict with them"""
    last_date_dict = {}
    for folder_name, sub_folders, file_names in list(os.walk(path_folder))[1:]:

        comic_name = os.path.basename(folder_name)

        if not file_names:
            last_date_dict[comic_name] = DEFAULT_DATE
        else:
            comic_date = file_names[-1].split('__')[0]
            last_date_dict[comic_name] = comic_date

    return last_date_dict


def valid_date(s):
    """Datetime validator"""
    try:
        return datetime.datetime.strptime(s, '%Y-%m-%d')
    except ValueError:
        msg = "not a valid date: {0!r}".format(s)
        raise argparse.ArgumentTypeError(msg)


def parse_params():
    """Change the default download folder"""
    parser = argparse.ArgumentParser(prog='loader', description='loader comics')
    parser.add_argument('--outdir', type=str,
                        default=r'E:\GitHub\Autoloader-comics-schedule\comics_folder',
                        help='Output absolut path')
    parser.add_argument('--date_limit', type=valid_date,
                        default=DEFAULT_DATE, help="The Date - format YYYY-MM-DD")
    args = parser.parse_args()

    if args.outdir is None:
        args.outdir = DEFAULT_PATH
    elif not os.path.isabs(args.outdir):
        raise ValueError('Path is not absolute')

    if args.date_limit is None:
        args.date_limit = parse_date(DEFAULT_DATE)

    return args


def all_files_date(path_folder: str) -> dict:
    """Get create date all files"""
    all_files = {}
    for folder_name, _, filenames in os.walk(path_folder):
        for filename in filenames:
            file_path = os.path.join(folder_name, filename)
            file_cdate = datetime.datetime.fromtimestamp(getctime(file_path))
            all_files[file_path] = file_cdate

    return all_files


def check_new_comics(path_folder: str) -> list[str]:
    """Check new comics and return list of new comics"""
    all_files = all_files_date(path_folder)

    new_files = {}
    for file_path, file_cdate in all_files.items():
        if file_cdate >= START_TIME:
            new_files[file_path] = file_cdate

    return list(new_files.keys())


def notify_user(new_comics: list[str]):
    """Add file with details of new comix in user desktop"""
    new_comics_info = '\n'.join(new_comics)
    with open(NEW_COMICS_INFO_PATH, 'w') as f:
        f.write(new_comics_info)


def main():
    print("Start program.")
    try:
        run_parsers()
        print("End program.")
    except KeyboardInterrupt:
        print('Forced program termination!')
        return
    # get_last_date()


if __name__ == '__main__':
    main()
