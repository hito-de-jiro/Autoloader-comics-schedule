#!python3
import argparse
import datetime
import os
import subprocess
import sys

from os.path import getctime

DESKTOP_PATH = r'E:\Domix\Desktop'
NEW_COMICS_INFO_PATH = os.path.join(DESKTOP_PATH, 'new_comics_info.txt')
DEFAULT_PATH = r'E:\GitHub\Autoloader-comics-schedule\comics_folder'
START_TIME = datetime.datetime.now()


def run_parsers():
    """Run main loop of program"""
    comics_path = parse_params()
    os.makedirs(comics_path, exist_ok=True)

    comix_parsers = {
        "buttersafe": "buttersafe.py",  # <--comic_name, base_folder
        # "exocomics": "exocomics.py",
        # "left_handed": "left_handed.py",
        # "lunarbaboon": "lunarbaboon.py",
        # "savage_chickens": "chickens.py",
        # "wonderella": "wonderella.py",
        # "moonbeard": "moonbeard.py",  # <-- not worked
    }

    # Run parsers
    for name, comix_parser in comix_parsers.items():
        path = os.path.join(comics_path, name)
        subprocess.run([sys.executable, comix_parser, '--outdir', path])

    # Check new comics
    new_comics = check_new_comics(comics_path)
    if not new_comics:
        print('Not found new comics')
        return

    # Notify user about new comics
    notify_user(new_comics)

    # Create logs comics downloads
    # create_log(JSON_PATH)


def parse_params() -> str:
    """Change the default download folder"""
    parser = argparse.ArgumentParser(prog='loader', description='loader comics')
    parser.add_argument('--outdir', type=str,
                        default=r'E:\GitHub\Autoloader-comics-schedule\comics_folder',
                        help='Output absolut path')
    args = parser.parse_args()

    outdir = args.outdir
    if os.path.isabs(outdir):
        return outdir
    else:
        raise ValueError('Path is not absolute')


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
    print("start program")
    try:
        run_parsers()
        print("end program")
    except KeyboardInterrupt:
        print('Forced program termination!')
        return


if __name__ == '__main__':
    main()
