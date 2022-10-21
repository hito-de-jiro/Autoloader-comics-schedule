#!python3
import argparse
import os
import subprocess
import sys


os.makedirs('comics_folder', exist_ok=True)


def run_parsers():
    comix_parsers = {
        "buttersafe": "buttersafe.py",   # <--comic_name, base_folder
        "exocomics": "exocomics.py",
        "left_handed_toons": "left_handed_toons.py",
        "lunarbaboon": "lunarbaboon.py",
        "moonbeard": "moonbeard.py",
        "savage_chickens": "savage_chickens.py",
        "wonderella.py": "wonderella.py",
    }

    for comix_parser in comix_parsers.values():
        subprocess.run([sys.executable, comix_parser])


def choice_folder():
    parser = argparse.ArgumentParser(description='Choice folder for saving comics')
    parser.add_argument('comic_dir', type=str, help='Output dir for downloading comics')
    args = parser.parse_args()

    print(args.comic_dir)
    return args.comic_dir

def check_new_comix() -> list[str]:
    pass
    # TODO: check new comix and return list of new chapters(images)
    return ["comix name1 - chapters 100, 99"]


def notify_user(new_comix: list[str]):
    pass
    # TODO: add file new_comix.txt with details of new comix in user desktop


if __name__ == '__main__':
    print("start program")
    run_parsers()
    new_comix = check_new_comix()
    if new_comix:
        notify_user(new_comix)
    print("end program")
