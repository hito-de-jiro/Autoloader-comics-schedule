#!python3
import argparse
import os
import subprocess
import sys

from pathlib import Path


def run_parsers():
    """Run main loop of program"""
    comics_path = choice_folder()
    os.makedirs(comics_path, exist_ok=True)

    comix_parsers = {
        "buttersafe": "buttersafe.py",  # <--comic_name, base_folder
        # "exocomics": "exocomics.py",
        # "left_handed_toons": "left_handed_toons.py",
        # "lunarbaboon": "lunarbaboon.py",
        # "savage_chickens": "savage_chickens.py",
        # "wonderella.py": "wonderella.py",
        # "moonbeard": "moonbeard.py",  # <-- not worked
    }

    for comix_parser in comix_parsers.values():
        subprocess.run([sys.executable, comix_parser, comics_path])
    print(comics_path)


def choice_folder() -> str:
    """Change the default download folder"""
    folder = 'comics_folder'
    parser = argparse.ArgumentParser(prog='loader', description='loader comics shit')
    parser.add_argument('outdir', type=str, nargs='?', default=folder, help='Output absolut path')
    args = parser.parse_args()

    if Path(args.outdir).is_absolute():
        new_folder = args.outdir
        return new_folder
    else:
        return folder


def check_new_comix() -> list[str]:
    pass
    # TODO: check new comix and return list of new chapters(images)
    return ["comix name1 - chapters 100, 99"]


def notify_user(new_comix: list[str]):
    pass
    # TODO: add file new_comix.txt with details of new comix in user desktop


def main():
    print("start program")
    try:
        run_parsers()
        # new_comix = check_new_comix()
        # if new_comix:
        #     notify_user(new_comix)
        print("end program")
    except KeyboardInterrupt:
        print('Forced program termination!')
        return


if __name__ == '__main__':
    main()



# E:\\GitHub\\Autoloader-comics-schedule\\comics_folder_2